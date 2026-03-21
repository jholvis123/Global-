import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';
import { Cliente, ClienteCreate, ClienteUpdate } from '../../../models';
import { PaginatedResponse, DataResponse } from '../../../core/models/api-response.model';

@Injectable({ providedIn: 'root' })
export class ClientesService {
  private endpoint = '/clientes';

  constructor(private api: ApiService) {}

  getAll(params?: any): Observable<PaginatedResponse<Cliente>> {
    return this.api.get<PaginatedResponse<Cliente>>(this.endpoint, params);
  }

  getById(id: number): Observable<Cliente> {
    return this.api.get<DataResponse<Cliente>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  create(data: ClienteCreate): Observable<Cliente> {
    return this.api.post<DataResponse<Cliente>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  update(id: number, data: ClienteUpdate): Observable<Cliente> {
    return this.api.put<DataResponse<Cliente>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  delete(id: number): Observable<any> {
    return this.api.delete(`${this.endpoint}/${id}`);
  }

  getActivos(): Observable<Cliente[]> {
    return this.api.get<PaginatedResponse<Cliente>>(this.endpoint, { estado: 'ACTIVO', limit: 1000 })
      .pipe(map(res => res.data));
  }
}
