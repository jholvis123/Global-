import { BaseEntity, EstadoGeneral } from './common.types';

// ========================================
// INTERFACES DE CLIENTE
// ========================================

export interface Cliente extends BaseEntity {
  razon_social: string;
  nombre_comercial?: string;
  nit?: string;
  rubro?: string;
  // Contacto principal
  contacto_nombre?: string;
  contacto_telefono?: string;
  contacto_email?: string;
  contacto_cargo?: string;
  // Ubicación
  direccion?: string;
  ciudad?: string;
  departamento?: string;
  // Facturación
  email_facturacion?: string;
  telefono_facturacion?: string;
  // Estado
  estado: EstadoGeneral;
  usuario_id?: number;
  // Computed
  total_viajes?: number;
  ingresos_generados?: number;
  ultimo_viaje?: Date;
}

/**
 * Versión resumida del cliente para listados y referencias
 */
export interface ClienteBasico {
  id: number;
  razon_social: string;
  nombre_comercial?: string;
  nit?: string;
  ciudad?: string;
  estado: EstadoGeneral;
}

export interface ClienteCreate {
  razon_social: string;
  nombre_comercial?: string;
  nit?: string;
  rubro?: string;
  contacto_nombre?: string;
  contacto_telefono?: string;
  contacto_email?: string;
  contacto_cargo?: string;
  direccion?: string;
  ciudad?: string;
  departamento?: string;
  email_facturacion?: string;
  telefono_facturacion?: string;
}

export interface ClienteUpdate extends Partial<ClienteCreate> {
  estado?: EstadoGeneral;
}

export interface ClienteFilters {
  search?: string;
  estado?: EstadoGeneral;
  ciudad?: string;
  rubro?: string;
}

export interface ClienteStats {
  total: number;
  activos: number;
  inactivos: number;
  con_viajes_mes: number;
}

