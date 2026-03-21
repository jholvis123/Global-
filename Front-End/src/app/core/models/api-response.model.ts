/**
 * Interfaces de respuesta de la API
 */

// Respuesta paginada genérica
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

// Respuesta de datos genérica
export interface DataResponse<T> {
  data: T;
  message?: string;
}

// Respuesta de éxito simple
export interface SuccessResponse {
  success: boolean;
  message: string;
}

// Respuesta de error
export interface ErrorResponse {
  detail: string;
  code?: string;
}

// Parámetros de paginación
export interface PaginationParams {
  page?: number;
  limit?: number;
}

// Parámetros de filtro base
export interface FilterParams extends PaginationParams {
  estado?: string;
  busqueda?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}
