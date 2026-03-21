import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface CrudParams {
  skip?: number;
  limit?: number;
  filters?: { [key: string]: any };
  order_by?: string;
}

@Injectable({
  providedIn: 'root'
})
export abstract class BaseCrudService<T, TCreate, TUpdate> {
  protected abstract endpoint: string;

  constructor(protected api: ApiService) {}

  getAll(params?: CrudParams): Observable<T[]> {
    return this.api.get<T[]>(this.endpoint, params);
  }

  getById(id: number): Observable<T> {
    return this.api.get<T>(`${this.endpoint}/${id}`);
  }

  create(data: TCreate): Observable<T> {
    return this.api.post<T>(this.endpoint, data);
  }

  update(id: number, data: TUpdate): Observable<T> {
    return this.api.put<T>(`${this.endpoint}/${id}`, data);
  }

  delete(id: number): Observable<any> {
    return this.api.delete(`${this.endpoint}/${id}`);
  }

  count(filters?: { [key: string]: any }): Observable<{ count: number }> {
    return this.api.get<{ count: number }>(`${this.endpoint}/count`, filters);
  }
}
