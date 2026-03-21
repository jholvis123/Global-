import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';
import { PaginatedResponse, DataResponse } from '../../../core/models/api-response.model';

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

export interface PendientesResponse {
  anticipos: Anticipo[];
  total_pendiente: number;
}

@Injectable({ providedIn: 'root' })
export class AnticiposService {
  private endpoint = '/anticipos';

  constructor(private api: ApiService) {}

  getAll(params?: any): Observable<PaginatedResponse<Anticipo>> {
    return this.api.get<PaginatedResponse<Anticipo>>(this.endpoint, params);
  }

  getById(id: number): Observable<Anticipo> {
    return this.api.get<DataResponse<Anticipo>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  create(data: AnticipoCreate): Observable<Anticipo> {
    return this.api.post<DataResponse<Anticipo>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  delete(id: number): Observable<any> {
    return this.api.delete(`${this.endpoint}/${id}`);
  }

  aprobar(id: number): Observable<Anticipo> {
    return this.api.post<DataResponse<Anticipo>>(`${this.endpoint}/${id}/aprobar`, {})
      .pipe(map(res => res.data));
  }

  rechazar(id: number, motivo?: string): Observable<Anticipo> {
    return this.api.post<DataResponse<Anticipo>>(`${this.endpoint}/${id}/rechazar`, { motivo })
      .pipe(map(res => res.data));
  }

  getPendientesChofer(choferId: number): Observable<PendientesResponse> {
    return this.api.get<PendientesResponse>(`${this.endpoint}/chofer/${choferId}/pendientes`);
  }
}
