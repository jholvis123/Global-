// src/app/core/services/chatbot-state.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { 
  ChatbotState, 
  CotizacionResponse, 
  CotizacionAvanzadaResponse,
  MensajeChat 
} from '../../shared/models/chatbot.models';

@Injectable({
  providedIn: 'root'
})
export class ChatbotStateService {
  private state$ = new BehaviorSubject<ChatbotState>({
    loading: false,
    error: null,
    cotizacion: null,
    cotizacion_avanzada: null,
    historial: [],
    modo: 'avanzada',
    mensajes: []
  });

  get state() {
    return this.state$.asObservable();
  }

  setLoading(loading: boolean) {
    this.updateState({ loading });
  }

  setError(error: string) {
    this.updateState({ error, loading: false });
  }

  setCotizacion(cotizacion: CotizacionResponse) {
    const currentState = this.state$.value;
    this.updateState({
      cotizacion,
      cotizacion_avanzada: null,
      historial: [...currentState.historial, cotizacion],
      loading: false,
      error: null,
      modo: 'simple'
    });
  }

  setCotizacionAvanzada(cotizacion: CotizacionAvanzadaResponse) {
    const currentState = this.state$.value;
    this.updateState({
      cotizacion: null,
      cotizacion_avanzada: cotizacion,
      historial: [...currentState.historial, cotizacion],
      loading: false,
      error: null,
      modo: 'avanzada'
    });
  }

  // === Métodos de conversación ===
  
  agregarMensajeUsuario(contenido: string): void {
    const mensaje: MensajeChat = {
      id: this.generarId(),
      tipo: 'usuario',
      contenido,
      timestamp: new Date()
    };
    const currentState = this.state$.value;
    this.updateState({
      mensajes: [...currentState.mensajes, mensaje],
      loading: true,
      error: null
    });
  }

  agregarMensajeBot(contenido: string, cotizacion_avanzada?: CotizacionAvanzadaResponse): void {
    const mensaje: MensajeChat = {
      id: this.generarId(),
      tipo: 'bot',
      contenido,
      timestamp: new Date(),
      cotizacion_avanzada
    };
    const currentState = this.state$.value;
    this.updateState({
      mensajes: [...currentState.mensajes, mensaje],
      cotizacion_avanzada: cotizacion_avanzada || currentState.cotizacion_avanzada,
      loading: false,
      error: null
    });
  }

  clearError() {
    this.updateState({ error: null });
  }

  resetState() {
    this.state$.next({
      loading: false,
      error: null,
      cotizacion: null,
      cotizacion_avanzada: null,
      historial: [],
      modo: 'avanzada',
      mensajes: []
    });
  }

  private updateState(update: Partial<ChatbotState>) {
    this.state$.next({ ...this.state$.value, ...update });
  }

  private generarId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }
}