/**
 * Mantenimiento Service - Comunicación con API de mantenimientos
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';
import { PaginatedResponse, DataResponse, FilterParams } from '../models/api-response.model';

export interface Mantenimiento {
  id: number;
  vehiculo_id: number;
  vehiculo?: { id: number; placa: string };
  tipo: string;
  descripcion: string;
  fecha_programada: string;
  fecha_realizada?: string;
  costo_bs?: number;
  kilometraje: number;
  estado: string;
  notas?: string;
}

export interface MantenimientoCreate {
  vehiculo_id: number;
  tipo: string;
  descripcion: string;
  fecha_programada: string;
  kilometraje: number;
}

export interface MantenimientoFilter extends FilterParams {
  vehiculo_id?: number;
  tipo?: string;
}

@Injectable({ providedIn: 'root' })
export class MantenimientoService {
  private endpoint = '/mantenimientos';

  constructor(private api: ApiService) {}

  listar(params?: MantenimientoFilter): Observable<PaginatedResponse<Mantenimiento>> {
    return this.api.get<PaginatedResponse<Mantenimiento>>(this.endpoint, params);
  }

  obtener(id: number): Observable<Mantenimiento> {
    return this.api.get<DataResponse<Mantenimiento>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  crear(data: MantenimientoCreate): Observable<Mantenimiento> {
    return this.api.post<DataResponse<Mantenimiento>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  actualizar(id: number, data: Partial<MantenimientoCreate>): Observable<Mantenimiento> {
    return this.api.put<DataResponse<Mantenimiento>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  completar(id: number, costoBs: number, notas?: string): Observable<Mantenimiento> {
    const params = { costo_bs: costoBs, notas };
    return this.api.post<DataResponse<Mantenimiento>>(
      `${this.endpoint}/${id}/completar`, 
      null
    ).pipe(map(res => res.data));
  }

  obtenerProximos(dias: number = 30): Observable<Mantenimiento[]> {
    return this.api.get<DataResponse<Mantenimiento[]>>(
      `${this.endpoint}/proximos`, 
      { dias }
    ).pipe(map(res => res.data));
  }

  obtenerHistorialVehiculo(vehiculoId: number): Observable<PaginatedResponse<Mantenimiento>> {
    return this.api.get<PaginatedResponse<Mantenimiento>>(
      `${this.endpoint}/vehiculo/${vehiculoId}/historial`
    );
  }
}
