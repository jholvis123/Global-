import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';

// Interfaz que coincide con el backend
export interface DashboardResponse {
  contadores: {
    viajes_planificados: number;
    viajes_en_ruta: number;
    pendientes_liquidacion: number;
    vehiculos_disponibles: number;
    vehiculos_mantenimiento: number;
  };
  mes_actual: {
    total_viajes: number;
    ingreso_bruto_bs: number;
    gastos_bs: number;
    ingreso_neto_bs: number;
    total_km: number;
    total_toneladas: number;
  };
  alertas: Alerta[];
}

// Interfaz para el template del dashboard
export interface DashboardStats {
  total_viajes: number;
  viajes_en_ruta: number;
  ingresos_mes: number;
  gastos_mes: number;
  ganancia_mes: number;
  rentabilidad: number;
  vehiculos_activos: number;
  vehiculos_mantenimiento: number;
  pendientes_liquidacion: number;
  choferes_activos: number;
  documentos_por_vencer: number;
  licencias_por_vencer: number;
}

export interface Alerta {
  tipo: 'warning' | 'danger' | 'info';
  mensaje: string;
  entidad?: string;
  entidad_id?: number;
}

export interface ResumenPeriodo {
  total_viajes: number;
  ingresos_brutos: number;
  gastos_combustible: number;
  gastos_otros: number;
  ingreso_neto: number;
}

@Injectable({ providedIn: 'root' })
export class DashboardService {

  constructor(private api: ApiService) { }

  getStats(): Observable<DashboardStats> {
    return this.api.get<DashboardResponse>('/dashboard').pipe(
      map(res => this.transformToStats(res))
    );
  }

  private transformToStats(res: DashboardResponse): DashboardStats {
    const ingresos = res.mes_actual?.ingreso_bruto_bs || 0;
    const gastos = res.mes_actual?.gastos_bs || 0;
    const ganancia = ingresos - gastos;
    const rentabilidad = ingresos > 0 ? Math.round((ganancia / ingresos) * 100) : 0;

    return {
      total_viajes: res.mes_actual?.total_viajes || 0,
      viajes_en_ruta: res.contadores?.viajes_en_ruta || 0,
      ingresos_mes: ingresos,
      gastos_mes: gastos,
      ganancia_mes: ganancia,
      rentabilidad: rentabilidad,
      vehiculos_activos: res.contadores?.vehiculos_disponibles || 0,
      vehiculos_mantenimiento: res.contadores?.vehiculos_mantenimiento || 0,
      pendientes_liquidacion: res.contadores?.pendientes_liquidacion || 0,
      choferes_activos: 0, // TODO: Agregar al backend
      documentos_por_vencer: 0, // TODO: Agregar al backend
      licencias_por_vencer: 0 // TODO: Agregar al backend
    };
  }

  getAlertas(): Observable<Alerta[]> {
    return this.api.get<DashboardResponse>('/dashboard').pipe(
      map(res => res.alertas || [])
    );
  }

  getResumenPeriodo(fechaInicio: string, fechaFin: string): Observable<ResumenPeriodo> {
    return this.api.get<ResumenPeriodo>('/dashboard/resumen', {
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin
    });
  }

  getViajesRecientes(limit: number = 5): Observable<any[]> {
    return this.api.get<any[]>('/viajes', { limit, orden: 'fecha_salida', direccion: 'desc' });
  }
}
