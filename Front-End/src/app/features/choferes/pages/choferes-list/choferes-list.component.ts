import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { ChoferesService } from '../../services/choferes.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { Chofer } from '../../../../models';

@Component({
  selector: 'app-choferes-list',
  templateUrl: './choferes-list.component.html',
  styleUrls: ['./choferes-list.component.scss']
})
export class ChoferesListComponent implements OnInit, AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  displayedColumns = ['nombre', 'ci', 'licencia', 'telefono', 'experiencia', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<Chofer>([]);
  selectedEstado = '';
  isLoading = false;
  totalRecords = 0;
  pageSize = 20;
  currentPage = 1;

  stats = { total: 0, disponibles: 0, enViaje: 0, licenciasVencer: 0 };

  constructor(
    public router: Router,
    private choferesService: ChoferesService,
    private notification: NotificationService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void { this.loadChoferes(); }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
  }

  loadChoferes(): void {
    this.isLoading = true;
    const params: any = { page: this.currentPage, limit: this.pageSize };
    if (this.selectedEstado) params.estado = this.selectedEstado;

    this.choferesService.getAll(params).subscribe({
      next: (response) => {
        this.dataSource.data = response.data;
        this.totalRecords = response.total;
        this.updateStats(response.data);
        this.isLoading = false;
      },
      error: () => {
        this.notification.error('Error al cargar choferes');
        this.isLoading = false;
      }
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadChoferes();
  }

  updateStats(choferes: Chofer[]): void {
    this.stats = {
      total: this.totalRecords,
      disponibles: choferes.filter(c => c.estado === 'ACTIVO').length,
      enViaje: choferes.filter(c => c.estado === 'EN_VIAJE').length,
      licenciasVencer: choferes.filter(c => this.isLicenciaProximaVencer(c) || this.isLicenciaVencida(c)).length
    };
  }

  getInitials(nombre: string, apellido: string): string {
    return `${nombre?.charAt(0) || ''}${apellido?.charAt(0) || ''}`.toUpperCase();
  }

  getEstadoIcon(estado: string): string {
    const icons: { [key: string]: string } = {
      'ACTIVO': 'check_circle', 'EN_VIAJE': 'local_shipping',
      'DESCANSO': 'hotel', 'INACTIVO': 'cancel'
    };
    return icons[estado] || 'help';
  }

  getEstadoLabel(estado: string): string {
    const labels: { [key: string]: string } = {
      'ACTIVO': 'Disponible', 'EN_VIAJE': 'En Ruta',
      'DESCANSO': 'Descanso', 'INACTIVO': 'Inactivo'
    };
    return labels[estado] || estado;
  }

  cambiarEstado(chofer: Chofer, estado: string): void {
    this.choferesService.update(chofer.id, { estado } as any).subscribe({
      next: () => {
        chofer.estado = estado as any;
        this.notification.success(`Estado de ${chofer.nombre} actualizado`);
        this.updateStats(this.dataSource.data);
      },
      error: () => this.notification.error('Error al actualizar estado')
    });
  }

  isLicenciaProximaVencer(chofer: Chofer): boolean {
    const vencimiento = new Date(chofer.licencia_vencimiento);
    const hoy = new Date();
    const diasRestantes = Math.ceil((vencimiento.getTime() - hoy.getTime()) / (1000 * 60 * 60 * 24));
    return diasRestantes > 0 && diasRestantes <= 30;
  }

  isLicenciaVencida(chofer: Chofer): boolean {
    return new Date(chofer.licencia_vencimiento) < new Date();
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  filterByEstado(): void {
    this.currentPage = 1;
    this.loadChoferes();
  }

  clearFilters(): void {
    this.selectedEstado = '';
    this.currentPage = 1;
    this.loadChoferes();
  }

  deleteChofer(chofer: Chofer): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Eliminar Chofer',
        message: `¿Está seguro de eliminar a ${chofer.nombre} ${chofer.apellido}?`,
        confirmText: 'Eliminar'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.choferesService.delete(chofer.id).subscribe({
          next: () => {
            this.notification.success('Chofer eliminado');
            this.loadChoferes();
          },
          error: () => this.notification.error('Error al eliminar chofer')
        });
      }
    });
  }
}
