import { Component, OnInit, HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';
import { ChatbotService } from '../../../../core/services/chatbot.service';
import { ChatbotStateService } from '../../../../core/services/chatbot-state.service';
import { 
  ChatbotState, 
  CotizacionResponse, 
  MensajeHistorial, 
  ConversacionResponse 
} from '../../../../shared/models/chatbot.models';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {
  isScrolled = false;
  currentYear = new Date().getFullYear();
  isAuthenticated = false;
  userName = '';

  stats = [
    { value: '150+', label: 'Vehículos', icon: 'local_shipping' },
    { value: '2,500+', label: 'Viajes Mensuales', icon: 'route' },
    { value: '15+', label: 'Años de Experiencia', icon: 'verified' },
    { value: '98%', label: 'Clientes Satisfechos', icon: 'thumb_up' }
  ];

  services = [
    {
      icon: 'local_shipping',
      title: 'Transporte de Carga',
      description: 'Transporte seguro y eficiente de mercancías a nivel nacional con seguimiento en tiempo real.'
    },
    {
      icon: 'inventory_2',
      title: 'Logística Integral',
      description: 'Soluciones completas de almacenamiento, distribución y gestión de inventarios.'
    },
    {
      icon: 'schedule',
      title: 'Entregas Programadas',
      description: 'Planificación precisa de entregas con horarios flexibles según tus necesidades.'
    },
    {
      icon: 'security',
      title: 'Carga Asegurada',
      description: 'Tu mercancía protegida con seguros completos y monitoreo GPS 24/7.'
    },
    {
      icon: 'support_agent',
      title: 'Soporte Dedicado',
      description: 'Equipo de atención al cliente disponible para resolver cualquier consulta.'
    },
    {
      icon: 'analytics',
      title: 'Reportes Detallados',
      description: 'Informes completos de tus operaciones para una mejor toma de decisiones.'
    }
  ];

  advantages = [
    { icon: 'speed', title: 'Rapidez', desc: 'Tiempos de entrega optimizados' },
    { icon: 'verified_user', title: 'Confianza', desc: 'Más de 15 años en el mercado' },
    { icon: 'attach_money', title: 'Precios Justos', desc: 'Tarifas competitivas' },
    { icon: 'gps_fixed', title: 'Rastreo GPS', desc: 'Seguimiento en tiempo real' }
  ];

  testimonials = [
    {
      name: 'Carlos Mendoza',
      company: 'Constructora Norte',
      text: 'Excelente servicio, siempre puntuales y con la mercancía en perfectas condiciones.',
      avatar: 'CM'
    },
    {
      name: 'María García',
      company: 'Distribuidora Central',
      text: 'El mejor aliado logístico que hemos tenido. Su sistema de seguimiento es increíble.',
      avatar: 'MG'
    },
    {
      name: 'Roberto Sánchez',
      company: 'Agroindustrial Sur',
      text: 'Profesionalismo y compromiso en cada entrega. Altamente recomendados.',
      avatar: 'RS'
    }
  ];

  // Chatbot
  isChatOpen = false;
  chatInput = '';
  isTyping = false;
  chatHistory: { sender: 'user' | 'bot'; text: string; time: string }[] = [];
  userMessages: any[] = [];
  chatMessages$: any;
  state$: Observable<ChatbotState>;
  isProcessingCotizacion = false;

  // Respuestas del bot
  private botResponses: { [key: string]: string } = {
    'servicios': '🚚 Ofrecemos:\n• Transporte de carga nacional\n• Logística integral\n• Entregas programadas\n• Carga asegurada con GPS 24/7\n\n¿Te gustaría más información sobre algún servicio?',
    'cotización': '📋 Para solicitar una cotización puedes:\n\n1. Llamarnos al (591) 3 456-7890\n2. Escribirnos a cotizaciones@transcarga.com\n3. Visitarnos en nuestras oficinas\n\n¿Necesitas algo más?',
    'horarios': '🕐 Nuestros horarios de atención:\n\n• Lunes a Viernes: 8:00 - 18:00\n• Sábados: 8:00 - 12:00\n• Domingos: Cerrado\n\nOperaciones 24/7 para emergencias.',
    'asesor': '👨‍💼 ¡Con gusto te comunicamos con un asesor!\n\nPuedes contactarnos:\n📞 (591) 3 456-7890\n📧 ventas@transcarga.com\n\nO déjanos tus datos y te llamamos.',
    'default': '¡Gracias por tu mensaje! 😊\n\nPuedo ayudarte con:\n• Información de servicios\n• Solicitar cotizaciones\n• Horarios de atención\n• Contactar un asesor\n\n¿Qué te gustaría saber?'
  };

  constructor(
    private router: Router,
    private authService: AuthService,
    private chatbotService: ChatbotService,
    private chatbotState: ChatbotStateService
  ) {
    this.state$ = this.chatbotState.state;
  }

  ngOnInit(): void {
    // Verificar si el usuario está autenticado
    this.isAuthenticated = this.authService.isAuthenticated;
    if (this.isAuthenticated) {
      const user = this.authService.currentUser;
      this.userName = user?.nombre || 'Usuario';
    }
  }

  @HostListener('window:scroll')
  onWindowScroll(): void {
    this.isScrolled = window.scrollY > 50;
  }

  navigateToLogin(): void {
    if (this.isAuthenticated) {
      this.router.navigate(['/app/dashboard']);
    } else {
      this.router.navigate(['/auth/login']);
    }
  }

  goToDashboard(): void {
    this.router.navigate(['/app/dashboard']);
  }

  scrollToSection(sectionId: string): void {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  }

  toggleChat(): void {
    this.isChatOpen = !this.isChatOpen;
  }

  sendMessage(): void {
    if (!this.chatInput.trim()) return;

    const userMessage = this.chatInput.trim();
    const now = new Date();
    const time = now.getHours().toString().padStart(2, '0') + ':' + 
                 now.getMinutes().toString().padStart(2, '0');

    // Agregar mensaje del usuario
    this.chatHistory.push({
      sender: 'user',
      text: userMessage,
      time: time
    });

    this.chatInput = '';
    this.isTyping = true;

    // Siempre procesar con el backend (que ya maneja conversación y cotización)
    this.processCotizacion(userMessage, time);
  }

  sendQuickMessage(message: string): void {
    this.chatInput = message;
    this.sendMessage();
  }

  private isCotizacionRequest(message: string): boolean {
    const lowerMessage = message.toLowerCase();
    const cotizacionKeywords = [
      'cotiza', 'cotización', 'precio', 'costo', 'transportar', 'llevar', 'enviar',
      'kg', 'toneladas', 'carga', 'desde', 'hasta', 'origen', 'destino'
    ];
    
    return cotizacionKeywords.some(keyword => lowerMessage.includes(keyword));
  }

  private processCotizacion(message: string, time: string): void {
    this.isProcessingCotizacion = true;
    
    const historial: MensajeHistorial[] = this.chatHistory.map(m => ({
      role: (m.sender === 'user' ? 'user' : 'assistant') as 'user' | 'assistant',
      content: m.text
    })).slice(-10);

    this.chatbotService.conversar(message, historial).subscribe({
      next: (response: ConversacionResponse) => {
        this.isTyping = false;
        this.isProcessingCotizacion = false;
        
        let responseText = response.respuesta;
        
        // Si hay una cotización generada, la mostramos formateada
        if (response.cotizacion_avanzada) {
          const cot = response.cotizacion_avanzada;
          responseText += `\n\n🚛 **RESUMEN DE COTIZACIÓN**\n` +
            `📍 Ruta: ${cot.ruta.origen} → ${cot.ruta.destino}\n` +
            `⚖️ Peso: ${cot.carga_toneladas} toneladas\n` +
            `📦 Tipo: ${cot.tipo_carga}\n` +
            `💰 Precio Promedio: ${cot.precios_por_escenario.promedio.toLocaleString('es-BO', { style: 'currency', currency: 'BOB' })}\n` +
            `✨ RECOMENDACIÓN: ${cot.recomendacion}`;
        }

        this.chatHistory.push({
          sender: 'bot',
          text: responseText,
          time: time
        });
      },
      error: (error) => {
        this.isTyping = false;
        this.isProcessingCotizacion = false;
        
        const errorText = 'Lo siento, hubo un error al conectar con el asistente logístico. 😔\n' +
                         'Por favor intenta de nuevo en unos momentos o contáctanos directamente.';
        
        this.chatHistory.push({
          sender: 'bot',
          text: errorText,
          time: time
        });
      }
    });
  }

  private getBotResponse(message: string): string {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('servicio') || lowerMessage.includes('ofrecen')) {
      return this.botResponses['servicios'];
    }
    if (lowerMessage.includes('cotiza') || lowerMessage.includes('precio') || lowerMessage.includes('costo')) {
      return this.botResponses['cotización'];
    }
    if (lowerMessage.includes('horario') || lowerMessage.includes('atencion') || lowerMessage.includes('abierto')) {
      return this.botResponses['horarios'];
    }
    if (lowerMessage.includes('asesor') || lowerMessage.includes('hablar') || lowerMessage.includes('contactar')) {
      return this.botResponses['asesor'];
    }
    
    return this.botResponses['default'];
  }
}
