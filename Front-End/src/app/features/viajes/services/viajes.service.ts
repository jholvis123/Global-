import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';
import { Viaje, ViajeCreate, ViajeUpdate, GastoViaje, GastoViajeCreate } from '../../../models';
import { PaginatedResponse, DataResponse } from '../../../core/models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class ViajesService {
  private endpoint = '/viajes';

  constructor(private api: ApiService) {}

  getAll(params?: any): Observable<PaginatedResponse<Viaje>> {
    return this.api.get<PaginatedResponse<Viaje>>(this.endpoint, params);
  }

  getById(id: number): Observable<Viaje> {
    return this.api.get<DataResponse<Viaje>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  create(data: ViajeCreate): Observable<Viaje> {
    return this.api.post<DataResponse<Viaje>>(this.endpoint, data)
      .pipe(map(res => res.data));
  }

  update(id: number, data: ViajeUpdate): Observable<Viaje> {
    return this.api.put<DataResponse<Viaje>>(`${this.endpoint}/${id}`, data)
      .pipe(map(res => res.data));
  }

  delete(id: number): Observable<any> {
    return this.api.delete(`${this.endpoint}/${id}`);
  }

  // Operaciones específicas de viajes
  cambiarEstado(id: number, estado: string): Observable<Viaje> {
    return this.api.patch<DataResponse<Viaje>>(`${this.endpoint}/${id}/estado`, { estado })
      .pipe(map(res => res.data));
  }

  getByEstado(estado: string): Observable<PaginatedResponse<Viaje>> {
    return this.api.get<PaginatedResponse<Viaje>>(`${this.endpoint}`, { estado });
  }

  getPendientesLiquidacion(): Observable<PaginatedResponse<Viaje>> {
    return this.api.get<PaginatedResponse<Viaje>>(`${this.endpoint}/pendientes-liquidacion`);
  }

  // Gastos del viaje
  getGastos(viajeId: number): Observable<GastoViaje[]> {
    return this.api.get<DataResponse<GastoViaje[]>>(`${this.endpoint}/${viajeId}/gastos`)
      .pipe(map(res => res.data));
  }

  agregarGasto(viajeId: number, gasto: GastoViajeCreate): Observable<GastoViaje> {
    return this.api.post<DataResponse<GastoViaje>>(`${this.endpoint}/${viajeId}/gastos`, gasto)
      .pipe(map(res => res.data));
  }

  eliminarGasto(viajeId: number, gastoId: number): Observable<any> {
    return this.api.delete(`${this.endpoint}/${viajeId}/gastos/${gastoId}`);
  }

  // Filtros
  getByChofer(choferId: number, fechaInicio?: Date, fechaFin?: Date): Observable<PaginatedResponse<Viaje>> {
    const params: any = { chofer_id: choferId };
    if (fechaInicio) params.fecha_inicio = fechaInicio.toISOString().split('T')[0];
    if (fechaFin) params.fecha_fin = fechaFin.toISOString().split('T')[0];
    return this.api.get<PaginatedResponse<Viaje>>(this.endpoint, params);
  }

  getByVehiculo(vehiculoId: number, fechaInicio?: Date, fechaFin?: Date): Observable<PaginatedResponse<Viaje>> {
    const params: any = { vehiculo_id: vehiculoId };
    if (fechaInicio) params.fecha_inicio = fechaInicio.toISOString().split('T')[0];
    if (fechaFin) params.fecha_fin = fechaFin.toISOString().split('T')[0];
    return this.api.get<PaginatedResponse<Viaje>>(this.endpoint, params);
  }

  getBySocio(socioId: number, fechaInicio?: Date, fechaFin?: Date): Observable<PaginatedResponse<Viaje>> {
    const params: any = { socio_id: socioId };
    if (fechaInicio) params.fecha_inicio = fechaInicio.toISOString().split('T')[0];
    if (fechaFin) params.fecha_fin = fechaFin.toISOString().split('T')[0];
    return this.api.get<PaginatedResponse<Viaje>>(this.endpoint, params);
  }
}
