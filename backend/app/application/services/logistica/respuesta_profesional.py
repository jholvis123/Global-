"""
RespuestaProf service: Formatea respuestas en tono profesional
Secciones: Confirmación → Análisis Logístico → Análisis Comercial → Cierre Comercial
"""
from typing import Dict, Optional

class FormateadorRespuestaProf:
    """
    Formatea respuestas de cotización en tono profesional logístico.
    Estructura: 4 secciones con progresión comercial clara.
    """
    
    # Saludos iniciales profesionales
    SALUDOS = [
        "Perfecto, he analizado su operación.",
        "Excelente, tengo los datos de su solicitud.",
        "Entendido. Aquí está el análisis completo.",
        "Muy bien. Analicemos esta operación.",
    ]
    
    # Cierres comerciales
    CIERRES_COMERCIALES = [
        "¿Desea que procesemos la cotización formal o necesita analizar más detalles?",
        "¿Confirmamos esta operación o requiere ajustes en los parámetros?",
        "¿Procedemos con la cotización completa o necesita más información?",
        "¿Buscamos optimizar algo más de esta operación o continuamos con la cotización?",
    ]
    
    def __init__(self):
        self.saludo_idx = 0
        self.cierre_idx = 0
    
    def formatear_respuesta_cotizacion(
        self,
        datos_cotizacion: Dict,
        tono: str = "profesional"
    ) -> str:
        """
        Formatea la respuesta completa con estructura profesional.
        
        Estructura:
        1. CONFIRMACIÓN - Resumen de solicitud
        2. ANÁLISIS LOGÍSTICO - Escenarios de carga
        3. ANÁLISIS COMERCIAL - Precios y rentabilidad
        4. CIERRE COMERCIAL - Próximos pasos
        """
        
        partes = []
        
        # SECCIÓN 1: CONFIRMACIÓN
        partes.append(self._generar_confirmacion(datos_cotizacion))
        
        # SECCIÓN 2: ANÁLISIS LOGÍSTICO
        partes.append(self._generar_analisis_logistico(datos_cotizacion))
        
        # SECCIÓN 3: ANÁLISIS COMERCIAL
        partes.append(self._generar_analisis_comercial(datos_cotizacion))
        
        # SECCIÓN 4: CIERRE COMERCIAL
        partes.append(self._generar_cierre_comercial(datos_cotizacion))
        
        return "\n\n".join(partes)
    
    def _generar_confirmacion(self, datos: Dict) -> str:
        """Sección 1: Confirmación profesional de la solicitud"""
        
        def plural(num):
            return "" if num == 1 else "s"
        
        ruta = datos.get('ruta', {})
        toneladas = datos.get('carga_toneladas', 0)
        tipo_carga = datos.get('tipo_carga', 'carga general')
        
        seccion = f"""
┌─── CONFIRMACIÓN DE SOLICITUD ───────────────────────────────┐
│
│ He procesado correctamente su solicitud de transporte:
│
│  • Cantidad: {toneladas:,.1f} tonelada{plural(int(toneladas))}
│  • Tipo de carga: {tipo_carga.upper()}
│  • Ruta: {ruta.get('origen', 'N/A')} → {ruta.get('destino', 'N/A')}
│  • Distancia: {ruta.get('distancia_km', 'N/A')} km
│
│ He analizado múltiples escenarios operativos para optimizar
│ su inversión logística. Detallo los números a continuación.
│
└─────────────────────────────────────────────────────────────┘"""
        
        return seccion
    
    def _generar_analisis_logistico(self, datos: Dict) -> str:
        """Sección 2: Análisis logístico con escenarios"""
        
        escenarios = datos.get('escenarios_logisticos', {})
        
        lineas = ["""
┌─── ANÁLISIS LOGÍSTICO OPERATIVO ───────────────────────────┐
│
│ Estimación de unidades necesarias según capacidad utilizada:
│"""]
        
        # ESCENARIO CONSERVADOR
        cons = escenarios.get('conservador', {})
        lineas.append(f"""│
│ 🔷 ESCENARIO CONSERVADOR
│    • Capacidad/Camión: {cons.get('capacidad_por_camion', 'N/A')} ton
│    • Unidades necesarias: {cons.get('cantidad_camiones', 'N/A')} camiones
│    • Utilización de carga: {cons.get('utilizacion_porcentaje', 'N/A')}%
│    › Ideal para flota limitada o restricciones de horario
│""")
        
        # ESCENARIO PROMEDIO (RECOMENDADO)
        prom = escenarios.get('promedio', {})
        lineas.append(f"""│
│ 🟢 ESCENARIO PROMEDIO (RECOMENDADO)
│    • Capacidad/Camión: {prom.get('capacidad_por_camion', 'N/A')} ton
│    • Unidades necesarias: {prom.get('cantidad_camiones', 'N/A')} camiones ✓
│    • Utilización de carga: {prom.get('utilizacion_porcentaje', 'N/A')}%
│    › OPCIÓN BALANCEADA - Rentabilidad vs disponibilidad
│""")
        
        # ESCENARIO ÓPTIMO
        opt = escenarios.get('optimo', {})
        lineas.append(f"""│
│ 🟦 ESCENARIO ÓPTIMO
│    • Capacidad/Camión: {opt.get('capacidad_por_camion', 'N/A')} ton
│    • Unidades necesarias: {opt.get('cantidad_camiones', 'N/A')} camiones
│    • Utilización de carga: {opt.get('utilizacion_porcentaje', 'N/A')}%
│    › Máxima eficiencia (requiere semirremolques completos)
│
└─────────────────────────────────────────────────────────────┘""")
        
        return "\n".join(lineas)
    
    def _generar_analisis_comercial(self, datos: Dict) -> str:
        """Sección 3: Análisis comercial de precios y rentabilidad"""
        
        analisis = datos.get('analisis_comercial', {})
        precios = datos.get('precios_por_escenario', {})
        
        def rentabilidad_emoji(nivel):
            emojis = {
                "Alto": "📈",
                "Medio": "📊",
                "Bajo": "📉"
            }
            return emojis.get(nivel, "📊")
        
        rentab = analisis.get('rentabilidad', 'Medio')
        
        seccion = f"""
┌─── ANÁLISIS COMERCIAL Y RENTABILIDAD ───────────────────────┐
│
│ Estructura de precios según escenario operativo:
│
│ 💰 PRECIOS TOTALES POR ESCENARIO:
│    • Escenario Conservador: Bs. {precios.get('conservador', 'N/A'):,.2f}
│    • Escenario Promedio:     Bs. {precios.get('promedio', 'N/A'):,.2f}
│    • Escenario Óptimo:       Bs. {precios.get('optimo', 'N/A'):,.2f}
│
│ 📊 MÉTRICAS OPERATIVAS:
│    • Precio/Tonelada: Bs. {analisis.get('precio_por_tonelada', 'N/A'):.2f}
│    • Margen Operativo: {analisis.get('margen_operativo_porcentaje', 'N/A'):.1f}%
│    • Factor de Rentabilidad: {rentab} {rentabilidad_emoji(rentab)}
│    • Plazo Estimado: {analisis.get('dias_estimados', 'N/A')} días
│
│ El escenario promedio ofrece el mejor balance entre
│ disponibilidad de flota y rentabilidad neta de operación.
│
└─────────────────────────────────────────────────────────────┘"""
        
        return seccion
    
    def _generar_cierre_comercial(self, datos: Dict) -> str:
        """Sección 4: Cierre comercial con próximos pasos"""
        
        recomendacion = datos.get('recomendacion', '')
        escenarios = datos.get('escenarios_logisticos', {})
        prom = escenarios.get('promedio', {})
        cantidad = prom.get('cantidad_camiones', '?')
        
        seccion = f"""
┌─── RECOMENDACIÓN Y PRÓXIMOS PASOS ──────────────────────────┐
│
│ 📋 RESUMEN EJECUTIVO:
│    {recomendacion}
│
│ Para esta operación de {datos.get('carga_toneladas', '?'):,.0f} toneladas
│ recomendamos {cantidad} unidades en el escenario promedio.
│
│ 📞 PRÓXIMOS PASOS:
│    1️⃣  Confirmar disponibilidad de {cantidad} camiones
│    2️⃣  Validar documentación de carga ({datos.get('tipo_carga', 'N/A')})
│    3️⃣  Agendar levante de carga
│    4️⃣  Confirmar ruta y tránsito ({datos.get('ruta', {}).get('origen', '?')} → {datos.get('ruta', {}).get('destino', '?')})
│
│ ¿Necesita más información o está listo para confirmar?
│
└─────────────────────────────────────────────────────────────┘"""
        
        return seccion
    
    def formatear_error(
        self,
        tipo_error: str,
        descripcion: str,
        sugerencia: Optional[str] = None
    ) -> str:
        """Formatea mensaje de error en tono profesional"""
        
        mensajes = {
            "origin_missing": "La ruta no fue completamente especificada",
            "destination_missing": "No identifiqué el destino de su operación",
            "weight_missing": "No pude extraer la cantidad a transportar",
            "invalid_route": "Esa combinación de ruta no está disponible actualmente",
            "no_tariff": "No tenemos tarifa configurada para esa ruta",
            "parse_error": "Hubo un problema al procesar su solicitud"
        }
        
        encabezado = mensajes.get(tipo_error, descripcion)
        
        error_msg = f"""
╔════════════════════════════════════════════════════════════╗
║                    ⚠️  INFORMACIÓN REQUERIDA             ║
╠════════════════════════════════════════════════════════════╣
║
║ {encabezado}
║
║ Para procesar su cotización necesito:
║ • Ciudad de origen (ej: La Paz, Santa Cruz, Cochabamba)
║ • Ciudad de destino (ej: Puerto Arica, Oruro)
║ • Cantidad a transportar (kg, toneladas, volumen)
║ • Tipo de carga (general, peligrosa, refrigerada, etc.)
║
║ Ejemplo: "Preciso transportar 500 toneladas de trigo
║           desde La Paz hacia Arica"
║
╚════════════════════════════════════════════════════════════╝"""
        
        if sugerencia:
            error_msg += f"\n\n💡 SUGERENCIA: {sugerencia}"
        
        return error_msg


if __name__ == "__main__":
    formateador = FormateadorRespuestaProf()
    
    # Datos de prueba
    datos_test = {
        "carga_toneladas": 500,
        "tipo_carga": "peligrosa",
        "ruta": {
            "origen": "LP",
            "destino": "CBB",
            "distancia_km": 450
        },
        "escenarios_logisticos": {
            "conservador": {
                "capacidad_por_camion": 26.0,
                "cantidad_camiones": 20,
                "utilizacion_porcentaje": 96.2,
                "carga_total": 520.0,
                "descripcion": "Conservador"
            },
            "promedio": {
                "capacidad_por_camion": 27.5,
                "cantidad_camiones": 19,
                "utilizacion_porcentaje": 95.8,
                "carga_total": 522.5,
                "descripcion": "Promedio"
            },
            "optimo": {
                "capacidad_por_camion": 28.5,
                "cantidad_camiones": 18,
                "utilizacion_porcentaje": 97.3,
                "carga_total": 513.0,
                "descripcion": "Óptimo"
            }
        },
        "analisis_comercial": {
            "precio_por_tonelada": 50.0,
            "precio_total_escenario_promedio": 25000.0,
            "margen_operativo_porcentaje": 28.5,
            "rentabilidad": "Alto",
            "dias_estimados": 4
        },
        "precios_por_escenario": {
            "conservador": 27500.0,
            "promedio": 25000.0,
            "optimo": 23750.0
        },
        "recomendacion": "Para transportar 500 toneladas de carga peligrosa, le recomendamos 19 unidades en escenario promedio para máxima eficiencia y rentabilidad."
    }
    
    respuesta = formateador.formatear_respuesta_cotizacion(datos_test)
    print(respuesta)
