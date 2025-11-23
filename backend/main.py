from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from upload_service import upload_file_to_vultr # Importamos tu nuevo servicio
import shutil

app = FastAPI()

# Modelo para recibir el prompt del usuario (además del archivo)
class AnalysisRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "API Online 🚀"}

@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):
    """
    1. Recibe el archivo.
    2. Lo sube a Vultr.
    3. (Próximamente) Lo manda a Gemini.
    """
    
    # 1. Subir archivo a Vultr
    print(f"Recibiendo archivo: {file.filename}")
    
    vultr_url = upload_file_to_vultr(file.file, file.filename, file.content_type)
    
    if not vultr_url:
        raise HTTPException(status_code=500, detail="Falló la subida a Vultr")

    # AQUÍ ES DONDE LLAMAREMOS A GEMINI EN EL SIGUIENTE PASO
    # Por ahora, devolvemos la URL para probar que funciona.
    
    return {
        "filename": file.filename,
        "url_vultr": vultr_url,
        "message": "Archivo guardado correctamente. Listo para análisis."
    }