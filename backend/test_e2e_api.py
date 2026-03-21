"""
DÍA 2: PRUEBAS E2E - Integración Frontend-Backend-Database
Validar flujo completo: Usuario → Angular → FastAPI → SQLite
"""
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000/api/v1"
CHATBOT_ENDPOINT = f"{API_URL}/chatbot"

print("=" * 70)
print("| DÍA 2: PRUEBAS E2E - INTEGRACIÓN COMPLETA                    |")
print("=" * 70)
print()

# ===== TEST 1: Health Check =====
print("TEST 1: Health Check")
print("-" * 70)
try:
    r = requests.get(f"{CHATBOT_ENDPOINT}/health")
    data = r.json()
    
    if r.status_code == 200 and data.get("status") == "healthy":
        print("✓ PASS: Backend respondiendo correctamente")
        print(f"  Response: {data}\n")
    else:
        print(f"✗ FAIL: Status {r.status_code}\n")
except Exception as e:
    print(f"✗ ERROR: {str(e)}\n")

# ===== TEST 2: Flujo básico de cotización =====
print("TEST 2: Cotización Básica (Santa Cruz → La Paz, 500kg)")
print("-" * 70)
payload = {
    "mensaje_texto": "Necesito transportar 500 kilos desde Santa Cruz a La Paz"
}
try:
    r = requests.post(f"{CHATBOT_ENDPOINT}/cotizar", json=payload)
    data = r.json()
    
    if r.status_code == 200:
        print("✓ PASS: Cotización generada")
        print(f"  ID: {data.get('id_solicitud')}")
        print(f"  Ruta: {data.get('origen')} → {data.get('destino')}")
        print(f"  Peso: {data.get('peso_kg')} kg")
        print(f"  Tipo: {data.get('tipo_carga')}")
        print(f"  Precio: {data.get('precio_cotizado_bs')} Bs")
        print(f"  Fecha: {data.get('fecha')}\n")
    else:
        print(f"✗ FAIL: Status {r.status_code} - {data}\n")
except Exception as e:
    print(f"✗ ERROR: {str(e)}\n")

# ===== TEST 3: Carga peligrosa con toneladas =====
print("TEST 3: Carga Peligrosa (2 toneladas → 2000kg)")
print("-" * 70)
payload = {
    "mensaje_texto": "2 toneladas de carga peligrosa Santa Cruz hacia Cochabamba"
}
try:
    r = requests.post(f"{CHATBOT_ENDPOINT}/cotizar", json=payload)
    data = r.json()
    
    if r.status_code == 200:
        peso_correcto = abs(data.get('peso_kg', 0) - 2000.0) < 1
        tipo_correcto = data.get('tipo_carga') == 'peligrosa'
        
        if peso_correcto and tipo_correcto:
            print("✓ PASS: Conversión de toneladas y tipo detectado")
            print(f"  Peso: {data.get('peso_kg')} kg (2 toneladas)")
            print(f"  Tipo: {data.get('tipo_carga')}")
            print(f"  Precio: {data.get('precio_cotizado_bs')} Bs\n")
        else:
            print(f"✗ FAIL: Parámetros incorrectos\n")
    else:
        print(f"✗ FAIL: Status {r.status_code}\n")
except Exception as e:
    print(f"✗ ERROR: {str(e)}\n")

# ===== TEST 4: Carga frágil =====
print("TEST 4: Carga Frágil")
print("-" * 70)
payload = {
    "mensaje_texto": "300 kilos carga fragil desde La Paz hasta Cochabamba"
}
try:
    r = requests.post(f"{CHATBOT_ENDPOINT}/cotizar", json=payload)
    data = r.json()
    
    if r.status_code == 200 and data.get('tipo_carga') == 'fragil':
        print("✓ PASS: Tipo de carga frágil detectado")
        print(f"  Origen: {data.get('origen')}")
        print(f"  Destino: {data.get('destino')}")
        print(f"  Tipo: {data.get('tipo_carga')}\n")
    else:
        print(f"✗ FAIL\n")
except Exception as e:
    print(f"✗ ERROR: {str(e)}\n")

# ===== TEST 5: Carga refrigerada =====
print("TEST 5: Carga Refrigerada")
print("-" * 70)
payload = {
    "mensaje_texto": "1500 kg carga refrigerada La Paz para Cochabamba"
}
try:
    r = requests.post(f"{CHATBOT_ENDPOINT}/cotizar", json=payload)
    data = r.json()
    
    if r.status_code == 200 and data.get('tipo_carga') == 'refrigerada':
        print("✓ PASS: Carga refrigerada detectada")
        print(f"  Peso: {data.get('peso_kg')} kg")
        print(f"  Tipo: {data.get('tipo_carga')}")
        print(f"  Precio: {data.get('precio_cotizado_bs')} Bs\n")
    else:
        print(f"✗ FAIL\n")
except Exception as e:
    print(f"✗ ERROR: {str(e)}\n")

# ===== TEST 6: Error - Sin destino =====
print("TEST 6: Validación - Mensaje sin destino (debe fallar)")
print("-" * 70)
payload = {
    "mensaje_texto": "500 kg desde La Paz"
}
try:
    r = requests.post(f"{CHATBOT_ENDPOINT}/cotizar", json=payload)
    
    if r.status_code == 400:
        print("✓ PASS: Error 400 detectado correctamente")
        print(f"  Mensaje: {r.json().get('detail')}\n")
    else:
        print(f"✗ FAIL: Debería retornar 400\n")
except Exception as e:
    print(f"✗ ERROR: {str(e)}\n")

# ===== TEST 7: Error - Ruta no disponible =====
print("TEST 7: Validación - Ruta no cubierta (debe fallar)")
print("-" * 70)
payload = {
    "mensaje_texto": "100 kg desde Beni a Pando"
}
try:
    r = requests.post(f"{CHATBOT_ENDPOINT}/cotizar", json=payload)
    
    if r.status_code == 400:
        print("✓ PASS: Error 400 por ruta no disponible")
        print(f"  Mensaje: {r.json().get('detail')}\n")
    else:
        print(f"✗ FAIL: Esperaba error\n")
except Exception as e:
    print(f"✗ ERROR: {str(e)}\n")

# ===== RESUMEN FINAL =====
print("=" * 70)
print("| RESUMEN: Todos los tests de API completados                |")
print("= Próximo: Validar en navegador (Frontend Integration)       =")
print("=" * 70)
