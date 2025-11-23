from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import io

# 1. IMPORTAMOS TUS SERVICIOS EXISTENTES Y LOS NUEVOS
from gemini_service import (
    analyze_file_with_gemini,
    analyze_json_dataset,
    compare_datasets,
    generate_synthetic_data_plan,
    analyze_bias_detailed,
    generate_data_quality_report,
    quick_analysis,
    deep_analysis,
    transcribe_audio_with_gemini, # <--- NUEVA FUNCIÓN IMPORTADA
    GeminiModel,
    AnalysisLevel
)

# 2. IMPORTAMOS EL SERVICIO DE VOZ (ELEVENLABS)
from tts_service import text_to_speech_stream

app = FastAPI(
    title="DataClean AI - Enhanced API",
    description="API multimodal: Análisis de Datos + Voz (TTS) + Escucha (STT)",
    version="2.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELOS PYDANTIC ====================

class JSONAnalysisRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="JSON data a analizar")
    prompt: str = Field(..., description="Objetivo del análisis")
    model: Optional[str] = Field(GeminiModel.PRO_2_5.value, description="Modelo de Gemini")

class CompareRequest(BaseModel):
    datasets: List[Dict[str, Any]] = Field(..., description="Lista de datasets a comparar")
    criteria: str = Field(..., description="Criterio de comparación")
    model: Optional[str] = Field(GeminiModel.PRO_2_5.value, description="Modelo de Gemini")

class SyntheticDataRequest(BaseModel):
    original_summary: Dict[str, Any] = Field(..., description="Resumen del dataset original")
    improvements: List[str] = Field(..., description="Mejoras objetivo")
    model: Optional[str] = Field(GeminiModel.PRO_2_5.value, description="Modelo de Gemini")

class BatchReportRequest(BaseModel):
    analysis_results: List[Dict[str, Any]] = Field(..., description="Resultados de análisis previos")
    model: Optional[str] = Field(GeminiModel.PRO_2_5.value, description="Modelo de Gemini")

# Modelo para la solicitud de voz (TTS)
class SpeakRequest(BaseModel):
    text: str

# ==================== ENDPOINTS DE AUDIO (NUEVOS) ====================

@app.post("/speak")
async def speak_text(request: SpeakRequest):
    """
    TEXT-TO-SPEECH (TTS): Convierte texto a voz usando ElevenLabs.
    Retorna un stream de audio MP3.
    """
    try:
        audio_stream = text_to_speech_stream(request.text)
        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en TTS: {str(e)}")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    SPEECH-TO-TEXT (STT): Recibe un archivo de audio (mp3, wav, webm) 
    y retorna la transcripción de texto usando Gemini 1.5 Flash.
    """
    try:
        audio_bytes = await file.read()
        mime_type = file.content_type or "audio/mp3"
        
        # Usamos la función nueva de gemini_service
        text = transcribe_audio_with_gemini(audio_bytes, mime_type)
        
        return {"transcription": text, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Transcripción: {str(e)}")

# ==================== ENDPOINTS DE ANÁLISIS DE DATOS ====================

@app.post("/analyze-batch")
async def analyze_batch(
    files: List[UploadFile] = File(...),
    prompt: str = Form(...)
):
    """ENDPOINT ORIGINAL - Mantiene compatibilidad con frontend actual."""
    results = []
    for file in files:
        try:
            file_bytes = await file.read()
            mime_type = file.content_type or "application/octet-stream"
            analysis = quick_analysis(file_bytes, mime_type, prompt)
            results.append({
                "filename": file.filename,
                "mime_type": mime_type,
                "analysis": analysis,
                "status": "success"
            })
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e), "status": "failed"})
    return {"results": results, "total": len(results)}

@app.post("/analyze-advanced")
async def analyze_advanced(
    files: List[UploadFile] = File(...),
    prompt: str = Form(...),
    model: str = Form(GeminiModel.PRO_2_5.value),
    analysis_level: str = Form(AnalysisLevel.EXPERT.value)
):
    """Análisis AVANZADO con Gemini Pro y niveles configurables."""
    results = []
    for file in files:
        try:
            file_bytes = await file.read()
            mime_type = file.content_type or "application/octet-stream"
            analysis = analyze_file_with_gemini(
                file_bytes, mime_type, prompt, model_name=model, analysis_level=analysis_level
            )
            results.append({
                "filename": file.filename,
                "analysis": analysis,
                "status": "success"
            })
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e), "status": "failed"})
    
    return {"results": results, "total": len(results), "model_used": model}

@app.post("/analyze-json")
async def analyze_json(request: JSONAnalysisRequest):
    """Analiza datasets JSON estructurados."""
    try:
        result = analyze_json_dataset(request.data, request.prompt, model_name=request.model)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare-datasets")
async def compare_datasets_endpoint(request: CompareRequest):
    """Compara múltiples datasets."""
    try:
        result = compare_datasets(request.datasets, request.criteria, model_name=request.model)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthetic-data-plan")
async def synthetic_data_plan(request: SyntheticDataRequest):
    """Genera un plan para datos sintéticos."""
    try:
        result = generate_synthetic_data_plan(request.original_summary, request.improvements, model_name=request.model)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-bias-detailed")
async def bias_analysis(
    file: UploadFile = File(...),
    focus_areas: str = Form('["gender", "race", "age", "geographic", "temporal", "selection"]'),
    model: str = Form(GeminiModel.PRO_2_5.value)
):
    """Análisis EXHAUSTIVO de sesgos."""
    try:
        import json
        file_bytes = await file.read()
        mime_type = file.content_type or "application/octet-stream"
        areas = json.loads(focus_areas)
        result = analyze_bias_detailed(file_bytes, mime_type, areas, model_name=model)
        return JSONResponse(content={"filename": file.filename, "bias_analysis": result, "status": "success"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-report")
async def generate_report(request: BatchReportRequest):
    """Genera reporte ejecutivo consolidado."""
    try:
        result = generate_data_quality_report(request.analysis_results, model_name=request.model)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quick-check")
async def quick_check(
    file: UploadFile = File(...),
    prompt: str = Form("Analiza rápidamente si este dato sirve para IA")
):
    """Análisis ULTRA-RÁPIDO."""
    try:
        file_bytes = await file.read()
        mime_type = file.content_type or "application/octet-stream"
        result = quick_analysis(file_bytes, mime_type, prompt)
        return JSONResponse(content={"filename": file.filename, "quick_check": result, "status": "success"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deep-analysis")
async def deep_analysis_endpoint(
    file: UploadFile = File(...),
    prompt: str = Form("Análisis experto completo para entrenamiento de IA")
):
    """Análisis PROFUNDO con Gemini Pro + nivel EXPERT."""
    try:
        file_bytes = await file.read()
        mime_type = file.content_type or "application/octet-stream"
        result = deep_analysis(file_bytes, mime_type, prompt)
        return JSONResponse(content={"filename": file.filename, "deep_analysis": result, "status": "success"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE UTILIDAD ====================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.1.0", "services": ["Gemini", "ElevenLabs"]}

@app.get("/")
async def root():
    return {
        "message": "DataClean AI API v2.1",
        "docs": "/docs",
        "audio_features": {
            "tts": "/speak (Texto a Voz)",
            "stt": "/transcribe (Voz a Texto)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)