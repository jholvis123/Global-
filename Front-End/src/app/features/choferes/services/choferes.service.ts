import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';
import { PaginatedResponse, DataResponse } from '../../../core/models/api-response.model';
import { Chofer, ChoferCreate, ChoferUpdate } from '../../../models';

@Injectable({ providedIn: 'root' })
export class ChoferesService {
  private endpoint = '/choferes';

  constructor(private api: ApiService) {}

  getAll(params?: any): Observable<PaginatedResponse<Chofer>> {
    return this.api.get<PaginatedResponse<Chofer>>(this.endpoint, params);
  }

  getById(id: number): Observable<Chofer> {
    return this.api.get<DataResponse<Chofer>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  create(data: ChoferCreate): Observable<Chofer> {
    return this.api.post<DataResponse<Chofer>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  update(id: number, data: ChoferUpdate): Observable<Chofer> {
    return this.api.put<DataResponse<Chofer>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  delete(id: number): Observable<any> {
    return this.api.delete(`${this.endpoint}/${id}`);
  }

  getDisponibles(): Observable<Chofer[]> {
    return this.api.get<DataResponse<Chofer[]>>(`${this.endpoint}/disponibles`)
      .pipe(map(res => res.data));
  }

  getByEstado(estado: string): Observable<PaginatedResponse<Chofer>> {
    return this.api.get<PaginatedResponse<Chofer>>(this.endpoint, { estado });
  }
}
