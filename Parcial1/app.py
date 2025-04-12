import boto3
import pytesseract
from PIL import Image
import io
import json
import os

# Configuración de buckets
INPUT_BUCKET = os.getenv('INPUT_BUCKET')
OUTPUT_BUCKET = os.getenv('OUTPUT_BUCKET')

s3 = boto3.client('s3')

def descargar_imagen(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return Image.open(io.BytesIO(response['Body'].read()))

def extraer_datos_texto(texto):
    lineas = texto.split("\n")
    datos = {
        "numero_recibo": None,
        "fecha": None,
        "total": None,
        "nombre_restaurante": None
    }
    for linea in lineas:
        if "Recibo" in linea:
            datos["numero_recibo"] = linea.split()[-1]
        elif "Fecha" in linea:
            datos["fecha"] = linea.split()[-1]
        elif "Total" in linea:
            datos["total"] = linea.split()[-1]
        elif "Restaurante" in linea:
            datos["nombre_restaurante"] = linea.replace("Restaurante", "").strip()
    return datos

def guardar_json_s3(datos, nombre_json):
    s3.put_object(Bucket=OUTPUT_BUCKET, Key=nombre_json, Body=json.dumps(datos))

def procesar_recibo(key):
    imagen = descargar_imagen(INPUT_BUCKET, key)
    texto = pytesseract.image_to_string(imagen)
    datos = extraer_datos_texto(texto)
    nombre_json = key.replace('.jpg', '.json').replace('.png', '.json')
    guardar_json_s3(datos, nombre_json)


