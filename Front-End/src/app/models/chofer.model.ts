import { BaseEntity, EstadoChofer, CategoriaLicencia } from './common.types';

// ========================================
// INTERFACES DE CHOFER
// ========================================

export interface Chofer extends BaseEntity {
  nombre: string;
  apellido: string;
  ci: string;
  fecha_nacimiento?: Date;
  // Licencia
  licencia_numero: string;
  licencia_categoria: CategoriaLicencia | string;
  licencia_vencimiento: Date;
  // Contacto
  telefono?: string;
  direccion?: string;
  email?: string;
  // Contacto emergencia
  contacto_emergencia_nombre?: string;
  contacto_emergencia_telefono?: string;
  // Experiencia
  experiencia_anos: number;
  fecha_ingreso?: Date;
  // Estado
  estado: EstadoChofer;
  usuario_id?: number;
  observaciones?: string;
  // Computed
  nombre_completo?: string;
  licencia_vigente?: boolean;
  dias_para_vencer_licencia?: number;
  edad?: number;
  viajes_realizados?: number;
}

/**
 * Versión resumida del chofer para listados y referencias
 */
export interface ChoferBasico {
  id: number;
  nombre: string;
  apellido: string;
  nombre_completo?: string;
  ci: string;
  licencia_categoria: CategoriaLicencia | string;
  telefono?: string;
  estado: EstadoChofer;
}

export interface ChoferCreate {
  nombre: string;
  apellido: string;
  ci: string;
  fecha_nacimiento?: Date | string;
  licencia_numero: string;
  licencia_categoria: CategoriaLicencia | string;
  licencia_vencimiento: Date | string;
  telefono?: string;
  direccion?: string;
  email?: string;
  contacto_emergencia_nombre?: string;
  contacto_emergencia_telefono?: string;
  experiencia_anos?: number;
  fecha_ingreso?: Date | string;
  observaciones?: string;
}

export interface ChoferUpdate extends Partial<ChoferCreate> {
  estado?: EstadoChofer;
}

export interface ChoferFilters {
  search?: string;
  estado?: EstadoChofer;
  licencia_categoria?: CategoriaLicencia | string;
  licencia_por_vencer?: boolean;
  disponible?: boolean;
}

export interface ChoferStats {
  total: number;
  activos: number;
  enViaje: number;
  descanso: number;
  licenciasPorVencer: number;
}

