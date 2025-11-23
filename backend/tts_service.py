import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Voz: Rachel
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" 

def text_to_speech_stream(text):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    # 1. Chequeo de seguridad: ¿Existe la clave?
    if not api_key:
        print(" ERROR: No se encontró ELEVENLABS_API_KEY en el archivo .env")
        yield b""
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2", # Intenta usar v2 para español
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    print(f"📡 Enviando petición a ElevenLabs... (Key termina en: ...{api_key[-4:]})")
    
    # Hacemos la petición
    response = requests.post(url, json=data, headers=headers, stream=True)

    # 2. Si falla, imprimimos el mensaje EXACTO de ElevenLabs
    if response.status_code != 200:
        print(f" ERROR CRÍTICO ELEVENLABS ({response.status_code}):")
        print(response.text) # <--- ESTO NOS DIRÁ EL PROBLEMA REAL
        yield b""
        return

    print("✅ Audio recibido correctamente, iniciando stream...")
    
    # Devolvemos el audio
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            yield chunk