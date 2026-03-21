import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-chart-card',
  template: `
    <mat-card class="chart-card">
      <mat-card-header>
        <mat-card-title>{{ title }}</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="chart-container">
          <ng-content></ng-content>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .chart-card {
      height: 100%;
    }

    mat-card-title {
      font-size: 16px !important;
      font-weight: 500;
    }

    .chart-container {
      height: 300px;
      position: relative;
    }
  `]
})
export class ChartCardComponent {
  @Input() title: string = '';
}
