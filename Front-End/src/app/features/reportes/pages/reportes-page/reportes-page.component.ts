import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

interface ReportType {
  id: string;
  name: string;
  icon: string;
  description: string;
  color: string;
}

@Component({
  selector: 'app-reportes-page',
  templateUrl: './reportes-page.component.html',
  styleUrls: ['./reportes-page.component.scss']
})
export class ReportesPageComponent implements OnInit {
  filterForm!: FormGroup;
  isLoading = false;
  selectedReport: ReportType | null = null;

  reportTypes: ReportType[] = [
    {
      id: 'viajes',
      name: 'Reporte de Viajes',
      icon: 'route',
      description: 'Detalle de todos los viajes realizados en el período seleccionado',
      color: '#3b82f6'
    },
    {
      id: 'ingresos',
      name: 'Reporte de Ingresos',
      icon: 'payments',
      description: 'Resumen de ingresos por cliente, vehículo y período',
      color: '#22c55e'
    },
    {
      id: 'vehiculos',
      name: 'Reporte de Vehículos',
      icon: 'local_shipping',
      description: 'Estado y rendimiento de la flota vehicular',
      color: '#f59e0b'
    },
    {
      id: 'choferes',
      name: 'Reporte de Choferes',
      icon: 'badge',
      description: 'Productividad y rendimiento de conductores',
      color: '#8b5cf6'
    },
    {
      id: 'clientes',
      name: 'Reporte de Clientes',
      icon: 'business',
      description: 'Análisis de clientes y facturación',
      color: '#ec4899'
    },
    {
      id: 'liquidaciones',
      name: 'Reporte de Liquidaciones',
      icon: 'receipt_long',
      description: 'Detalle de liquidaciones y pagos a socios',
      color: '#06b6d4'
    }
  ];

  // Datos de ejemplo
  reportData: any[] = [];
  displayedColumns: string[] = [];

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.filterForm = this.fb.group({
      reportType: ['viajes'],
      fechaInicio: [this.getFirstDayOfMonth()],
      fechaFin: [new Date()],
      estado: [''],
      cliente: ['']
    });
  }

  getFirstDayOfMonth(): Date {
    const date = new Date();
    return new Date(date.getFullYear(), date.getMonth(), 1);
  }

  selectReport(report: ReportType): void {
    this.selectedReport = report;
    this.filterForm.patchValue({ reportType: report.id });
  }

  generateReport(): void {
    this.isLoading = true;

    // Simular generación de reporte
    setTimeout(() => {
      this.isLoading = false;
      this.loadSampleData();
    }, 1500);
  }

  loadSampleData(): void {
    const type = this.filterForm.get('reportType')?.value;

    switch (type) {
      case 'viajes':
        this.displayedColumns = ['codigo', 'fecha', 'origen', 'destino', 'cliente', 'estado', 'monto'];
        this.reportData = [
          { codigo: 'VJ-2026-001', fecha: '2026-02-01', origen: 'Santa Cruz', destino: 'La Paz', cliente: 'Empresa A', estado: 'Completado', monto: 2500 },
          { codigo: 'VJ-2026-002', fecha: '2026-02-02', origen: 'Cochabamba', destino: 'Sucre', cliente: 'Empresa B', estado: 'En Ruta', monto: 1800 },
          { codigo: 'VJ-2026-003', fecha: '2026-02-03', origen: 'La Paz', destino: 'Oruro', cliente: 'Empresa C', estado: 'Completado', monto: 1200 },
        ];
        break;
      case 'ingresos':
        this.displayedColumns = ['mes', 'viajes', 'ingresos', 'gastos', 'utilidad'];
        this.reportData = [
          { mes: 'Enero 2026', viajes: 125, ingresos: 185000, gastos: 92000, utilidad: 93000 },
          { mes: 'Febrero 2026', viajes: 142, ingresos: 210000, gastos: 98000, utilidad: 112000 },
        ];
        break;
      default:
        this.displayedColumns = ['item', 'descripcion', 'valor'];
        this.reportData = [
          { item: 'Total', descripcion: 'Sin datos disponibles', valor: 0 }
        ];
    }
  }

  exportPDF(): void {
    // Aquí iría la lógica de exportación a PDF
    console.log('Exportando a PDF...');
    alert('Función de exportación a PDF - Requiere integración con librería como jsPDF');
  }

  exportExcel(): void {
    // Aquí iría la lógica de exportación a Excel
    console.log('Exportando a Excel...');
    alert('Función de exportación a Excel - Requiere integración con librería como xlsx');
  }

  printReport(): void {
    window.print();
  }
}
