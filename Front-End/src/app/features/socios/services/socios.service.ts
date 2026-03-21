import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';
import { Socio, SocioCreate, SocioUpdate } from '../../../models';

@Injectable({ providedIn: 'root' })
export class SociosService {
  private endpoint = '/socios';

  constructor(private api: ApiService) {}

  getAll(params?: any): Observable<Socio[]> {
    return this.api.get<Socio[]>(this.endpoint, params);
  }

  getById(id: number): Observable<Socio> {
    return this.api.get<Socio>(`${this.endpoint}/${id}`);
  }

  create(data: SocioCreate): Observable<Socio> {
    return this.api.post<Socio>(this.endpoint, data);
  }

  update(id: number, data: SocioUpdate): Observable<Socio> {
    return this.api.put<Socio>(`${this.endpoint}/${id}`, data);
  }

  delete(id: number): Observable<any> {
    return this.api.delete(`${this.endpoint}/${id}`);
  }

  getActivos(): Observable<Socio[]> {
    return this.api.get<Socio[]>(`${this.endpoint}/activos`);
  }

  getResumenFinanciero(socioId: number, mes?: number, año?: number): Observable<any> {
    const params: any = {};
    if (mes) params.mes = mes;
    if (año) params.año = año;
    return this.api.get<any>(`${this.endpoint}/${socioId}/resumen-financiero`, params);
  }

  getVehiculos(socioId: number): Observable<any[]> {
    return this.api.get<any[]>(`${this.endpoint}/${socioId}/vehiculos`);
  }
}
