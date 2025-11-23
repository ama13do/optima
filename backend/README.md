# Optima Backend - API Documentation

Backend API construido con FastAPI para análisis multimodal de datos usando Google Gemini y ElevenLabs.

---

## 🏗️ Arquitectura

```
backend/
├── main.py              # FastAPI app principal y endpoints
├── gemini_service.py    # Servicios de análisis con Google Gemini
├── tts_service.py       # Text-to-Speech con ElevenLabs
├── upload_service.py    # Gestión de uploads a Vultr
├── general.py           # Utilidades generales
├── test_keys.py         # Validación de API keys
└── .env                 # Variables de entorno (no incluido)
```

---

## 🚀 Instalación y Configuración

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install fastapi uvicorn google-generativeai python-dotenv requests python-multipart
```

### 3. Configurar variables de entorno

Crear archivo `.env` en la raíz del backend:

```env
# Google Gemini API
GOOGLE_API_KEY=your_google_api_key_here

# ElevenLabs API
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Vultr (Opcional - para uploads)
VULTR_API_KEY=your_vultr_api_key_here
VULTR_BUCKET_NAME=your_bucket_name
```

### 4. Iniciar el servidor

```bash
# Modo desarrollo
python main.py

# Modo producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 Endpoints Principales

### 🔍 Análisis de Datos

#### `POST /analyze-batch`
Análisis rápido de múltiples archivos.

**Parámetros:**
- `files`: Lista de archivos (imagen, PDF, CSV, JSON)
- `prompt`: Objetivo del análisis

**Respuesta:**
```json
{
  "results": [
    {
      "filename": "dataset.csv",
      "mime_type": "text/csv",
      "analysis": "Análisis detallado...",
      "status": "success"
    }
  ],
  "total": 1
}
```

#### `POST /analyze-advanced`
Análisis avanzado con configuración de modelo y nivel.

**Parámetros:**
- `files`: Archivos a analizar
- `prompt`: Descripción del análisis deseado
- `model`: Modelo Gemini (gemini-2.5-pro, gemini-2.5-flash)
- `analysis_level`: Nivel de detalle (basic, standard, advanced, expert)

#### `POST /quick-check`
Validación rápida de datos para IA.

#### `POST /deep-analysis`
Análisis exhaustivo con Gemini Pro.

---

### 🎙️ Audio (Text-to-Speech & Speech-to-Text)

#### `POST /speak`
Convierte texto a voz usando ElevenLabs.

**Body:**
```json
{
  "text": "Hola, este es un mensaje de prueba"
}
```

**Respuesta:** Stream de audio MP3

**Ejemplo cURL:**
```bash
curl -X POST "http://localhost:8000/speak" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola desde Optima"}' \
  --output audio.mp3
```

#### `POST /transcribe`
Transcribe audio a texto usando Gemini.

**Parámetros:**
- `file`: Archivo de audio (mp3, wav, webm, ogg)

**Respuesta:**
```json
{
  "transcription": "Texto transcrito del audio",
  "status": "success"
}
```

---

### 📊 Análisis Especializados

#### `POST /analyze-bias-detailed`
Análisis exhaustivo de sesgos en datasets.

**Áreas de análisis:**
- Género
- Raza
- Edad
- Geográfico
- Temporal
- Selección

#### `POST /analyze-json`
Análisis de datasets JSON estructurados.

**Body:**
```json
{
  "data": {"usuarios": [...], "productos": [...]},
  "prompt": "Analiza la distribución de usuarios",
  "model": "gemini-2.5-pro"
}
```

#### `POST /compare-datasets`
Compara múltiples datasets.

**Body:**
```json
{
  "datasets": [
    {"name": "Dataset A", "data": {...}},
    {"name": "Dataset B", "data": {...}}
  ],
  "criteria": "Compara completitud y calidad",
  "model": "gemini-2.5-pro"
}
```

#### `POST /synthetic-data-plan`
Genera un plan para crear datos sintéticos.

#### `POST /generate-report`
Genera reporte ejecutivo consolidado.

---

### 🛠️ Utilidades

#### `GET /health`
Chequeo de salud del API.

**Respuesta:**
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "services": ["Gemini", "ElevenLabs"]
}
```

#### `GET /`
Información general del API.

---

## 🧠 Servicios de Gemini

### Modelos Disponibles

```python
class GeminiModel(Enum):
    FLASH_2_5 = "gemini-2.5-flash"      # Rápido y eficiente
    PRO_2_5 = "gemini-2.5-pro"          # Mayor precisión
    FLASH_1_5 = "gemini-1.5-flash"      # Legacy rápido
    PRO_1_5 = "gemini-1.5-pro"          # Legacy preciso
```

### Niveles de Análisis

```python
class AnalysisLevel(Enum):
    BASIC = "basic"         # Análisis superficial
    STANDARD = "standard"   # Análisis estándar
    ADVANCED = "advanced"   # Análisis detallado
    EXPERT = "expert"       # Análisis exhaustivo
```

### Funciones Principales

- `analyze_file_with_gemini()`: Análisis general de archivos
- `analyze_json_dataset()`: Análisis de JSON estructurado
- `compare_datasets()`: Comparación de múltiples datasets
- `analyze_bias_detailed()`: Detección avanzada de sesgos
- `transcribe_audio_with_gemini()`: Transcripción de audio
- `quick_analysis()`: Análisis rápido (Flash)
- `deep_analysis()`: Análisis profundo (Pro + Expert)

---

## 🎤 Servicio de Voz (ElevenLabs)

### Configuración

```python
# Voice ID (Rachel - voz por defecto)
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

# Modelo multilingüe
MODEL = "eleven_multilingual_v2"
```

### Uso Programático

```python
from tts_service import text_to_speech_stream

# Generar audio
audio_stream = text_to_speech_stream("Hola mundo")

# Guardar a archivo
with open("output.mp3", "wb") as f:
    for chunk in audio_stream:
        f.write(chunk)
```

---

## 🔧 Testing

### Probar API Keys

```bash
python test_keys.py
```

### Probar endpoint específico

```bash
# Health check
curl http://localhost:8000/health

# Análisis rápido
curl -X POST "http://localhost:8000/quick-check" \
  -F "file=@test.csv" \
  -F "prompt=¿Este dataset es válido?"

# Text-to-Speech
curl -X POST "http://localhost:8000/speak" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola desde Optima"}' \
  --output test.mp3
```

---

## 📈 Optimización y Escalabilidad

### Configuración en Vultr

```bash
# Instalar dependencias del sistema
sudo apt update
sudo apt install python3-pip python3-venv

# Configurar servicio systemd
sudo nano /etc/systemd/system/optima-api.service
```

**optima-api.service:**
```ini
[Unit]
Description=Optima FastAPI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/optima/backend
Environment="PATH=/home/optima/backend/venv/bin"
ExecStart=/home/optima/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Activar servicio
sudo systemctl enable optima-api
sudo systemctl start optima-api
sudo systemctl status optima-api
```

---

## 🔒 Seguridad

### Mejores Prácticas

1. **Nunca commitear `.env`**: Incluir en `.gitignore`
2. **Validar inputs**: FastAPI valida automáticamente con Pydantic
3. **Rate limiting**: Implementar con `slowapi` si es necesario
4. **CORS**: Configurar orígenes permitidos en producción
5. **HTTPS**: Usar reverse proxy (nginx/caddy) con SSL

### Configuración CORS Producción

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tortadetamal.fit"],  # Especificar dominios
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## 📊 Monitoreo y Logs

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Métricas

Considerar integrar:
- **Prometheus**: Métricas de rendimiento
- **Sentry**: Error tracking
- **Grafana**: Dashboards de monitoreo

---

## 🐛 Troubleshooting

### Error: "GOOGLE_API_KEY not found"

```bash
# Verificar .env existe
ls -la .env

# Verificar contenido (sin mostrar keys)
grep "GOOGLE_API_KEY" .env
```

### Error: ElevenLabs 401 Unauthorized

- Verificar que la API key sea válida
- Verificar que tienes créditos disponibles
- Revisar `test_keys.py` para diagnóstico

### Error: Import errors

```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt
```

### Error: Puerto 8000 ya en uso

```bash
# Encontrar proceso
lsof -i :8000

# Matar proceso
kill -9 <PID>
```

---

## 📦 Dependencias Completas

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
python-multipart>=0.0.6
requests>=2.31.0
pydantic>=2.0.0
```

---

## 🔗 Enlaces Útiles

- **API Docs**: http://45.77.163.127:8000/docs
- **Gemini API**: https://ai.google.dev/
- **ElevenLabs**: https://elevenlabs.io/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **Vultr**: https://www.vultr.com/docs/

---

## 🤝 Contribuir

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para guías de desarrollo.

---

**Construido con ❤️ usando FastAPI, Gemini y ElevenLabs**
