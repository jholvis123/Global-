import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { NotificationService } from '../services/notification.service';
import { Router } from '@angular/router';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  constructor(
    private notification: NotificationService,
    private router: Router
  ) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorMessage = 'Ha ocurrido un error inesperado';

        if (error.error instanceof ErrorEvent) {
          // Error del cliente
          errorMessage = `Error: ${error.error.message}`;
        } else {
          // Error del servidor
          switch (error.status) {
            case 0:
              errorMessage = 'No se puede conectar con el servidor';
              break;
            case 400:
              errorMessage = error.error?.message || 'Solicitud inválida';
              break;
            case 401:
              errorMessage = 'Sesión expirada. Por favor, inicie sesión nuevamente';
              break;
            case 403:
              errorMessage = 'No tiene permisos para realizar esta acción';
              break;
            case 404:
              errorMessage = 'Recurso no encontrado';
              break;
            case 409:
              errorMessage = error.error?.message || 'Conflicto con el recurso existente';
              break;
            case 422:
              errorMessage = this.handleValidationError(error);
              break;
            case 500:
              errorMessage = 'Error interno del servidor';
              break;
            case 503:
              errorMessage = 'Servicio no disponible temporalmente';
              break;
            default:
              errorMessage = error.error?.message || `Error ${error.status}`;
          }
        }

        // Mostrar notificación de error (excepto para 401 que se maneja en auth interceptor)
        if (error.status !== 401) {
          this.notification.error(errorMessage);
        }

        return throwError(() => ({ ...error, userMessage: errorMessage }));
      })
    );
  }

  private handleValidationError(error: HttpErrorResponse): string {
    if (error.error?.detail) {
      if (Array.isArray(error.error.detail)) {
        return error.error.detail.map((e: any) => e.msg).join(', ');
      }
      return error.error.detail;
    }
    return 'Error de validación en los datos enviados';
  }
}
