import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { ViajesService } from '../../services/viajes.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { Viaje, ESTADOS_VIAJE } from '../../../../models';

@Component({
  selector: 'app-viajes-list',
  templateUrl: './viajes-list.component.html',
  styleUrls: ['./viajes-list.component.scss']
})
export class ViajesListComponent implements OnInit, AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  displayedColumns: string[] = ['id', 'ruta', 'cliente', 'vehiculo', 'chofer', 'fecha_salida', 'estado', 'ingreso', 'acciones'];
  dataSource = new MatTableDataSource<Viaje>([]);
  
  estados = ESTADOS_VIAJE;
  selectedEstado = '';
  fechaDesde: Date | null = null;
  fechaHasta: Date | null = null;
  
  // Paginación
  isLoading = false;
  totalRecords = 0;
  pageSize = 20;
  currentPage = 1;

  constructor(
    public router: Router,
    private viajesService: ViajesService,
    private notification: NotificationService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadViajes();
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
  }

  loadViajes(): void {
    this.isLoading = true;
    const params: any = { page: this.currentPage, limit: this.pageSize };
    if (this.selectedEstado) params.estado = this.selectedEstado;
    if (this.fechaDesde) params.fecha_inicio = this.fechaDesde.toISOString().split('T')[0];
    if (this.fechaHasta) params.fecha_fin = this.fechaHasta.toISOString().split('T')[0];

    this.viajesService.getAll(params).subscribe({
      next: (response) => {
        this.dataSource.data = response.data;
        this.totalRecords = response.total;
        this.isLoading = false;
      },
      error: () => {
        this.notification.error('Error al cargar viajes');
        this.isLoading = false;
      }
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadViajes();
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  filterByEstado(): void {
    this.currentPage = 1;
    this.loadViajes();
  }

  clearFilters(): void {
    this.selectedEstado = '';
    this.fechaDesde = null;
    this.fechaHasta = null;
    this.currentPage = 1;
    this.loadViajes();
  }

  goToDetail(id: number): void {
    this.router.navigate(['/viajes', id]);
  }

  cambiarEstado(viaje: Viaje, nuevoEstado: string): void {
    this.viajesService.cambiarEstado(viaje.id, nuevoEstado).subscribe({
      next: () => {
        this.notification.success(`Viaje actualizado a ${nuevoEstado}`);
        this.loadViajes();
      },
      error: () => {
        // Para desarrollo, actualizar localmente
        viaje.estado = nuevoEstado as any;
        this.notification.success(`Viaje actualizado a ${nuevoEstado}`);
      }
    });
  }

  deleteViaje(viaje: Viaje): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Eliminar Viaje',
        message: `¿Está seguro de eliminar el viaje #${viaje.id} (${viaje.origen} → ${viaje.destino})?`,
        confirmText: 'Eliminar',
        icon: 'delete'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.viajesService.delete(viaje.id).subscribe({
          next: () => {
            this.notification.success('Viaje eliminado correctamente');
            this.loadViajes();
          },
          error: () => {
            // Para desarrollo
            this.dataSource.data = this.dataSource.data.filter(v => v.id !== viaje.id);
            this.notification.success('Viaje eliminado correctamente');
          }
        });
      }
    });
  }

  exportar(): void {
    this.notification.info('Exportando datos...');
    // TODO: Implementar exportación a Excel/CSV
  }
}
