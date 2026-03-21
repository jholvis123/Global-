# app/infrastructure/chatbot/nlp/openai_service.py
"""
Servicio de NLP potenciado por OpenAI GPT.
Implementa la interfaz ServicioPLN del dominio y agrega conversación natural.
"""
import json
import logging
from typing import Dict, Any, List, Optional
from openai import OpenAI

from app.domain.chatbot.interfaces import ServicioPLN
from app.core.config import settings

logger = logging.getLogger(__name__)


# System prompt para extracción de datos de cotización
SYSTEM_PROMPT_EXTRACCION = """Eres un asistente de la empresa GLOBAL R.L. - Cooperativa de Transporte Nacional e Internacional de Bolivia.

Tu tarea es extraer datos estructurados del mensaje del usuario para generar una cotización de transporte.

Debes devolver SOLO un JSON válido con estos campos:
{
  "origen": "código de ciudad o null",
  "destino": "código de ciudad o null",
  "tipo_carga": "general|peligrosa|refrigerada|fragil",
  "peso_kg": numero o 0,
  "toneladas": numero o 0,
  "plazo_dias": numero o 5,
  "tipo_operacion": "normal|urgente|económico"
}

Ciudades de Bolivia y sus códigos:
- La Paz → LP
- Santa Cruz → SC
- Cochabamba → CBB
- Sucre → SCE
- Oruro → ORU
- Potosí → PT
- Tarija → TJ
- El Alto → LP
- Arica → ARICA

Reglas:
- Si mencionan toneladas, convierte a peso_kg (1 ton = 1000 kg) y también pon el valor en toneladas
- Si mencionan kg, convierte a toneladas también
- Si no mencionan peso, pon 0 en ambos
- Responde SOLO con el JSON, sin texto adicional"""


# System prompt para conversación natural
SYSTEM_PROMPT_CONVERSACION = """Eres el Asesor Logístico Virtual de GLOBAL R.L. - Cooperativa de Transporte Nacional e Internacional, ubicada en Bolivia.

Tu personalidad:
- Profesional pero amigable, hablas en español boliviano
- Experto en logística, transporte de carga pesada y rutas nacionales de Bolivia
- Conoces las rutas principales: La Paz, Santa Cruz, Cochabamba, Sucre, Oruro, Potosí, Tarija, El Alto, Arica
- Puedes hablar de temas generales pero siempre orientas la conversación hacia los servicios de transporte

Servicios de GLOBAL R.L.:
- Transporte de carga general, peligrosa, refrigerada y frágil
- Rutas nacionales e internacionales (Bolivia-Chile vía Arica)
- Flota de camiones pesados con diferentes capacidades (15-30 toneladas)
- Cotización instantánea basada en peso, distancia y tipo de carga
- Análisis multi-escenario (conservador, promedio, óptimo)

Instrucciones de respuesta:
1. Si el usuario saluda o hace preguntas generales, responde amablemente y menciona los servicios
2. Si el usuario describe una necesidad de transporte, ayúdalo a precisar los datos necesarios (origen, destino, peso, tipo de carga)
3. Cuando tengas suficientes datos para cotizar, indica que puedes generar una cotización
4. Sé conciso: respuestas de 2-4 oraciones máximo
5. Usa emojis moderadamente para ser más amigable 🚛

IMPORTANTE: Al final de CADA respuesta, agrega una línea separada con un JSON así:
___METADATA___
{"requiere_cotizacion": true/false, "datos": {"origen": "...", "destino": "...", "toneladas": N, "tipo_carga": "..."}}

- requiere_cotizacion = true SOLO cuando tienes origen, destino Y peso/toneladas claros del usuario
- Si no hay datos suficientes, pon datos como null
"""

class OpenAIServicioPLN(ServicioPLN):
    """Servicio de NLP usando OpenAI GPT como motor de comprensión."""
    
    def __init__(self):
        self.client = None
        self.model = settings.OPENAI_MODEL
        
        if settings.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info(f"OpenAI inicializado con modelo: {self.model}")
            except Exception as e:
                logger.error(f"Error inicializando OpenAI: {e}")
        else:
            logger.warning("OPENAI_API_KEY no configurada. El servicio OpenAI no estará disponible.")
    
    @property
    def disponible(self) -> bool:
        """Verifica si el servicio OpenAI está disponible."""
        return self.client is not None
    
    def extraer_datos_cotizacion(self, texto: str) -> Dict[str, Any]:
        """
        Extrae datos estructurados del texto usando GPT.
        Implementa la interfaz ServicioPLN del dominio.
        """
        if not self.disponible:
            raise RuntimeError("Servicio OpenAI no disponible")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_EXTRACCION},
                    {"role": "user", "content": texto}
                ],
                temperature=0.1,  # Baja temperatura para respuestas más deterministas
                max_tokens=300
            )
            
            contenido = response.choices[0].message.content.strip()
            
            # Limpiar posibles markdown code blocks
            if contenido.startswith("```"):
                contenido = contenido.split("```")[1]
                if contenido.startswith("json"):
                    contenido = contenido[4:]
                contenido = contenido.strip()
            
            datos = json.loads(contenido)
            
            # Asegurar que existan todos los campos esperados
            resultado = {
                "origen": datos.get("origen"),
                "destino": datos.get("destino"),
                "tipo_carga": datos.get("tipo_carga", "general"),
                "peso_kg": float(datos.get("peso_kg", 0)),
                "toneladas": float(datos.get("toneladas", 0)),
                "plazo_dias": int(datos.get("plazo_dias", 5)),
                "tipo_operacion": datos.get("tipo_operacion", "normal")
            }
            
            logger.info(f"GPT extrajo datos: {resultado}")
            return resultado
            
        except json.JSONDecodeError as e:
            logger.error(f"GPT devolvió JSON inválido: {e}")
            raise ValueError("No pude interpretar tu solicitud. Intenta con algo como: '500 toneladas desde La Paz a Cochabamba'")
        except Exception as e:
            logger.error(f"Error en OpenAI: {e}")
            raise
    
    def conversar(
        self, 
        mensaje: str, 
        historial: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Mantiene una conversación natural con el usuario.
        Devuelve la respuesta del bot y metadatos sobre si se requiere cotización.
        """
        if not self.disponible:
            raise RuntimeError("Servicio OpenAI no disponible")
        
        # Construir mensajes con historial
        messages = [{"role": "system", "content": SYSTEM_PROMPT_CONVERSACION}]
        
        if historial:
            for msg in historial[-10:]:  # Últimos 10 mensajes para contexto
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        messages.append({"role": "user", "content": mensaje})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=600
            )
            
            contenido_completo = response.choices[0].message.content.strip()
            
            # Separar respuesta visible del metadata
            respuesta_texto = contenido_completo
            metadata = {"requiere_cotizacion": False, "datos": None}
            
            if "___METADATA___" in contenido_completo:
                partes = contenido_completo.split("___METADATA___")
                respuesta_texto = partes[0].strip()
                
                try:
                    metadata_str = partes[1].strip()
                    metadata = json.loads(metadata_str)
                except (json.JSONDecodeError, IndexError):
                    logger.warning("No se pudo parsear metadata de GPT")
            
            return {
                "respuesta": respuesta_texto,
                "requiere_cotizacion": metadata.get("requiere_cotizacion", False),
                "datos_extraidos": metadata.get("datos"),
                "tokens_usados": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"Error en conversación OpenAI: {e}")
            raise
