import boto3
import os
import uuid
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Configuración de credenciales
ACCESS_KEY = os.getenv("VULTR_ACCESS_KEY")
SECRET_KEY = os.getenv("VULTR_SECRET_KEY")
# Asegurarse que el endpoint no tenga slash al final
ENDPOINT = os.getenv("VULTR_ENDPOINT").rstrip("/") 
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Crear el cliente S3 (boto3)
# Esto conecta tu Python con Vultr
s3_client = boto3.client(
    's3',
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name='ewr1' # Opcional, pero buena práctica poner tu región de Vultr
)

def upload_file_to_vultr(file_obj, original_filename, content_type):
    """
    Sube un archivo a Vultr Object Storage y devuelve su URL pública.
    """
    try:
        # 1. Generar un nombre único para el archivo (para evitar duplicados)
        # Ejemplo: de "mi_foto.png" pasa a "a1b2c3d4-mi_foto.png"
        file_extension = original_filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # 2. Subir el archivo
        # ExtraArgs={'ACL': 'public-read'} hace que el archivo sea accesible por internet
        # para que luego Gemini pueda leerlo.
        s3_client.upload_fileobj(
            file_obj,
            BUCKET_NAME,
            unique_filename,
            ExtraArgs={'ACL': 'public-read', 'ContentType': content_type}
        )

        # 3. Construir la URL pública
        # La estructura suele ser: https://ewr1.vultrobjects.com/nombre-bucket/nombre-archivo
        file_url = f"{ENDPOINT}/{BUCKET_NAME}/{unique_filename}"
        
        print(f"✅ Archivo subido con éxito: {file_url}")
        return file_url

    except Exception as e:
        print(f"❌ Error subiendo a Vultr: {e}")
        return None