import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';
import { PaginatedResponse, DataResponse } from '../../../core/models/api-response.model';
import { Vehiculo, VehiculoCreate, VehiculoUpdate } from '../../../models';

@Injectable({
  providedIn: 'root'
})
export class VehiculosService {
  private endpoint = '/vehiculos';

  constructor(private api: ApiService) {}

  getAll(params?: any): Observable<PaginatedResponse<Vehiculo>> {
    return this.api.get<PaginatedResponse<Vehiculo>>(this.endpoint, params);
  }

  getById(id: number): Observable<Vehiculo> {
    return this.api.get<DataResponse<Vehiculo>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  create(data: VehiculoCreate): Observable<Vehiculo> {
    return this.api.post<DataResponse<Vehiculo>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  update(id: number, data: VehiculoUpdate): Observable<Vehiculo> {
    return this.api.put<DataResponse<Vehiculo>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  delete(id: number): Observable<any> {
    return this.api.delete(`${this.endpoint}/${id}`);
  }

  // Operaciones específicas
  getBySocio(socioId: number): Observable<PaginatedResponse<Vehiculo>> {
    return this.api.get<PaginatedResponse<Vehiculo>>(this.endpoint, { socio_id: socioId });
  }

  getDisponibles(): Observable<Vehiculo[]> {
    return this.api.get<DataResponse<Vehiculo[]>>(`${this.endpoint}/disponibles`)
      .pipe(map(res => res.data));
  }

  cambiarEstado(id: number, estado: string): Observable<Vehiculo> {
    return this.api.put<DataResponse<Vehiculo>>(`${this.endpoint}/${id}`, { estado })
      .pipe(map(res => res.data));
  }
}
