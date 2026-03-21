"""
test_avanzado.py: Tests para servicios avanzados de logística
Verifica: servicios logísticos, cotización avanzada, formateo profesional
"""
import sys
import os
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def test_logistica_service():
    """Test del servicio logístico"""
    from app.infrastructure.logistica import LogisticaService
    
    servicio = LogisticaService()
    
    # Test 1: Calcular escenarios para 1000 toneladas, carga general
    escenarios = servicio.calcular_escenarios(1000, "general")
    
    assert "conservador" in escenarios
    assert "promedio" in escenarios
    assert "optimo" in escenarios
    
    # Verificar que escenario conservador requiere más camiones
    assert escenarios['conservador'].cantidad_camiones > escenarios['promedio'].cantidad_camiones
    assert escenarios['promedio'].cantidad_camiones > escenarios['optimo'].cantidad_camiones
    
    print("✓ Test LogisticaService - Escenarios básicos PASSED")
    
    # Test 2: Verificar factor de capacidad para carga peligrosa
    escenarios_peligr = servicio.calcular_escenarios(1000, "peligrosa")
    escenarios_general = servicio.calcular_escenarios(1000, "general")
    
    # Carga peligrosa debe requerir más camiones (menor capacidad)
    assert escenarios_peligr['promedio'].cantidad_camiones > escenarios_general['promedio'].cantidad_camiones
    
    print("✓ Test LogisticaService - Factor de carga PASSED")
    
    # Test 3: Estimación de tiempo
    tiempo = servicio.estimar_tiempo_transito(450)  # LP-CBB: 450km
    assert tiempo['dias_estimado'] > 0
    assert tiempo['horas_totales'] > 0
    
    print("✓ Test LogisticaService - Tiempo de tránsito PASSED")


def test_cotizacion_avanzada():
    """Test del servicio de cotización avanzada"""
    from app.infrastructure.logistica import ServicioCotizacionAvanzada
    
    class MockTarifaRepo:
        pass
    
    servicio = ServicioCotizacionAvanzada(MockTarifaRepo())
    
    # Test 1: Cotización integral
    resultado = servicio.cotizar_operacion_integral(
        toneladas=500,
        origen="LP",
        destino="CBB",
        tipo_carga="general"
    )
    
    assert resultado['carga_toneladas'] == 500
    assert resultado['escenarios_logisticos']['promedio']['cantidad_camiones'] > 0
    assert resultado['analisis_comercial']['precio_por_tonelada'] > 0
    assert 'recomendacion' in resultado
    
    print("✓ Test ServicioCotizacionAvanzada - Cotización integral PASSED")
    
    # Test 2: Multiplicador de carga peligrosa
    resultado_general = servicio.cotizar_operacion_integral(500, "LP", "CBB", "general")
    resultado_peligr = servicio.cotizar_operacion_integral(500, "LP", "CBB", "peligrosa")
    
    # Carga peligrosa debe ser más cara
    assert resultado_peligr['precios_por_escenario']['promedio'] > resultado_general['precios_por_escenario']['promedio']
    
    print("✓ Test ServicioCotizacionAvanzada - Multiplicadores PASSED")


def test_formateador():
    """Test del formateador de respuestas profesionales"""
    from app.infrastructure.logistica import FormateadorRespuestaProf
    
    formateador = FormateadorRespuestaProf()
    
    # Datos de prueba
    datos = {
        "carga_toneladas": 500,
        "tipo_carga": "general",
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
        "recomendacion": "Para transportar 500 toneladas...recomendamos 19 unidades."
    }
    
    # Test 1: Formateo de respuesta
    respuesta = formateador.formatear_respuesta_cotizacion(datos)
    
    assert "CONFIRMACIÓN" in respuesta
    assert "ANÁLISIS LOGÍSTICO" in respuesta
    assert "ANÁLISIS COMERCIAL" in respuesta
    assert "RECOMENDACIÓN" in respuesta
    assert "500" in respuesta
    assert "19" in respuesta
    
    print("✓ Test FormateadorRespuestaProf - Formato completo PASSED")
    
    # Test 2: Formateo de error
    error = formateador.formatear_error(
        "origin_missing",
        "No se identificó origen"
    )
    
    assert "INFORMACIÓN REQUERIDA" in error
    assert "origen" in error
    
    print("✓ Test FormateadorRespuestaProf - Formato error PASSED")


def test_nlp_mejorado():
    """Test del NLP mejorado con extracción de toneladas"""
    from app.infrastructure.chatbot.nlp.spacy_service import SpacyServicioPLN
    
    servicio = SpacyServicioPLN()
    
    # Test 1: Extracción de toneladas
    datos = servicio.extraer_datos_cotizacion(
        "Necesito transportar 500 toneladas de trigo desde La Paz a Cochabamba"
    )
    
    assert datos['toneladas'] == 500
    assert datos['peso_kg'] == 500000
    assert datos['origen'] == "LP"
    assert datos['destino'] == "CBB"
    
    print("✓ Test NLP - Extracción de toneladas PASSED")
    
    # Test 2: Extracción de plazo
    datos = servicio.extraer_datos_cotizacion(
        "Urgente: 100 toneladas en 3 días desde Santa Cruz a La Paz"
    )
    
    assert datos['plazo_dias'] == 3
    assert datos['tipo_operacion'] == "urgente"
    
    print("✓ Test NLP - Extracción de plazo y operación PASSED")
    
    # Test 3: Detección de tipo de carga
    datos = servicio.extraer_datos_cotizacion(
        "200 toneladas de químicos peligrosos desde Oruro a Arica"
    )
    
    assert datos['tipo_carga'] == "peligrosa"
    
    print("✓ Test NLP - Detección de tipo de carga PASSED")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("EJECUTANDO TESTS DE SERVICIOS AVANZADOS")
    print("="*60 + "\n")
    
    try:
        test_logistica_service()
        print()
        test_cotizacion_avanzada()
        print()
        test_formateador()
        print()
        test_nlp_mejorado()
        
        print("\n" + "="*60)
        print("✅ TODOS LOS TESTS PASSED (10/10)")
        print("="*60 + "\n")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
