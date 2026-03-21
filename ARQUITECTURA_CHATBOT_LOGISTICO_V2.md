# 🚚 ARQUITECTURA DE CHATBOT LOGÍSTICO PROFESIONAL
## Especificación Técnica v2.0

**Fecha**: 16 de Marzo, 2026  
**Objetivo**: Chatbot asesor logístico para transporte de carga internacional

---

## 1️⃣ MODELO DE DATOS - ESPECIFICACIONES OPERATIVAS

### Capacidades de Camiones
```
Escenarios operativos de carga disponibles:
├── 26.0 toneladas     (Conservador - camiones antiguos)
├── 27.0 toneladas     (Conservador-Medio)
├── 27.5 toneladas     (Promedio operativo)
└── 28.5 toneladas     (Óptimo - máxima capacidad)
```

### Variables de Análisis
```
Entrada del usuario: "Necesito transportar X toneladas de [tipo] de Y a Z"
├── Cantidad: ENTERO (toneladas)
├── Tipo de carga: general | peligrosa | fragil | refrigerada
├── Origen: CIUDAD
├── Destino: CIUDAD
└── Fecha estimada: OPCIONAL
```

---

## 2️⃣ LÓGICA DE ANÁLISIS LOGÍSTICO

### A. Cálculo de Escenarios
```python
escenario_conservador = math.ceil(toneladas_totales / 26.0)
escenario_promedio = math.ceil(toneladas_totales / 27.5)
escenario_optimo = math.ceil(toneladas_totales / 28.5)
```

### B. Flujo de Procesamiento
```
1. NLP: Extraer (toneladas, tipo, origen, destino)
2. Validación: Verificar rutas, ciudades
3. Análisis Logístico: Calcular escenarios de camiones
4. Cotización: Calcular precios por escenario
5. Respuesta Profesional: Formular en tono comercial
```

---

## 3️⃣ FORMATO DE RESPUESTA PROFESIONAL

### Estructura de Respuesta
```
[CONFIRMACIÓN DE SOLICITUD]
Para transportar {toneladas} toneladas de {tipo_carga}
desde {origen} hacia {destino}

[ANÁLISIS LOGÍSTICO]
Estimación de unidades necesarias:
• Escenario Conservador: {n_conservador} camiones @ 26 ton/camión
• Escenario Promedio:     {n_promedio} camiones @ 27.5 ton/camión  
• Escenario Óptimo:       {n_optimo} camiones @ 28.5 ton/camión

[ANÁLISIS COMERCIAL]
Ruta: {origen} → {destino}
Distancia: {distancia_km} km
Precio Base: ${precio_base}/ton
Precio Total (Escenario Promedio): ${precio_total}

[CIERRE COMERCIAL]
Para esta operación de {toneladas} toneladas, requerirá aproximadamente
{n_promedio} unidades de transporte. ¿Desea una cotización detallada
por disponibilidad de flota o cotización por viaje?
```

---

## 4️⃣ COMPONENTES DEL SISTEMA

### Backend (FastAPI)
```
POST /api/v1/chatbot/cotizar
├── Input: {"mensaje_texto": "..."}
├── NLP Service: Extrae parámetros
├── Logistics Service: Calcula escenarios
├── Quotation Service: Genera precios
└── Output: CotizacionAvanzada (escenarios + análisis)
```

### Nuevos Servicios Python
```
services/
├── logistica_service.py      ← Cálculo de escenarios de camiones
├── cotizacion_avanzada.py    ← Cotizaciones multi-escenario
└── respuesta_profesional.py  ← Formateo de respuestas comerciales
```

### Nuevos Schemas
```
CotizacionAvanzadaRequest
├── toneladas: float
├── tipo_carga: TipoCarga
├── origen: str
├── destino: str
└── referencia_cliente: Optional[str]

CotizacionAvanzadaResponse
├── escenario_conservador: ScenarioCamion
├── escenario_promedio: ScenarioCamion
├── escenario_optimo: ScenarioCamion
├── ruta_info: RutaInfo
├── respuesta_profesional: str
└── proximos_pasos: List[str]

ScenarioCamion
├── cantidad_camiones: int
├── capacidad_por_camion: float
├── precio_total: float
├── tiempo_estimado_dias: float
└── descripcion: str
```

---

## 5️⃣ EJEMPLOS DE PROCESAMIENTO

### Entrada del Usuario
```
"Preciso transportar 1500 toneladas de trigo desde La Paz a Arica en 7 días"
```

### Procesamiento NLP
```
toneladas: 1500
tipo_carga: general
origen: La Paz
destino: Arica
plazo_dias: 7
```

### Análisis Logístico
```
conservador: ceil(1500 / 26.0) = 58 camiones
promedio:    ceil(1500 / 27.5) = 55 camiones
optimo:      ceil(1500 / 28.5) = 53 camiones
```

### Respuesta del Chatbot (Profesional)
```
Para transportar 1500 toneladas de trigo desde La Paz hacia Arica:

ESTIMACIÓN DE UNIDADES NECESARIAS:
• Escenario Conservador: 58 camiones (26 ton/camión)
• Escenario Promedio:    55 camiones (27.5 ton/camión)
• Escenario Óptimo:      53 camiones (28.5 ton/camión)

ANÁLISIS COMERCIAL:
Ruta: La Paz → Arica | Distancia: 450 km
Tarifa Base: $2.50/ton
Carga Especial (Granel): +15%
Precio Total (Promedio): $55,000 USD
Tiempo Estimado: 3-4 días de tránsito

Para esta operación de 1500 toneladas, con optimización de flota,
requerirá aproximadamente 55 unidades de transporte. 

¿Le preparo una cotización detallada considerando disponibilidad
de flota determinada, o prefiere un análisis de costos por viaje?
```

---

## 6️⃣ MEJORAS RESPECTO AL SISTEMA ANTERIOR

| Aspecto | v1.0 | v2.0 (Nuevo) |
|--------|------|-------------|
| Entrada | kg/ton + ciudad | ton + ciudad + plazo + tipo operativo |
| Análisis | Precio fijo | 3 escenarios de carga |
| Respuesta | Cotización simple | Análisis comercial completo |
| Tono | Transaccional | Asesor profesional |
| Próximos pasos | Ninguno | Guía hacia operación |

---

## 7️⃣ TABLA DE TARIFAS AVANZADA

### Por Tipo de Operación
```
general_seca:        $1.80/ton → +0% en camión
granel_cereales:     $2.00/ton → -5% capacidad (polvo)
peligrosa_quimica:   $3.50/ton → -15% capacidad (norma)
refrigerada:         $2.80/ton → +20% costo
fragil_vidrio:       $3.20/ton → -20% capacidad
contenedor_20ft:     $250.00/viaje (fijo)
contenedor_40ft:     $400.00/viaje (fijo)
```

### Por Ruta (Ejemplo)
```
La Paz → Arica:      $2.50/ton (450 km)
La Paz → Lima:       $2.80/ton (550 km)
Santa Cruz → Arica:  $2.00/ton (680 km)
Cochabamba → Buenos Aires: $3.00/ton (1200 km)
```

---

## 8️⃣ FLUJO CONVERSACIONAL MEJORADO

```
Usuario: "Necesito transportar 750 toneladas"
         ↓
Chatbot: "Para una operación de 750 toneladas, necesitaría:
          • 29 camiones (conservador)
          • 28 camiones (promedio)
          • 27 camiones (óptimo)
          
          ¿Qué ruta y tipo de carga?"
         ↓
Usuario: "De Santa Cruz a Arica, carga general"
         ↓
Chatbot: [RESPUESTA COMPLETA CON ANÁLISIS]
         ↓
Usuario: "¿Cuánto cuesta?"
         ↓
Chatbot: "Para 750 toneladas en escenario promedio:
          28 camiones × $2.00/ton = $1,400/ton
          Costo total operativo: $1,050,000"
         ↓
Usuario: "¿Disponibilidad?"
         ↓
Chatbot: "¿Qué fecha requiere? Le validaré flota disponible..."
```

---

## 9️⃣ MÉTRICAS DE ÉXITO

✅ Comprensión de toneladas (no solo kg)  
✅ Cálculo automático de escenarios  
✅ Respuestas profesionales multi-línea  
✅ Guía conversacional hacia cierre  
✅ Análisis comercial completo  
✅ Flexibilidad en capacidades de camiones  

---

## 🔟 TIMELINE DE IMPLEMENTACIÓN

**Fase 1** (Horas 0-2): Diseño + Servicios logísticos  
**Fase 2** (Horas 2-4): NLP mejorado para toneladas  
**Fase 3** (Horas 4-6): Formateo de respuestas profesionales  
**Fase 4** (Horas 6-8): Testing exhaustivo  
**Fase 5** (Horas 8+): Deployment y validación  

---

**Clasificación**: Arquitectura de Sistema Conversacional  
**Complejidad**: Media-Alta  
**Impacto**: Transformación de transaccional → consultivo
