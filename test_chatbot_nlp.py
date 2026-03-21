import sys
import os

# Ajustar path para importar app
# Asumiendo que se ejecuta desde d:/Elvis-SecretProyect/Global/Global-
sys.path.append(os.path.abspath('./backend'))

from app.infrastructure.chatbot.nlp.spacy_service import SpacyServicioPLN

def test_nlp_extraction():
    nlp = SpacyServicioPLN()
    
    test_cases = [
        "Llevar de Santa Cruz a La Paz",
        "De La Paz a Santa Cruz",
        "Transportar 500kg de manzanas de Cochabamba a Oruro",
        "500 kg de carga fragil de Sucre a Potosi"
    ]
    
    print("--- Resultados de Extracción NLP ---")
    for text in test_cases:
        result = nlp.extraer_datos_cotizacion(text)
        print(f"Texto: {text}")
        print(f"Resultado: Origen: {result['origen']} | Destino: {result['destino']} | Peso: {result['peso_kg']} | Tipo: {result['tipo_carga']}")
        print("-" * 40)

if __name__ == "__main__":
    test_nlp_extraction()
