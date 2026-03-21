#!/usr/bin/env python
"""
Script interactivo para probar el chatbot con GPT desde la terminal
Uso: python test_chatbot_interactive.py
"""

import requests
import json
from colorama import init, Fore, Back, Style
from datetime import datetime

# Inicializar colorama para colores en terminal
init(autoreset=True)

BASE_URL = "http://127.0.0.1:8000/api/v1/chatbot"

class ChatbotTester:
    def __init__(self):
        self.historial = []
        self.session = requests.Session()
        
    def print_header(self):
        """Imprime el header del chatbot"""
        print("\n" + "="*70)
        print(Fore.CYAN + Style.BRIGHT + "🚛 CHATBOT DE GLOBAL R.L. - PRUEBA INTERACTIVA 🚛")
        print("="*70)
        print(Fore.GREEN + "Escribe tus mensajes y presiona Enter")
        print(Fore.YELLOW + "Escribe 'salir' para terminar")
        print(Fore.CYAN + "Escribe 'limpiar' para borrar el historial")
        print("="*70 + "\n")
    
    def verificar_conexion(self):
        """Verifica que el servidor esté disponible"""
        try:
            response = self.session.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(Fore.GREEN + f"✓ Servidor disponible")
                print(f"  - OpenAI disponible: {data.get('openai_disponible', False)}")
                return True
            else:
                print(Fore.RED + f"✗ Servidor respondió con error {response.status_code}")
                return False
        except Exception as e:
            print(Fore.RED + f"✗ No se puede conectar al servidor: {e}")
            print(Fore.YELLOW + "Asegúrate de que uvicorn está corriendo en http://127.0.0.1:8000")
            return False
    
    def enviar_mensaje(self, mensaje: str):
        """Envía un mensaje al chatbot"""
        try:
            # Construir payload
            payload = {
                "mensaje": mensaje,
                "historial": self.historial
            }
            
            # Mostrar que estamos enviando
            print(Fore.YELLOW + "⏳ Esperando respuesta...")
            
            # Enviar solicitud
            response = self.session.post(
                f"{BASE_URL}/conversar",
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(Fore.RED + f"✗ Error {response.status_code}: {response.text}")
                return None
            
            data = response.json()
            
            # Agregar a historial
            self.historial.append({
                "role": "user",
                "content": mensaje
            })
            self.historial.append({
                "role": "assistant",
                "content": data.get("respuesta", "")
            })
            
            return data
            
        except requests.Timeout:
            print(Fore.RED + "✗ Error: Timeout - La respuesta tardó demasiado")
            return None
        except Exception as e:
            print(Fore.RED + f"✗ Error: {e}")
            return None
    
    def mostrar_respuesta(self, data: dict):
        """Muestra la respuesta del bot de forma bonita"""
        if not data:
            return
        
        respuesta = data.get("respuesta", "")
        requiere_cotizacion = data.get("requiere_cotizacion", False)
        datos_extraidos = data.get("datos_extraidos", {})
        cotizacion = data.get("cotizacion_avanzada")
        
        # Mostrar respuesta
        print("\n" + "="*70)
        print(Fore.CYAN + "📱 Respuesta del Bot:")
        print("="*70)
        print(Fore.WHITE + respuesta)
        
        # Mostrar datos extraídos si existen
        if datos_extraidos and any(datos_extraidos.values()):
            print("\n" + Fore.BLUE + "📊 Datos Extraídos:")
            if datos_extraidos.get("origen"):
                print(f"  • Origen: {datos_extraidos.get('origen')}")
            if datos_extraidos.get("destino"):
                print(f"  • Destino: {datos_extraidos.get('destino')}")
            if datos_extraidos.get("toneladas", 0) > 0:
                print(f"  • Toneladas: {datos_extraidos.get('toneladas')}")
            if datos_extraidos.get("tipo_carga"):
                print(f"  • Tipo de carga: {datos_extraidos.get('tipo_carga')}")
        
        # Mostrar cotización si fue generada
        if cotizacion:
            print("\n" + Fore.GREEN + "💰 Cotización Generada:")
            ruta = cotizacion.get("ruta", {})
            print(f"  Ruta: {ruta.get('origen')} → {ruta.get('destino')}")
            print(f"  Distancia: {ruta.get('distancia_km')} km")
            print(f"  Toneladas: {cotizacion.get('carga_toneladas')}")
            
            precios = cotizacion.get("precios_por_escenario", {})
            if precios:
                print(f"\n  Precios por escenario:")
                print(f"    🔸 Conservador: Bs. {precios.get('conservador', 0):.2f}")
                print(f"    🟡 Promedio: Bs. {precios.get('promedio', 0):.2f} ⭐ RECOMENDADO")
                print(f"    🟢 Óptimo: Bs. {precios.get('optimo', 0):.2f}")
        
        elif requiere_cotizacion:
            print("\n" + Fore.YELLOW + "ℹ️ Cotización activada pero no se generó automáticamente")
        
        print("="*70 + "\n")
    
    def mostrar_ayuda(self):
        """Muestra ejemplos de qué preguntar"""
        print("\n" + Fore.CYAN + "💡 Ejemplos de preguntas:")
        ejemplos = [
            ("Hola", "Saludo inicial"),
            ("¿Qué servicios ofrecen?", "Información de servicios"),
            ("Necesito transportar 500 toneladas desde La Paz a Santa Cruz", "Solicitar cotización"),
            ("¿Qué tipos de carga manejan?", "Información de tipos de carga"),
            ("¿Cuáles son sus rutas?", "Información de rutas disponibles"),
        ]
        
        for ejemplo, descripcion in ejemplos:
            print(f"  • {Fore.YELLOW}\"{ejemplo}\"" + Fore.WHITE + f" - {descripcion}")
        print()
    
    def run(self):
        """Loop principal del chatbot"""
        self.print_header()
        
        # Verificar conexión
        if not self.verificar_conexion():
            return
        
        print(Fore.GREEN + "✓ Conexión establecida\n")
        self.mostrar_ayuda()
        
        # Loop de conversación
        while True:
            try:
                # Obtener entrada del usuario
                usuario_input = input(Fore.GREEN + "Tú: " + Style.RESET_ALL).strip()
                
                if not usuario_input:
                    continue
                
                # Comandos especiales
                if usuario_input.lower() == "salir":
                    print(Fore.YELLOW + "\n¡Hasta luego! 👋\n")
                    break
                
                if usuario_input.lower() == "limpiar":
                    self.historial = []
                    print(Fore.YELLOW + "✓ Historial limpiado\n")
                    continue
                
                if usuario_input.lower() == "ayuda":
                    self.mostrar_ayuda()
                    continue
                
                if usuario_input.lower() == "historial":
                    self._mostrar_historial()
                    continue
                
                # Enviar mensaje al chatbot
                respuesta_data = self.enviar_mensaje(usuario_input)
                
                # Mostrar respuesta
                if respuesta_data:
                    self.mostrar_respuesta(respuesta_data)
                
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\n¡Hasta luego! 👋\n")
                break
            except Exception as e:
                print(Fore.RED + f"Error: {e}\n")
    
    def _mostrar_historial(self):
        """Muestra el historial de conversación"""
        if not self.historial:
            print(Fore.YELLOW + "El historial está vacío\n")
            return
        
        print("\n" + Fore.CYAN + "📜 Historial de Conversación:")
        print("="*70)
        
        for msg in self.historial:
            if msg.get("role") == "user":
                print(Fore.GREEN + f"Tú: {msg.get('content')}")
            else:
                print(Fore.CYAN + f"Bot: {msg.get('content')}")
            print()
        print("="*70 + "\n")


if __name__ == "__main__":
    tester = ChatbotTester()
    tester.run()
