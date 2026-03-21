import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface TourStep {
  id: string;
  target: string;
  title: string;
  content: string;
  position: 'top' | 'bottom' | 'left' | 'right';
  order: number;
}

export interface Tour {
  id: string;
  name: string;
  steps: TourStep[];
}

@Injectable({
  providedIn: 'root'
})
export class OnboardingService {
  private currentTourSubject = new BehaviorSubject<Tour | null>(null);
  private currentStepSubject = new BehaviorSubject<number>(0);
  private isActiveSubject = new BehaviorSubject<boolean>(false);
  
  currentTour$ = this.currentTourSubject.asObservable();
  currentStep$ = this.currentStepSubject.asObservable();
  isActive$ = this.isActiveSubject.asObservable();

  private readonly STORAGE_KEY = 'onboarding_completed';

  // Tours predefinidos
  private tours: Map<string, Tour> = new Map([
    ['dashboard', {
      id: 'dashboard',
      name: 'Tour del Dashboard',
      steps: [
        {
          id: 'welcome',
          target: '.page-header',
          title: '¡Bienvenido al Sistema!',
          content: 'Este es tu panel de control. Aquí podrás ver un resumen de toda la información importante de tu empresa de transporte.',
          position: 'bottom',
          order: 1
        },
        {
          id: 'kpi-cards',
          target: '.kpi-grid',
          title: 'Indicadores Clave',
          content: 'Estos son tus KPIs principales: viajes activos, ingresos, gastos y más. Mantén un ojo en estos números.',
          position: 'bottom',
          order: 2
        },
        {
          id: 'sidebar',
          target: '.sidebar',
          title: 'Menú de Navegación',
          content: 'Desde aquí puedes acceder a todos los módulos: Viajes, Vehículos, Choferes, Clientes y más.',
          position: 'right',
          order: 3
        },
        {
          id: 'search',
          target: '.search-trigger',
          title: 'Búsqueda Rápida',
          content: 'Usa Ctrl+K para buscar rápidamente cualquier viaje, vehículo, chofer o cliente.',
          position: 'bottom',
          order: 4
        },
        {
          id: 'notifications',
          target: '.action-btn[matMenuTriggerFor]',
          title: 'Notificaciones',
          content: 'Aquí verás alertas importantes como documentos por vencer, mantenimientos programados, etc.',
          position: 'bottom',
          order: 5
        },
        {
          id: 'user-menu',
          target: '.user-trigger',
          title: 'Tu Perfil',
          content: 'Desde aquí puedes acceder a tu perfil, configuración y cerrar sesión.',
          position: 'bottom',
          order: 6
        }
      ]
    }],
    ['viajes', {
      id: 'viajes',
      name: 'Tour de Viajes',
      steps: [
        {
          id: 'viajes-list',
          target: '.page-header',
          title: 'Gestión de Viajes',
          content: 'Aquí puedes ver y gestionar todos los viajes de tu empresa.',
          position: 'bottom',
          order: 1
        },
        {
          id: 'nuevo-viaje',
          target: 'button[color="primary"]',
          title: 'Crear Nuevo Viaje',
          content: 'Haz clic aquí para programar un nuevo viaje.',
          position: 'left',
          order: 2
        },
        {
          id: 'filtros',
          target: '.filters-card',
          title: 'Filtros',
          content: 'Usa los filtros para encontrar viajes específicos por fecha, estado, vehículo, etc.',
          position: 'bottom',
          order: 3
        },
        {
          id: 'exportar',
          target: 'button[matMenuTriggerFor]',
          title: 'Exportar Datos',
          content: 'Puedes exportar la lista de viajes a Excel o PDF para tus reportes.',
          position: 'left',
          order: 4
        }
      ]
    }]
  ]);

  constructor() {}

  startTour(tourId: string): void {
    const tour = this.tours.get(tourId);
    if (tour) {
      this.currentTourSubject.next(tour);
      this.currentStepSubject.next(0);
      this.isActiveSubject.next(true);
    }
  }

  nextStep(): void {
    const tour = this.currentTourSubject.value;
    const currentStep = this.currentStepSubject.value;
    
    if (tour && currentStep < tour.steps.length - 1) {
      this.currentStepSubject.next(currentStep + 1);
    } else {
      this.completeTour();
    }
  }

  previousStep(): void {
    const currentStep = this.currentStepSubject.value;
    if (currentStep > 0) {
      this.currentStepSubject.next(currentStep - 1);
    }
  }

  skipTour(): void {
    this.completeTour();
  }

  private completeTour(): void {
    const tour = this.currentTourSubject.value;
    if (tour) {
      this.markTourAsCompleted(tour.id);
    }
    this.currentTourSubject.next(null);
    this.currentStepSubject.next(0);
    this.isActiveSubject.next(false);
  }

  getCurrentStep(): TourStep | null {
    const tour = this.currentTourSubject.value;
    const stepIndex = this.currentStepSubject.value;
    return tour ? tour.steps[stepIndex] : null;
  }

  getTotalSteps(): number {
    const tour = this.currentTourSubject.value;
    return tour ? tour.steps.length : 0;
  }

  isTourCompleted(tourId: string): boolean {
    const completed = localStorage.getItem(this.STORAGE_KEY);
    if (completed) {
      const completedTours: string[] = JSON.parse(completed);
      return completedTours.includes(tourId);
    }
    return false;
  }

  private markTourAsCompleted(tourId: string): void {
    const completed = localStorage.getItem(this.STORAGE_KEY);
    let completedTours: string[] = completed ? JSON.parse(completed) : [];
    
    if (!completedTours.includes(tourId)) {
      completedTours.push(tourId);
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(completedTours));
    }
  }

  resetAllTours(): void {
    localStorage.removeItem(this.STORAGE_KEY);
  }

  shouldShowTour(tourId: string): boolean {
    return !this.isTourCompleted(tourId);
  }
}
