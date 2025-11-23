# Optima: Recuperando el Tiempo para Innovar

> *"La creatividad no debería morir en una hoja de cálculo."*

[![API Status](http://45.77.163.127:8000/health)](http://45.77.163.127:8000/docs)
[![Live Demo](https://img.shields.io/badge/demo-live-success)](http://tortadetamal.fit/)
[![GitHub](https://img.shields.io/badge/github-optima-blue)](https://github.com/ama13do/optima)

---

## 🎯 El Problema

¿Recuerdas esa sensación de tener una idea revolucionaria, pero sentir cómo se apaga lentamente mientras pasas **semanas enteras** limpiando archivos CSV rotos, renombrando imágenes una por una o luchando contra formatos ilegibles?

La estadística es fría: los científicos de datos pierden el **80% de su tiempo** en la limpieza de datos (Data Cleaning). Pero la realidad humana es peor: es tiempo que le robamos a la innovación, a la solución de problemas reales y, a veces, a nuestra propia vida personal.

**Optima** nace de esa frustración compartida. No construimos otra herramienta de ETL; construimos el compañero que hubiéramos deseado tener en esas noches largas antes de un deadline.

---

## 💡 La Solución: Empatía Técnica + Potencia en la Nube

**Optima** es una plataforma multimodal de auditoría y curación de datos que entiende el contexto como lo haría un humano, pero procesa a la velocidad de la nube.

Utilizamos la infraestructura robusta de **[Vultr](https://www.vultr.com/)** para escalar sin límites y el cerebro de **Google Gemini 1.5** para encontrar sentido en el caos no estructurado.

**Nuestra misión es simple: Que tú te dediques a crear, mientras Optima se dedica a limpiar.**

---

## ✨ ¿Cómo funciona la Magia?

En lugar de escribir scripts interminables y frágiles, nuestra arquitectura permite que la IA "vea", "lea" y "entienda" el contexto de tus archivos.

```python
# El núcleo de Optima: Simple pero poderoso
def analyze_dataset_with_optima(file):
    # 1. Gemini analiza el contexto visual y semántico
    context = gemini.vision(file)
    
    # 2. Detectamos si los datos son justos (Fairness AI)
    bias_report = gemini.detect_hidden_biases(context, protect=["gender", "race"])
    
    if bias_report.severity > critical_threshold:
        # 3. ElevenLabs te avisa humanamente
        return elevenlabs.speak("Atención: He detectado un sesgo crítico en este archivo.")
    
    return generate_training_ready_json(context)
```

---

## 🧮 El Corazón del Proyecto: Ética Matemática

Lo que más nos preocupa no es solo que el código falle, sino que el código discrimine. Un modelo entrenado con datos sesgados perpetúa injusticias.

En Optima, calculamos la **Puntuación de Integridad** ($I_{score}$) de tu dataset en tiempo real. Definimos la calidad no solo por la estructura técnica, sino por la equidad ética:

$$Q_{final} = \frac{\sum (w_i \cdot C_i)}{1 + \alpha \cdot B_{detected}}$$

Donde:

- $Q_{final}$: Calidad ética y técnica del dataset.
- $C_i$: Completitud de los datos (Missing values, ruido, resolución).
- $B_{detected}$: Nivel de sesgo detectado por los modelos de visión de Gemini.

Si el sesgo aumenta, la calidad desciende matemáticamente, obligándonos a ser mejores ingenieros desde el inicio.

---

## 🎙️ Interacción Humana Real (ElevenLabs)

Sabemos que mirar tablas de logs en silencio es agotador y solitario. Por eso, integramos **ElevenLabs**.

Optima no te lanza un error en rojo en la consola. **Optima habla contigo.**

🔊 **Agente Optima:** *"Hola, he notado que el 90% de tus imágenes etiquetadas como 'ingenieros' son hombres. Para evitar un modelo sesgado, te sugiero agregar diversidad a la muestra antes de entrenar."*

---

## 🛠️ Stack Tecnológico

Hemos construido Optima sobre hombros de gigantes:

| Componente | Tecnología | Función |
|------------|-----------|---------|
| **Infraestructura** | [Vultr Cloud Compute](https://www.vultr.com/) | Procesamiento de alto rendimiento y baja latencia. |
| **Almacenamiento** | Vultr Object Storage | Escalabilidad infinita para Datasets masivos. |
| **Inteligencia** | [Google Gemini 1.5 & 2.5](https://ai.google.dev/) | Análisis Multimodal (Visión + Texto + Audio). |
| **Voz** | [ElevenLabs API](https://elevenlabs.io/) | Feedback empático, natural y humano. |
| **Backend** | Python (FastAPI) | Orquestación asíncrona y veloz. |
| **Frontend** | React + Vite + Tailwind CSS | Experiencia de usuario moderna y fluida. |
| **Dominio** | GoDaddy + Vultr | Hosting profesional y confiable. |

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8+
- Node.js 18+
- Cuenta en [Vultr](https://www.vultr.com/)
- API Keys: [Google Gemini](https://ai.google.dev/), [ElevenLabs](https://elevenlabs.io/)

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/ama13do/optima.git
cd optima
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install fastapi uvicorn google-generativeai python-dotenv requests python-multipart

# Crear archivo .env
cat > .env << EOL
GOOGLE_API_KEY=tu_api_key_aqui
ELEVENLABS_API_KEY=tu_api_key_aqui
EOL

# Iniciar servidor
python main.py
```

3. **Frontend Setup**
```bash
cd ../frontend
npm install
npm run dev
```

4. **Acceder a la aplicación**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

## 🌐 Despliegues en Producción

### Aplicación Live
- **Vultr Direct**: http://45.77.163.127
- **Dominio GoDaddy**: http://tortadetamal.fit/

### API Backend
- **API Docs**: http://45.77.163.127:8000/docs
- **Health Check**: http://45.77.163.127:8000/health

---

## 📚 Documentación Detallada

- **[Backend README](./backend/README.md)** - Arquitectura del API, servicios y endpoints
- **[Frontend README](./frontend/README.md)** - Componentes, UI y deployment

---

## 🎯 Características Principales

### 🔍 Análisis Multimodal
- Soporta imágenes, PDFs, CSV, JSON, audio
- Detección automática de sesgos (género, raza, edad)
- Evaluación de calidad para entrenamiento de IA

### 🎤 Interfaz de Voz
- Text-to-Speech con ElevenLabs
- Speech-to-Text con Gemini
- Feedback auditivo en tiempo real

### ⚡ Procesamiento Inteligente
- Análisis rápido con Gemini Flash
- Análisis profundo con Gemini Pro
- Comparación de datasets
- Generación de datos sintéticos

### 📊 Reportes Detallados
- Visualizaciones interactivas
- Métricas de calidad
- Recomendaciones accionables
- Exportación JSON/PDF

---

## 🔮 Hacia el Futuro

Hoy, Optima limpia y audita datos. Mañana, será la fábrica de agentes autónomos.

### Roadmap

- **Generación de Agentes "No-Code"**: Crear un chatbot experto en tus datos con un solo clic.
- **Contexto Web en Tiempo Real**: Enriquecimiento automático de datasets buscando información faltante en internet.
- **Marketplace de Datos Limpios**: Compartir datasets ya auditados y certificados por Optima.

Queremos un futuro donde crear una IA sea tan fácil como explicarle tu idea a un amigo.

**Devolvámosle el tiempo a los desarrolladores para que hagan lo que mejor saben hacer: cambiar el mundo.**

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Equipo

Construido con ❤️ por desarrolladores que entienden el dolor de la limpieza de datos.

**GitHub**: [ama13do](https://github.com/ama13do)

---

## 📞 Soporte

¿Tienes preguntas? Abre un [Issue](https://github.com/ama13do/optima/issues) o contacta al equipo.

---

*"La mejor herramienta es la que no ves, porque simplemente funciona."*
