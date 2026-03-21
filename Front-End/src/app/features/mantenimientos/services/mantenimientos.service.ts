import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';
import { PaginatedResponse, DataResponse } from '../../../core/models/api-response.model';

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

@Injectable({ providedIn: 'root' })
export class MantenimientosService {
  private endpoint = '/mantenimientos';

  constructor(private api: ApiService) {}

  getAll(params?: any): Observable<PaginatedResponse<Mantenimiento>> {
    return this.api.get<PaginatedResponse<Mantenimiento>>(this.endpoint, params);
  }

  getById(id: number): Observable<Mantenimiento> {
    return this.api.get<DataResponse<Mantenimiento>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  create(data: MantenimientoCreate): Observable<Mantenimiento> {
    return this.api.post<DataResponse<Mantenimiento>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  update(id: number, data: Partial<MantenimientoCreate>): Observable<Mantenimiento> {
    return this.api.put<DataResponse<Mantenimiento>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  completar(id: number, costoBs: number, notas?: string): Observable<Mantenimiento> {
    return this.api.post<DataResponse<Mantenimiento>>(
      `${this.endpoint}/${id}/completar?costo_bs=${costoBs}${notas ? '&notas=' + encodeURIComponent(notas) : ''}`,
      {}
    ).pipe(map(res => res.data));
  }

  getProximos(dias: number = 30): Observable<Mantenimiento[]> {
    return this.api.get<DataResponse<Mantenimiento[]>>(`${this.endpoint}/proximos`, { dias })
      .pipe(map(res => res.data));
  }

  getHistorialVehiculo(vehiculoId: number): Observable<PaginatedResponse<Mantenimiento>> {
    return this.api.get<PaginatedResponse<Mantenimiento>>(
      `${this.endpoint}/vehiculo/${vehiculoId}/historial`
    );
  }
}
