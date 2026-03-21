/**
 * Anticipo Service - Comunicación con API de anticipos
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';
import { PaginatedResponse, DataResponse, FilterParams } from '../models/api-response.model';

export interface Anticipo {
  id: number;
  chofer_id: number;
  chofer?: { id: number; nombre: string };
  monto_bs: number;
  fecha: string;
  motivo: string;
  estado: string;
  viaje_id?: number;
}

export interface AnticipoCreate {
  chofer_id: number;
  monto_bs: number;
  fecha: string;
  motivo: string;
}

export interface AnticipoFilter extends FilterParams {
  chofer_id?: number;
}

export interface PendientesChoferResponse {
  anticipos: Anticipo[];
  total_pendiente: number;
}

@Injectable({ providedIn: 'root' })
export class AnticipoService {
  private endpoint = '/anticipos';

  constructor(private api: ApiService) {}

  listar(params?: AnticipoFilter): Observable<PaginatedResponse<Anticipo>> {
    return this.api.get<PaginatedResponse<Anticipo>>(this.endpoint, params);
  }

  obtener(id: number): Observable<Anticipo> {
    return this.api.get<DataResponse<Anticipo>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  crear(data: AnticipoCreate): Observable<Anticipo> {
    return this.api.post<DataResponse<Anticipo>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  eliminar(id: number): Observable<void> {
    return this.api.delete<void>(`${this.endpoint}/${id}`);
  }

  obtenerPendientesChofer(choferId: number): Observable<PendientesChoferResponse> {
    return this.api.get<PendientesChoferResponse>(
      `${this.endpoint}/chofer/${choferId}/pendientes`
    );
  }
}
