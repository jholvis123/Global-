import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { NotificationService } from '../../../../core/services/notification.service';
import { ExportService } from '../../../../core/services/export.service';
import { AnticiposService, Anticipo } from '../../services/anticipos.service';

@Component({
  selector: 'app-anticipos-list',
  templateUrl: './anticipos-list.component.html',
  styleUrls: ['./anticipos-list.component.scss']
})
export class AnticiposListComponent implements OnInit {
  displayedColumns: string[] = ['id', 'chofer', 'monto', 'fecha', 'motivo', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<Anticipo>([]);
  isLoading = true;
  selectedStatus = '';
  searchQuery = '';
  totalRecords = 0;
  pageSize = 20;
  currentPage = 1;

  stats = { total: 0, pendientes: 0, aprobados: 0, montoTotal: 0 };

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private dialog: MatDialog,
    private notification: NotificationService,
    private exportService: ExportService,
    private anticiposService: AnticiposService
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.isLoading = true;
    const params: any = { page: this.currentPage, limit: this.pageSize };
    if (this.selectedStatus) params.estado = this.selectedStatus;

    this.anticiposService.getAll(params).subscribe({
      next: (response) => {
        this.dataSource.data = response.data;
        this.totalRecords = response.total;
        this.dataSource.sort = this.sort;
        this.calculateStats(response.data);
        this.isLoading = false;
      },
      error: () => {
        this.notification.error('Error al cargar anticipos');
        this.isLoading = false;
      }
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadData();
  }

  calculateStats(anticipos: Anticipo[]): void {
    this.stats.total = this.totalRecords;
    this.stats.pendientes = anticipos.filter(a => a.estado === 'PENDIENTE').length;
    this.stats.aprobados = anticipos.filter(a => a.estado === 'APROBADO').length;
    this.stats.montoTotal = anticipos
      .filter(a => a.estado === 'APROBADO' || a.estado === 'DESCONTADO')
      .reduce((sum, a) => sum + a.monto_bs, 0);
  }

  applyFilter(): void {
    this.currentPage = 1;
    this.loadData();
  }

  clearFilters(): void {
    this.selectedStatus = '';
    this.searchQuery = '';
    this.currentPage = 1;
    this.loadData();
  }

  delete(anticipo: Anticipo): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Eliminar Anticipo',
        message: `¿Está seguro de eliminar este anticipo?`,
        confirmText: 'Eliminar',
        type: 'warn'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.anticiposService.delete(anticipo.id).subscribe({
          next: () => {
            this.notification.success('Anticipo eliminado correctamente');
            this.loadData();
          },
          error: () => this.notification.error('Error al eliminar anticipo')
        });
      }
    });
  }

  exportToExcel(): void {
    this.exportService.exportToExcel(this.dataSource.data, 'Anticipos');
  }

  exportToPDF(): void {
    this.exportService.exportToPDF(this.dataSource.data, 'Anticipos', 'Listado de Anticipos');
  }

  getStatusClass(estado: string): string {
    const classes: { [key: string]: string } = {
      'PENDIENTE': 'status--pending',
      'APROBADO': 'status--success',
      'RECHAZADO': 'status--error',
      'DESCONTADO': 'status--info'
    };
    return classes[estado] || '';
  }

  getInitials(name: string): string {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  }

  aprobar(anticipo: Anticipo): void {
    this.anticiposService.aprobar(anticipo.id).subscribe({
      next: () => {
        this.notification.success('Anticipo aprobado correctamente');
        this.loadData();
      },
      error: () => this.notification.error('Error al aprobar anticipo')
    });
  }

  rechazar(anticipo: Anticipo): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Rechazar Anticipo',
        message: '¿Está seguro de rechazar este anticipo?',
        confirmText: 'Rechazar',
        type: 'warn'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.anticiposService.rechazar(anticipo.id).subscribe({
          next: () => {
            this.notification.success('Anticipo rechazado');
            this.loadData();
          },
          error: () => this.notification.error('Error al rechazar anticipo')
        });
      }
    });
  }
}
