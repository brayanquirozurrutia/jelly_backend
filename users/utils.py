import os

import cv2
import pytesseract
import numpy as np
import face_recognition

os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

class ImageAnalyzer:
    """
    Base class for image analysis.

    :param image: numpy array representing the image

    Methods:
    is_blurry: Check if the image is blurry
    has_text: Check if the image has text
    is_cut: Check if the image is cut
    is_correct_orientation: Check if the image is in the correct orientation
    has_face: Check if the image has a face
    """
    def __init__(self, image):
        self.image = image

    def is_blurry(self, threshold=40) -> bool:
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var < threshold

    def has_text(self) -> bool:
        text = pytesseract.image_to_string(self.image)
        return bool(text.strip())

    def is_cut(self, expected_aspect_ratio=(85.6, 53.98)) -> bool:
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            expected_ratio = expected_aspect_ratio[0] / expected_aspect_ratio[1]
            if 0.9 < aspect_ratio / expected_ratio < 1.1:
                return False
        return True

    def is_correct_orientation(self) -> bool:
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        if lines is None:
            return False
        for line in lines:
            rho, theta = line[0]
            angle = np.degrees(theta)
            if 85 < angle < 95:
                return True

    def has_face(self) -> bool:
        small_image = cv2.resize(self.image, (0, 0), fx=0.5, fy=0.5)
        face_locations = face_recognition.face_locations(small_image)
        return len(face_locations) > 0


class FrontIdAnalyzer(ImageAnalyzer):
    """
    Class for analyzing the front of an ID card.

    Methods:
    validate: Check if the image is valid
    """
    def validate(self) -> bool:
        if self.is_blurry():
            return False
        if not self.has_text():
            return False
        if self.is_cut():
            return False
        if not self.is_correct_orientation():
            return False
        if not self.has_face():
            return False
        return True


class BackIdAnalyzer(ImageAnalyzer):
    """
    Class for analyzing the back of an ID card.

    Methods:
    validate: Check if the image is valid
    has_fingerprint: Check if the image has a fingerprint
    """
    def validate(self):
        if self.is_blurry():
            return False
        if not self.has_text():
            return False
        if self.is_cut():
            return False
        if not self.is_correct_orientation():
            return False
        if not self.has_fingerprint():
            return False
        return True

    def has_fingerprint(self) -> bool:
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        sobel_combined = cv2.sqrt(sobelx ** 2 + sobely ** 2)

        _, binary_image = cv2.threshold(sobel_combined, 100, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(np.uint8(binary_image), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 5:
            return True
        else:
            return False

class FaceComparison:
    """
    Class for comparing a face image to an ID card image.

    :param face_image: numpy array representing the face image
    :param id_image: numpy array representing the ID card image

    Methods:
    compare_faces: Compare the face to the ID card
    :return: bool indicating whether the face matches the ID card
    """
    def __init__(self, face_image, id_image):
        self.face_image = face_image
        self.id_image = id_image

    def compare_faces(self):
        # Resize images for consistency
        face_image_resized = cv2.resize(self.face_image, (0, 0), fx=0.5, fy=0.5)
        id_image_resized = cv2.resize(self.id_image, (0, 0), fx=0.5, fy=0.5)

        face_encodings = face_recognition.face_encodings(face_image_resized)
        id_face_encodings = face_recognition.face_encodings(id_image_resized)

        if len(face_encodings) == 0:
            return False
        if len(id_face_encodings) == 0:
            return False

        face_encoding = face_encodings[0]
        id_face_encoding = id_face_encodings[0]
        results = face_recognition.compare_faces([id_face_encoding], face_encoding)
        return results[0]


class IdentityValidator:
    """
    Class for validating the images of a Chilean ID card.

    :param front_id_image: numpy array representing the front of the ID card
    :param back_id_image: numpy array representing the back of the ID card
    :param face_image: numpy array representing the face image

    Methods:
    validate: Validate the images

    :return: bool indicating whether the images are valid
    """
    def __init__(self, front_id_image, back_id_image, face_image):
        self.front_id_analyzer = FrontIdAnalyzer(front_id_image)
        self.back_id_analyzer = BackIdAnalyzer(back_id_image)
        self.face_comparison = FaceComparison(face_image, front_id_image)

    def validate(self):
        if not self.front_id_analyzer.validate():
            return False
        elif not self.back_id_analyzer.validate():
            return False
        elif not self.face_comparison.compare_faces():
            return False
        return True
