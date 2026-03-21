import { BaseEntity, EstadoVehiculo, TipoCombustible } from './common.types';
import { Socio } from './socio.model';

// ========================================
// INTERFACES DE VEHÍCULO
// ========================================

export interface Vehiculo extends BaseEntity {
  placa: string;
  marca: string;
  modelo: string;
  anio: number;
  capacidad_ton: number;
  tipo_combustible?: TipoCombustible;
  numero_motor?: string;
  numero_chasis?: string;
  color?: string;
  socio_id: number;
  socio?: Socio | { id: number; nombre: string; nombre_completo?: string };
  estado: EstadoVehiculo;
  // Documentación
  soat_vencimiento?: Date;
  inspeccion_vencimiento?: Date;
  itv_vencimiento?: Date;
  seguro_vencimiento?: Date;
  // Computed
  identificacion_completa?: string;
  documentos_vigentes?: boolean;
  documentos_por_vencer?: DocumentoPorVencer[];
  km_actual?: number;
  proximo_mantenimiento?: Date;
}

export interface DocumentoPorVencer {
  tipo: 'SOAT' | 'ITV' | 'SEGURO' | 'INSPECCION';
  nombre: string;
  fecha_vencimiento: Date;
  dias_restantes: number;
  estado: 'vigente' | 'por_vencer' | 'vencido';
}

/**
 * Versión resumida del vehículo para listados y referencias
 */
export interface VehiculoBasico {
  id: number;
  placa: string;
  marca: string;
  modelo: string;
  capacidad_ton: number;
  estado: EstadoVehiculo;
  identificacion_completa?: string;
}

export interface VehiculoCreate {
  placa: string;
  marca: string;
  modelo: string;
  anio: number;
  capacidad_ton: number;
  tipo_combustible?: TipoCombustible;
  numero_motor?: string;
  numero_chasis?: string;
  color?: string;
  socio_id: number;
  estado?: EstadoVehiculo;
  soat_vencimiento?: Date | string;
  inspeccion_vencimiento?: Date | string;
  itv_vencimiento?: Date | string;
  seguro_vencimiento?: Date | string;
}

export interface VehiculoUpdate extends Partial<VehiculoCreate> {
  estado?: EstadoVehiculo;
}

export interface VehiculoFilters {
  search?: string;
  estado?: EstadoVehiculo;
  socio_id?: number;
  marca?: string;
  documentos_por_vencer?: boolean;
}

export interface VehiculoStats {
  total: number;
  activos: number;
  enMantenimiento: number;
  inactivos: number;
  vencimientos: number;
}

// Remolque
export interface Remolque extends BaseEntity {
  placa: string;
  tipo: string;
  capacidad_ton: number;
  vehiculo_id?: number;
  vehiculo?: Vehiculo;
  estado: EstadoVehiculo;
}

