import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { LoadingService } from '../services/loading.service';

@Injectable()
export class LoadingInterceptor implements HttpInterceptor {

  private excludedUrls = [
    '/health',
    '/api/v1/info'
  ];

  constructor(private loadingService: LoadingService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    // No mostrar loading para ciertas URLs
    if (this.isExcluded(request.url)) {
      return next.handle(request);
    }

    this.loadingService.show();

    return next.handle(request).pipe(
      finalize(() => {
        this.loadingService.hide();
      })
    );
  }

  private isExcluded(url: string): boolean {
    return this.excludedUrls.some(excluded => url.includes(excluded));
  }
}
