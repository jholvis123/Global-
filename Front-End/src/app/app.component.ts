import { Component, OnInit } from '@angular/core';
import { LoadingService } from './core/services/loading.service';
import { delay } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  template: `
    <!-- Barra de progreso global -->
    <mat-progress-bar 
      *ngIf="isLoading$ | async" 
      mode="indeterminate" 
      color="accent"
      class="global-loading-bar">
    </mat-progress-bar>

    <!-- Contenido principal -->
    <router-outlet></router-outlet>
  `,
  styles: [`
    .global-loading-bar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 9999;
      height: 3px;
    }
  `]
})
export class AppComponent implements OnInit {
  title = 'Sistema de Gestión de Transporte SRL';
  isLoading$ = this.loadingService.loading$.pipe(delay(0));

  constructor(private loadingService: LoadingService) {}

  ngOnInit(): void {
    console.log('🚛 Sistema de Gestión de Transporte SRL iniciado');
  }
}
