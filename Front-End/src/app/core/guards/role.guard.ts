import { Injectable } from '@angular/core';
import { 
  CanActivate, 
  ActivatedRouteSnapshot, 
  RouterStateSnapshot, 
  Router,
  UrlTree 
} from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { NotificationService } from '../services/notification.service';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private router: Router,
    private notification: NotificationService
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    
    // Verificar autenticación primero
    if (!this.authService.isAuthenticated) {
      return this.router.createUrlTree(['/auth/login']);
    }

    // Obtener roles requeridos de la ruta
    const requiredRoles = route.data['roles'] as string[];
    
    if (!requiredRoles || requiredRoles.length === 0) {
      return true;
    }

    // Verificar si el usuario tiene alguno de los roles requeridos
    if (this.authService.hasAnyRole(requiredRoles)) {
      return true;
    }

    // Usuario no tiene permisos
    this.notification.error('No tiene permisos para acceder a esta sección');
    return this.router.createUrlTree(['/app/dashboard']);
  }
}
