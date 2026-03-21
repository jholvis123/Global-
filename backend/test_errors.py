import requests
import json

url = "http://localhost:8000/api/v1/chatbot/cotizar"

# Test casos de error
error_cases = [
    ("500 kg desde La Paz", "Sin destino"),
    ("Cochabamba sin peso especificado", "Sin peso"),
    ("300 kg desde Ciudad Inexistente a Cochabamba", "Ciudad inválida"),
    ("", "Mensaje vacío"),
    ("blah blah blah", "Sin parámetros válidos"),
    ("500 kg Beni a Pando", "Ruta no disponible (sin tarifa)"),
]

print("=== PRUEBAS DE MANEJO DE ERRORES ===\n")

success_errors = 0
bad_errors = 0

for msg, description in error_cases:
    try:
        resp = requests.post(url, json={"mensaje_texto": msg})
        
        if resp.status_code in [400, 422]:
            error_data = resp.json()
            print(f"✓ {description}")
            print(f"  Status: {resp.status_code} | Detail: {error_data.get('detail', error_data.get('message', 'N/A'))[:60]}\n")
            success_errors += 1
        else:
            data = resp.json()
            print(f"✗ {description} - Debería haber fallado")
            print(f"  Status: {resp.status_code} | Respuesta inesperada: {data}\n")
            bad_errors += 1
            
    except Exception as e:
        print(f"✗ {description}")
        print(f"  Exception: {str(e)[:70]}\n")
        bad_errors += 1

print(f"\n=== RESUMEN ===")
print(f"Errores manejados correctamente: {success_errors}")
print(f"Errores no manejados: {bad_errors}")
print(f"Total: {len(error_cases)}")
