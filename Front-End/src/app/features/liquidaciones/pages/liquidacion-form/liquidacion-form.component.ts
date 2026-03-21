import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-liquidacion-form',
  template: `
    <div class="page-container">
      <div class="page-header">
        <div class="page-header__content">
          <button mat-icon-button (click)="cancel()">
            <mat-icon>arrow_back</mat-icon>
          </button>
          <div>
            <h1 class="page-header__title">Nueva Liquidación</h1>
            <p class="page-header__subtitle">Crea una nueva liquidación de viaje</p>
          </div>
        </div>
      </div>
      <div class="coming-soon">
        <mat-icon>construction</mat-icon>
        <h2>Formulario en Desarrollo</h2>
        <p>El formulario de liquidación estará disponible próximamente</p>
        <button mat-flat-button color="primary" (click)="cancel()">Volver al Listado</button>
      </div>
    </div>
  `,
  styles: [`
    .coming-soon {
      text-align: center;
      padding: 80px 20px;
      background: var(--card-bg);
      border-radius: 12px;
      mat-icon { font-size: 64px; width: 64px; height: 64px; color: #f59e0b; margin-bottom: 16px; }
      h2 { margin: 0 0 8px; color: var(--text-primary); }
      p { margin: 0 0 24px; color: var(--text-secondary); }
    }
  `]
})
export class LiquidacionFormComponent {
  constructor(private router: Router) {}
  cancel(): void { this.router.navigate(['/app/liquidaciones']); }
}
