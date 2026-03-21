import { Component, OnInit } from '@angular/core';
import { DashboardService, DashboardStats, Alerta } from '../../services/dashboard.service';
import { ChartConfiguration, ChartData } from 'chart.js';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  stats: DashboardStats | null = null;
  isLoading = true;
  recentTrips: any[] = [];
  alerts: Alerta[] = [];

  // Chart configurations
  lineChartData: ChartData<'line'> = {
    labels: ['Ago', 'Sep', 'Oct', 'Nov', 'Dic', 'Ene'],
    datasets: [
      {
        label: 'Ingresos',
        data: [380000, 420000, 450000, 410000, 520000, 485750],
        borderColor: '#4caf50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        label: 'Gastos',
        data: [280000, 295000, 310000, 290000, 340000, 312480],
        borderColor: '#f44336',
        backgroundColor: 'rgba(244, 67, 54, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  lineChartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top' } },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { callback: (value) => 'Bs ' + Number(value).toLocaleString() }
      }
    }
  };

  pieChartData: ChartData<'doughnut'> = {
    labels: ['Liquidados', 'Entregados', 'En Ruta', 'Planificados'],
    datasets: [{
      data: [120, 16, 8, 12],
      backgroundColor: ['#9c27b0', '#ff9800', '#2196f3', '#4caf50']
    }]
  };

  pieChartOptions: ChartConfiguration<'doughnut'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'right' } }
  };

  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  private loadDashboardData(): void {
    this.isLoading = true;

    this.dashboardService.getStats().subscribe({
      next: (data) => {
        this.stats = data;
        this.isLoading = false;
      },
      error: () => {
        // Fallback a datos por defecto si hay error
        this.stats = {
          total_viajes: 0,
          viajes_en_ruta: 0,
          ingresos_mes: 0,
          gastos_mes: 0,
          ganancia_mes: 0,
          rentabilidad: 0,
          vehiculos_activos: 0,
          vehiculos_mantenimiento: 0,
          pendientes_liquidacion: 0,
          choferes_activos: 0,
          documentos_por_vencer: 0,
          licencias_por_vencer: 0
        };
        this.isLoading = false;
      }
    });

    this.dashboardService.getAlertas().subscribe({
      next: (alertas) => this.alerts = alertas,
      error: () => this.alerts = []
    });

    this.dashboardService.getViajesRecientes(5).subscribe({
      next: (trips) => this.recentTrips = trips,
      error: () => this.recentTrips = []
    });
  }
}
