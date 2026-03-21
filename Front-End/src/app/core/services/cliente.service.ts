/**
 * Cliente Service - Comunicación con API de clientes
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';
import { PaginatedResponse, DataResponse, FilterParams } from '../models/api-response.model';

export interface Cliente {
  id: number;
  razon_social: string;
  nit: string;
  direccion: string;
  telefono: string;
  email: string;
  contacto: string;
  estado: string;
}

export interface ClienteCreate {
  razon_social: string;
  nit: string;
  direccion?: string;
  telefono?: string;
  email?: string;
  contacto?: string;
}

@Injectable({ providedIn: 'root' })
export class ClienteService {
  private endpoint = '/clientes';

  constructor(private api: ApiService) {}

  listar(params?: FilterParams): Observable<PaginatedResponse<Cliente>> {
    return this.api.get<PaginatedResponse<Cliente>>(this.endpoint, params);
  }

  obtener(id: number): Observable<Cliente> {
    return this.api.get<DataResponse<Cliente>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  crear(data: ClienteCreate): Observable<Cliente> {
    return this.api.post<DataResponse<Cliente>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  actualizar(id: number, data: Partial<ClienteCreate>): Observable<Cliente> {
    return this.api.put<DataResponse<Cliente>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  eliminar(id: number): Observable<void> {
    return this.api.delete<void>(`${this.endpoint}/${id}`);
  }

  obtenerActivos(): Observable<Cliente[]> {
    return this.api.get<DataResponse<Cliente[]>>(`${this.endpoint}/activos`)
      .pipe(map(res => res.data));
  }
}
