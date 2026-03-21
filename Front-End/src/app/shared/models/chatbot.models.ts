// src/app/shared/models/chatbot.models.ts

export interface CotizacionRequest {
  mensaje_texto: string;
}

// Respuesta Simple (Endpoint antiguo)
export interface CotizacionResponse {
  id_solicitud: number;
  origen: string;
  destino: string;
  peso_kg: number;
  tipo_carga: string;
  precio_cotizado_bs: number;
  fecha: string;
}

// Respuesta Avanzada (Phase 3.5)
export interface EscenarioCamion {
  capacidad_por_camion: number;
  cantidad_camiones: number;
  carga_total: number;
  utilizacion_porcentaje: number;
  descripcion: string;
}

export interface AnalisisComercial {
  precio_por_tonelada: number;
  precio_total_escenario_promedio: number;
  margen_operativo_porcentaje: number;
  rentabilidad: 'Alto' | 'Medio' | 'Bajo';
  dias_estimados: number;
}

export interface Ruta {
  origen: string;
  destino: string;
  distancia_km: number;
}

export interface CotizacionAvanzadaResponse {
  carga_toneladas: number;
  ruta: Ruta;
  tipo_carga: string;
  escenarios_logisticos: {
    conservador: EscenarioCamion;
    promedio: EscenarioCamion;
    optimo: EscenarioCamion;
  };
  analisis_comercial: AnalisisComercial;
  precios_por_escenario: {
    conservador: number;
    promedio: number;
    optimo: number;
  };
  recomendacion: string;
  respuesta_profesional?: string;
}

// === CONVERSACIÓN NATURAL (OpenAI GPT) ===

export interface MensajeHistorial {
  role: 'user' | 'assistant';
  content: string;
}

export interface ConversacionRequest {
  mensaje: string;
  historial: MensajeHistorial[];
}

export interface ConversacionResponse {
  respuesta: string;
  requiere_cotizacion: boolean;
  datos_extraidos: any | null;
  cotizacion_avanzada: CotizacionAvanzadaResponse | null;
}

export interface MensajeChat {
  id: string;
  tipo: 'usuario' | 'bot';
  contenido: string;
  timestamp: Date;
  cotizacion?: CotizacionResponse;
  cotizacion_avanzada?: CotizacionAvanzadaResponse;
}

export interface ChatbotState {
  loading: boolean;
  error: string | null;
  cotizacion: CotizacionResponse | null;
  cotizacion_avanzada: CotizacionAvanzadaResponse | null;
  historial: (CotizacionResponse | CotizacionAvanzadaResponse)[];
  modo: 'simple' | 'avanzada';
  mensajes: MensajeChat[];
}