import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { VehiculosService } from '../../services/vehiculos.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { Vehiculo } from '../../../../models';

@Component({
  selector: 'app-vehiculos-list',
  templateUrl: './vehiculos-list.component.html',
  styleUrls: ['./vehiculos-list.component.scss']
})
export class VehiculosListComponent implements OnInit, AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  displayedColumns = ['placa', 'marca', 'anio', 'capacidad', 'socio', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<Vehiculo>([]);
  selectedEstado = '';
  isLoading = false;
  totalRecords = 0;
  pageSize = 20;
  currentPage = 1;

  stats = { total: 0, activos: 0, enMantenimiento: 0, vencimientos: 0 };

  constructor(
    public router: Router,
    private vehiculosService: VehiculosService,
    private notification: NotificationService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadVehiculos();
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
  }

  loadVehiculos(): void {
    this.isLoading = true;
    const params: any = { page: this.currentPage, limit: this.pageSize };
    if (this.selectedEstado) params.estado = this.selectedEstado;

    this.vehiculosService.getAll(params).subscribe({
      next: (response) => {
        this.dataSource.data = response.data;
        this.totalRecords = response.total;
        this.updateStats(response.data);
        this.isLoading = false;
      },
      error: (err) => {
        this.notification.error('Error al cargar vehículos');
        this.isLoading = false;
      }
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadVehiculos();
  }

  updateStats(vehiculos: Vehiculo[]): void {
    this.stats = {
      total: this.totalRecords,
      activos: vehiculos.filter(v => v.estado === 'ACTIVO').length,
      enMantenimiento: vehiculos.filter(v => v.estado === 'EN_MANTENIMIENTO').length,
      vencimientos: 0
    };
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  filterByEstado(): void {
    this.currentPage = 1;
    this.loadVehiculos();
  }

  clearFilters(): void {
    this.selectedEstado = '';
    this.currentPage = 1;
    this.loadVehiculos();
  }

  cambiarEstado(vehiculo: Vehiculo, estado: string): void {
    this.vehiculosService.cambiarEstado(vehiculo.id, estado).subscribe({
      next: (updated) => {
        vehiculo.estado = updated.estado;
        this.notification.success(`Vehículo ${vehiculo.placa} actualizado`);
        this.updateStats(this.dataSource.data);
      },
      error: () => this.notification.error('Error al actualizar estado')
    });
  }

  deleteVehiculo(vehiculo: Vehiculo): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Eliminar Vehículo',
        message: `¿Está seguro de eliminar el vehículo ${vehiculo.placa}?`,
        confirmText: 'Eliminar'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.vehiculosService.delete(vehiculo.id).subscribe({
          next: () => {
            this.notification.success('Vehículo eliminado');
            this.loadVehiculos();
          },
          error: () => this.notification.error('Error al eliminar vehículo')
        });
      }
    });
  }

  getMarcaIcon(marca: string): string {
    const iconMap: { [key: string]: string } = {
      'volvo': 'local_shipping',
      'scania': 'fire_truck',
      'mercedes': 'airport_shuttle',
      'man': 'rv_hookup',
      'iveco': 'directions_bus'
    };
    return iconMap[marca?.toLowerCase()] || 'local_shipping';
  }

  getInitials(name: string | undefined): string {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  }
}
