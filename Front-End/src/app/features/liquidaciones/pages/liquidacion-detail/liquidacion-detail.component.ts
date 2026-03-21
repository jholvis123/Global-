import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

interface Liquidacion {
  id: number;
  codigo: string;
  viaje: { origen: string; destino: string; fecha: string; cliente: string };
  vehiculo: { placa: string; modelo: string };
  chofer: { nombre: string; documento: string };
  ingresos: { flete: number; adicionales: number; total: number };
  gastos: { combustible: number; peajes: number; viaticos: number; otros: number; total: number };
  anticipos: { monto: number; fecha: string }[];
  resultado: { bruto: number; neto: number; comisionChofer: number; utilidadEmpresa: number };
  estado: string;
  fechaCreacion: string;
  observaciones: string;
}

@Component({
  selector: 'app-liquidacion-detail',
  templateUrl: './liquidacion-detail.component.html',
  styleUrls: ['./liquidacion-detail.component.scss']
})
export class LiquidacionDetailComponent implements OnInit {
  liquidacion: Liquidacion | null = null;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.loadLiquidacion(Number(id));
  }

  loadLiquidacion(id: number): void {
    // Simular carga de datos
    setTimeout(() => {
      this.liquidacion = {
        id: id,
        codigo: 'LIQ-2024-0001',
        viaje: {
          origen: 'Lima',
          destino: 'Arequipa',
          fecha: '2024-01-15',
          cliente: 'Empresa ABC S.A.C.'
        },
        vehiculo: {
          placa: 'ABC-123',
          modelo: 'Volvo FH 500'
        },
        chofer: {
          nombre: 'Juan Pérez García',
          documento: '12345678'
        },
        ingresos: {
          flete: 5000,
          adicionales: 500,
          total: 5500
        },
        gastos: {
          combustible: 1200,
          peajes: 350,
          viaticos: 200,
          otros: 150,
          total: 1900
        },
        anticipos: [
          { monto: 500, fecha: '2024-01-14' },
          { monto: 300, fecha: '2024-01-16' }
        ],
        resultado: {
          bruto: 3600,
          neto: 2800,
          comisionChofer: 840,
          utilidadEmpresa: 1960
        },
        estado: 'completada',
        fechaCreacion: '2024-01-18',
        observaciones: 'Viaje completado sin novedades. Cliente satisfecho con el servicio.'
      };
      this.loading = false;
    }, 500);
  }

  getEstadoClass(estado: string): string {
    const classes: { [key: string]: string } = {
      'pendiente': 'status-pending',
      'en_proceso': 'status-process',
      'completada': 'status-completed',
      'cancelada': 'status-cancelled'
    };
    return classes[estado] || 'status-pending';
  }

  getEstadoLabel(estado: string): string {
    const labels: { [key: string]: string } = {
      'pendiente': 'Pendiente',
      'en_proceso': 'En Proceso',
      'completada': 'Completada',
      'cancelada': 'Cancelada'
    };
    return labels[estado] || estado;
  }

  goBack(): void {
    this.router.navigate(['/app/liquidaciones']);
  }

  editLiquidacion(): void {
    if (this.liquidacion) {
      this.router.navigate(['/app/liquidaciones/editar', this.liquidacion.id]);
    }
  }

  printLiquidacion(): void {
    window.print();
  }

  exportToPDF(): void {
    // Implementar exportación a PDF
    console.log('Exportar a PDF');
  }
}
