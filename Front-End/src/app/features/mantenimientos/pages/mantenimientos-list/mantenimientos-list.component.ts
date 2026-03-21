import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { Router } from '@angular/router';
import { MantenimientosService, Mantenimiento } from '../../services/mantenimientos.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { ExportService } from '../../../../core/services/export.service';

@Component({
  selector: 'app-mantenimientos-list',
  templateUrl: './mantenimientos-list.component.html',
  styleUrls: ['./mantenimientos-list.component.scss']
})
export class MantenimientosListComponent implements OnInit {
  displayedColumns: string[] = ['vehiculo', 'tipo', 'fechaProgramada', 'kilometraje', 'costo', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<Mantenimiento>([]);
  
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  // Filtros y paginación
  searchText = '';
  filtroTipo = '';
  filtroEstado = '';
  filtroPrioridad = '';
  isLoading = false;
  totalRecords = 0;
  pageSize = 20;
  currentPage = 1;

  // Stats
  stats = { programados: 0, enProceso: 0, completados: 0, vencidos: 0, costoMensual: 0 };

  tipos = ['PREVENTIVO', 'CORRECTIVO', 'PREDICTIVO'];
  estados = ['PROGRAMADO', 'EN_PROCESO', 'COMPLETADO', 'CANCELADO'];
  prioridades = ['BAJA', 'MEDIA', 'ALTA', 'URGENTE'];

  constructor(
    private router: Router,
    private mantenimientosService: MantenimientosService,
    private notification: NotificationService,
    private exportService: ExportService
  ) {}

  ngOnInit(): void {
    this.loadMantenimientos();
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
  }

  loadMantenimientos(): void {
    this.isLoading = true;
    const params: any = { page: this.currentPage, limit: this.pageSize };
    if (this.filtroTipo) params.tipo = this.filtroTipo;
    if (this.filtroEstado) params.estado = this.filtroEstado;

    this.mantenimientosService.getAll(params).subscribe({
      next: (response) => {
        this.dataSource.data = response.data;
        this.totalRecords = response.total;
        this.calculateStats(response.data);
        this.isLoading = false;
      },
      error: () => {
        this.notification.error('Error al cargar mantenimientos');
        this.isLoading = false;
      }
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadMantenimientos();
  }

  calculateStats(data: Mantenimiento[]): void {
    this.stats.programados = data.filter(m => m.estado === 'PROGRAMADO').length;
    this.stats.enProceso = data.filter(m => m.estado === 'EN_PROCESO').length;
    this.stats.completados = data.filter(m => m.estado === 'COMPLETADO').length;
    this.stats.costoMensual = data.reduce((sum, m) => sum + (m.costo_bs || 0), 0);
  }

  applyFilter(): void {
    this.currentPage = 1;
    this.loadMantenimientos();
  }

  clearFilters(): void {
    this.searchText = '';
    this.filtroTipo = '';
    this.filtroEstado = '';
    this.filtroPrioridad = '';
    this.currentPage = 1;
    this.loadMantenimientos();
  }

  nuevoMantenimiento(): void {
    this.router.navigate(['/app/mantenimientos/nuevo']);
  }

  verDetalle(mantenimiento: Mantenimiento): void {
    this.router.navigate(['/app/mantenimientos/detalle', mantenimiento.id]);
  }

  editarMantenimiento(mantenimiento: Mantenimiento): void {
    this.router.navigate(['/app/mantenimientos/editar', mantenimiento.id]);
  }

  eliminarMantenimiento(mantenimiento: Mantenimiento): void {
    if (confirm('¿Está seguro de eliminar este mantenimiento?')) {
      // Implementar eliminación via API si es necesario
      this.notification.info('Funcionalidad en desarrollo');
    }
  }

  getEstadoClass(estado: string): string {
    const classes: { [key: string]: string } = {
      'PROGRAMADO': 'status-scheduled', 'EN_PROCESO': 'status-process',
      'COMPLETADO': 'status-completed', 'CANCELADO': 'status-cancelled'
    };
    return classes[estado] || 'status-scheduled';
  }

  getEstadoLabel(estado: string): string {
    const labels: { [key: string]: string } = {
      'PROGRAMADO': 'Programado', 'EN_PROCESO': 'En Proceso',
      'COMPLETADO': 'Completado', 'CANCELADO': 'Cancelado'
    };
    return labels[estado] || estado;
  }

  getPrioridadClass(prioridad: string): string {
    const classes: { [key: string]: string } = {
      'BAJA': 'priority-low', 'MEDIA': 'priority-medium',
      'ALTA': 'priority-high', 'URGENTE': 'priority-urgent'
    };
    return classes[prioridad] || 'priority-medium';
  }

  getPrioridadLabel(prioridad: string): string {
    const labels: { [key: string]: string } = {
      'BAJA': 'Baja', 'MEDIA': 'Media',
      'ALTA': 'Alta', 'URGENTE': 'Urgente'
    };
    return labels[prioridad] || prioridad;
  }

  exportToExcel(): void {
    this.exportService.exportToExcel(this.dataSource.data, 'Mantenimientos');
  }

  exportToPDF(): void {
    this.exportService.exportToPDF(this.dataSource.data, 'Mantenimientos', 'Listado de Mantenimientos');
  }
}
