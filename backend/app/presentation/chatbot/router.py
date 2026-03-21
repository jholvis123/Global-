from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

# Infraestructura
from app.infrastructure.chatbot.nlp.spacy_service import SpacyServicioPLN
from app.infrastructure.chatbot.nlp.openai_service import OpenAIServicioPLN
from app.infrastructure.chatbot.repository import PostgresRepositorioTarifas
from app.infrastructure.logistica import (
    LogisticaService,
    ServicioCotizacionAvanzada,
    FormateadorRespuestaProf
)

# Aplicacion y Presentacion
from app.application.chatbot.use_cases import GenerarCotizacionCasoUso
from app.presentation.chatbot.schemas import (
    CotizacionRequest, 
    CotizacionResponse,
    CotizacionAvanzadaRequest,
    CotizacionAvanzadaResponse,
    ConversacionRequest,
    ConversacionResponse
)
from app.db.database import get_db

router = APIRouter(prefix="/chatbot", tags=["Chatbot Inteligente"])

logger = logging.getLogger(__name__)

# Servicio NLP global (singleton)
servicio_nlp_global = SpacyServicioPLN()
servicio_openai = OpenAIServicioPLN()
logistica_service = LogisticaService()
formateador = FormateadorRespuestaProf()

@router.get("/health")
def health_check():
    """Endpoint de health check para el módulo chatbot"""
    return {
        "status": "healthy", 
        "module": "chatbot",
        "openai_disponible": servicio_openai.disponible
    }

@router.post("/cotizar", response_model=CotizacionResponse)
async def procesar_cotizacion_nlp(
    request: CotizacionRequest, 
    session: Session = Depends(get_db)
):
    logger.info(f"Procesando cotización: {request.mensaje_texto[:50]}...")
    try:
        repositorio_pg = PostgresRepositorioTarifas(session=session)
        
        # Usar OpenAI si está disponible, sino fallback a spaCy (regex)
        try:
            if servicio_openai.disponible:
                servicio_pln = servicio_openai
                logger.info("✓ Usando OpenAI para extracción de datos")
            else:
                raise RuntimeError("OpenAI no disponible")
        except Exception as e:
            logger.warning(f"OpenAI no disponible, usando spaCy: {str(e)}")
            servicio_pln = servicio_nlp_global
        
        caso_uso = GenerarCotizacionCasoUso(
            repositorio_tarifas=repositorio_pg,
            servicio_pln=servicio_pln
        )

        solicitud_resultado = caso_uso.ejecutar(texto_usuario=request.mensaje_texto)

        logger.info(f"✓ Cotización generada: {solicitud_resultado.id}")
        return CotizacionResponse(
            id_solicitud=solicitud_resultado.id,
            origen=solicitud_resultado.origen,
            destino=solicitud_resultado.destino,
            peso_kg=solicitud_resultado.peso_kg,
            tipo_carga=solicitud_resultado.tipo_carga,
            precio_cotizado_bs=solicitud_resultado.precio_calculado,
            fecha=solicitud_resultado.fecha_solicitud
        )

    except ValueError as e:
        logger.warning(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error interno: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/cotizar-avanzada", response_model=CotizacionAvanzadaResponse)
async def procesar_cotizacion_avanzada(
    request: CotizacionAvanzadaRequest,
    session: Session = Depends(get_db)
):
    """
    Endpoint avanzado de cotización con análisis multi-escenario.
    Procesa solicitudes en toneladas y devuelve análisis logístico-comercial.
    Fallback a spaCy si OpenAI no disponible.
    """
    logger.info(f"Procesando cotización avanzada: {request.mensaje_texto[:50]}...")
    
    try:
        # 1. Extraer datos con NLP (OpenAI primero, fallback a spaCy)
        datos = None
        
        if servicio_openai.disponible:
            try:
                datos = servicio_openai.extraer_datos_cotizacion(request.mensaje_texto)
                logger.info("✓ Usando OpenAI para extracción de datos")
            except Exception as e:
                logger.warning(f"OpenAI falló, usando spaCy: {str(e)}")
                datos = None
        
        if datos is None:
            datos = servicio_nlp_global.extraer_datos_cotizacion(request.mensaje_texto)
            logger.info("✓ Usando spaCy (fallback) para extracción de datos")
        
        # 2. Validar datos esenciales
        if not datos.get("origen"):
            raise ValueError("No identifiqué la ciudad de origen en su solicitud")
        if not datos.get("destino"):
            raise ValueError("No identifiqué la ciudad de destino en su solicitud")
        if datos.get("toneladas", 0) == 0 and datos.get("peso_kg", 0) == 0:
            raise ValueError("No pude extraer la cantidad a transportar (toneladas o kg)")
        
        # Normalizar a toneladas
        toneladas = datos.get("toneladas") or (datos.get("peso_kg", 0) / 1000)
        
        # 3. Obtener repositorio de tarifas
        repositorio = PostgresRepositorioTarifas(session=session)
        
        # 4. Crear servicio de cotización avanzada
        servicio_cotizacion = ServicioCotizacionAvanzada(repositorio)
        
        # 5. Generar cotización integral
        resultado_cotizacion = servicio_cotizacion.cotizar_operacion_integral(
            toneladas=toneladas,
            origen=datos.get("origen"),
            destino=datos.get("destino"),
            tipo_carga=datos.get("tipo_carga", "general"),
            plazo_dias=datos.get("plazo_dias", 5)
        )
        
        # 6. Formatear respuesta profesional
        respuesta_profesional = formateador.formatear_respuesta_cotizacion(resultado_cotizacion)
        
        # 7. Agregar respuesta profesional al diccionario
        resultado_cotizacion["respuesta_profesional"] = respuesta_profesional
        
        logger.info(f"✓ Cotización avanzada generada para {toneladas} toneladas")
        
        return CotizacionAvanzadaResponse(**resultado_cotizacion)
        
    except ValueError as e:
        logger.warning(f"Error de validación (Avanzada): {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error interno (Avanzada): {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar cotización avanzada: {str(e)}"
        )


def _generar_respuesta_conversacional_fallback(mensaje: str, datos_extraidos: dict) -> str:
    """Genera respuesta conversacional natural cuando spaCy es fallback"""
    mensaje_lower = mensaje.lower()
    
    # Saludos
    if any(word in mensaje_lower for word in ['hola', 'buenos', 'buenas', 'hi', 'hey', 'qué tal']):
        return (
            "¡Gracias por tu mensaje! 😊\n\n"
            "Puedo ayudarte con:\n"
            "• Información de servicios\n"
            "• Solicitar cotizaciones\n"
            "• Horarios de atención\n"
            "• Contactar un asesor\n\n"
            "¿Qué te gustaría saber?"
        )
    
    # Preguntas sobre servicios
    if any(word in mensaje_lower for word in ['servicios', 'ofrecen', 'qué hacen', 'quién eres']):
        return (
            "¡Excelente pregunta! 🚛\n\n"
            "GLOBAL R.L. es una cooperativa de transporte especializada en:\n"
            "• Carga general\n"
            "• Carga peligrosa\n"
            "• Carga refrigerada\n"
            "• Carga frágil\n\n"
            "Cubrimos rutas nacionales e internacionales desde Bolivia. "
            "¿Necesitas una cotización?"
        )
    
    # Solicitudes de cotización claras
    if datos_extraidos.get("origen") and datos_extraidos.get("destino"):
        return (
            f"Perfecto, entiendo que necesitas transportar desde {datos_extraidos.get('origen')} "
            f"hasta {datos_extraidos.get('destino')}. "
            f"💰 Voy a generar una cotización detallada para ti...\n\n"
            "Obtén análisis con 3 escenarios de precios y utilización de camiones."
        )
    
    # Preguntas sobre tipos de carga
    if any(word in mensaje_lower for word in ['carga', 'tipo', 'qué transportan', 'productos']):
        return (
            "Transportamos todo tipo de carga:\n"
            "• General: Productos secos y diversos\n"
            "• Peligrosa: Químicos y materiales regulados\n"
            "• Refrigerada: Alimentos y productos perecederos\n"
            "• Frágil: Equipos delicados y vidrio\n\n"
            "¿Qué tipo de carga necesitas transportar?"
        )
    
    # Preguntas sobre rutas
    if any(word in mensaje_lower for word in ['ruta', 'dónde', 'zona', 'ciudades', 'llegan']):
        return (
            "Cubrimos las principales ciudades de Bolivia:\n"
            "La Paz • Santa Cruz • Cochabamba • Sucre • Oruro • Potosí • Tarija\n\n"
            "También hacemos rutas internacionales (Bolivia-Chile vía Arica).\n"
            "Mándame origen y destino para una cotización. ✈️"
        )
    
    # Default conversacional
    return (
        "¡Gracias por tu mensaje! 😊\n\n"
        "Soy el Asesor Logístico de GLOBAL R.L. Puedo ayudarte con:\n"
        "📋 Cotizar transporte\n"
        "ℹ️ Información sobre servicios\n"
        "🗺️ Rutas disponibles\n"
        "📞 Contactar un asesor\n\n"
        "¿Con qué puedo asistirte?"
    )


@router.post("/conversar", response_model=ConversacionResponse)
async def conversar_con_chatbot(
    request: ConversacionRequest,
    session: Session = Depends(get_db)
):
    """
    Endpoint de conversación natural con GPT.
    Permite al usuario chatear de forma natural.
    Si GPT detecta datos suficientes, auto-genera cotización avanzada.
    Fallback a spaCy si OpenAI no está disponible o falla.
    """
    logger.info(f"Conversación: {request.mensaje[:50]}...")
    
    try:
        # 1. Convertir historial al formato esperado
        historial = [
            {"role": msg.role, "content": msg.content}
            for msg in (request.historial or [])
        ]
        
        # 2. Intenta obtener respuesta de GPT, fallback a spaCy
        resultado_gpt = None
        usando_openai = False
        
        if servicio_openai.disponible:
            try:
                resultado_gpt = servicio_openai.conversar(
                    mensaje=request.mensaje,
                    historial=historial
                )
                usando_openai = True
                logger.info("✓ Usando OpenAI para conversación")
            except Exception as e:
<<<<<<< HEAD
                import traceback
                error_trace = traceback.format_exc()
                logger.warning(f"OpenAI falló, usando fallback: {str(e)}\n{error_trace}")
                # Temporalmente para depurar
                # respuesta_natural = f"FALLBACK ERROR: {str(e)}"
=======
                logger.warning(f"OpenAI falló, usando fallback: {str(e)}")
>>>>>>> 01f2c85 (subiendo correccion del modulo chatbot)
                resultado_gpt = None
        
        # Fallback a spaCy en caso de que OpenAI no esté disponible o haya fallado
        if resultado_gpt is None:
            datos_extraidos = servicio_nlp_global.extraer_datos_cotizacion(request.mensaje)
            respuesta_natural = _generar_respuesta_conversacional_fallback(
                request.mensaje, 
                datos_extraidos
            )
            resultado_gpt = {
                "respuesta": respuesta_natural,
                "requiere_cotizacion": bool(datos_extraidos.get("origen") and datos_extraidos.get("toneladas", 0) > 0),
                "datos_extraidos": datos_extraidos
            }
            logger.info("✓ Usando spaCy (fallback) con respuesta conversacional")
        
        # 3. Si se detectó que requiere cotización, intentar generar
        cotizacion_generada = None
        if resultado_gpt.get("requiere_cotizacion") and resultado_gpt.get("datos_extraidos"):
            try:
                datos = resultado_gpt["datos_extraidos"]
                toneladas = datos.get("toneladas", 0) or 0
                
                if datos.get("origen") and datos.get("destino") and toneladas > 0:
                    repositorio = PostgresRepositorioTarifas(session=session)
                    servicio_cotizacion = ServicioCotizacionAvanzada(repositorio)
                    
                    resultado_cotizacion = servicio_cotizacion.cotizar_operacion_integral(
                        toneladas=toneladas,
                        origen=datos.get("origen"),
                        destino=datos.get("destino"),
                        tipo_carga=datos.get("tipo_carga", "general"),
                        plazo_dias=datos.get("plazo_dias", 5)
                    )
                    
                    respuesta_profesional = formateador.formatear_respuesta_cotizacion(resultado_cotizacion)
                    resultado_cotizacion["respuesta_profesional"] = respuesta_profesional
                    
                    cotizacion_generada = CotizacionAvanzadaResponse(**resultado_cotizacion)
                    
                    logger.info(f"✓ Cotización auto-generada para {toneladas} ton")
                    
            except Exception as e:
                logger.warning(f"No se pudo auto-generar cotización: {e}")
                # No es error fatal, continuamos con la conversación
        
        return ConversacionResponse(
            respuesta=resultado_gpt["respuesta"],
            requiere_cotizacion=resultado_gpt.get("requiere_cotizacion", False),
            datos_extraidos=resultado_gpt.get("datos_extraidos"),
            cotizacion_avanzada=cotizacion_generada
        )
        
    except Exception as e:
        logger.error(f"Error en conversación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la conversación: {str(e)}"
        )

