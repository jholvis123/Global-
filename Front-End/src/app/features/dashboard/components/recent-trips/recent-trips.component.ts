import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-recent-trips',
  template: `
    <div class="trips-list" *ngIf="trips.length > 0; else emptyState">
      <div class="trip-item" *ngFor="let trip of trips">
        <div class="trip-icon">
          <mat-icon>local_shipping</mat-icon>
        </div>
        <div class="trip-info">
          <span class="trip-route">{{ trip.ruta }}</span>
          <span class="trip-details">
            {{ trip.chofer }} • {{ trip.vehiculo }}
          </span>
        </div>
        <div class="trip-status">
          <app-status-badge [status]="trip.estado"></app-status-badge>
        </div>
      </div>
    </div>

    <ng-template #emptyState>
      <app-empty-state
        icon="route"
        title="Sin viajes recientes"
        message="No hay viajes registrados recientemente">
      </app-empty-state>
    </ng-template>
  `,
  styles: [`
    .trips-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .trip-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px;
      background: #f5f7fa;
      border-radius: 8px;
      transition: background 0.2s;
    }

    .trip-item:hover {
      background: #eef1f5;
    }

    .trip-icon {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      background: #e3f2fd;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .trip-icon mat-icon {
      color: #1976d2;
    }

    .trip-info {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .trip-route {
      font-weight: 500;
      color: #333;
    }

    .trip-details {
      font-size: 12px;
      color: #666;
    }
  `]
})
export class RecentTripsComponent {
  @Input() trips: any[] = [];
}
