/**
 * Vehiculo Service - Comunicación con API de vehículos
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';
import { PaginatedResponse, DataResponse, FilterParams } from '../models/api-response.model';

export interface Vehiculo {
  id: number;
  placa: string;
  marca: string;
  modelo: string;
  anio: number;
  capacidad_tn: number;
  tipo_vehiculo: string;
  estado: string;
  socio_id: number;
  socio?: { id: number; nombre: string };
}

export interface VehiculoCreate {
  placa: string;
  marca: string;
  modelo: string;
  anio: number;
  capacidad_tn: number;
  tipo_vehiculo: string;
  socio_id: number;
}

export interface VehiculoFilter extends FilterParams {
  socio_id?: number;
}

@Injectable({ providedIn: 'root' })
export class VehiculoService {
  private endpoint = '/vehiculos';

  constructor(private api: ApiService) {}

  listar(params?: VehiculoFilter): Observable<PaginatedResponse<Vehiculo>> {
    return this.api.get<PaginatedResponse<Vehiculo>>(this.endpoint, params);
  }

  obtener(id: number): Observable<Vehiculo> {
    return this.api.get<DataResponse<Vehiculo>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  crear(data: VehiculoCreate): Observable<Vehiculo> {
    return this.api.post<DataResponse<Vehiculo>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  actualizar(id: number, data: Partial<VehiculoCreate>): Observable<Vehiculo> {
    return this.api.put<DataResponse<Vehiculo>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  eliminar(id: number): Observable<void> {
    return this.api.delete<void>(`${this.endpoint}/${id}`);
  }

  obtenerDisponibles(): Observable<Vehiculo[]> {
    return this.api.get<DataResponse<Vehiculo[]>>(`${this.endpoint}/disponibles`)
      .pipe(map(res => res.data));
  }
}
