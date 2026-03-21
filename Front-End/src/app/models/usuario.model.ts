import { BaseEntity, EstadoUsuario, RolUsuario } from './common.types';

// ========================================
// INTERFACES DE USUARIO
// ========================================

export interface Usuario extends BaseEntity {
  email: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  estado: EstadoUsuario;
  roles: RolUsuario[] | string[];
  intentos_fallidos: number;
  ultimo_login?: Date;
  // Computed
  nombre_completo?: string;
  avatar_url?: string;
}

export interface UsuarioCreate {
  email: string;
  password: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  estado?: EstadoUsuario;
  roles: RolUsuario[] | string[];
}

export interface UsuarioUpdate {
  nombre?: string;
  apellido?: string;
  telefono?: string;
  estado?: EstadoUsuario;
  password?: string;
  roles?: RolUsuario[] | string[];
}

export interface LoginRequest {
  email: string;
  password: string;
  remember_me?: boolean;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  usuario: Usuario;
}

export interface ChangePasswordRequest {
  password_actual: string;
  password_nueva: string;
  confirmar_password?: string;
}

export interface ResetPasswordRequest {
  email: string;
}

export interface Rol {
  id: number;
  nombre: RolUsuario | string;
  descripcion?: string;
  permisos?: string[];
}

export interface SessionInfo {
  usuario: Usuario;
  token_expires_at: Date;
  last_activity: Date;
}

