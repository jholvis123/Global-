/**
 * Viaje Service - Comunicación con API de viajes
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';
import { PaginatedResponse, DataResponse, FilterParams } from '../models/api-response.model';

export interface Viaje {
  id: number;
  codigo: string;
  cliente_id: number;
  cliente?: { id: number; razon_social: string };
  vehiculo_id: number;
  vehiculo?: { id: number; placa: string };
  chofer_id: number;
  chofer?: { id: number; nombre: string };
  origen: string;
  destino: string;
  fecha_salida: string;
  fecha_llegada?: string;
  kilometraje_inicial: number;
  kilometraje_final?: number;
  ingreso_bs: number;
  gastos_combustible?: number;
  gastos_otros?: number;
  estado: string;
}

export interface ViajeCreate {
  cliente_id: number;
  vehiculo_id: number;
  chofer_id: number;
  origen: string;
  destino: string;
  fecha_salida: string;
  kilometraje_inicial: number;
  ingreso_bs: number;
}

export interface ViajeFilter extends FilterParams {
  cliente_id?: number;
  vehiculo_id?: number;
  chofer_id?: number;
}

export interface FinalizarViajeData {
  kilometraje_final: number;
  gastos_combustible?: number;
  gastos_otros?: number;
  notas?: string;
}

@Injectable({ providedIn: 'root' })
export class ViajeService {
  private endpoint = '/viajes';

  constructor(private api: ApiService) {}

  listar(params?: ViajeFilter): Observable<PaginatedResponse<Viaje>> {
    return this.api.get<PaginatedResponse<Viaje>>(this.endpoint, params);
  }

  obtener(id: number): Observable<Viaje> {
    return this.api.get<DataResponse<Viaje>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  crear(data: ViajeCreate): Observable<Viaje> {
    return this.api.post<DataResponse<Viaje>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  actualizar(id: number, data: Partial<ViajeCreate>): Observable<Viaje> {
    return this.api.put<DataResponse<Viaje>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  iniciar(id: number): Observable<Viaje> {
    return this.api.post<DataResponse<Viaje>>(`${this.endpoint}/${id}/iniciar`, {})
      .pipe(map(res => res.data));
  }

  finalizar(id: number, data: FinalizarViajeData): Observable<Viaje> {
    const params = { ...data };
    return this.api.post<DataResponse<Viaje>>(`${this.endpoint}/${id}/finalizar`, null)
      .pipe(map(res => res.data));
  }

  cancelar(id: number, motivo: string): Observable<void> {
    return this.api.delete<void>(`${this.endpoint}/${id}?motivo=${encodeURIComponent(motivo)}`);
  }
}
