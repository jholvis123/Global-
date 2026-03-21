import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { ClientesService } from '../../services/clientes.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { ConfirmDialogComponent } from '../../../../shared/components/confirm-dialog/confirm-dialog.component';
import { Cliente } from '../../../../models';

@Component({
  selector: 'app-clientes-list',
  templateUrl: './clientes-list.component.html',
  styleUrls: ['./clientes-list.component.scss']
})
export class ClientesListComponent implements OnInit, AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  displayedColumns = ['razon_social', 'nit', 'contacto', 'email', 'ciudad', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<Cliente>([]);
  selectedEstado = '';
  stats = { total: 0, activos: 0, viajesActivos: 0, frecuentes: 0 };

  // Paginación
  isLoading = false;
  totalRecords = 0;
  pageSize = 20;
  currentPage = 1;

  constructor(
    public router: Router,
    private clientesService: ClientesService,
    private notification: NotificationService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void { this.loadClientes(); }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
  }

  loadClientes(): void {
    this.isLoading = true;
    const params: any = { page: this.currentPage, limit: this.pageSize };
    if (this.selectedEstado) params.estado = this.selectedEstado;

    this.clientesService.getAll(params).subscribe({
      next: (response) => {
        this.dataSource.data = response.data;
        this.totalRecords = response.total;
        this.updateStats(response.data);
        this.isLoading = false;
      },
      error: () => {
        this.notification.error('Error al cargar clientes');
        this.isLoading = false;
      }
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadClientes();
  }

  updateStats(clientes: Cliente[]): void {
    this.stats = {
      total: this.totalRecords,
      activos: clientes.filter(c => c.estado === 'ACTIVO').length,
      viajesActivos: 0,
      frecuentes: 0
    };
  }

  getContactInitials(nombre: string): string {
    if (!nombre) return '?';
    return nombre.split(' ')
      .map(n => n[0])
      .join('')
      .substring(0, 2)
      .toUpperCase();
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  filterByEstado(): void {
    this.currentPage = 1;
    this.loadClientes();
  }

  clearFilters(): void {
    this.selectedEstado = '';
    this.currentPage = 1;
    this.loadClientes();
  }

  deleteCliente(cliente: Cliente): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Eliminar Cliente',
        message: `¿Está seguro de eliminar a ${cliente.razon_social}?`,
        confirmText: 'Eliminar'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.clientesService.delete(cliente.id).subscribe({
          next: () => {
            this.notification.success('Cliente eliminado correctamente');
            this.loadClientes();
          },
          error: () => this.notification.error('Error al eliminar cliente')
        });
      }
    });
  }
}
