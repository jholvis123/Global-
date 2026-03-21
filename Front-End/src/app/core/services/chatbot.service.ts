// src/app/core/services/chatbot.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { 
  CotizacionRequest, 
  CotizacionResponse,
  CotizacionAvanzadaResponse,
  ConversacionRequest,
  ConversacionResponse,
  MensajeHistorial
} from '../../shared/models/chatbot.models';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = `${environment.apiUrl}/chatbot`;

  constructor(private http: HttpClient) {}

  // Endpoint antiguo - Cotización simple
  generarCotizacion(mensaje: string): Observable<CotizacionResponse> {
    const request: CotizacionRequest = { mensaje_texto: mensaje };
    return this.http.post<CotizacionResponse>(`${this.apiUrl}/cotizar`, request);
  }

  // Endpoint nuevo - Cotización avanzada con multi-escenarios
  generarCotizacionAvanzada(mensaje: string): Observable<CotizacionAvanzadaResponse> {
    const request: CotizacionRequest = { mensaje_texto: mensaje };
    return this.http.post<CotizacionAvanzadaResponse>(`${this.apiUrl}/cotizar-avanzada`, request);
  }

  // Conversación natural con GPT
  conversar(mensaje: string, historial: MensajeHistorial[]): Observable<ConversacionResponse> {
    const request: ConversacionRequest = { mensaje, historial };
    return this.http.post<ConversacionResponse>(`${this.apiUrl}/conversar`, request);
  }

  healthCheck(): Observable<{ status: string; module: string; openai_disponible: boolean }> {
    return this.http.get<{ status: string; module: string; openai_disponible: boolean }>(`${this.apiUrl}/health`);
  }
}