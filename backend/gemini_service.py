import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
from enum import Enum

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class GeminiModel(Enum):
    """Modelos disponibles de Gemini"""
    FLASH_2_5 = "gemini-2.5-flash"
    PRO_2_5 = "gemini-2.5-pro"
    FLASH_1_5 = "gemini-1.5-flash"
    PRO_1_5 = "gemini-1.5-pro"

class AnalysisLevel(Enum):
    """Niveles de profundidad de análisis"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    EXPERT = "expert"

# ==================== PROMPTS MEJORADOS ====================

EXPERT_SYSTEM_PROMPT = """
Actúa como un Ingeniero de Datos Senior con especialización en Machine Learning y Data Quality.

Tu objetivo es analizar archivos (imágenes, PDFs, JSON, CSV) para determinar su viabilidad en entrenamiento de IA.

CRITERIOS DE EVALUACIÓN:
1. **Calidad de Datos**: Resolución, legibilidad, completitud, consistencia
2. **Sesgos**: Género, raza, edad, geográfico, temporal, selección
3. **Representatividad**: Diversidad, balance de clases, cobertura
4. **Metadata**: Contexto, etiquetas, anotaciones
5. **Compliance**: GDPR, privacidad, derechos de autor

ANÁLISIS REQUERIDO:
- Calidad general (0-100%)
- Sesgos detectados con severidad (bajo/medio/alto)
- Usabilidad para IA (0-100%)
- Recomendaciones específicas
- Riesgos potenciales
"""

def get_analysis_prompt(analysis_level: str, user_goal: str) -> str:
    """Genera prompt según nivel de análisis"""
    
    base_schema = {
        "summary": "string - Resumen conciso del contenido",
        "data_quality_score": "number - Puntuación 0-100",
        "data_quality_details": {
            "resolution": "string - Alta/Media/Baja",
            "clarity": "string - Excelente/Buena/Regular/Mala",
            "completeness": "number - % de datos completos",
            "consistency": "string - Evaluación de consistencia"
        },
        "biases": {
            "detected": "boolean",
            "types": ["array de tipos de sesgo"],
            "severity": "string - Bajo/Medio/Alto/Crítico",
            "details": "string - Descripción detallada"
        },
        "usable_for_training": "boolean",
        "usability_score": "number - Puntuación 0-100",
        "recommendations": ["array de recomendaciones"],
        "risks": ["array de riesgos potenciales"]
    }
    
    if analysis_level == AnalysisLevel.BASIC.value:
        return f"""
{EXPERT_SYSTEM_PROMPT}

OBJETIVO DEL USUARIO: {user_goal}

Genera un JSON con análisis BÁSICO:
{{
    "summary": "Resumen breve",
    "data_quality_score": 0-100,
    "biases": {{"detected": true/false, "types": []}},
    "usable_for_training": true/false,
    "usability_score": 0-100
}}
"""
    
    elif analysis_level == AnalysisLevel.EXPERT.value:
        return f"""
{EXPERT_SYSTEM_PROMPT}

OBJETIVO DEL USUARIO: {user_goal}

Genera un JSON COMPLETO con análisis EXPERTO:
{json.dumps(base_schema, indent=2)}

INCLUYE ADEMÁS:
- "data_distribution": Análisis de distribución de datos
- "feature_analysis": Análisis de características/features
- "preprocessing_suggestions": Sugerencias de preprocesamiento
- "model_recommendations": Modelos de IA recomendados
- "ethical_considerations": Consideraciones éticas
- "compliance_check": Verificación de compliance (GDPR, privacidad)
"""
    
    else:  # STANDARD/ADVANCED
        return f"""
{EXPERT_SYSTEM_PROMPT}

OBJETIVO DEL USUARIO: {user_goal}

Genera un JSON con análisis {'AVANZADO' if analysis_level == AnalysisLevel.ADVANCED.value else 'ESTÁNDAR'}:
{json.dumps(base_schema, indent=2)}
"""

# ==================== FUNCIONES PRINCIPALES ====================

def analyze_file_with_gemini(
    file_bytes: bytes, 
    mime_type: str, 
    user_prompt: str,
    model_name: str = GeminiModel.FLASH_2_5.value,
    analysis_level: str = AnalysisLevel.STANDARD.value
) -> Dict[str, Any]:
    """
    Analiza archivos usando Gemini con configuración avanzada.
    
    Args:
        file_bytes: Bytes del archivo
        mime_type: Tipo MIME del archivo
        user_prompt: Objetivo del usuario
        model_name: Modelo de Gemini a usar
        analysis_level: Nivel de profundidad del análisis
    """
    try:
        model = genai.GenerativeModel(
            model_name,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,  # Más determinístico para análisis
                "top_p": 0.8,
                "top_k": 40
            }
        )

        file_part = {
            "mime_type": mime_type,
            "data": file_bytes
        }

        prompt = get_analysis_prompt(analysis_level, user_prompt)
        response = model.generate_content([prompt, file_part])
        
        result = json.loads(response.text)
        result["model_used"] = model_name
        result["analysis_level"] = analysis_level
        
        return result

    except Exception as e:
        print(f"❌ Error en Gemini: {e}")
        return {
            "error": str(e), 
            "status": "failed",
            "model_used": model_name
        }

def analyze_json_dataset(
    json_data: Dict[str, Any],
    user_prompt: str,
    model_name: str = GeminiModel.PRO_2_5.value
) -> Dict[str, Any]:
    """
    Analiza datasets en formato JSON usando Gemini Pro para lógica compleja.
    
    Perfecto para: datasets estructurados, configuraciones, resultados de API
    """
    try:
        model = genai.GenerativeModel(
            model_name,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.1
            }
        )

        prompt = f"""
{EXPERT_SYSTEM_PROMPT}

OBJETIVO: {user_prompt}

DATOS JSON A ANALIZAR:
{json.dumps(json_data, indent=2)}

Genera un análisis PROFUNDO del JSON incluyendo:
{{
    "data_structure": {{
        "schema_valid": true/false,
        "fields_count": number,
        "nested_levels": number,
        "data_types": {{"field": "type"}}
    }},
    "data_quality": {{
        "completeness": 0-100,
        "consistency_score": 0-100,
        "missing_values": {{"field": count}},
        "duplicates": number,
        "outliers_detected": boolean
    }},
    "statistical_analysis": {{
        "numeric_fields": [{{"field": "name", "mean": 0, "std": 0, "min": 0, "max": 0}}],
        "categorical_fields": [{{"field": "name", "unique_values": 0, "most_common": ""}}]
    }},
    "biases": {{
        "detected": boolean,
        "types": ["temporal", "selection", "sampling"],
        "severity": "Bajo/Medio/Alto",
        "recommendations": ["acciones correctivas"]
    }},
    "ml_readiness": {{
        "usable_for_training": boolean,
        "usability_score": 0-100,
        "preprocessing_needed": ["steps"],
        "feature_engineering_suggestions": ["suggestions"]
    }},
    "recommendations": ["Lista de recomendaciones priorizadas"],
    "summary": "Resumen ejecutivo"
}}
"""

        response = model.generate_content(prompt)
        result = json.loads(response.text)
        result["model_used"] = model_name
        result["dataset_size"] = len(str(json_data))
        
        return result

    except Exception as e:
        return {"error": str(e), "status": "failed"}

def compare_datasets(
    datasets: List[Dict[str, Any]],
    comparison_criteria: str,
    model_name: str = GeminiModel.PRO_2_5.value
) -> Dict[str, Any]:
    """
    Compara múltiples datasets y genera recomendaciones.
    
    Útil para: seleccionar el mejor dataset, identificar complementariedades
    """
    try:
        model = genai.GenerativeModel(
            model_name,
            generation_config={"response_mime_type": "application/json"}
        )

        prompt = f"""
Eres un experto en Data Science. Compara estos datasets según: {comparison_criteria}

DATASETS:
{json.dumps(datasets, indent=2)}

Genera:
{{
    "overall_ranking": [
        {{"dataset_index": 0, "score": 0-100, "reason": "string"}}
    ],
    "comparison_matrix": {{
        "quality": [{{"dataset": 0, "score": 0-100}}],
        "bias_level": [{{"dataset": 0, "score": 0-100}}],
        "usability": [{{"dataset": 0, "score": 0-100}}]
    }},
    "best_for_training": {{
        "dataset_index": 0,
        "confidence": 0-100,
        "reasons": ["razones"]
    }},
    "combination_strategy": {{
        "should_combine": boolean,
        "datasets_to_combine": [0, 1],
        "combination_method": "string",
        "expected_improvement": "percentage"
    }},
    "summary": "Resumen ejecutivo"
}}
"""

        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        return {"error": str(e), "status": "failed"}

def generate_synthetic_data_plan(
    original_data_summary: Dict[str, Any],
    target_improvements: List[str],
    model_name: str = GeminiModel.PRO_2_5.value
) -> Dict[str, Any]:
    """
    Genera un plan para crear datos sintéticos que mejoren el dataset.
    
    Útil para: aumentar diversidad, balancear clases, reducir sesgos
    """
    try:
        model = genai.GenerativeModel(
            model_name,
            generation_config={"response_mime_type": "application/json"}
        )

        prompt = f"""
Eres un experto en Synthetic Data Generation y Data Augmentation.

DATOS ORIGINALES:
{json.dumps(original_data_summary, indent=2)}

MEJORAS OBJETIVO:
{json.dumps(target_improvements, indent=2)}

Genera un PLAN DETALLADO:
{{
    "data_augmentation_strategy": {{
        "techniques": ["técnica1", "técnica2"],
        "parameters": {{"technique": {{"param": "value"}}}},
        "expected_increase": "percentage"
    }},
    "synthetic_data_generation": {{
        "method": "GAN/VAE/Statistical",
        "target_samples": number,
        "diversity_improvements": ["aspectos a diversificar"]
    }},
    "bias_mitigation": {{
        "techniques": ["resampling", "reweighting"],
        "target_groups": ["grupo1", "grupo2"],
        "expected_bias_reduction": "percentage"
    }},
    "quality_assurance": {{
        "validation_metrics": ["metric1", "metric2"],
        "acceptance_criteria": {{"metric": threshold}}
    }},
    "implementation_steps": [
        {{"step": 1, "action": "string", "tools": ["tool1"], "estimated_time": "string"}}
    ],
    "estimated_improvement": {{
        "usability_score": "+X%",
        "bias_reduction": "X%",
        "data_quality": "+X%"
    }}
}}
"""

        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        return {"error": str(e), "status": "failed"}

def analyze_bias_detailed(
    file_bytes: bytes,
    mime_type: str,
    focus_areas: List[str],
    model_name: str = GeminiModel.PRO_2_5.value
) -> Dict[str, Any]:
    """
    Análisis PROFUNDO de sesgos con recomendaciones específicas.
    
    focus_areas: ["gender", "race", "age", "geographic", "temporal", "selection"]
    """
    try:
        model = genai.GenerativeModel(
            model_name,
            generation_config={"response_mime_type": "application/json"}
        )

        file_part = {"mime_type": mime_type, "data": file_bytes}

        prompt = f"""
Eres un experto en Fairness in AI y Bias Detection.

ÁREAS DE ENFOQUE: {', '.join(focus_areas)}

Analiza EXHAUSTIVAMENTE los sesgos en este archivo:

{{
    "bias_analysis": {{
        "gender": {{
            "detected": boolean,
            "severity": 0-100,
            "evidence": ["ejemplos"],
            "affected_groups": ["grupos"],
            "recommendations": ["acciones"]
        }},
        "race_ethnicity": {{
            "detected": boolean,
            "severity": 0-100,
            "representation": {{"group": "percentage"}},
            "recommendations": ["acciones"]
        }},
        "age": {{
            "detected": boolean,
            "severity": 0-100,
            "distribution": {{"range": "percentage"}},
            "recommendations": ["acciones"]
        }},
        "geographic": {{
            "detected": boolean,
            "severity": 0-100,
            "regions_covered": ["regiones"],
            "underrepresented": ["regiones"],
            "recommendations": ["acciones"]
        }},
        "temporal": {{
            "detected": boolean,
            "time_period": "string",
            "recency_bias": boolean,
            "recommendations": ["acciones"]
        }},
        "selection_bias": {{
            "detected": boolean,
            "sampling_method": "string",
            "representativeness": 0-100,
            "recommendations": ["acciones"]
        }}
    }},
    "overall_fairness_score": 0-100,
    "risk_level": "Bajo/Medio/Alto/Crítico",
    "mitigation_priority": [
        {{"bias_type": "string", "priority": "Alta/Media/Baja", "action": "string"}}
    ],
    "compliance_check": {{
        "gdpr_compliant": boolean,
        "ethical_guidelines": boolean,
        "concerns": ["preocupaciones"]
    }},
    "summary": "Resumen ejecutivo de sesgos"
}}
"""

        response = model.generate_content([prompt, file_part])
        return json.loads(response.text)

    except Exception as e:
        return {"error": str(e), "status": "failed"}

def generate_data_quality_report(
    analysis_results: List[Dict[str, Any]],
    model_name: str = GeminiModel.PRO_2_5.value
) -> Dict[str, Any]:
    """
    Genera un reporte ejecutivo consolidado de múltiples análisis.
    """
    try:
        model = genai.GenerativeModel(
            model_name,
            generation_config={"response_mime_type": "application/json"}
        )

        prompt = f"""
Eres un Data Science Manager. Genera un REPORTE EJECUTIVO consolidado.

ANÁLISIS INDIVIDUALES:
{json.dumps(analysis_results, indent=2)}

Genera:
{{
    "executive_summary": "Resumen de 3-5 líneas",
    "key_findings": [
        {{"finding": "string", "impact": "Alto/Medio/Bajo", "action_required": boolean}}
    ],
    "overall_quality_score": 0-100,
    "overall_usability_score": 0-100,
    "critical_issues": [
        {{"issue": "string", "severity": "Crítico/Alto", "recommendation": "string"}}
    ],
    "dataset_statistics": {{
        "total_files": number,
        "usable_for_training": number,
        "requires_preprocessing": number,
        "rejected": number
    }},
    "bias_summary": {{
        "files_with_bias": number,
        "bias_types_found": ["tipos"],
        "average_severity": "string"
    }},
    "recommendations": {{
        "immediate": ["acciones urgentes"],
        "short_term": ["acciones 1-2 semanas"],
        "long_term": ["acciones estratégicas"]
    }},
    "next_steps": [
        {{"step": 1, "action": "string", "priority": "Alta/Media/Baja"}}
    ],
    "estimated_timeline": "string",
    "estimated_cost_savings": "string (opcional)"
}}
"""

        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        return {"error": str(e), "status": "failed"}

# ==================== FUNCIONES AUXILIARES ====================

def quick_analysis(file_bytes: bytes, mime_type: str, user_prompt: str) -> Dict[str, Any]:
    """Análisis rápido con Flash 2.5 (mantiene compatibilidad con frontend actual)"""
    return analyze_file_with_gemini(
        file_bytes, 
        mime_type, 
        user_prompt,
        model_name=GeminiModel.FLASH_2_5.value,
        analysis_level=AnalysisLevel.STANDARD.value
    )

def deep_analysis(file_bytes: bytes, mime_type: str, user_prompt: str) -> Dict[str, Any]:
    """Análisis profundo con Pro 2.5"""
    return analyze_file_with_gemini(
        file_bytes, 
        mime_type, 
        user_prompt,
        model_name=GeminiModel.PRO_2_5.value,
        analysis_level=AnalysisLevel.EXPERT.value
    )
# --- AGREGA ESTO AL FINAL DE TU gemini_service.py ---

def transcribe_audio_with_gemini(
    audio_bytes: bytes, 
    mime_type: str = "audio/mp3"
) -> str:
    """
    Transcribe audio a texto usando la capacidad multimodal de Gemini 1.5 Flash.
    """
    try:
        # Usamos Flash 1.5 porque es el mejor y más rápido para audio actualmente
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        audio_part = {
            "mime_type": mime_type,
            "data": audio_bytes
        }

        prompt = """
        Eres un transcriptor experto. 
        Transcribe el siguiente audio exactamente como se escucha. 
        Si hay ruido o silencio, ignóralo. 
        Devuelve SOLO el texto transcrito, sin explicaciones adicionales.
        """

        response = model.generate_content([prompt, audio_part])
        return response.text.strip()

    except Exception as e:
        print(f"❌ Error transcribiendo audio con Gemini: {e}")
        return "Error al transcribir el audio."