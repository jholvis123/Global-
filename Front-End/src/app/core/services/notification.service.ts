import { Injectable } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  private defaultConfig: MatSnackBarConfig = {
    duration: 4000,
    horizontalPosition: 'end',
    verticalPosition: 'top'
  };

  constructor(private snackBar: MatSnackBar) { }

  success(message: string, action: string = 'OK'): void {
    this.snackBar.open(message, action, {
      ...this.defaultConfig,
      panelClass: ['snackbar-success']
    });
  }

  error(message: string, action: string = 'Cerrar'): void {
    this.snackBar.open(message, action, {
      ...this.defaultConfig,
      duration: 6000,
      panelClass: ['snackbar-error']
    });
  }

  warning(message: string, action: string = 'OK'): void {
    this.snackBar.open(message, action, {
      ...this.defaultConfig,
      duration: 5000,
      panelClass: ['snackbar-warning']
    });
  }

  info(message: string, action: string = 'OK'): void {
    this.snackBar.open(message, action, {
      ...this.defaultConfig,
      panelClass: ['snackbar-info']
    });
  }

  custom(message: string, action: string, config: MatSnackBarConfig): void {
    this.snackBar.open(message, action, { ...this.defaultConfig, ...config });
  }
}
