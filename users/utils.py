import os
import cv2
import pytesseract
import numpy as np
from PIL import Image
import re
import face_recognition

# Configurar la variable de entorno TESSDATA_PREFIX
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/'

# Configurar el comando de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


class ChileanIDValidator:
    """
    Base class for validating Chilean ID cards.

    Attributes:
    - image_file: The image file to validate.
    - image: PIL Image object.
    - image_np: Numpy array representation of the image.
    - gray: Grayscale version of the image.
    - thresh: Thresholded image.
    - text: Extracted text from the image.

    Methods:
    - preprocess_image: Preprocess the image for text extraction.
    - extract_text: Use OCR to extract text from the image.
    - clean_text: Clean up the extracted text.
    - validate_resolution: Check if the image resolution is sufficient.
    - validate_edges: Check if the image edges are visible.
    - validate_orientation: Check if the image is correctly oriented.
    - validate_text_presence: Check if the image contains text.
    - validate: Run all validation checks.

    Subclasses should implement the `validate` method to include specific validations.
    """
    def __init__(self, image_file):
        self.image = Image.open(image_file)
        self.image_np = np.array(self.image.convert('RGB'))
        self.gray = cv2.cvtColor(self.image_np, cv2.COLOR_RGB2GRAY)
        self.thresh = None
        self.text = ""

    def preprocess_image(self):
        """
        Preprocess the image for text extraction.
        :return: None
        """
        blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        equalized = cv2.equalizeHist(blurred)
        self.thresh = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
        kernel = np.ones((3, 3), np.uint8)
        self.thresh = cv2.dilate(self.thresh, kernel, iterations=2)
        self.thresh = cv2.erode(self.thresh, kernel, iterations=1)

    def extract_text(self):
        """
        Extract text from the preprocessed image.
        :return: None
        """
        custom_config = r'--oem 3 --psm 6'
        self.text = pytesseract.image_to_string(self.thresh, lang='spa', config=custom_config)

    def clean_text(self):
        """
        Clean up the extracted text.
        :return: None
        """
        self.text = re.sub(r'\s+', ' ', self.text).strip()
        self.text = re.sub(r'[^\w\s\-.,]', '', self.text)

    def validate_resolution(self) -> str:
        """
        Check if the image resolution is sufficient.
        :return: Error message if resolution is too low, None otherwise.
        """
        if self.gray.shape[0] < 500 or self.gray.shape[1] < 800:
            return "La resolución de la imagen es demasiado baja."

    def validate_edges(self) -> str:
        """
        Check if the image edges are visible.
        :return: Error message if edges are not visible, None otherwise.
        """
        edges = cv2.Canny(self.thresh, 50, 150)
        if np.sum(edges) < 1000:
            return "La imagen parece estar cortada o de baja calidad."

    def validate_orientation(self) -> str:
        """
        Check if the image is correctly oriented.
        :return: Error message if image is incorrectly oriented, None otherwise.
        """
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        if len(faces) > 0:
            if faces[0][2] < faces[0][3]:  # Ancho menor que altura, posiblemente girada
                return "La imagen parece estar orientada incorrectamente."

    def validate_text_presence(self) -> str:
        """
        Check if the image contains text.
        :return: Error message if no text is detected, None otherwise.
        """
        if not self.text.strip():
            return "La imagen no contiene texto."

    def validate(self) -> str:
        """
        Run all validation checks.
        :return: Error message if any validation fails, or a success message if all checks pass.
        """
        self.preprocess_image()
        self.extract_text()
        self.clean_text()

        resolution_error = self.validate_resolution()
        if resolution_error:
            return resolution_error

        edges_error = self.validate_edges()
        if edges_error:
            return edges_error

        orientation_error = self.validate_orientation()
        if orientation_error:
            return orientation_error

        text_error = self.validate_text_presence()
        if text_error:
            return text_error

        return "Validaciones comunes superadas."


class ChileanIDFrontValidator(ChileanIDValidator):
    """
    Validator for the front side of a Chilean ID card.

    Methods:
    - validate: Run all validation checks specific to the front side.

    Additional validations:
    - Check for the presence of a face in the image.

    Subclasses can add more specific validations as needed.
    """
    def validate(self) -> str:
        """
        Run all validation checks specific to the front side.
        :return: Error message if any validation fails, or a success message if all checks pass.
        """
        common_validation = super().validate()
        if "superadas" not in common_validation:
            return common_validation

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        if len(faces) == 0:
            return "No se detectó un rostro en la imagen."

        return "La imagen frontal del carnet es válida."


class ChileanIDBackValidator(ChileanIDValidator):
    """
    Validator for the back side of a Chilean ID card.

    Methods:
    - validate: Run all validation checks specific to the back side.

    Additional validations:
    - Check for the presence of a fingerprint in the image.

    Subclasses can add more specific validations as needed.
    """
    def validate(self) -> str:
        """
        Run all validation checks specific to the back side.
        :return: Error message if any validation fails, or a success message if all checks pass.
        """
        common_validation = super().validate()
        if "superadas" not in common_validation:
            return common_validation

        height, width = self.gray.shape
        huella_region = self.gray[0:height // 3, width * 2 // 3:width]
        edges = cv2.Canny(huella_region, 100, 200)
        huella_detectada = np.sum(edges) > 5000
        if not huella_detectada:
            return "No se detectó una huella dactilar en la esquina superior derecha."

        return "La imagen trasera del carnet es válida."


def verify_identity_with_ai(id_image_file, face_image_file, tolerance=0.6) -> bool:
    """
    Verifica si la cara en la imagen de la cédula de identidad coincide con la cara en la imagen proporcionada.

    :param id_image_file: Ruta al archivo de imagen de la cédula de identidad.
    :param face_image_file: Ruta al archivo de imagen del rostro a comparar.
    :param tolerance: Umbral para la coincidencia de rostros. Valores más bajos significan una coincidencia más estricta.
    :return: True si las caras coinciden, False en caso contrario.
    """
    try:
        id_image = face_recognition.load_image_file(id_image_file)
        face_image = face_recognition.load_image_file(face_image_file)
        id_face_encodings = face_recognition.face_encodings(id_image)
        face_face_encodings = face_recognition.face_encodings(face_image)

        if len(id_face_encodings) == 0:
            print("No se detectó un rostro en la imagen de la cédula.")
            return False
        if len(face_face_encodings) == 0:
            print("No se detectó un rostro en la imagen proporcionada.")
            return False

        id_face_encoding = max(id_face_encodings, key=lambda encoding: encoding.shape[0])

        for face_encoding in face_face_encodings:
            distance = face_recognition.face_distance([id_face_encoding], face_encoding)[0]
            if distance <= tolerance:
                print(f"Las caras coinciden con una distancia de {distance:.2f}.")
                return True
        print("Las caras no coinciden.")
        return False

    except Exception as e:
        print(f"Error en la verificación de identidad con IA: {e}")
        return False
