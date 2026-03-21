import { EstadoViaje, TipoCarga } from './common.types';

// ========================================
// INTERFACES DE RESPUESTA API
// ========================================

/**
 * Respuesta genérica de API
 */
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
  timestamp?: string;
}

/**
 * Respuesta paginada de API
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

/**
 * Error de API
 */
export interface ApiError {
  error: boolean;
  message: string;
  status_code: number;
  correlation_id?: string;
  errors?: ValidationError[];
  timestamp?: string;
}

/**
 * Error de validación individual
 */
export interface ValidationError {
  field: string;
  message: string;
  code?: string;
}

// ========================================
// INTERFACES DE DASHBOARD
// ========================================

/**
 * Estadísticas principales del Dashboard
 */
export interface DashboardStats {
  // Viajes
  total_viajes: number;
  viajes_en_ruta: number;
  viajes_planificados: number;
  viajes_entregados?: number;
  viajes_por_estado?: Record<EstadoViaje, number>;
  
  // Financiero
  ingresos_mes: number;
  gastos_mes: number;
  ganancia_mes: number;
  rentabilidad: number;
  ingresos_formateados?: string;
  gastos_formateados?: string;
  ganancia_formateada?: string;
  
  // Comparación con mes anterior
  variacion_ingresos?: number;
  variacion_gastos?: number;
  variacion_ganancia?: number;
  tendencia?: 'UP' | 'DOWN' | 'STABLE';
  
  // Recursos
  vehiculos_activos: number;
  vehiculos_totales?: number;
  choferes_activos: number;
  choferes_totales?: number;
  socios_activos?: number;
  clientes_activos?: number;
  
  // Alertas
  documentos_por_vencer: number;
  licencias_por_vencer: number;
  mantenimientos_pendientes?: number;
  anticipos_pendientes?: number;
}

/**
 * Alertas del sistema para el Dashboard
 */
export interface DashboardAlerta {
  id: number;
  tipo: 'DOCUMENTO' | 'LICENCIA' | 'MANTENIMIENTO' | 'ANTICIPO' | 'VIAJE';
  prioridad: 'BAJA' | 'MEDIA' | 'ALTA' | 'URGENTE';
  titulo: string;
  descripcion: string;
  entidad_id: number;
  entidad_tipo: string;
  fecha_vencimiento?: Date | string;
  dias_restantes?: number;
  accion_url?: string;
}

/**
 * KPI (Key Performance Indicator) para widgets
 */
export interface DashboardKPI {
  id: string;
  titulo: string;
  valor: number | string;
  valor_formateado: string;
  unidad?: string;
  icono: string;
  color: 'primary' | 'accent' | 'warn' | '';
  variacion?: number;
  tendencia?: 'UP' | 'DOWN' | 'STABLE';
  enlace?: string;
}

// ========================================
// INTERFACES DE REPORTES
// ========================================

/**
 * Reporte diario de operaciones
 */
export interface ReporteDiario {
  fecha: Date | string;
  total_viajes: number;
  ingresos_bs: number;
  gastos_bs: number;
  ganancia_bs: number;
  rentabilidad_porcentaje: number;
  viajes_por_estado: Record<EstadoViaje, number>;
  tipos_carga: Record<TipoCarga, number>;
  km_totales: number;
  peso_total_ton: number;
}

/**
 * Reporte mensual de operaciones
 */
export interface ReporteMensual {
  anio: number;
  mes: number;
  nombre_mes: string;
  total_viajes: number;
  ingresos_bs: number;
  gastos_bs: number;
  ganancia_bs: number;
  rentabilidad_porcentaje: number;
  dias_laborables: number;
  promedio_diario_bs: number;
  km_totales: number;
  peso_total_ton: number;
  viajes_por_estado: Record<EstadoViaje, number>;
  comparacion_mes_anterior?: ComparacionMensual;
}

/**
 * Comparación con el mes anterior
 */
export interface ComparacionMensual {
  variacion_ingresos: number;
  variacion_gastos: number;
  variacion_ganancia: number;
  variacion_viajes: number;
  porcentaje_ingresos: number;
  porcentaje_gastos: number;
  porcentaje_ganancia: number;
}

/**
 * Reporte anual de operaciones
 */
export interface ReporteAnual {
  anio: number;
  total_viajes: number;
  ingresos_bs: number;
  gastos_bs: number;
  ganancia_bs: number;
  rentabilidad_porcentaje: number;
  mejor_mes: string;
  peor_mes: string;
  detalle_mensual: ReporteMensual[];
}

// ========================================
// INTERFACES DE GRÁFICAS
// ========================================

/**
 * Datos para gráficas (compatible con Chart.js)
 */
export interface ChartData {
  labels: string[];
  datasets: ChartDataset[];
}

/**
 * Dataset individual para gráfica
 */
export interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string | string[];
  borderColor?: string | string[];
  borderWidth?: number;
  fill?: boolean;
  tension?: number;
  type?: 'line' | 'bar' | 'pie' | 'doughnut';
}

/**
 * Configuración de gráfica
 */
export interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'doughnut' | 'radar';
  data: ChartData;
  options?: ChartOptions;
}

/**
 * Opciones de gráfica
 */
export interface ChartOptions {
  responsive?: boolean;
  maintainAspectRatio?: boolean;
  plugins?: {
    legend?: { display?: boolean; position?: string };
    title?: { display?: boolean; text?: string };
    tooltip?: { enabled?: boolean };
  };
  scales?: {
    x?: { display?: boolean; title?: { display?: boolean; text?: string } };
    y?: { display?: boolean; title?: { display?: boolean; text?: string }; beginAtZero?: boolean };
  };
}

// ========================================
// INTERFACES DE EXPORTACIÓN
// ========================================

/**
 * Configuración de exportación
 */
export interface ExportConfig {
  formato: 'PDF' | 'EXCEL' | 'CSV';
  incluir_graficas: boolean;
  rango_fechas: { desde: Date | string; hasta: Date | string };
  filtros?: Record<string, unknown>;
}

/**
 * Resultado de exportación
 */
export interface ExportResult {
  success: boolean;
  url?: string;
  filename?: string;
  message?: string;
  size_bytes?: number;
}
