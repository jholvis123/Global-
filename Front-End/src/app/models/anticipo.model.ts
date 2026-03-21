import { BaseEntity, PaginationParams, DateRange, EstadoAnticipo } from './common.types';
import { Socio, SocioBasico } from './socio.model';
import { Chofer, ChoferBasico } from './chofer.model';
import { Viaje, ViajeResumen } from './viaje.model';

// ========================================
// TYPES Y ENUMS
// ========================================

export type TipoBeneficiario = 'SOCIO' | 'CHOFER';
// Re-exportar para uso local
export { EstadoAnticipo };

// ========================================
// INTERFACES DE ANTICIPO
// ========================================

/**
 * Entidad principal de Anticipo
 * Representa un pago adelantado a socio o chofer
 */
export interface Anticipo extends BaseEntity {
  // Viaje asociado (opcional)
  viaje_id?: number;
  viaje?: Viaje;
  
  // Beneficiario
  socio_id?: number;
  socio?: Socio;
  chofer_id?: number;
  chofer?: Chofer;
  beneficiario_tipo: TipoBeneficiario;
  
  // Datos del anticipo
  monto_bs: number;
  fecha: Date | string;
  observacion?: string;
  estado: EstadoAnticipo;
  
  // Liquidación (si aplicable)
  liquidacion_id?: number;
  fecha_liquidacion?: Date | string;
  
  // Propiedades calculadas
  readonly beneficiario_nombre?: string;
  readonly monto_formateado?: string;
}

/**
 * Versión resumida de anticipo para listados
 */
export interface AnticipoResumen {
  id: number;
  beneficiario_tipo: TipoBeneficiario;
  beneficiario_nombre: string;
  monto_bs: number;
  monto_formateado: string;
  fecha: Date | string;
  estado: EstadoAnticipo;
  viaje_ruta?: string;
}

/**
 * DTO para crear un anticipo
 */
export interface AnticipoCreate {
  viaje_id?: number;
  socio_id?: number;
  chofer_id?: number;
  beneficiario_tipo: TipoBeneficiario;
  monto_bs: number;
  fecha: Date | string;
  observacion?: string;
}

/**
 * DTO para actualizar un anticipo
 */
export interface AnticipoUpdate {
  monto_bs?: number;
  fecha?: Date | string;
  observacion?: string;
  estado?: EstadoAnticipo;
}

// ========================================
// INTERFACES DE FILTROS Y ESTADÍSTICAS
// ========================================

/**
 * Filtros para búsqueda de anticipos
 */
export interface AnticipoFilters extends PaginationParams {
  search?: string;
  beneficiario_tipo?: TipoBeneficiario;
  estado?: EstadoAnticipo | EstadoAnticipo[];
  socio_id?: number;
  chofer_id?: number;
  viaje_id?: number;
  fecha_desde?: Date | string;
  fecha_hasta?: Date | string;
  rango_fechas?: DateRange;
  monto_minimo?: number;
  monto_maximo?: number;
  solo_pendientes?: boolean;
  ordenar_por?: 'fecha' | 'monto_bs' | 'created_at';
  direccion?: 'asc' | 'desc';
}

/**
 * Estadísticas de anticipos
 */
export interface AnticipoStats {
  total_anticipos: number;
  anticipos_pendientes: number;
  anticipos_liquidados: number;
  monto_total_bs: number;
  monto_pendiente_bs: number;
  monto_liquidado_bs: number;
  anticipos_a_socios: number;
  monto_socios_bs: number;
  anticipos_a_choferes: number;
  monto_choferes_bs: number;
  promedio_anticipo_bs: number;
  anticipos_ultimo_mes: number;
  monto_ultimo_mes_bs: number;
}

/**
 * Resumen de anticipos por beneficiario
 */
export interface ResumenAnticiposBeneficiario {
  beneficiario_id: number;
  beneficiario_tipo: TipoBeneficiario;
  beneficiario_nombre: string;
  cantidad_anticipos: number;
  monto_total_bs: number;
  monto_pendiente_bs: number;
  monto_liquidado_bs: number;
  ultimo_anticipo: Date | string;
}

// ========================================
// CONSTANTES
// ========================================

export const TIPOS_BENEFICIARIO = [
  { value: 'SOCIO', label: 'Socio', icon: 'business' },
  { value: 'CHOFER', label: 'Chofer', icon: 'person' }
] as const;

export const ESTADOS_ANTICIPO = [
  { value: 'PENDIENTE', label: 'Pendiente', color: 'warn', icon: 'schedule' },
  { value: 'LIQUIDADO', label: 'Liquidado', color: 'primary', icon: 'check_circle' }
] as const;
