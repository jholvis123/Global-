import { BaseEntity, PaginationParams, DateRange, EstadoLiquidacion } from './common.types';
import { Viaje, ViajeResumen } from './viaje.model';
import { Socio, SocioBasico } from './socio.model';
import { Chofer, ChoferBasico } from './chofer.model';

// ========================================
// TYPES Y ENUMS
// ========================================

// Re-exportar para uso local
export { EstadoLiquidacion };

// ========================================
// INTERFACES DE LIQUIDACIÓN
// ========================================

/**
 * Entidad principal de Liquidación
 * Representa el cálculo y pago de un viaje completado
 */
export interface Liquidacion extends BaseEntity {
  // Viaje asociado
  viaje_id: number;
  viaje?: Viaje;
  
  // Montos principales
  ingreso_bs: number;
  gastos_bs: number;
  
  // Pagos a socios y choferes
  socio_id?: number;
  socio?: Socio;
  pago_socio_bs: number;
  porcentaje_socio: number;
  saldo_socio_bs: number;
  
  chofer_id?: number;
  chofer?: Chofer;
  pago_chofer_bs?: number;
  saldo_chofer_bs: number;
  
  // Estado y fechas
  estado: EstadoLiquidacion;
  fecha: Date | string;
  fecha_aprobacion?: Date | string;
  fecha_pago?: Date | string;
  
  // Observaciones
  notas?: string;
  
  // Propiedades calculadas
  readonly margen_bs?: number;
  readonly ingreso_formateado?: string;
  readonly gastos_formateados?: string;
  readonly margen_formateado?: string;
  readonly pago_socio_formateado?: string;
  readonly rentabilidad_porcentaje?: number;
}

/**
 * Versión resumida de liquidación para listados
 */
export interface LiquidacionResumen {
  id: number;
  viaje_id: number;
  viaje_ruta: string;
  socio_nombre?: string;
  chofer_nombre?: string;
  ingreso_bs: number;
  gastos_bs: number;
  margen_bs: number;
  rentabilidad_porcentaje: number;
  estado: EstadoLiquidacion;
  fecha: Date | string;
}

/**
 * DTO para crear una liquidación
 */
export interface LiquidacionCreate {
  viaje_id: number;
  ingreso_bs: number;
  gastos_bs: number;
  socio_id?: number;
  pago_socio_bs: number;
  porcentaje_socio?: number;
  saldo_socio_bs: number;
  chofer_id?: number;
  pago_chofer_bs?: number;
  saldo_chofer_bs?: number;
  fecha: Date | string;
  notas?: string;
}

/**
 * DTO para actualizar una liquidación
 */
export interface LiquidacionUpdate {
  ingreso_bs?: number;
  gastos_bs?: number;
  pago_socio_bs?: number;
  porcentaje_socio?: number;
  saldo_socio_bs?: number;
  pago_chofer_bs?: number;
  saldo_chofer_bs?: number;
  estado?: EstadoLiquidacion;
  notas?: string;
}

/**
 * DTO para aprobar o rechazar liquidación
 */
export interface LiquidacionAprobacion {
  aprobado: boolean;
  notas?: string;
}

// ========================================
// INTERFACES DE FILTROS Y ESTADÍSTICAS
// ========================================

/**
 * Filtros para búsqueda de liquidaciones
 */
export interface LiquidacionFilters extends PaginationParams {
  search?: string;
  estado?: EstadoLiquidacion | EstadoLiquidacion[];
  viaje_id?: number;
  socio_id?: number;
  chofer_id?: number;
  fecha_desde?: Date | string;
  fecha_hasta?: Date | string;
  rango_fechas?: DateRange;
  rentabilidad_minima?: number;
  rentabilidad_maxima?: number;
  ordenar_por?: 'fecha' | 'ingreso_bs' | 'margen_bs' | 'rentabilidad_porcentaje';
  direccion?: 'asc' | 'desc';
}

/**
 * Estadísticas generales de liquidaciones
 */
export interface LiquidacionStats {
  total_liquidaciones: number;
  liquidaciones_pendientes: number;
  liquidaciones_aprobadas: number;
  liquidaciones_pagadas: number;
  ingresos_totales_bs: number;
  gastos_totales_bs: number;
  margen_total_bs: number;
  margen_promedio_bs: number;
  rentabilidad_promedio: number;
  pagos_socios_totales_bs: number;
  pagos_choferes_totales_bs: number;
  saldos_pendientes_socios_bs: number;
  saldos_pendientes_choferes_bs: number;
  liquidaciones_ultimo_mes: number;
  ingresos_ultimo_mes_bs: number;
}

/**
 * Resumen de liquidaciones por socio
 */
export interface ResumenLiquidacionesSocio {
  socio_id: number;
  socio: SocioBasico;
  cantidad_liquidaciones: number;
  ingresos_totales_bs: number;
  gastos_totales_bs: number;
  margen_total_bs: number;
  pagos_recibidos_bs: number;
  saldo_pendiente_bs: number;
  rentabilidad_promedio: number;
}

/**
 * Resumen mensual de liquidaciones
 */
export interface ResumenMensualLiquidaciones {
  mes: string;
  anio: number;
  cantidad_liquidaciones: number;
  ingresos_bs: number;
  gastos_bs: number;
  margen_bs: number;
  rentabilidad_porcentaje: number;
  pagos_socios_bs: number;
  pagos_choferes_bs: number;
}

// ========================================
// CONSTANTES
// ========================================

export const ESTADOS_LIQUIDACION = [
  { value: 'PENDIENTE', label: 'Pendiente', color: 'warn', icon: 'hourglass_empty' },
  { value: 'APROBADA', label: 'Aprobada', color: 'accent', icon: 'check' },
  { value: 'PAGADA', label: 'Pagada', color: 'primary', icon: 'payments' }
] as const;
