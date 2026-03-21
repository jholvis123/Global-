import re
from typing import Dict, Any, Optional
from app.domain.chatbot.interfaces import ServicioPLN

class SpacyServicioPLN(ServicioPLN):
    def __init__(self):
        # Sin spaCy, usamos expresiones regulares simples
        self.ciudades_bolivia = [
            "la paz", "santa cruz", "cochabamba", "sucre", "oruro", "potosi", "tarija", "beni", "pando",
            "el alto", "sacaba", "quillacollo", "montero", "trinidad", "cobija", "arica"
        ]
        
        # Mapeo de códigos de ciudades para rutas
        self.codigo_ciudades = {
            "la paz": "LP",
            "santa cruz": "SC",
            "cochabamba": "CBB",
            "sucre": "SCE",
            "oruro": "ORU",
            "potosi": "PT",
            "tarija": "TJ",
            "el alto": "LP",  # Mismo código que LP
            "arica": "ARICA"
        }
        
        self.sinonimos_carga = {
            "peligrosa": ["peligrosa", "peligroso", "químico", "inflamable", "tóxico", "explosivo"],
            "refrigerada": ["refrigerada", "refrigerado", "frío", "congelado", "perecedero", "frutas"],
            "fragil": ["frágil", "fragil", "vidrio", "delicado", "cerámica"]
        }

    def extraer_datos_cotizacion(self, texto: str) -> Dict[str, Any]:
        texto_lower = texto.lower()
        
        datos_extraidos = {
            "origen": None,
            "destino": None,
            "tipo_carga": "general",
            "peso_kg": 0.0,
            "toneladas": 0.0,
            "plazo_dias": 5,  # Default
            "tipo_operacion": "normal"  # normal, urgente, económico
        }

        # Extraer ciudades con detección de preposiciones
        ciudades_con_posicion = []
        for ciudad in self.ciudades_bolivia:
            if ciudad in texto_lower:
                pos = texto_lower.find(ciudad)
                ciudades_con_posicion.append((ciudad.title(), pos, self.codigo_ciudades.get(ciudad, ciudad.upper())))
        
        ciudades_con_posicion.sort(key=lambda x: x[1])
        
        # Intentar detectar origen/destino usando preposiciones
        preposiciones_origen = ['desde', 'de ', 'desde ']
        preposiciones_destino = ['hasta', 'hacia', 'para', 'a ', 'hacia ']
        
        origen_detectado = None
        destino_detectado = None
        codigo_origen = None
        codigo_destino = None
        
        for prep in preposiciones_origen:
            prep_pos = texto_lower.find(prep)
            if prep_pos != -1:
                for ciudad, pos, codigo in ciudades_con_posicion:
                    if pos > prep_pos:
                        origen_detectado = ciudad
                        codigo_origen = codigo
                        break
                if origen_detectado:
                    break
        
        for prep in preposiciones_destino:
            prep_pos = texto_lower.find(prep)
            if prep_pos != -1:
                for ciudad, pos, codigo in ciudades_con_posicion:
                    if pos > prep_pos and ciudad != origen_detectado:
                        destino_detectado = ciudad
                        codigo_destino = codigo
                        break
                if destino_detectado:
                    break
        
        # Usar detección por preposiciones si es disponible
        if origen_detectado and destino_detectado:
            datos_extraidos["origen"] = codigo_origen or origen_detectado
            datos_extraidos["destino"] = codigo_destino or destino_detectado
        elif len(ciudades_con_posicion) >= 2:
            datos_extraidos["origen"] = ciudades_con_posicion[0][2]
            datos_extraidos["destino"] = ciudades_con_posicion[1][2]
        elif len(ciudades_con_posicion) == 1:
            datos_extraidos["origen"] = ciudades_con_posicion[0][2]

        # Extraer peso - MEJORADO para capturar toneladas correctamente
        # Patrón: detecta "NNN toneladas/ton/Tn/tn"
        peso_match = re.search(
            r'(\d+(?:[.,]\d+)?)\s*(kg|kilos|kilogramos|toneladas|ton|tn|Tn|t\b)',
            texto_lower
        )
        
        if peso_match:
            valor = float(peso_match.group(1).replace(',', '.'))
            unidad = peso_match.group(2).lower()
            
            if unidad in ['toneladas', 'ton', 'tn', 't']:
                datos_extraidos["toneladas"] = valor
                datos_extraidos["peso_kg"] = valor * 1000
            else:
                datos_extraidos["peso_kg"] = valor
                datos_extraidos["toneladas"] = valor / 1000
        
        # Extraer tipo de carga
        tipo_carga_ampliado = {
            "peligrosa": ["peligrosa", "peligroso", "químico", "inflamable", "tóxico", "explosivo"],
            "refrigerada": ["refrigerada", "refrigerado", "frío", "congelado", "perecedero", "frutas"],
            "fragil": ["frágil", "fragil", "vidrio", "delicado", "cerámica"]
        }
        
        for tipo, sinonimos in tipo_carga_ampliado.items():
            if any(sin in texto_lower for sin in sinonimos):
                datos_extraidos["tipo_carga"] = tipo
                break
        
        # Extraer plazo solicitado
        plazo_match = re.search(r'(\d+)\s*(día|días|día|semana|semanas)', texto_lower)
        if plazo_match:
            cantidad = int(plazo_match.group(1))
            unidad = plazo_match.group(2)
            
            if 'semana' in unidad:
                cantidad *= 7
            
            datos_extraidos["plazo_dias"] = cantidad
        
        # Detectar tipo de operación
        if any(word in texto_lower for word in ['urgente', 'inmediato', 'rápido', 'express']):
            datos_extraidos["tipo_operacion"] = "urgente"
        elif any(word in texto_lower for word in ['económico', 'barato', 'presupuesto', 'oferta']):
            datos_extraidos["tipo_operacion"] = "económico"

        return datos_extraidos
