FROM python:3.9-slim

# Instalar dependencias de Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    apt-get clean

# Crear directorio de la app
WORKDIR /app

# Copiar requerimientos y código
COPY requirements.txt .
COPY app.py .

# Instalar librerías Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
