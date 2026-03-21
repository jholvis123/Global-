import { BaseEntity, EstadoGeneral, TipoParticipacion } from './common.types';
import { Vehiculo } from './vehiculo.model';

// ========================================
// INTERFACES DE SOCIO
// ========================================

export interface Socio extends BaseEntity {
  nombre: string;
  apellido?: string;
  nit?: string;
  ci?: string;
  direccion?: string;
  telefono?: string;
  email?: string;
  // Información bancaria
  cuenta_bancaria?: string;
  banco?: string;
  tipo_cuenta?: 'AHORRO' | 'CORRIENTE';
  // Participación
  participacion_tipo: TipoParticipacion;
  participacion_valor: number;
  porcentaje_ganancia?: number; // Alias
  // Saldos
  saldo_anticipos: number;
  saldo_pendiente?: number;
  // Relaciones
  usuario_id?: number;
  vehiculos?: Vehiculo[];
  estado: EstadoGeneral;
  // Computed
  nombre_completo?: string;
  total_vehiculos?: number;
  ingresos_mes?: number;
}

/**
 * Versión resumida del socio para listados y referencias
 */
export interface SocioBasico {
  id: number;
  nombre: string;
  apellido?: string;
  nombre_completo?: string;
  nit?: string;
  telefono?: string;
  estado: EstadoGeneral;
}

export interface SocioCreate {
  nombre: string;
  apellido?: string;
  nit?: string;
  ci?: string;
  direccion?: string;
  telefono?: string;
  email?: string;
  cuenta_bancaria?: string;
  banco?: string;
  tipo_cuenta?: 'AHORRO' | 'CORRIENTE';
  participacion_tipo?: TipoParticipacion;
  participacion_valor?: number;
  porcentaje_ganancia?: number;
}

export interface SocioUpdate extends Partial<SocioCreate> {
  estado?: EstadoGeneral;
}

export interface SocioFilters {
  search?: string;
  estado?: EstadoGeneral;
  con_vehiculos?: boolean;
  con_saldo_pendiente?: boolean;
}

export interface SocioStats {
  total: number;
  activos: number;
  vehiculos: number;
  saldo_total_anticipos: number;
}

export interface SocioResumenFinanciero {
  socio_id: number;
  periodo: string;
  total_viajes: number;
  ingresos_brutos: number;
  gastos: number;
  participacion_empresa: number;
  ganancia_socio: number;
  anticipos_descontados: number;
  neto_a_pagar: number;
}

