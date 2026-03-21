import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';
import { PaginatedResponse, DataResponse } from '../../../core/models/api-response.model';

export interface Liquidacion {
  id: number;
  viaje_id: number;
  viaje?: any;
  ingreso_bruto_bs: number;
  porcentaje_empresa: number;
  monto_empresa_bs: number;
  monto_socio_bs: number;
  descuento_anticipos_bs: number;
  neto_pagar_bs: number;
  fecha_liquidacion: string;
  estado: string;
}

@Injectable({ providedIn: 'root' })
export class LiquidacionesService {
  private endpoint = '/liquidaciones';

  constructor(private api: ApiService) {}

  getAll(params?: any): Observable<PaginatedResponse<Liquidacion>> {
    return this.api.get<PaginatedResponse<Liquidacion>>(this.endpoint, params);
  }

  getById(id: number): Observable<Liquidacion> {
    return this.api.get<DataResponse<Liquidacion>>(`${this.endpoint}/${id}`)
      .pipe(map(res => res.data));
  }

  generar(viajeId: number): Observable<Liquidacion> {
    return this.api.post<DataResponse<Liquidacion>>(`${this.endpoint}/viaje/${viajeId}`, {})
      .pipe(map(res => res.data));
  }

  getPendientes(): Observable<any[]> {
    return this.api.get<DataResponse<any[]>>(`${this.endpoint}/pendientes`)
      .pipe(map(res => res.data));
  }
}
