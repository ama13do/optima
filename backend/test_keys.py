import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("--- DIAGNÓSTICO DE CLAVES ---")

# 1. Checar Vultr
vultr = os.getenv("VULTR_ACCESS_KEY")
print(f"✅ Vultr Key detectada: {'SÍ' if vultr else '❌ NO (Revisa tu .env)'}")

# 2. Checar ElevenLabs
eleven = os.getenv("ELEVENLABS_API_KEY")
print(f"✅ ElevenLabs Key detectada: {'SÍ' if eleven else '❌ NO (Revisa tu .env)'}")

# 3. Checar Gemini (Prueba real de conexión)
google_key = os.getenv("GOOGLE_API_KEY")
if google_key:
    print(f"✅ Google Key detectada. Probando conexión...")
    try:
        genai.configure(api_key=google_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Di 'Hola'")
        print(f"🚀 Gemini responde: {response.text}")
    except Exception as e:
        print(f"❌ Error conectando con Gemini: {e}")
else:
    print("❌ NO se encontró GOOGLE_API_KEY")