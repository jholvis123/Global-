/**
 * Chofer Service - Comunicación con API de choferes
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';
import { PaginatedResponse, DataResponse, FilterParams } from '../models/api-response.model';

export interface Chofer {
  id: number;
  nombre: string;
  ci: string;
  licencia: string;
  categoria_licencia: string;
  fecha_vencimiento_licencia: string;
  telefono: string;
  estado: string;
}

export interface ChoferCreate {
  nombre: string;
  ci: string;
  licencia: string;
  categoria_licencia: string;
  fecha_vencimiento_licencia: string;
  telefono?: string;
}

@Injectable({ providedIn: 'root' })
export class ChoferService {
  private endpoint = '/choferes';

  constructor(private api: ApiService) {}

  listar(params?: FilterParams): Observable<PaginatedResponse<Chofer>> {
    return this.api.get<PaginatedResponse<Chofer>>(this.endpoint, params);
  }

  obtener(id: number): Observable<Chofer> {
    return this.api.get<DataResponse<Chofer>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  crear(data: ChoferCreate): Observable<Chofer> {
    return this.api.post<DataResponse<Chofer>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  actualizar(id: number, data: Partial<ChoferCreate>): Observable<Chofer> {
    return this.api.put<DataResponse<Chofer>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  eliminar(id: number): Observable<void> {
    return this.api.delete<void>(`${this.endpoint}/${id}`);
  }

  obtenerDisponibles(): Observable<Chofer[]> {
    return this.api.get<DataResponse<Chofer[]>>(`${this.endpoint}/disponibles`)
      .pipe(map(res => res.data));
  }
}
