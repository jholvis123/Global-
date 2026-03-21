// ========================================
// TIPOS COMUNES Y ENUMERACIONES
// Sistema de Gestión de Transporte SRL
// ========================================

// Estados generales
export type EstadoGeneral = 'ACTIVO' | 'INACTIVO';
export type EstadoUsuario = 'ACTIVO' | 'INACTIVO' | 'BLOQUEADO';
export type EstadoChofer = 'ACTIVO' | 'INACTIVO' | 'SUSPENDIDO' | 'EN_VIAJE' | 'DESCANSO';
export type EstadoVehiculo = 'ACTIVO' | 'EN_MANTENIMIENTO' | 'INACTIVO' | 'BAJA';
export type EstadoViaje = 'PLANIFICADO' | 'EN_RUTA' | 'ENTREGADO' | 'LIQUIDADO' | 'CANCELADO';
export type EstadoLiquidacion = 'PENDIENTE' | 'APROBADA' | 'PAGADA';
export type EstadoAnticipo = 'PENDIENTE' | 'LIQUIDADO';

// Tipos de tarifa
export type TipoTarifa = 'KM' | 'TON' | 'FIJA';

// Tipos de gasto
export type TipoGasto = 'COMBUSTIBLE' | 'PEAJE' | 'VIATICO' | 'TALLER' | 'REPUESTO' | 'OTRO';

// Tipos de carga
export type TipoCarga = 'CARGA_GENERAL' | 'MINERALES' | 'CEMENTO' | 'GRANOS' | 'COMBUSTIBLE' | 'MAQUINARIA' | 'CONTENEDOR' | 'CARGA_PELIGROSA' | 'OTRO';

// Tipos de mantenimiento
export type TipoMantenimiento = 'PREVENTIVO' | 'CORRECTIVO' | 'EMERGENCIA';

// Tipos de participación
export type TipoParticipacion = 'NETO' | 'BRUTO';

// Categorías de licencia
export type CategoriaLicencia = 'A' | 'B' | 'C' | 'P' | 'M' | 'T';

// Roles del sistema
export type RolUsuario = 'ADMINISTRADOR' | 'OPERACIONES' | 'FINANZAS' | 'SOCIO' | 'CHOFER';

// Tipos de combustible
export type TipoCombustible = 'DIESEL' | 'GASOLINA' | 'GNV';

// Interface base para entidades
export interface BaseEntity {
  id: number;
  created_at?: Date | string;
  updated_at?: Date | string;
  deleted_at?: Date | string;
}

// Interface para entidades con soft delete
export interface SoftDeleteEntity extends BaseEntity {
  deleted_at?: Date | string;
}

// Interface para entidades con estado
export interface StatefulEntity<T = EstadoGeneral> extends BaseEntity {
  estado: T;
}

// Interface para filtros de paginación
export interface PaginationParams {
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

// Interface para filtros con búsqueda
export interface SearchParams extends PaginationParams {
  search?: string;
}

// Interface para rangos de fechas
export interface DateRange {
  desde?: Date | string;
  hasta?: Date | string;
}

// Interface para filtros comunes
export interface CommonFilters extends SearchParams, DateRange {
  estado?: string;
}

// Constantes de estados con labels para UI
export const ESTADOS_VIAJE: { value: EstadoViaje; label: string; color: string; icon: string }[] = [
  { value: 'PLANIFICADO', label: 'Planificado', color: 'info', icon: 'schedule' },
  { value: 'EN_RUTA', label: 'En Ruta', color: 'primary', icon: 'local_shipping' },
  { value: 'ENTREGADO', label: 'Entregado', color: 'success', icon: 'check_circle' },
  { value: 'LIQUIDADO', label: 'Liquidado', color: 'accent', icon: 'paid' },
  { value: 'CANCELADO', label: 'Cancelado', color: 'warn', icon: 'cancel' }
];

export const ESTADOS_VEHICULO: { value: EstadoVehiculo; label: string; color: string; icon: string }[] = [
  { value: 'ACTIVO', label: 'Activo', color: 'success', icon: 'check_circle' },
  { value: 'EN_MANTENIMIENTO', label: 'En Mantenimiento', color: 'warning', icon: 'build' },
  { value: 'INACTIVO', label: 'Inactivo', color: 'default', icon: 'pause_circle' },
  { value: 'BAJA', label: 'De Baja', color: 'error', icon: 'cancel' }
];

export const ESTADOS_CHOFER: { value: EstadoChofer; label: string; color: string; icon: string }[] = [
  { value: 'ACTIVO', label: 'Activo', color: 'success', icon: 'check_circle' },
  { value: 'EN_VIAJE', label: 'En Viaje', color: 'primary', icon: 'local_shipping' },
  { value: 'DESCANSO', label: 'Descanso', color: 'info', icon: 'hotel' },
  { value: 'SUSPENDIDO', label: 'Suspendido', color: 'warning', icon: 'warning' },
  { value: 'INACTIVO', label: 'Inactivo', color: 'default', icon: 'pause_circle' }
];

export const TIPOS_TARIFA: { value: TipoTarifa; label: string; unidad: string }[] = [
  { value: 'KM', label: 'Por Kilómetro', unidad: 'Bs/km' },
  { value: 'TON', label: 'Por Tonelada', unidad: 'Bs/ton' },
  { value: 'FIJA', label: 'Tarifa Fija', unidad: 'Bs' }
];

export const TIPOS_GASTO: { value: TipoGasto; label: string; icon: string }[] = [
  { value: 'COMBUSTIBLE', label: 'Combustible', icon: 'local_gas_station' },
  { value: 'PEAJE', label: 'Peaje', icon: 'toll' },
  { value: 'VIATICO', label: 'Viático', icon: 'restaurant' },
  { value: 'TALLER', label: 'Taller', icon: 'build' },
  { value: 'REPUESTO', label: 'Repuesto', icon: 'settings' },
  { value: 'OTRO', label: 'Otro', icon: 'receipt' }
];

export const CATEGORIAS_LICENCIA: { value: CategoriaLicencia; label: string }[] = [
  { value: 'A', label: 'Categoría A - Motocicletas' },
  { value: 'B', label: 'Categoría B - Automóviles' },
  { value: 'C', label: 'Categoría C - Camiones' },
  { value: 'P', label: 'Profesional - Transporte Pesado' },
  { value: 'M', label: 'Categoría M - Maquinaria' },
  { value: 'T', label: 'Categoría T - Especial' }
];

export const TIPOS_CARGA: { value: TipoCarga; label: string; icon: string }[] = [
  { value: 'CARGA_GENERAL', label: 'Carga General', icon: 'inventory_2' },
  { value: 'MINERALES', label: 'Minerales', icon: 'terrain' },
  { value: 'CEMENTO', label: 'Cemento', icon: 'foundation' },
  { value: 'GRANOS', label: 'Granos', icon: 'grass' },
  { value: 'COMBUSTIBLE', label: 'Combustible', icon: 'local_gas_station' },
  { value: 'MAQUINARIA', label: 'Maquinaria', icon: 'precision_manufacturing' },
  { value: 'CONTENEDOR', label: 'Contenedor', icon: 'inventory' },
  { value: 'CARGA_PELIGROSA', label: 'Carga Peligrosa', icon: 'warning' },
  { value: 'OTRO', label: 'Otro', icon: 'category' }
];

export const MARCAS_VEHICULO: string[] = [
  'Volvo',
  'Scania',
  'Mercedes-Benz',
  'MAN',
  'Iveco',
  'DAF',
  'Kenworth',
  'Freightliner',
  'International',
  'Hino',
  'Otro'
];

// Ciudades de Bolivia
export const CIUDADES_BOLIVIA: string[] = [
  'Santa Cruz',
  'La Paz',
  'Cochabamba',
  'Oruro',
  'Potosí',
  'Tarija',
  'Sucre',
  'Trinidad',
  'Cobija',
  'Yacuiba',
  'Villamontes',
  'Montero',
  'Warnes'
];
