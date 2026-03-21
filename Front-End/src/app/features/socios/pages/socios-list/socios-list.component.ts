import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { SociosService } from '../../services/socios.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { Socio } from '../../../../models';

@Component({
  selector: 'app-socios-list',
  templateUrl: './socios-list.component.html',
  styleUrls: ['./socios-list.component.scss']
})
export class SociosListComponent implements OnInit, AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  displayedColumns = ['nombre', 'ci', 'telefono', 'porcentaje', 'vehiculos', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<Socio>([]);
  selectedEstado = '';
  stats = { total: 0, activos: 0, vehiculos: 0, promedioGanancia: 0 };

  constructor(
    public router: Router,
    private sociosService: SociosService,
    private notification: NotificationService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void { this.loadSocios(); }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  loadSocios(): void {
    this.sociosService.getAll().subscribe({
      next: (socios) => {
        this.dataSource.data = socios;
        this.updateStats(socios);
      },
      error: () => {
        const mockData = this.getMockData();
        this.dataSource.data = mockData;
        this.updateStats(mockData);
      }
    });
  }

  updateStats(socios: Socio[]): void {
    const activos = socios.filter(s => s.estado === 'ACTIVO');
    const totalGanancia = activos.reduce((sum, s) => sum + (s.porcentaje_ganancia || 0), 0);
    this.stats = {
      total: socios.length,
      activos: activos.length,
      vehiculos: socios.reduce((sum, s) => sum + (s.vehiculos?.length || 0), 0),
      promedioGanancia: activos.length > 0 ? Math.round(totalGanancia / activos.length) : 0
    };
  }

  getInitials(socio: Socio): string {
    const firstInitial = socio.nombre?.charAt(0) || '';
    const lastInitial = socio.apellido?.charAt(0) || '';
    return `${firstInitial}${lastInitial}`.toUpperCase();
  }

  goToDetail(id: number): void {
    this.router.navigate(['/socios', id]);
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  filterByEstado(): void {
    this.dataSource.filter = this.selectedEstado?.toLowerCase() || '';
  }

  clearFilters(): void {
    this.selectedEstado = '';
    this.dataSource.filter = '';
  }

  deleteSocio(socio: Socio): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Eliminar Socio',
        message: `¿Está seguro de eliminar a ${socio.nombre} ${socio.apellido}?`,
        confirmText: 'Eliminar'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.dataSource.data = this.dataSource.data.filter(s => s.id !== socio.id);
        this.notification.success('Socio eliminado');
        this.updateStats(this.dataSource.data);
      }
    });
  }

  private getMockData(): Socio[] {
    return [
      { id: 1, nombre: 'Juan', apellido: 'García', ci: '1234567', telefono: '77712345', porcentaje_ganancia: 70, participacion_tipo: 'NETO', participacion_valor: 70, saldo_anticipos: 0, estado: 'ACTIVO', vehiculos: [{}, {}] as any, created_at: new Date(), updated_at: new Date() },
      { id: 2, nombre: 'María', apellido: 'López', ci: '7654321', telefono: '76654321', porcentaje_ganancia: 65, participacion_tipo: 'NETO', participacion_valor: 65, saldo_anticipos: 1500, estado: 'ACTIVO', vehiculos: [{}] as any, created_at: new Date(), updated_at: new Date() },
      { id: 3, nombre: 'Pedro', apellido: 'Martínez', ci: '1122334', telefono: '71123456', porcentaje_ganancia: 75, participacion_tipo: 'BRUTO', participacion_valor: 75, saldo_anticipos: 0, estado: 'INACTIVO', vehiculos: [] as any, created_at: new Date(), updated_at: new Date() }
    ];
  }
}
