import requests
import json

url = "http://localhost:8000/api/v1/chatbot/cotizar"

tests = [
    ("300 kilos carga fragil desde La Paz hasta Cochabamba", "La Paz", "Cochabamba"),
    ("2 toneladas peligrosa Santa Cruz a Cochabamba", "Santa Cruz", "Cochabamba"),
    ("500 kg refrigerado La Paz para Cochabamba", "La Paz", "Cochabamba"),
]

print("=== PRUEBAS NLP MEJORADO ===\n")

for msg, exp_origen, exp_dest in tests:
    try:
        resp = requests.post(url, json={"mensaje_texto": msg})
        data = resp.json()
        
        origen_ok = data.get('origen') == exp_origen
        dest_ok = data.get('destino') == exp_dest
        status = "✓" if (origen_ok and dest_ok) else "✗"
        
        print(f"{status} Mensaje: {msg[:45]}...")
        print(f"  Origen: {data.get('origen')} (esperado: {exp_origen}) {'✓' if origen_ok else '✗'}")
        print(f"  Destino: {data.get('destino')} (esperado: {exp_dest}) {'✓' if dest_ok else '✗'}")
        print(f"  Tipo: {data.get('tipo_carga')} | Peso: {data.get('peso_kg')} kg | Precio: {data.get('precio_cotizado_bs')} Bs\n")
        
    except Exception as e:
        print(f"✗ Error en: {msg[:45]}")
        print(f"  Excepción: {str(e)[:80]}\n")
