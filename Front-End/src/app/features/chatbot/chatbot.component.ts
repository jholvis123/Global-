// src/app/features/chatbot/chatbot.component.ts
import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Observable } from 'rxjs';
import { ChatbotService } from '../../core/services/chatbot.service';
import { ChatbotStateService } from '../../core/services/chatbot-state.service';
import { 
  ChatbotState, 
  CotizacionAvanzadaResponse,
  MensajeHistorial,
  ConversacionResponse 
} from '../../shared/models/chatbot.models';
import { CommonModule } from '@angular/common';
import { MatCardModule } from "@angular/material/card";
import { MatIconModule } from "@angular/material/icon";
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatTableModule } from '@angular/material/table';
import { TextFieldModule } from '@angular/cdk/text-field';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatDividerModule,
    MatListModule,
    MatTableModule,
    TextFieldModule,
    MatTooltipModule
  ]
})
export class ChatbotComponent implements OnInit, AfterViewChecked {
  chatbotForm: FormGroup;
  state$: Observable<ChatbotState>;
  
  @ViewChild('mensajesContainer') private mensajesContainer!: ElementRef;
  private shouldScrollToBottom = false;

  constructor(
    private fb: FormBuilder,
    private chatbotService: ChatbotService,
    private chatbotState: ChatbotStateService
  ) {
    this.state$ = this.chatbotState.state;
    this.chatbotForm = this.fb.group({
      mensaje: ['', [Validators.required, Validators.minLength(1)]]
    });
  }

  ngOnInit(): void {
    this.chatbotState.resetState();
  }

  ngAfterViewChecked(): void {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  onSubmit(): void {
    if (this.chatbotForm.valid) {
      const mensaje = this.chatbotForm.value.mensaje.trim();
      if (!mensaje) return;
      
      this.enviarMensaje(mensaje);
      this.chatbotForm.reset();
      this.chatbotForm.get('mensaje')?.setValue('');
    }
  }

  enviarSugerencia(texto: string): void {
    this.enviarMensaje(texto);
  }

  private enviarMensaje(mensaje: string): void {
    // 1. Agregar mensaje del usuario al estado
    this.chatbotState.agregarMensajeUsuario(mensaje);
    this.shouldScrollToBottom = true;
    
    // 2. Construir historial para GPT
    this.state$.subscribe(state => {
      const historial: MensajeHistorial[] = state.mensajes
        .filter(m => m.contenido !== mensaje || m.tipo !== 'usuario')  // Excluir el mensaje actual
        .slice(-10)  // Últimos 10 mensajes
        .map(m => ({
          role: m.tipo === 'usuario' ? 'user' as const : 'assistant' as const,
          content: m.contenido
        }));
      
      // 3. Llamar al endpoint de conversación
      this.chatbotService.conversar(mensaje, historial).subscribe({
        next: (response: ConversacionResponse) => {
          this.chatbotState.agregarMensajeBot(
            response.respuesta,
            response.cotizacion_avanzada || undefined
          );
          this.shouldScrollToBottom = true;
        },
        error: (error) => {
          console.error('Error en conversación:', error);
          const errorMsg = error.error?.detail || 'Error de conexión con el servidor. ¿Está activo el backend?';
          this.chatbotState.setError(errorMsg);
          this.chatbotState.agregarMensajeBot(
            '⚠️ Lo siento, hubo un error al procesar tu mensaje. Por favor intenta nuevamente.'
          );
          this.shouldScrollToBottom = true;
        }
      });
    }).unsubscribe();  // Subscribirse una sola vez para obtener el estado actual
  }

  getEscenariosList(cotizacion: CotizacionAvanzadaResponse): any[] {
    if (!cotizacion) return [];
    return [
      {
        nombre: 'Conservador',
        precio: cotizacion.precios_por_escenario.conservador,
        camiones: cotizacion.escenarios_logisticos.conservador.cantidad_camiones
      },
      {
        nombre: 'Promedio',
        precio: cotizacion.precios_por_escenario.promedio,
        camiones: cotizacion.escenarios_logisticos.promedio.cantidad_camiones
      },
      {
        nombre: 'Óptimo',
        precio: cotizacion.precios_por_escenario.optimo,
        camiones: cotizacion.escenarios_logisticos.optimo.cantidad_camiones
      }
    ];
  }

  clearError(): void {
    this.chatbotState.clearError();
  }

  resetChat(): void {
    this.chatbotState.resetState();
  }

  private scrollToBottom(): void {
    try {
      if (this.mensajesContainer) {
        this.mensajesContainer.nativeElement.scrollTop = 
          this.mensajesContainer.nativeElement.scrollHeight;
      }
    } catch (err) {}
  }
}