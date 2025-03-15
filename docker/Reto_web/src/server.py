from flask import Flask, render_template, request, jsonify
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Función para listar objetos en un bucket de S3
def listar_objetos(bucket_name):
    s3 = boto3.client('s3')

    try:
        # Intentar obtener la lista de objetos en el bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        # Si el bucket tiene objetos, devolverlos
        if 'Contents' in response:
            objects = []
            for obj in response['Contents']:
                objects.append({
                    'Key': obj['Key'],
                    'LastModified': obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
                })
            return objects
        else:
            return "El bucket está vacío."
    
    except ClientError as e:
        # Manejo de errores si no tienes acceso o el bucket no existe
        if e.response['Error']['Code'] == 'AccessDenied':
            return f"No tienes acceso al bucket '{bucket_name}' o el bucket no existe."
        else:
            return f"Error al intentar acceder al bucket '{bucket_name}': {e}"

# Ruta principal (formulario para ingresar el nombre del bucket)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el formulario y listar los objetos
@app.route('/listar', methods=['POST'])
def listar():
    bucket_name = request.form.get('bucket_name')
    if not bucket_name:
        return "Por favor, proporciona un nombre de bucket válido."

    # Llamar la función listar_objetos con el nombre del bucket proporcionado
    result = listar_objetos(bucket_name)

    if isinstance(result, list):
        return render_template('result.html', objects=result, bucket_name=bucket_name)
    else:
        return render_template('result.html', error=result, bucket_name=bucket_name)

if __name__ == '__main__':
    app.run(debug=True)