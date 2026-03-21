#!/usr/bin/env python
"""
Script para verificar la comunicación Frontend <-> Backend
"""

import requests
import json

FRONTEND_HOST = "127.0.0.1"
BACKEND_HOST = "127.0.0.1"
FRONTEND_PORT = 4200
BACKEND_PORT = 8000

def test_frontend():
    """Verifica que el frontend esté accesible"""
    print(f"\n🔍 Verificando Frontend en http://{FRONTEND_HOST}:{FRONTEND_PORT}...")
    try:
        response = requests.get(f"http://{FRONTEND_HOST}:{FRONTEND_PORT}", timeout=5)
        print(f"✅ Frontend accesible: Status {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Frontend no accesible: {e}")
        return False

def test_backend():
    """Verifica que el backend esté accesible"""
    print(f"\n🔍 Verificando Backend en http://{BACKEND_HOST}:{BACKEND_PORT}...")
    try:
        response = requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/v1/chatbot/health", timeout=5)
        data = response.json()
        print(f"✅ Backend accesible: Status {response.status_code}")
        print(f"   - OpenAI disponible: {data.get('openai_disponible')}")
        return True
    except Exception as e:
        print(f"❌ Backend no accesible: {e}")
        return False

def test_cors():
    """Prueba CORS entre frontend y backend"""
    print(f"\n🔍 Probando CORS (Frontend -> Backend)...")
    try:
        headers = {
            "Origin": f"http://{FRONTEND_HOST}:{FRONTEND_PORT}",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
        
        response = requests.options(
            f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/v1/chatbot/conversar",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ CORS habilitado: Status {response.status_code}")
            print(f"   - Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'N/A')}")
            return True
        else:
            print(f"⚠️  CORS respuesta: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en CORS: {e}")
        return False

def test_chat_endpoint():
    """Prueba que el endpoint de chat funcione correctamente"""
    print(f"\n🔍 Probando endpoint /conversar...")
    try:
        payload = {
            "mensaje": "Hola, soy una prueba desde el frontend",
            "historial": []
        }
        
        response = requests.post(
            f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/v1/chatbot/conversar",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Endpoint funcionando: Status {response.status_code}")
            print(f"   - Respuesta: {data.get('respuesta', '')[:80]}...")
            print(f"   - Usando OpenAI: {'✅' if 'Gracias' in data.get('respuesta', '') else '⚠️'}")
            return True
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(f"   - Detalle: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error en endpoint: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("🔗 VERIFICANDO COMUNICACIÓN FRONTEND <-> BACKEND")
    print("="*70)
    
    results = []
    
    results.append(("Frontend (puerto 4200)", test_frontend()))
    results.append(("Backend (puerto 8000)", test_backend()))
    results.append(("CORS (Cross-Origin)", test_cors()))
    results.append(("Chatbot Endpoint", test_chat_endpoint()))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN")
    print("="*70)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ OK" if result else "❌ FALLO"
        print(f"{status:8} - {test_name}")
        if not result:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 ¡Todo funciona correctamente!")
        print("   El frontend debería poder comunicarse con el chatbot sin problemas")
        print(f"\n   Accede a: http://{FRONTEND_HOST}:{FRONTEND_PORT}")
        print("   Navega al componente de Chatbot y prueba a escribir mensajes")
    else:
        print("\n⚠️  Hay problemas de comunicación que necesitan arreglarse")
    
    print()

if __name__ == "__main__":
    main()
