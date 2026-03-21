import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { ViajesService } from '../../services/viajes.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { Viaje, TIPOS_TARIFA, TIPOS_GASTO, TIPOS_CARGA, ESTADOS_VIAJE, GastoViaje, TipoGasto, TipoCarga } from '../../../../models';
import { GastoDialogComponent } from '../../components/gasto-dialog/gasto-dialog.component';

@Component({
  selector: 'app-viaje-detail',
  templateUrl: './viaje-detail.component.html',
  styleUrls: ['./viaje-detail.component.scss']
})
export class ViajeDetailComponent implements OnInit {
  viaje: Viaje | null = null;
  isLoading = true;
  gastosColumns = ['tipo', 'descripcion', 'fecha', 'monto'];

  // Constantes para labels
  private tiposTarifa = TIPOS_TARIFA;
  private tiposGasto = TIPOS_GASTO;
  private tiposCarga = TIPOS_CARGA;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private viajesService: ViajesService,
    private notification: NotificationService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.loadViaje(+id);
    }
  }

  private loadViaje(id: number): void {
    this.isLoading = true;
    this.viajesService.getById(id).subscribe({
      next: (viaje) => {
        this.viaje = viaje;
        this.isLoading = false;
      },
      error: () => {
        // Mock data para desarrollo
        this.viaje = {
          id: id,
          cliente_id: 1,
          cliente: { id: 1, razon_social: 'Empresa ABC S.A.', estado: 'ACTIVO', created_at: new Date(), updated_at: new Date() },
          vehiculo_id: 1,
          vehiculo: { id: 1, placa: 'ABC-123', marca: 'Volvo', modelo: 'FH16', anio: 2022, capacidad_ton: 30, socio_id: 1, estado: 'ACTIVO', created_at: new Date(), updated_at: new Date() },
          chofer_id: 1,
          chofer: { id: 1, nombre: 'Juan', apellido: 'Perez', ci: '1234567', licencia_numero: 'L123', licencia_categoria: 'C', licencia_vencimiento: new Date(), experiencia_anos: 5, estado: 'ACTIVO', created_at: new Date(), updated_at: new Date(), nombre_completo: 'Juan Perez' },
          origen: 'Santa Cruz',
          destino: 'La Paz',
          fecha_salida: new Date(),
          tipo_carga: 'CEMENTO',
          peso_ton: 28,
          km_estimado: 850,
          tarifa_tipo: 'TON',
          tarifa_valor: 120,
          estado: 'EN_RUTA',
          ingreso_total_bs: 3360,
          total_gastos_bs: 1200,
          margen_bruto_bs: 2160,
          notas: 'Entregar antes del mediodía',
          gastos: [
            { id: 1, viaje_id: id, tipo: 'COMBUSTIBLE', monto_bs: 800, fecha: new Date(), descripcion: 'Diesel 200L', created_at: new Date() },
            { id: 2, viaje_id: id, tipo: 'PEAJE', monto_bs: 350, fecha: new Date(), descripcion: 'Peajes ruta principal', created_at: new Date() },
            { id: 3, viaje_id: id, tipo: 'VIATICO', monto_bs: 50, fecha: new Date(), descripcion: 'Almuerzo chofer', created_at: new Date() }
          ],
          created_at: new Date(),
          updated_at: new Date()
        };
        this.isLoading = false;
      }
    });
  }

  getTarifaLabel(tipo: string): string {
    const found = this.tiposTarifa.find(t => t.value === tipo);
    return found ? found.label : tipo;
  }

  getTipoCargaLabel(tipo: string): string {
    const found = this.tiposCarga.find(t => t.value === tipo);
    return found ? found.label : tipo;
  }

  getTipoGastoLabel(tipo: string): string {
    const found = this.tiposGasto.find(t => t.value === tipo);
    return found ? found.label : tipo;
  }

  cambiarEstado(nuevoEstado: string): void {
    if (!this.viaje) return;

    this.viajesService.cambiarEstado(this.viaje.id, nuevoEstado).subscribe({
      next: () => {
        this.notification.success(`Viaje actualizado a ${nuevoEstado}`);
        this.viaje!.estado = nuevoEstado as any;
      },
      error: () => {
        // Para desarrollo
        this.viaje!.estado = nuevoEstado as any;
        this.notification.success(`Viaje actualizado a ${nuevoEstado}`);
      }
    });
  }

  addGasto(): void {
    if (!this.viaje) return;

    const dialogRef = this.dialog.open(GastoDialogComponent, {
      width: '500px',
      data: { viaje_id: this.viaje.id }
    });

    dialogRef.afterClosed().subscribe((result: GastoViaje | undefined) => {
      if (result && this.viaje) {
        // Agregar el gasto a la lista local
        if (!this.viaje.gastos) {
          this.viaje.gastos = [];
        }
        this.viaje.gastos.push(result);
        this.notification.success('Gasto agregado correctamente');
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/viajes']);
  }
}
