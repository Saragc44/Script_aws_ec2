from flask import Flask, request, jsonify, render_template_string
import boto3
import uuid
import pytesseract
from PIL import Image
import io
import json
import re

app = Flask(__name__)

s3 = boto3.client('s3', region_name='us-east-1')

BUCKET_ENTRADA = 'parcialsara-images'
BUCKET_SALIDA = 'parcialsara-json'

UPLOAD_FORM = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sube el Recibo</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #f8f9fa;
    }
    .form-container {
      max-width: 500px;
      margin: 80px auto;
      padding: 30px;
      background-color: white;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>

  <div class="container">
    <div class="form-container">
      <h2 class="mb-4 text-center">Subir imagen del recibo</h2>
      <form method="post" enctype="multipart/form-data" action="/upload">
        <div class="mb-3">
          <label for="file" class="form-label">Seleccionar imagen (JPG o PNG):</label>
          <input class="form-control" type="file" name="file" id="file" required>
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Subir Recibo</button>
        </div>
      </form>
    </div>
  </div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(UPLOAD_FORM)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    filename = f"{uuid.uuid4()}.png"

    s3.upload_fileobj(file, BUCKET_ENTRADA, filename)

    return jsonify({'mensaje': 'Felicidades la imagen subio con exito', 'archivo': filename})

@app.route('/salir', methods=['GET'])
def salir():
    bucket = BUCKET_ENTRADA
    nombre_archivo = request.args.get('file')

    if not bucket or not nombre_archivo:
        return jsonify({'error': 'Faltan parametros en el archivo'}), 400

    try:
        response = s3.get_object(Bucket=bucket, Key=nombre_archivo)
        imagen = Image.open(io.BytesIO(response['Body'].read()))

        texto = pytesseract.image_to_string(imagen, lang='spa')
        datos = extraer_datos(texto)

        salida_key = nombre_archivo.replace('.png', '.json')
        json_bytes = io.BytesIO(json.dumps(datos, indent=2).encode('utf-8'))
        s3.upload_fileobj(json_bytes, BUCKET_SALIDA, salida_key)

        return jsonify({'mensaje': 'Informacion procesada ', 'datos': datos})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extraer_datos(texto):
    datos = {}

    num_match = re.search(r'(N[úu]mero|N\u00ba|#)\s*[:\-]?\s*(\d+)', texto, re.IGNORECASE)
    fecha_match = re.search(r'(\d{2}[\/\-\.]\d{2}[\/\-\.]\d{4})', texto)
    total_match = re.search(r'(Total|TOTAL)\s*[:\-]?\s*\$?\s*([\d,.]+)', texto)
    restaurante_match = re.search(r'Restaurante\s*[:\-]?\s*(.+)', texto, re.IGNORECASE)

    if num_match:
        datos['numero_recibo'] = num_match.group(2)
    if fecha_match:
        datos['fecha'] = fecha_match.group(1)
    if total_match:
        datos['total'] = total_match.group(2)
    if restaurante_match:
        datos['restaurante'] = restaurante_match.group(1).strip()

    return datos

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

