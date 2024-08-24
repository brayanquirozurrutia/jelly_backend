FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    libleptonica-dev \
    libtesseract-dev \
    tesseract-ocr \
    tesseract-ocr-spa \
    libgl1-mesa-glx \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /usr/share/tesseract-ocr/5/tessdata/spa.traineddata \
    https://github.com/tesseract-ocr/tessdata/raw/main/spa.traineddata

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
