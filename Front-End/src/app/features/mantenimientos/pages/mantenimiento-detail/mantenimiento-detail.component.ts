import { Component } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-mantenimiento-detail',
  template: `
    <div class="page-container">
      <div class="page-header">
        <div class="page-header__content">
          <button mat-icon-button (click)="goBack()">
            <mat-icon>arrow_back</mat-icon>
          </button>
          <div>
            <h1 class="page-header__title">Detalle de Mantenimiento</h1>
            <p class="page-header__subtitle">Información completa del mantenimiento</p>
          </div>
        </div>
      </div>
      <div class="coming-soon">
        <mat-icon>construction</mat-icon>
        <h2>Vista en Desarrollo</h2>
        <p>El detalle de mantenimiento estará disponible próximamente</p>
        <button mat-flat-button color="primary" (click)="goBack()">Volver al Listado</button>
      </div>
    </div>
  `,
  styles: [`
    .page-container { padding: 24px; max-width: 1200px; margin: 0 auto; }
    .page-header { display: flex; align-items: center; margin-bottom: 24px; }
    .page-header__content { display: flex; align-items: center; gap: 16px; }
    .page-header__title { font-size: 24px; font-weight: 600; margin: 0; color: var(--text-primary); }
    .page-header__subtitle { font-size: 14px; color: var(--text-secondary); margin: 4px 0 0; }
    .coming-soon {
      text-align: center;
      padding: 80px 20px;
      background: var(--card-bg);
      border-radius: 12px;
      border: 1px solid var(--border-color);
      mat-icon { font-size: 64px; width: 64px; height: 64px; color: #f59e0b; margin-bottom: 16px; }
      h2 { margin: 0 0 8px; color: var(--text-primary); }
      p { margin: 0 0 24px; color: var(--text-secondary); }
    }
  `]
})
export class MantenimientoDetailComponent {
  constructor(private router: Router, private route: ActivatedRoute) {}
  goBack(): void { this.router.navigate(['/app/mantenimientos']); }
}
