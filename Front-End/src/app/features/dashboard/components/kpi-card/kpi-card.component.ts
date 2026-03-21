import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-kpi-card',
  template: `
    <mat-card class="kpi-card" [ngClass]="'kpi-' + color">
      <mat-card-content>
        <div class="kpi-content">
          <div class="kpi-icon">
            <mat-icon>{{ icon }}</mat-icon>
          </div>
          <div class="kpi-info">
            <span class="kpi-title">{{ title }}</span>
            <span class="kpi-value">
              {{ isCurrency ? (value | currencyBs) : value }}
            </span>
            <div class="kpi-footer" *ngIf="trend !== null || subtitle">
              <span class="kpi-trend" *ngIf="trend !== null" [class.positive]="trend > 0" [class.negative]="trend < 0">
                <mat-icon>{{ trend > 0 ? 'arrow_upward' : 'arrow_downward' }}</mat-icon>
                {{ trend > 0 ? '+' : '' }}{{ trend }}%
              </span>
              <span class="kpi-trend-label" *ngIf="trendLabel">{{ trendLabel }}</span>
              <span class="kpi-subtitle" *ngIf="subtitle && !trend">{{ subtitle }}</span>
            </div>
          </div>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .kpi-card {
      height: 100%;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .kpi-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    .kpi-content {
      display: flex;
      align-items: flex-start;
      gap: 16px;
    }

    .kpi-icon {
      width: 56px;
      height: 56px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .kpi-icon mat-icon {
      font-size: 28px;
      width: 28px;
      height: 28px;
      color: #fff;
    }

    .kpi-primary .kpi-icon { background: linear-gradient(135deg, #1976d2, #1565c0); }
    .kpi-accent .kpi-icon { background: linear-gradient(135deg, #ff4081, #f50057); }
    .kpi-success .kpi-icon { background: linear-gradient(135deg, #4caf50, #388e3c); }
    .kpi-info .kpi-icon { background: linear-gradient(135deg, #00bcd4, #0097a7); }
    .kpi-warning .kpi-icon { background: linear-gradient(135deg, #ff9800, #f57c00); }

    .kpi-info {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .kpi-title {
      font-size: 12px;
      color: #666;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .kpi-value {
      font-size: 28px;
      font-weight: 600;
      color: #333;
      margin: 4px 0;
    }

    .kpi-footer {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
    }

    .kpi-trend {
      display: flex;
      align-items: center;
      font-weight: 500;
    }

    .kpi-trend.positive {
      color: #4caf50;
    }

    .kpi-trend.negative {
      color: #f44336;
    }

    .kpi-trend mat-icon {
      font-size: 14px;
      width: 14px;
      height: 14px;
    }

    .kpi-trend-label, .kpi-subtitle {
      color: #999;
    }
  `]
})
export class KpiCardComponent {
  @Input() title: string = '';
  @Input() value: number = 0;
  @Input() icon: string = 'info';
  @Input() color: 'primary' | 'accent' | 'success' | 'info' | 'warning' = 'primary';
  @Input() isCurrency: boolean = false;
  @Input() trend: number | null = null;
  @Input() trendLabel: string = '';
  @Input() subtitle: string = '';
}
