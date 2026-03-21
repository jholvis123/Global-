import { BaseEntity, PaginationParams, DateRange, TipoMantenimiento } from './common.types';
import { Vehiculo, VehiculoBasico } from './vehiculo.model';

// ========================================
// TYPES Y ENUMS
// ========================================

// Re-exportar TipoMantenimiento desde common.types
export { TipoMantenimiento };
export type EstadoMantenimiento = 'PROGRAMADO' | 'EN_PROCESO' | 'COMPLETADO' | 'CANCELADO';
export type PrioridadMantenimiento = 'BAJA' | 'MEDIA' | 'ALTA' | 'URGENTE';

// ========================================
// INTERFACES DE MANTENIMIENTO
// ========================================

/**
 * Entidad principal de Mantenimiento
 * Representa un servicio de mantenimiento de vehículo
 */
export interface Mantenimiento extends BaseEntity {
  // Vehículo asociado
  vehiculo_id: number;
  vehiculo?: Vehiculo;
  
  // Tipo y descripción
  tipo: TipoMantenimiento;
  descripcion: string;
  estado: EstadoMantenimiento;
  prioridad: PrioridadMantenimiento;
  
  // Costos
  costo_bs: number;
  costo_repuestos_bs?: number;
  costo_mano_obra_bs?: number;
  
  // Fechas
  fecha: Date | string;
  fecha_programada?: Date | string;
  fecha_inicio?: Date | string;
  fecha_fin?: Date | string;
  
  // Kilometraje
  km_actual?: number;
  proximo_km?: number;
  proxima_fecha?: Date | string;
  
  // Taller y técnico
  taller?: string;
  direccion_taller?: string;
  telefono_taller?: string;
  tecnico_responsable?: string;
  
  // Repuestos y documentos
  repuestos_utilizados?: RepuestoMantenimiento[];
  documentos?: DocumentoMantenimiento[];
  notas?: string;
  
  // Propiedades calculadas
  readonly costo_formateado?: string;
  readonly costo_total_bs?: number;
  readonly es_preventivo?: boolean;
  readonly es_correctivo?: boolean;
  readonly dias_hasta_proximo?: number;
  readonly km_hasta_proximo?: number;
  readonly esta_vencido?: boolean;
}

/**
 * Versión resumida de mantenimiento para listados
 */
export interface MantenimientoResumen {
  id: number;
  vehiculo: VehiculoBasico;
  tipo: TipoMantenimiento;
  descripcion: string;
  estado: EstadoMantenimiento;
  prioridad: PrioridadMantenimiento;
  costo_bs: number;
  fecha: Date | string;
  proximo_km?: number;
  proxima_fecha?: Date | string;
}

/**
 * DTO para crear un mantenimiento
 */
export interface MantenimientoCreate {
  vehiculo_id: number;
  tipo: TipoMantenimiento;
  descripcion: string;
  estado?: EstadoMantenimiento;
  prioridad?: PrioridadMantenimiento;
  costo_bs: number;
  costo_repuestos_bs?: number;
  costo_mano_obra_bs?: number;
  fecha: Date | string;
  fecha_programada?: Date | string;
  km_actual?: number;
  taller?: string;
  direccion_taller?: string;
  telefono_taller?: string;
  tecnico_responsable?: string;
  proximo_km?: number;
  proxima_fecha?: Date | string;
  notas?: string;
}

/**
 * DTO para actualizar un mantenimiento
 */
export interface MantenimientoUpdate {
  tipo?: TipoMantenimiento;
  descripcion?: string;
  estado?: EstadoMantenimiento;
  prioridad?: PrioridadMantenimiento;
  costo_bs?: number;
  costo_repuestos_bs?: number;
  costo_mano_obra_bs?: number;
  fecha?: Date | string;
  fecha_inicio?: Date | string;
  fecha_fin?: Date | string;
  km_actual?: number;
  taller?: string;
  direccion_taller?: string;
  telefono_taller?: string;
  tecnico_responsable?: string;
  proximo_km?: number;
  proxima_fecha?: Date | string;
  notas?: string;
}

/**
 * Repuesto utilizado en mantenimiento
 */
export interface RepuestoMantenimiento {
  id?: number;
  mantenimiento_id?: number;
  nombre: string;
  cantidad: number;
  precio_unitario_bs: number;
  precio_total_bs: number;
  proveedor?: string;
  numero_parte?: string;
}

/**
 * Documento/evidencia del mantenimiento
 */
export interface DocumentoMantenimiento {
  id?: number;
  mantenimiento_id?: number;
  tipo: 'FACTURA' | 'FOTO' | 'INFORME' | 'GARANTIA' | 'OTRO';
  nombre: string;
  url: string;
  fecha_subida: Date | string;
}

// ========================================
// INTERFACES DE FILTROS Y ESTADÍSTICAS
// ========================================

/**
 * Filtros para búsqueda de mantenimientos
 */
export interface MantenimientoFilters extends PaginationParams {
  search?: string;
  vehiculo_id?: number;
  tipo?: TipoMantenimiento | TipoMantenimiento[];
  estado?: EstadoMantenimiento | EstadoMantenimiento[];
  prioridad?: PrioridadMantenimiento | PrioridadMantenimiento[];
  taller?: string;
  fecha_desde?: Date | string;
  fecha_hasta?: Date | string;
  rango_fechas?: DateRange;
  costo_minimo?: number;
  costo_maximo?: number;
  incluir_vencidos?: boolean;
  ordenar_por?: 'fecha' | 'costo_bs' | 'proxima_fecha' | 'proximo_km';
  direccion?: 'asc' | 'desc';
}

/**
 * Estadísticas de mantenimientos
 */
export interface MantenimientoStats {
  total_mantenimientos: number;
  mantenimientos_por_tipo: Record<TipoMantenimiento, number>;
  mantenimientos_por_estado: Record<EstadoMantenimiento, number>;
  mantenimientos_preventivos: number;
  mantenimientos_correctivos: number;
  mantenimientos_pendientes: number;
  costo_total_bs: number;
  costo_preventivo_bs: number;
  costo_correctivo_bs: number;
  costo_promedio_bs: number;
  mantenimientos_ultimo_mes: number;
  costo_ultimo_mes_bs: number;
  proximos_vencimientos: number;
  ratio_preventivo_correctivo: number;
}

/**
 * Resumen de mantenimientos por vehículo
 */
export interface ResumenMantenimientoVehiculo {
  vehiculo_id: number;
  vehiculo: VehiculoBasico;
  cantidad_mantenimientos: number;
  cantidad_preventivos: number;
  cantidad_correctivos: number;
  costo_total_bs: number;
  ultimo_mantenimiento: Date | string;
  proximo_vencimiento?: Date | string;
  proximo_km?: number;
}

/**
 * Mantenimientos próximos o vencidos
 */
export interface MantenimientoPendiente {
  vehiculo: VehiculoBasico;
  tipo_alerta: 'PROXIMO' | 'VENCIDO';
  tipo_mantenimiento: TipoMantenimiento;
  descripcion: string;
  fecha_limite?: Date | string;
  km_limite?: number;
  km_actual?: number;
  dias_restantes?: number;
  km_restantes?: number;
  prioridad: PrioridadMantenimiento;
}

// ========================================
// CONSTANTES
// ========================================

export const TIPOS_MANTENIMIENTO = [
  { value: 'PREVENTIVO', label: 'Preventivo', color: 'primary', icon: 'build' },
  { value: 'CORRECTIVO', label: 'Correctivo', color: 'warn', icon: 'build_circle' }
] as const;

export const ESTADOS_MANTENIMIENTO = [
  { value: 'PROGRAMADO', label: 'Programado', color: 'accent', icon: 'schedule' },
  { value: 'EN_PROCESO', label: 'En Proceso', color: 'primary', icon: 'engineering' },
  { value: 'COMPLETADO', label: 'Completado', color: 'primary', icon: 'check_circle' },
  { value: 'CANCELADO', label: 'Cancelado', color: 'warn', icon: 'cancel' }
] as const;

export const PRIORIDADES_MANTENIMIENTO = [
  { value: 'BAJA', label: 'Baja', color: '', icon: 'arrow_downward' },
  { value: 'MEDIA', label: 'Media', color: 'accent', icon: 'remove' },
  { value: 'ALTA', label: 'Alta', color: 'warn', icon: 'arrow_upward' },
  { value: 'URGENTE', label: 'Urgente', color: 'warn', icon: 'priority_high' }
] as const;
