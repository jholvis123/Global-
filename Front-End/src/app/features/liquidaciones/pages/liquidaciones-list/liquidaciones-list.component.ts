import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { ExportService } from '../../../../core/services/export.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { LiquidacionesService, Liquidacion } from '../../services/liquidaciones.service';

@Component({
  selector: 'app-liquidaciones-list',
  templateUrl: './liquidaciones-list.component.html',
  styleUrls: ['./liquidaciones-list.component.scss']
})
export class LiquidacionesListComponent implements OnInit {
  displayedColumns: string[] = ['id', 'viaje', 'ingresos', 'gastos', 'neto', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<Liquidacion>([]);
  isLoading = true;
  selectedStatus = '';
  totalRecords = 0;
  pageSize = 20;
  currentPage = 1;

  stats = { total: 0, pendientes: 0, pagadas: 0, montoTotal: 0 };

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private exportService: ExportService,
    private notification: NotificationService,
    private liquidacionesService: LiquidacionesService
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.isLoading = true;
    const params: any = { page: this.currentPage, limit: this.pageSize };
    if (this.selectedStatus) params.estado = this.selectedStatus;

    this.liquidacionesService.getAll(params).subscribe({
      next: (response) => {
        this.dataSource.data = response.data;
        this.totalRecords = response.total;
        this.dataSource.sort = this.sort;
        this.calculateStats(response.data);
        this.isLoading = false;
      },
      error: () => {
        this.notification.error('Error al cargar liquidaciones');
        this.isLoading = false;
      }
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadData();
  }

  calculateStats(liquidaciones: Liquidacion[]): void {
    this.stats.total = this.totalRecords;
    this.stats.pendientes = liquidaciones.filter(l => l.estado === 'PENDIENTE').length;
    this.stats.pagadas = liquidaciones.filter(l => l.estado === 'PAGADA').length;
    this.stats.montoTotal = liquidaciones
      .filter(l => l.estado === 'PAGADA')
      .reduce((sum, l) => sum + l.neto_pagar_bs, 0);
  }

  filterByStatus(): void {
    this.currentPage = 1;
    this.loadData();
  }

  exportToExcel(): void {
    this.exportService.exportToExcel(this.dataSource.data, 'Liquidaciones');
  }

  exportToPDF(): void {
    this.exportService.exportToPDF(this.dataSource.data, 'Liquidaciones', 'Listado de Liquidaciones');
  }

  getStatusClass(estado: string): string {
    const classes: { [key: string]: string } = {
      'PENDIENTE': 'status--pending',
      'PROCESADA': 'status--info',
      'PAGADA': 'status--success',
      'ANULADA': 'status--error'
    };
    return classes[estado] || '';
  }

  getInitials(name: string): string {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  }
}
