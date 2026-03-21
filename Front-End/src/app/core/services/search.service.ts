import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';

export interface SearchResult {
  id: number | string;
  type: 'viaje' | 'vehiculo' | 'chofer' | 'cliente' | 'socio' | 'anticipo' | 'liquidacion' | 'mantenimiento';
  title: string;
  subtitle: string;
  icon: string;
  route: string;
}

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private searchTermSubject = new BehaviorSubject<string>('');
  private isOpenSubject = new BehaviorSubject<boolean>(false);
  
  searchTerm$ = this.searchTermSubject.asObservable();
  isOpen$ = this.isOpenSubject.asObservable();

  // Mock data para búsqueda - en producción vendría del backend
  private mockData: SearchResult[] = [
    // Viajes
    { id: 1, type: 'viaje', title: 'Viaje Lima - Arequipa', subtitle: 'ABC-123 • Juan Pérez', icon: 'route', route: '/app/viajes/detalle/1' },
    { id: 2, type: 'viaje', title: 'Viaje Cusco - Lima', subtitle: 'XYZ-789 • Carlos López', icon: 'route', route: '/app/viajes/detalle/2' },
    { id: 3, type: 'viaje', title: 'Viaje Trujillo - Chiclayo', subtitle: 'DEF-456 • Pedro García', icon: 'route', route: '/app/viajes/detalle/3' },
    
    // Vehículos
    { id: 1, type: 'vehiculo', title: 'ABC-123 • Volvo FH 500', subtitle: 'Tractocamión • Activo', icon: 'local_shipping', route: '/app/vehiculos/detalle/1' },
    { id: 2, type: 'vehiculo', title: 'XYZ-789 • Scania R450', subtitle: 'Tractocamión • Activo', icon: 'local_shipping', route: '/app/vehiculos/detalle/2' },
    { id: 3, type: 'vehiculo', title: 'DEF-456 • Mercedes Actros', subtitle: 'Tractocamión • Mantenimiento', icon: 'local_shipping', route: '/app/vehiculos/detalle/3' },
    
    // Choferes
    { id: 1, type: 'chofer', title: 'Juan Pérez García', subtitle: 'DNI: 12345678 • Activo', icon: 'badge', route: '/app/choferes/detalle/1' },
    { id: 2, type: 'chofer', title: 'Carlos López Mendoza', subtitle: 'DNI: 87654321 • Activo', icon: 'badge', route: '/app/choferes/detalle/2' },
    { id: 3, type: 'chofer', title: 'Pedro García Silva', subtitle: 'DNI: 11223344 • Vacaciones', icon: 'badge', route: '/app/choferes/detalle/3' },
    
    // Clientes
    { id: 1, type: 'cliente', title: 'Empresa ABC S.A.C.', subtitle: 'RUC: 20123456789', icon: 'business', route: '/app/clientes/detalle/1' },
    { id: 2, type: 'cliente', title: 'Comercial del Norte', subtitle: 'RUC: 20987654321', icon: 'business', route: '/app/clientes/detalle/2' },
    { id: 3, type: 'cliente', title: 'Distribuidora Sur', subtitle: 'RUC: 20112233445', icon: 'business', route: '/app/clientes/detalle/3' },
    
    // Socios
    { id: 1, type: 'socio', title: 'Transportes Unidos', subtitle: '3 vehículos asignados', icon: 'handshake', route: '/app/socios/detalle/1' },
    { id: 2, type: 'socio', title: 'Carga Pesada SAC', subtitle: '5 vehículos asignados', icon: 'handshake', route: '/app/socios/detalle/2' },
    
    // Anticipos
    { id: 1, type: 'anticipo', title: 'ANT-2024-0001', subtitle: 'S/. 500 • Juan Pérez', icon: 'payments', route: '/app/anticipos/detalle/1' },
    { id: 2, type: 'anticipo', title: 'ANT-2024-0002', subtitle: 'S/. 800 • Carlos López', icon: 'payments', route: '/app/anticipos/detalle/2' },
    
    // Liquidaciones
    { id: 1, type: 'liquidacion', title: 'LIQ-2024-0001', subtitle: 'Lima - Arequipa • S/. 5,500', icon: 'receipt_long', route: '/app/liquidaciones/detalle/1' },
    { id: 2, type: 'liquidacion', title: 'LIQ-2024-0002', subtitle: 'Cusco - Lima • S/. 4,200', icon: 'receipt_long', route: '/app/liquidaciones/detalle/2' },
    
    // Mantenimientos
    { id: 1, type: 'mantenimiento', title: 'Cambio de aceite ABC-123', subtitle: 'Programado • 25/01/2024', icon: 'build', route: '/app/mantenimientos/detalle/1' },
    { id: 2, type: 'mantenimiento', title: 'Reparación frenos XYZ-789', subtitle: 'Completado • 20/01/2024', icon: 'build', route: '/app/mantenimientos/detalle/2' },
  ];

  constructor() { }

  search(term: string): Observable<SearchResult[]> {
    if (!term || term.length < 2) {
      return of([]);
    }

    const normalizedTerm = term.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    
    const results = this.mockData.filter(item => {
      const title = item.title.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const subtitle = item.subtitle.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      
      return title.includes(normalizedTerm) || subtitle.includes(normalizedTerm);
    });

    return of(results.slice(0, 10)); // Máximo 10 resultados
  }

  searchByType(term: string, type: SearchResult['type']): Observable<SearchResult[]> {
    return this.search(term).pipe(
      switchMap(results => of(results.filter(r => r.type === type)))
    );
  }

  setSearchTerm(term: string): void {
    this.searchTermSubject.next(term);
  }

  openSearch(): void {
    this.isOpenSubject.next(true);
  }

  closeSearch(): void {
    this.isOpenSubject.next(false);
    this.searchTermSubject.next('');
  }

  toggleSearch(): void {
    this.isOpenSubject.next(!this.isOpenSubject.value);
  }

  getTypeLabel(type: SearchResult['type']): string {
    const labels: Record<SearchResult['type'], string> = {
      viaje: 'Viaje',
      vehiculo: 'Vehículo',
      chofer: 'Chofer',
      cliente: 'Cliente',
      socio: 'Socio',
      anticipo: 'Anticipo',
      liquidacion: 'Liquidación',
      mantenimiento: 'Mantenimiento'
    };
    return labels[type] || type;
  }

  getTypeColor(type: SearchResult['type']): string {
    const colors: Record<SearchResult['type'], string> = {
      viaje: '#3b82f6',
      vehiculo: '#10b981',
      chofer: '#f59e0b',
      cliente: '#8b5cf6',
      socio: '#ec4899',
      anticipo: '#06b6d4',
      liquidacion: '#6366f1',
      mantenimiento: '#ef4444'
    };
    return colors[type] || '#6b7280';
  }
}
