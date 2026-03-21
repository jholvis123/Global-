#!/usr/bin/env python
"""Script para verificar si OpenAI está funcionando correctamente"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1/chatbot"

def test_openai_simple():
    """Test simple para verificar OpenAI"""
    print("\n" + "="*70)
    print("🧪 PROBANDO OPENAI CON MENSAJE SIMPLE")
    print("="*70)
    
    # Test 1: Health
    print("\n1️⃣ Verificando Health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"OpenAI disponible: {data.get('openai_disponible')}")
        
        if not data.get('openai_disponible'):
            print("❌ OpenAI NO está disponible")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Conversación simple
    print("\n2️⃣ Enviando mensaje: 'Hola' a OpenAI...")
    try:
        payload = {
            "mensaje": "Hola",
            "historial": []
        }
        
        response = requests.post(
            f"{BASE_URL}/conversar",
            json=payload,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ RESPUESTA RECIBIDA:")
            print(f"Usando OpenAI: {'✅ SÍ' if 'Gracias' in data.get('respuesta', '') and len(data.get('respuesta', '')) > 100 else '⚠️ Probablemente fallback'}")
            print(f"\nRespuesta completa:")
            print("-" * 70)
            print(data.get('respuesta', ''))
            print("-" * 70)
            
            # Verificar si es respuesta de OpenAI o fallback
            respuesta = data.get('respuesta', '')
            
            # Respuestas de fallback siempre tienen estas frases
            respuestas_fallback = [
                "Transportamos todo tipo de carga",
                "Cubrimos las principales ciudades",
                "Soy el Asesor Logístico"
            ]
            
            es_fallback = any(frase in respuesta for frase in respuestas_fallback)
            
            if es_fallback:
                print("\n⚠️ USANDO FALLBACK (spaCy) - NO ES OpenAI")
                return False
            else:
                print("\n✅ USANDO OpenAI - RESPUESTA NATURAL")
                return True
        else:
            print(f"❌ Error {response.status_code}")
            print(response.text[:500])
            return False
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - OpenAI tardó demasiado (probablemente sin cuota)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cotizacion():
    """Test de cotización"""
    print("\n" + "="*70)
    print("🧪 PROBANDO COTIZACIÓN")
    print("="*70)
    
    payload = {
        "mensaje": "Necesito 500 toneladas de La Paz a Santa Cruz",
        "historial": []
    }
    
    print("\nEnviando solicitud de cotización...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/conversar",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Respuesta recibida")
            print(f"Requiere cotización: {data.get('requiere_cotizacion')}")
            
            if data.get('cotizacion_avanzada'):
                print("✅ Cotización generada automáticamente")
                precios = data['cotizacion_avanzada'].get('precios_por_escenario', {})
                print(f"   - Conservador: Bs. {precios.get('conservador')}")
                print(f"   - Promedio: Bs. {precios.get('promedio')}")
                print(f"   - Óptimo: Bs. {precios.get('optimo')}")
            return True
        else:
            print(f"❌ Error {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔍 VERIFICACIÓN COMPLETA DE OpenAI")
    print("="*70)
    
    openai_ok = test_openai_simple()
    cotizacion_ok = test_cotizacion()
    
    print("\n" + "="*70)
    print("📊 RESULTADO FINAL")
    print("="*70)
    
    if openai_ok and cotizacion_ok:
        print("\n✅✅✅ ¡OPENAI FUNCIONA CORRECTAMENTE!")
        print("El frontend debería recibir respuestas naturales de GPT")
        print("\nAcciones:")
        print("1. Haz Hard Refresh en el navegador (Ctrl+Shift+R)")
        print("2. Vacía el caché de Angular")
        print("3. Recarga la página")
    else:
        print("\n❌ OPENAI NO ESTÁ FUNCIONANDO")
        if not openai_ok:
            print("- Las respuestas vienen del fallback (spaCy)")
        if not cotizacion_ok:
            print("- Las cotizaciones no se generan")
    
    print()
