/**
 * Liquidacion Service - Comunicación con API de liquidaciones
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';
import { PaginatedResponse, DataResponse, FilterParams } from '../models/api-response.model';
import { Viaje } from './viaje.service';

export interface Liquidacion {
  id: number;
  viaje_id: number;
  viaje?: Viaje;
  ingreso_bruto_bs: number;
  porcentaje_empresa: number;
  monto_empresa_bs: number;
  monto_socio_bs: number;
  descuento_anticipos_bs: number;
  neto_pagar_bs: number;
  fecha_liquidacion: string;
  estado: string;
}

export interface LiquidacionFilter extends FilterParams {
  viaje_id?: number;
}

@Injectable({ providedIn: 'root' })
export class LiquidacionService {
  private endpoint = '/liquidaciones';

  constructor(private api: ApiService) {}

  listar(params?: LiquidacionFilter): Observable<PaginatedResponse<Liquidacion>> {
    return this.api.get<PaginatedResponse<Liquidacion>>(this.endpoint, params);
  }

  obtener(id: number): Observable<Liquidacion> {
    return this.api.get<DataResponse<Liquidacion>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  generar(viajeId: number): Observable<Liquidacion> {
    return this.api.post<DataResponse<Liquidacion>>(
      `${this.endpoint}/viaje/${viajeId}`, 
      {}
    ).pipe(map(res => res.data));
  }

  obtenerPendientes(): Observable<Viaje[]> {
    return this.api.get<DataResponse<Viaje[]>>(`${this.endpoint}/pendientes`)
      .pipe(map(res => res.data));
  }
}
