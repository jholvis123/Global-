# app/infrastructure/chatbot/nlp/openai_service.py
import json
import logging
import math
from typing import Dict, Any, List, Optional, Tuple
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
SYSTEM_PROMPT_CONVERSACION = """Eres el Asesor Logístico Virtual de GLOBAL R.L., empresa especializada en transporte de carga pesada a nivel nacional e internacional (Bolivia - Chile).

No eres un asistente genérico. Operas bajo reglas estrictas de negocio y logística.

========================
🌎 RUTAS Y COBERTURA
========================

Operas en las siguientes ciudades:

- La Paz (LP)
- Santa Cruz (SC)
- Cochabamba (CBB)
- Sucre (SCE)
- Oruro (ORU)
- Potosí (PT)
- Tarija (TJ)
- El Alto (LP)

Ruta internacional:
- Bolivia ↔ Arica (Chile)

Reglas:
- Debes reconocer estas ciudades automáticamente
- Mapear nombres a códigos (ej: La Paz → LP)
- Si falta origen o destino, debes solicitarlo SIEMPRE
- No se puede cotizar sin origen y destino
- Si mencionan ciudades no listadas, pedir confirmación

========================
🔒 REGLAS DE NEGOCIO
========================

1. CÁLCULO DE CAMIONES (OBLIGATORIO)

Si el usuario menciona toneladas (tn, ton, toneladas), debes calcular:

Capacidades disponibles:
- 28.5 tn
- 28 tn
- 27.5 tn
- 27 tn
- 26.5 tn
- 26 tn

Reglas:
- Usar primero los camiones de mayor capacidad
- Minimizar cantidad de camiones
- Mostrar distribución clara
- Mostrar total

Ejemplo:
"Para transportar 1000 toneladas:
- 35 camiones de 28.5 tn
- 1 camión adicional
Total: 36 camiones"

2. MONEDA (OBLIGATORIO)

- Usar SIEMPRE USD
- Tipo de cambio fijo: 1 USD = 6.69 Bs
- Si el usuario usa bolivianos, convertir automáticamente

3. FORMATO DE RESPUESTA (OBLIGATORIO)

Siempre responder así:

📦 Resumen:
(explicación clara)

🚛 Distribución:
(solo si hay toneladas)

💰 Información de costos:
(si aplica o solicitar datos)

📌 Recomendación:
(siguiente paso claro)

4. INTERPRETACIÓN INTELIGENTE

- "tn", "ton", "toneladas" = lo mismo
- Detectar ciudades automáticamente
- Si faltan datos, solicitarlos claramente

5. PROHIBIDO

- No inventar precios
- No omitir cálculos si hay toneladas
- No responder sin estructura
- No dejar origen/destino en null si fueron mencionados

========================
🧠 COMPORTAMIENTO
========================

- Profesional, claro y directo
- Español boliviano
- Máximo 4-6 líneas por sección
- Usa emojis moderadamente 🚛
- Siempre guiar hacia cotización

========================
📊 METADATA (OBLIGATORIO)
========================

Al final de CADA respuesta debes agregar:

___METADATA___
{"requiere_cotizacion": true/false, "datos": {"origen": "...", "destino": "...", "toneladas": N, "tipo_carga": "..."}}

Reglas:
- requiere_cotizacion = true SOLO si hay origen + destino + toneladas
- Si faltan datos, usar null
- Si el usuario menciona ciudades, debes mapearlas a códigos:
  LP, SC, CBB, SCE, ORU, PT, TJ, ARICA

========================
🎯 OBJETIVO
========================

Ayudar al cliente a:
- Entender cuántos camiones necesita
- Cómo se distribuye su carga
- Preparar una cotización clara en USD
- Guiarlo a completar los datos faltantes
"""


class OpenAIServicioPLN(ServicioPLN):
    """
    Servicio de Inteligencia Artificial para el Asesor Logístico de GLOBAL R.L.
    
    Provee capacidades de procesamiento de lenguaje natural, extracción de datos
    y cálculos logísticos de optimización de carga.
    """
    
    # Capacidades estándar de camiones en toneladas (orden descendente para optimización)
    CAPACIDADES_CAMIONES = [28.5, 28.0, 27.5, 27.0, 26.5, 26.0]

    def __init__(self):
        """Inicializa el cliente de OpenAI y configura el modelo."""
        self.client = None
        self.model = getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")
        api_key = getattr(settings, "OPENAI_API_KEY", None)
        
        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
                logger.info(f"✓ OpenAI Engine Engine inicializado [Modelo: {self.model}]")
            except Exception as e:
                logger.error(f"Error inicializando motor OpenAI: {str(e)}")
        else:
            logger.warning("OPENAI_API_KEY no detectada. El servicio no estará disponible.")

    @property
    def disponible(self) -> bool:
        """Indica si el motor GPT está listo para procesar solicitudes."""
        return self.client is not None

    def calcular_distribucion_logistica(self, toneladas: float) -> Dict[str, Any]:
        """
        Realiza el cálculo matemático profesional de distribución de camiones.
        """
        if toneladas <= 0:
            return {"total_camiones": 0, "distribucion": [], "total_calculado": 0}

        restante = toneladas
        distribucion = []
        total_camiones = 0
        
        for capacidad in self.CAPACIDADES_CAMIONES:
            cantidad = int(restante // capacidad)
            if cantidad > 0:
                distribucion.append({
                    "capacidad": capacidad,
                    "cantidad": cantidad,
                    "subtotal": round(cantidad * capacidad, 2)
                })
                total_camiones += cantidad
                restante -= (cantidad * capacidad)
            
            if restante <= 0:
                break
        
        if restante > 0.01:
            total_camiones += 1
            unidad_ajuste = min([c for c in self.CAPACIDADES_CAMIONES if c >= restante] or [max(self.CAPACIDADES_CAMIONES)])
            distribucion.append({
                "capacidad": unidad_ajuste,
                "cantidad": 1,
                "subtotal": round(restante, 2),
                "ajuste": True
            })

        return {
            "toneladas_originales": toneladas,
            "total_camiones": total_camiones,
            "distribucion": distribucion,
            "total_calculado": round(toneladas, 2)
        }

    def convertir_bob_a_usd(self, bolivianos: float) -> float:
        """Convierte montos de Bolivianos a Dólares usando la tasa oficial."""
        return round(bolivianos / settings.TIPO_CAMBIO_USD_BOB, 2)

    def extraer_datos_cotizacion(self, texto: str) -> Dict[str, Any]:
        """Extrae parámetros de cotización del mensaje del usuario."""
        if not self.disponible:
            raise RuntimeError("Servicio de Inteligencia Logística no iniciado.")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_EXTRACCION},
                    {"role": "user", "content": texto}
                ],
                temperature=0
            )
            
            raw_content = response.choices[0].message.content.strip()
            # Limpiar posibles markdown
            if raw_content.startswith("```"):
                raw_content = raw_content.split("```")[1]
                if raw_content.startswith("json"):
                    raw_content = raw_content[4:]
                raw_content = raw_content.strip()

            datos = json.loads(raw_content)
            
            toneladas = float(datos.get("toneladas", 0))
            if toneladas == 0 and float(datos.get("peso_kg", 0)) > 0:
                toneladas = float(datos.get("peso_kg")) / 1000

            return {
                "origen": datos.get("origen"),
                "destino": datos.get("destino"),
                "tipo_carga": datos.get("tipo_carga", "general"),
                "peso_kg": toneladas * 1000,
                "toneladas": toneladas,
                "plazo_dias": int(datos.get("plazo_dias", 5)),
                "tipo_operacion": datos.get("tipo_operacion", "normal")
            }
            
        except Exception as e:
            logger.error(f"Error en extracción NLP: {str(e)}")
            return None  # Permite que el llamador use el fallback local

    def conversar(
        self, 
        mensaje: str, 
        historial: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Gestiona la conversación inteligente."""
        if not self.disponible:
            return {
                "respuesta": "Lo siento, mi servicio de inteligencia no está disponible. 🚛",
                "requiere_cotizacion": False,
                "datos_extraidos": None
            }

        messages = [{"role": "system", "content": SYSTEM_PROMPT_CONVERSACION}]
        if historial:
            for msg in historial[-10:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        messages.append({"role": "user", "content": mensaje})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )

            full_content = completion.choices[0].message.content.strip()
            respuesta_visible, metadata = self._parsear_hibrido(full_content)
            
            # Cálculo de validación en Python para asegurar precisión
            if metadata.get("datos") and metadata["datos"].get("toneladas"):
                try:
                    toneladas = float(metadata["datos"]["toneladas"])
                    metadata["calculo_logistico"] = self.calcular_distribucion_logistica(toneladas)
                except: pass

            return {
                "respuesta": respuesta_visible,
                "requiere_cotizacion": metadata.get("requiere_cotizacion", False),
                "datos_extraidos": metadata.get("datos"),
                "logistica": metadata.get("calculo_logistico"),
                "tokens": completion.usage.total_tokens if completion.usage else 0
            }

        except Exception as e:
            logger.error(f"Error en motor de diálogo: {str(e)}")
            # Permitir que el error escale para que el router use el fallback local
            return None

    def _parsear_hibrido(self, contenido: str) -> Tuple[str, Dict[str, Any]]:
        marcador = "___METADATA___"
        if marcador not in contenido:
            return contenido, {"requiere_cotizacion": False, "datos": None}
        
        partes = contenido.split(marcador)
        texto = partes[0].strip()
        
        try:
            json_str = partes[1].strip()
            if "```" in json_str:
                json_str = json_str.replace("```json", "").replace("```", "").strip()
            
            return texto, json.loads(json_str)
        except:
            return texto, {"requiere_cotizacion": False, "datos": None}
