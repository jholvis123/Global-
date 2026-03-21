#!/usr/bin/env python
"""Test script para endpoints del chatbot"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1/chatbot"

def test_health():
    """Test endpoint health"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_greeting():
    """Test saludos simples"""
    print("\n" + "="*60)
    print("TEST 2: Conversación - Saludo Simple")
    print("="*60)
    
    payload = {
        "mensaje": "Hola",
        "historial": []
    }
    
    print(f"Enviando: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/conversar",
            json=payload,
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"\n📱 Respuesta del Bot:\n{data['respuesta']}")
        print(f"\nMetadatos:")
        print(f"  - requiere_cotizacion: {data.get('requiere_cotizacion')}")
        print(f"  - datos_extraidos: {data.get('datos_extraidos')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cotization_request():
    """Test solicitud de cotización"""
    print("\n" + "="*60)
    print("TEST 3: Conversación - Solicitud de Cotización")
    print("="*60)
    
    payload = {
        "mensaje": "Necesito transportar 500 toneladas desde La Paz a Santa Cruz",
        "historial": []
    }
    
    print(f"Enviando: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/conversar",
            json=payload,
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"\n📱 Respuesta del Bot:\n{data['respuesta']}")
        print(f"\nMetadatos:")
        print(f"  - requiere_cotizacion: {data.get('requiere_cotizacion')}")
        print(f"  - datos_extraidos: {json.dumps(data.get('datos_extraidos'), indent=2)}")
        
        if data.get('cotizacion_avanzada'):
            print(f"\n💰 Cotización Generada:")
            cotizacion = data['cotizacion_avanzada']
            print(f"  - Ruta: {cotizacion['ruta']['origen']} → {cotizacion['ruta']['destino']}")
            print(f"  - Distancia: {cotizacion['ruta']['distancia_km']} km")
            print(f"  - Toneladas: {cotizacion['carga_toneladas']}")
            print(f"  - Precios: {json.dumps(cotizacion['precios_por_escenario'], indent=4)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_history():
    """Test conversación con historial"""
    print("\n" + "="*60)
    print("TEST 4: Conversación con Historial")
    print("="*60)
    
    historial = [
        {"role": "user", "content": "Hola, ¿qué servicios ofrecen?"},
        {"role": "assistant", "content": "Ofrecemos transporte de carga general, peligrosa, refrigerada y frágil en Bolivia."},
        {"role": "user", "content": "Perfecto, necesito una cotización"}
    ]
    
    payload = {
        "mensaje": "Para 300 toneladas desde La Paz a Cochabamba",
        "historial": historial
    }
    
    print(f"Enviando mensaje con historial de {len(historial)} mensajes")
    
    try:
        response = requests.post(
            f"{BASE_URL}/conversar",
            json=payload,
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"\n📱 Respuesta del Bot:\n{data['respuesta']}")
        
        if data.get('cotizacion_avanzada'):
            print(f"\n✅ Cotización generada automáticamente")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🚛 PRUEBAS DE ENDPOINTS DEL CHATBOT 🚛")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health
    results.append(("Health Check", test_health()))
    
    # Esperar un poco entre tests
    time.sleep(1)
    
    # Test 2: Saludo simple
    results.append(("Saludo Simple", test_simple_greeting()))
    time.sleep(1)
    
    # Test 3: Solicitud de cotización
    results.append(("Solicitud de Cotización", test_cotization_request()))
    time.sleep(1)
    
    # Test 4: Conversación con historial
    results.append(("Conversación con Historial", test_conversation_history()))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} - {test_name}")
    
    total_pass = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nTotal: {total_pass}/{total} pruebas pasadas")
