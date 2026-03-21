import { 
  BaseEntity, 
  EstadoViaje, 
  TipoTarifa, 
  TipoGasto, 
  DateRange, 
  PaginationParams,
  TipoCarga 
} from './common.types';
import { Cliente, ClienteBasico } from './cliente.model';
import { Vehiculo, VehiculoBasico } from './vehiculo.model';
import { Chofer, ChoferBasico } from './chofer.model';

// ========================================
// INTERFACES DE VIAJE
// ========================================

/**
 * Entidad principal de Viaje
 * Representa un viaje de transporte de carga
 */
export interface Viaje extends BaseEntity {
  // Referencias a entidades relacionadas
  cliente_id: number;
  cliente?: Cliente;
  vehiculo_id: number;
  vehiculo?: Vehiculo;
  chofer_id: number;
  chofer?: Chofer;
  
  // Información de ruta
  origen: string;
  destino: string;
  fecha_salida: Date | string;
  fecha_llegada?: Date | string;
  
  // Información de carga
  tipo_carga: TipoCarga;
  peso_ton: number;
  volumen_m3?: number;
  descripcion_carga?: string;
  
  // Kilometraje
  km_estimado: number;
  km_real?: number;
  
  // Tarificación
  tarifa_tipo: TipoTarifa;
  tarifa_valor: number;
  
  // Estado y notas
  estado: EstadoViaje;
  notas?: string;
  
  // Propiedades calculadas (readonly del backend)
  readonly ingreso_total_bs?: number;
  readonly total_gastos_bs?: number;
  readonly margen_bruto_bs?: number;
  readonly ruta_completa?: string;
  readonly duracion_horas?: number;
  readonly rendimiento_km_gal?: number;
  
  // Relaciones
  gastos?: GastoViaje[];
}

/**
 * Versión resumida del viaje para listados
 */
export interface ViajeResumen {
  id: number;
  cliente: ClienteBasico;
  vehiculo: VehiculoBasico;
  chofer: ChoferBasico;
  origen: string;
  destino: string;
  ruta_completa: string;
  fecha_salida: Date | string;
  fecha_llegada?: Date | string;
  estado: EstadoViaje;
  ingreso_total_bs: number;
  total_gastos_bs: number;
  margen_bruto_bs: number;
}

/**
 * DTO para crear un nuevo viaje
 */
export interface ViajeCreate {
  cliente_id: number;
  vehiculo_id: number;
  chofer_id: number;
  origen: string;
  destino: string;
  fecha_salida: Date | string;
  fecha_llegada?: Date | string;
  tipo_carga: TipoCarga;
  peso_ton: number;
  volumen_m3?: number;
  descripcion_carga?: string;
  km_estimado: number;
  tarifa_tipo: TipoTarifa;
  tarifa_valor: number;
  notas?: string;
}

/**
 * DTO para actualizar un viaje existente
 */
export interface ViajeUpdate {
  cliente_id?: number;
  vehiculo_id?: number;
  chofer_id?: number;
  origen?: string;
  destino?: string;
  fecha_salida?: Date | string;
  fecha_llegada?: Date | string;
  tipo_carga?: TipoCarga;
  peso_ton?: number;
  volumen_m3?: number;
  descripcion_carga?: string;
  km_estimado?: number;
  km_real?: number;
  tarifa_tipo?: TipoTarifa;
  tarifa_valor?: number;
  estado?: EstadoViaje;
  notas?: string;
}

/**
 * DTO para cambiar estado del viaje
 */
export interface CambioEstadoViaje {
  estado: EstadoViaje;
  km_real?: number;
  fecha_llegada?: Date | string;
  notas?: string;
}

// ========================================
// INTERFACES DE GASTOS
// ========================================

/**
 * Gasto asociado a un viaje
 */
export interface GastoViaje extends BaseEntity {
  viaje_id: number;
  tipo: TipoGasto;
  monto_bs: number;
  descripcion?: string;
  comprobante_url?: string;
  fecha: Date | string;
  ubicacion?: string;
  // Propiedades formateadas
  readonly monto_formateado?: string;
  readonly tipo_label?: string;
}

/**
 * DTO para crear un gasto de viaje
 */
export interface GastoViajeCreate {
  tipo: TipoGasto;
  monto_bs: number;
  descripcion?: string;
  comprobante_url?: string;
  fecha: Date | string;
  ubicacion?: string;
}

/**
 * DTO para actualizar un gasto
 */
export interface GastoViajeUpdate {
  tipo?: TipoGasto;
  monto_bs?: number;
  descripcion?: string;
  comprobante_url?: string;
  fecha?: Date | string;
  ubicacion?: string;
}

// ========================================
// INTERFACES DE FILTROS Y ESTADÍSTICAS
// ========================================

/**
 * Filtros para búsqueda de viajes
 */
export interface ViajeFilters extends PaginationParams {
  search?: string;
  estado?: EstadoViaje | EstadoViaje[];
  cliente_id?: number;
  vehiculo_id?: number;
  chofer_id?: number;
  tipo_carga?: TipoCarga;
  tarifa_tipo?: TipoTarifa;
  origen?: string;
  destino?: string;
  fecha_desde?: Date | string;
  fecha_hasta?: Date | string;
  rango_fechas?: DateRange;
  km_minimo?: number;
  km_maximo?: number;
  ingreso_minimo?: number;
  ingreso_maximo?: number;
  ordenar_por?: 'fecha_salida' | 'ingreso_total_bs' | 'margen_bruto_bs' | 'km_real';
  direccion?: 'asc' | 'desc';
}

/**
 * Estadísticas generales de viajes
 */
export interface ViajeStats {
  total_viajes: number;
  viajes_por_estado: Record<EstadoViaje, number>;
  viajes_planificados: number;
  viajes_en_ruta: number;
  viajes_entregados: number;
  viajes_liquidados: number;
  km_totales: number;
  km_promedio: number;
  peso_total_ton: number;
  ingresos_totales_bs: number;
  gastos_totales_bs: number;
  margen_bruto_total_bs: number;
  margen_promedio_bs: number;
  rentabilidad_porcentaje: number;
  viajes_ultimo_mes: number;
  ingresos_ultimo_mes_bs: number;
  tendencia_mensual: number; // Porcentaje de cambio vs mes anterior
}

/**
 * Estadísticas por ruta
 */
export interface RutaStats {
  origen: string;
  destino: string;
  ruta_completa: string;
  cantidad_viajes: number;
  km_promedio: number;
  ingreso_promedio_bs: number;
  gasto_promedio_bs: number;
  margen_promedio_bs: number;
  ultimo_viaje: Date | string;
}

/**
 * Resumen mensual de viajes
 */
export interface ResumenMensualViajes {
  mes: string;
  anio: number;
  cantidad_viajes: number;
  km_totales: number;
  ingresos_bs: number;
  gastos_bs: number;
  margen_bs: number;
  rentabilidad_porcentaje: number;
}

/**
 * Resumen de gastos por tipo
 */
export interface ResumenGastosPorTipo {
  tipo: TipoGasto;
  tipo_label: string;
  cantidad: number;
  total_bs: number;
  promedio_bs: number;
  porcentaje: number;
}

// ========================================
// CONSTANTES - Re-exportadas de common.types
// ========================================

export { TIPOS_CARGA, TIPOS_TARIFA, TIPOS_GASTO, ESTADOS_VIAJE } from './common.types';
