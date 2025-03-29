import os
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

app = Flask(__name__)

# Inicializa el cliente de S3 sin credenciales hardcodeadas
s3_client = boto3.client('s3')

# Nombre del bucket de S3
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')  # Asegúrate de establecer esta variable de entorno

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Subir el archivo a S3
        s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)
        return jsonify({'message': 'File uploaded successfully'}), 200
    except NoCredentialsError:
        return jsonify({'error': 'Credentials not available'}), 403
    except ClientError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
