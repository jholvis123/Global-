/**
 * Dashboard Service - Comunicación con API del dashboard
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface DashboardStats {
  viajes: {
    total: number;
    en_curso: number;
    completados_mes: number;
    ingresos_mes: number;
  };
  vehiculos: {
    total: number;
    disponibles: number;
    en_mantenimiento: number;
  };
  choferes: {
    total: number;
    disponibles: number;
    en_viaje: number;
  };
  alertas: Alerta[];
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
  vehiculos_mas_usados: { placa: string; viajes: number }[];
  clientes_principales: { nombre: string; viajes: number; monto: number }[];
}

@Injectable({ providedIn: 'root' })
export class DashboardService {
  private endpoint = '/dashboard';

  constructor(private api: ApiService) {}

  obtenerDashboard(): Observable<DashboardStats> {
    return this.api.get<DashboardStats>(this.endpoint);
  }

  obtenerResumenPeriodo(fechaInicio: string, fechaFin: string): Observable<ResumenPeriodo> {
    return this.api.get<ResumenPeriodo>(`${this.endpoint}/resumen`, {
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin
    });
  }
}
