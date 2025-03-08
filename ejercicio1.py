import boto3
from botocore.exceptions import ClientError


# Crear un cliente de S3
s3_client = boto3.client('s3', region_name='us-east-1')

# Función para crear un bucket de S3
def create_s3_bucket(bucket_name):
    try:
        # Si la región es us-east-1, no se necesita LocationConstraint
        s3_client.create_bucket(Bucket=bucket_name)       
        
        print(f"Bucket '{bucket_name}' creado exitosamente.")
    except ClientError as e:
        print(f"Error al crear el bucket: {e}")


# Crear un cliente de EC2
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Función para lanzar una instancia de EC2
def create_ec2_instance():
    try:
        response = ec2_client.run_instances(
            ImageId='ami-08b5b3a93ed654d19',  # Cambia a la AMI que prefieras
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            KeyName='sara_',  # Cambia al nombre de tu par de claves
        )
        print("Instancia de EC2 lanzada exitosamente.")
        return response
    except ClientError as e:
        print(f"Error al lanzar la instancia: {e}")

# Uso de las funciones
bucket_name = 'sara-garcia-1-bucket'  # Cambia al nombre deseado para tu bucket
create_s3_bucket(bucket_name)
create_ec2_instance()