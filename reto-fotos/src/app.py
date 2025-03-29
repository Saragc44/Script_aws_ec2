import os
from flask import Flask, request, jsonify
import boto3
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError

# Configuración de Flask
app = Flask(__name__)

# Configuración de AWS
s3_client = boto3.client('s3', region_name='us-east-1')  # Cambia la región si es necesario
bucket_name = 'sara-garcia-01-bucket'  # Nombre de tu bucket de S3

# Extensiones permitidas para las fotos
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Función para verificar las extensiones de los archivos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función para subir fotos a S3
def upload_file_to_s3(file, bucket_name):
    try:
        # Crear un nombre único para el archivo
        filename = secure_filename(file.filename)

        # Subir el archivo a S3
        s3_client.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={'ACL': 'public-read'}  # Permitir acceso público al archivo
        )

        # Obtener la URL pública del archivo subido
        file_url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"
        return file_url

    except ClientError as e:
        print(f"Error al subir archivo: {e}")
        return None

# Ruta para subir fotos
@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        file_url = upload_file_to_s3(file, bucket_name)

        if file_url:
            return jsonify({"message": "File uploaded successfully", "file_url": file_url}), 200
        else:
            return jsonify({"error": "Failed to upload file"}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
