import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-alerts-widget',
  template: `
    <div class="alerts-list" *ngIf="alerts.length > 0; else emptyState">
      <div class="alert-item" *ngFor="let alert of alerts" [ngClass]="'alert-' + alert.type">
        <div class="alert-icon">
          <mat-icon>{{ alert.icon }}</mat-icon>
        </div>
        <div class="alert-content">
          <span class="alert-title">{{ alert.title }}</span>
          <span class="alert-message">{{ alert.message }}</span>
        </div>
        <button mat-icon-button class="alert-action">
          <mat-icon>chevron_right</mat-icon>
        </button>
      </div>
    </div>

    <ng-template #emptyState>
      <app-empty-state
        icon="check_circle"
        title="Todo en orden"
        message="No hay alertas pendientes">
      </app-empty-state>
    </ng-template>
  `,
  styles: [`
    .alerts-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .alert-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px;
      border-radius: 8px;
      border-left: 4px solid;
    }

    .alert-warning {
      background: #fff8e1;
      border-color: #ff9800;
    }

    .alert-warning .alert-icon mat-icon {
      color: #ff9800;
    }

    .alert-error {
      background: #ffebee;
      border-color: #f44336;
    }

    .alert-error .alert-icon mat-icon {
      color: #f44336;
    }

    .alert-info {
      background: #e3f2fd;
      border-color: #2196f3;
    }

    .alert-info .alert-icon mat-icon {
      color: #2196f3;
    }

    .alert-success {
      background: #e8f5e9;
      border-color: #4caf50;
    }

    .alert-success .alert-icon mat-icon {
      color: #4caf50;
    }

    .alert-icon {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .alert-content {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .alert-title {
      font-weight: 500;
      color: #333;
      font-size: 14px;
    }

    .alert-message {
      font-size: 12px;
      color: #666;
    }
  `]
})
export class AlertsWidgetComponent {
  @Input() alerts: any[] = [];
}
