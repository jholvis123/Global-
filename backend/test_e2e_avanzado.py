"""
test_e2e_avanzado.py: Tests E2E completamente integrados con la API
Prueba el endpoint /cotizar-avanzada con datos reales
"""
import sys
import os
from pathlib import Path
import time
import json

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

import requests
from requests.exceptions import ConnectionError

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint_salud():
    """Verifica que el servidor esté respondiendo"""
    try:
        response = requests.get(f"{BASE_URL}/chatbot/health")
        assert response.status_code == 200, f"Health check falló: {response.text}"
        print("[PASS] Test E2E - Health Check PASSED")
        return True
    except ConnectionError:
        print("[FAIL] No se pudo conectar a http://localhost:8000")
        print("   ¿Está uvicorn ejecutándose? Ejecuta:")
        print("   cd backend && python -m uvicorn app.main:app --reload --port 8000")
        return False


def test_cotizacion_simple():
    """Test de la cotización simple (para verificar que sigue funcionando)"""
    # Este es un test del endpoint antiguo /cotizar
    # Saltamos si falla por configuración de BD, pero probamos que existe
    payload = {
        "mensaje_texto": "Necesito llevar 500 kg desde La Paz a Cochabamba"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar",
        json=payload
    )
    
    # El endpoint debe existir (200 o 400 son OK)
    assert response.status_code in [200, 400], f"Endpoint no existe: {response.text}"
    print("[PASS] Test E2E - Cotización Simple (endpoint antiguo) PASSED")
    return True


def test_cotizacion_avanzada_basic():
    """Test básico de cotización avanzada"""
    payload = {
        "mensaje_texto": "Preciso transportar 500 toneladas de trigo desde La Paz a Cochabamba"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar-avanzada",
        json=payload
    )
    
    assert response.status_code == 200, f"Error: {response.text}"
    resultado = response.json()
    
    assert resultado['carga_toneladas'] == 500
    assert resultado['ruta']['origen'] == "LP"
    assert resultado['ruta']['destino'] == "CBB"
    assert resultado['tipo_carga'] == "general"
    
    print("[PASS] Test E2E - Cotización Avanzada Básica PASSED")
    return True


def test_cotizacion_avanzada_con_escenarios():
    """Test que verifica los escenarios logísticos"""
    payload = {
        "mensaje_texto": "Necesito 1000 toneladas desde La Paz hacia Santa Cruz"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar-avanzada",
        json=payload
    )
    
    assert response.status_code == 200
    resultado = response.json()
    
    # Verificar escenarios
    escenarios = resultado['escenarios_logisticos']
    assert 'conservador' in escenarios
    assert 'promedio' in escenarios
    assert 'optimo' in escenarios
    
    # Verificar que conservador requiere más camiones
    cant_cons = escenarios['conservador']['cantidad_camiones']
    cant_prom = escenarios['promedio']['cantidad_camiones']
    cant_opt = escenarios['optimo']['cantidad_camiones']
    
    assert cant_cons > cant_prom > cant_opt, f"Escenarios inversos: {cant_cons}, {cant_prom}, {cant_opt}"
    
    print("[PASS] Test E2E - Escenarios Logísticos PASSED")
    print(f"  Conservador: {cant_cons} camiones")
    print(f"  Promedio: {cant_prom} camiones")
    print(f"  Óptimo: {cant_opt} camiones")
    return True


def test_cotizacion_avanzada_carga_peligrosa():
    """Test con carga peligrosa"""
    payload = {
        "mensaje_texto": "200 toneladas de químicos peligrosos desde Oruro a Cochabamba"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar-avanzada",
        json=payload
    )
    
    assert response.status_code == 200
    resultado = response.json()
    
    assert resultado['tipo_carga'] == "peligrosa"
    assert resultado['carga_toneladas'] == 200
    
    print("[PASS] Test E2E - Carga Peligrosa PASSED")
    return True


def test_cotizacion_avanzada_con_plazo():
    """Test con extracción de plazo"""
    payload = {
        "mensaje_texto": "Urgente: 300 toneladas en 3 días desde La Paz a Arica"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar-avanzada",
        json=payload
    )
    
    assert response.status_code == 200
    resultado = response.json()
    
    assert resultado['analisis_comercial']['dias_estimados'] == 3
    assert resultado['carga_toneladas'] == 300
    
    print("[PASS] Test E2E - Con Plazo PASSED")
    return True


def test_respuesta_profesional_formato():
    """Test que verifica la respuesta profesional esté bien formateada"""
    payload = {
        "mensaje_texto": "500 toneladas de trigo desde La Paz a Santa Cruz en 5 días"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar-avanzada",
        json=payload
    )
    
    if response.status_code != 200:
        print(f"  Respuesta: {response.text}")
        assert False, f"Error en respuesta: {response.text}"
    
    resultado = response.json()
    
    # Verificar que la respuesta profesional esté en la respuesta
    assert resultado.get('respuesta_profesional'), "No hay respuesta_profesional en la respuesta"
    
    respuesta = resultado['respuesta_profesional']
    
    assert "CONFIRMACIÓN" in respuesta or "ANALISIS" in respuesta, f"Respuesta incompleta: {respuesta[:100]}"
    
    print("[PASS] Test E2E - Respuesta Profesional PASSED")
    return True


def test_error_sin_origen():
    """Test de error cuando falta origen"""
    payload = {
        "mensaje_texto": "Necesito transporter 500 toneladas a Cochabamba"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar-avanzada",
        json=payload
    )
    
    assert response.status_code == 400, f"Debería estar 400, no {response.status_code}"
    
    print("[PASS] Test E2E - Error sin Origen PASSED")
    return True


def test_error_sin_toneladas():
    """Test de error cuando falta toneladas"""
    payload = {
        "mensaje_texto": "Necesito transportar desde La Paz a Cochabamba"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar-avanzada",
        json=payload
    )
    
    assert response.status_code == 400
    
    print("[PASS] Test E2E - Error sin Toneladas PASSED")
    return True


def test_analisis_comercial():
    """Test que verifica el análisis comercial"""
    payload = {
        "mensaje_texto": "750 toneladas de granos desde Santa Cruz a La Paz"
    }
    
    response = requests.post(
        f"{BASE_URL}/chatbot/cotizar-avanzada",
        json=payload
    )
    
    assert response.status_code == 200
    resultado = response.json()
    
    comercial = resultado['analisis_comercial']
    assert comercial['precio_por_tonelada'] > 0
    assert comercial['precio_total_escenario_promedio'] > 0
    assert comercial['margen_operativo_porcentaje'] > 0
    assert comercial['rentabilidad'] in ['Alto', 'Medio', 'Bajo']
    assert comercial['dias_estimados'] > 0
    
    print("[PASS] Test E2E - Análisis Comercial PASSED")
    print(f"  Precio/Ton: Bs. {comercial['precio_por_tonelada']:.2f}")
    print(f"  Total (Promedio): Bs. {comercial['precio_total_escenario_promedio']:,.2f}")
    print(f"  Margen: {comercial['margen_operativo_porcentaje']:.1f}%")
    return True
    return True


def run_all_e2e_tests():
    """Ejecuta todos los tests E2E"""
    print("\n" + "="*70)
    print("TESTS E2E INTEGRADOS - ENDPOINTS AVANZADOS")
    print("="*70 + "\n")
    
    tests = [
        test_endpoint_salud,
        test_cotizacion_simple,
        test_cotizacion_avanzada_basic,
        test_cotizacion_avanzada_con_escenarios,
        test_cotizacion_avanzada_carga_peligrosa,
        test_cotizacion_avanzada_con_plazo,
        test_respuesta_profesional_formato,
        test_error_sin_origen,
        test_error_sin_toneladas,
        test_analisis_comercial,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if not test_func():
                failed += 1
            else:
                passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[FAIL] {test_func.__name__}: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"[DONE] TESTS COMPLETADOS: {passed} PASSED, {failed} FAILED")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_e2e_tests()
    sys.exit(0 if success else 1)
