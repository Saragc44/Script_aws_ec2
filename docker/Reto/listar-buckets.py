import boto3
from botocore.exceptions import ClientError

def listar_objetos(bucket_name):
    # Crear una sesión de S3 usando boto3
    s3 = boto3.client('s3')

    try:
        # Intentar obtener la lista de objetos en el bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        # Si el bucket tiene objetos, listarlos
        if 'Contents' in response:
            print(f"Objetos en el bucket '{bucket_name}':")
            for obj in response['Contents']:
                print(f"{obj['Key']} (Última modificación: {obj['LastModified']})")
        else:
            print(f"El bucket '{bucket_name}' está vacío.")
    
    except ClientError as e:
        # Si ocurre un error (acceso denegado o bucket no existe)
        if e.response['Error']['Code'] == 'AccessDenied':
            print(f"No tienes acceso al bucket '{bucket_name}' o el bucket no existe.")
        else:
            print(f"Error al intentar acceder al bucket '{bucket_name}': {e}")
            
# Verificar si se ha pasado el nombre del bucket como parámetro
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Por favor, proporciona el nombre de un bucket como parámetro.")
        sys.exit(1)

    bucket_name = sys.argv[1]
    listar_objetos(bucket_name)
