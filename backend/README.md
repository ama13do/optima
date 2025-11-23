# 🧠 Optima Backend (API)

El cerebro de la plataforma Optima. Esta API RESTful maneja la orquestación entre el almacenamiento en Vultr, el análisis cognitivo de Gemini y la síntesis de voz de ElevenLabs.

## 🌐 URLs de Producción

* **API Docs:** __http://45.77.163.127:8000/docs__
* **API Root:** __http://45.77.163.127:8000__

---

## ✨ Características

* **Análisis Multimodal:** Procesa imágenes, PDFs y Audio.
* **Streaming de Datos:** Sube archivos a Vultr Object Storage sin tocar el disco local (memoria eficiente).
* **Streaming de Audio:** Genera voz en tiempo real (chunked transfer) para baja latencia.
* **Detección de Sesgos:** Algoritmos de Fairness AI mediante prompts expertos.
* **Speech-to-Text (STT):** Transcripción de audio nativa con Gemini.

---

## 🛠️ Instalación

1.  **Crear entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install fastapi uvicorn boto3 python-multipart google-generativeai python-dotenv requests
    ```

3.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz de `backend/` con el siguiente contenido:

    ```env
    # --- VULTR CONFIG ---
    VULTR_ACCESS_KEY=tu_access_key
    VULTR_SECRET_KEY=tu_secret_key
    VULTR_ENDPOINT=https://ewr1.vultrobjects.com
    BUCKET_NAME=nombre-de-tu-bucket

    # --- AI SERVICES ---
    GOOGLE_API_KEY=tu_gemini_key
    ELEVENLABS_API_KEY=tu_elevenlabs_key
    ```

---

## 🚀 Ejecución

**Modo Desarrollo (Local):**
```bash
uvicorn main:app --reload
```

* Swagger UI: **http://127.0.0.1:8000/docs**
* API Root: **http://127.0.0.1:8000**

**Modo Producción (Servidor):**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📡 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/analyze-batch` | Sube archivos a Vultr y analiza calidad/sesgos con Gemini. |
| POST | `/speak` | Convierte texto a stream de audio (TTS). |
| POST | `/transcribe` | Convierte archivo de audio a texto (STT). |
| POST | `/analyze-json` | Análisis estadístico de datos estructurados. |
