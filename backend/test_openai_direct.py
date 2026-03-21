import os
import sys

# Add backend to path
sys.path.append(os.getcwd())

from app.core.config import settings
from app.infrastructure.chatbot.nlp.openai_service import OpenAIServicioPLN

print(f"DEBUG: settings.OPENAI_API_KEY length: {len(settings.OPENAI_API_KEY)}")
print(f"DEBUG: settings.OPENAI_API_KEY starts with: {settings.OPENAI_API_KEY[:10]}...")
print(f"DEBUG: settings.OPENAI_MODEL: {settings.OPENAI_MODEL}")

service = OpenAIServicioPLN()
print(f"DEBUG: service.disponible: {service.disponible}")

if service.disponible:
    try:
        hist = [{"role": "user", "content": "hola"}, {"role": "assistant", "content": "hola"}]
        response = service.conversar("ola", hist)
        print(f"DEBUG: Response: {response['respuesta']}")
    except Exception as e:
        print(f"DEBUG: Error: {e}")
else:
    print("DEBUG: OpenAI Service NOT available")
