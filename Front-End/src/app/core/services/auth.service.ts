import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { map, tap, catchError, switchMap } from 'rxjs/operators';
import { Router } from '@angular/router';
import { environment } from '../../../environments/environment';
import { StorageService } from './storage.service';
import { 
  Usuario, 
  LoginRequest, 
  TokenResponse, 
  ChangePasswordRequest,
  UsuarioCreate 
} from '../../models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly API_URL = `${environment.apiUrl}/auth`;
  
  private currentUserSubject = new BehaviorSubject<Usuario | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(
    private http: HttpClient,
    private storage: StorageService,
    private router: Router
  ) {
    this.checkAuthStatus();
  }

  // Verificar estado de autenticación al iniciar
  private checkAuthStatus(): void {
    const token = this.storage.getToken();
    const user = this.storage.getUser();
    
    if (token && user) {
      this.currentUserSubject.next(user);
      this.isAuthenticatedSubject.next(true);
    }
  }

  // Login
  login(credentials: LoginRequest): Observable<TokenResponse> {
    // Mock login para desarrollo
    if (this.isMockLogin(credentials)) {
      return this.mockLogin(credentials);
    }

    return this.http.post<TokenResponse>(`${this.API_URL}/login`, credentials)
      .pipe(
        tap(response => this.handleAuthResponse(response)),
        catchError(error => {
          console.error('Error en login:', error);
          // Intentar mock login si el backend no está disponible
          return this.mockLogin(credentials);
        })
      );
  }

  // Mock login para desarrollo sin backend
  private isMockLogin(credentials: LoginRequest): boolean {
    return credentials.email === 'admin@srl.com' || 
           credentials.email === 'operador@srl.com' ||
           credentials.email === 'finanzas@srl.com';
  }

  private mockLogin(credentials: LoginRequest): Observable<TokenResponse> {
    const mockUsers: { [key: string]: { user: Usuario; password: string } } = {
      'admin@srl.com': {
        password: 'admin123',
        user: {
          id: 1,
          nombre: 'Administrador',
          apellido: 'Sistema',
          email: 'admin@srl.com',
          roles: ['ADMINISTRADOR'],
          estado: 'ACTIVO',
          intentos_fallidos: 0,
          created_at: new Date(),
          updated_at: new Date()
        }
      },
      'operador@srl.com': {
        password: 'operador123',
        user: {
          id: 2,
          nombre: 'Usuario',
          apellido: 'Operador',
          email: 'operador@srl.com',
          roles: ['OPERACIONES'],
          estado: 'ACTIVO',
          intentos_fallidos: 0,
          created_at: new Date(),
          updated_at: new Date()
        }
      },
      'finanzas@srl.com': {
        password: 'finanzas123',
        user: {
          id: 3,
          nombre: 'Usuario',
          apellido: 'Finanzas',
          email: 'finanzas@srl.com',
          roles: ['FINANZAS'],
          estado: 'ACTIVO',
          intentos_fallidos: 0,
          created_at: new Date(),
          updated_at: new Date()
        }
      }
    };

    const mockUser = mockUsers[credentials.email];
    
    if (mockUser && mockUser.password === credentials.password) {
      const response: TokenResponse = {
        access_token: 'mock_access_token_' + Date.now(),
        refresh_token: 'mock_refresh_token_' + Date.now(),
        token_type: 'bearer',
        expires_in: 3600,
        usuario: mockUser.user
      };
      
      this.handleAuthResponse(response);
      return of(response);
    }

    return throwError(() => ({ 
      status: 401, 
      error: { detail: 'Credenciales incorrectas' } 
    }));
  }

  // Logout
  logout(): void {
    // Llamar endpoint de logout (opcional, depende del backend)
    this.http.post(`${this.API_URL}/logout`, {}).pipe(
      catchError(() => of(null))
    ).subscribe();

    this.clearAuthData();
    this.router.navigate(['/']);  // Ir a la landing page
  }

  // Refrescar token
  refreshToken(): Observable<TokenResponse> {
    const refreshToken = this.storage.getRefreshToken();
    
    if (!refreshToken) {
      this.logout();
      return throwError(() => new Error('No refresh token available'));
    }

    return this.http.post<TokenResponse>(`${this.API_URL}/refresh`, { refresh_token: refreshToken })
      .pipe(
        tap(response => this.handleAuthResponse(response)),
        catchError(error => {
          this.logout();
          return throwError(() => error);
        })
      );
  }

  // Cambiar contraseña
  changePassword(data: ChangePasswordRequest): Observable<any> {
    return this.http.post(`${this.API_URL}/change-password`, data);
  }

  // Obtener perfil actual
  getProfile(): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.API_URL}/profile`);
  }

  // Registrar nuevo usuario (solo admin)
  register(userData: UsuarioCreate): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.API_URL}/register`, userData);
  }

  // Desbloquear usuario (solo admin)
  unblockUser(userId: number): Observable<any> {
    return this.http.post(`${this.API_URL}/unblock/${userId}`, {});
  }

  // Manejar respuesta de autenticación
  private handleAuthResponse(response: TokenResponse): void {
    this.storage.setToken(response.access_token);
    this.storage.setRefreshToken(response.refresh_token);
    this.storage.setUser(response.usuario);
    
    this.currentUserSubject.next(response.usuario);
    this.isAuthenticatedSubject.next(true);
  }

  // Limpiar datos de autenticación
  private clearAuthData(): void {
    this.storage.clearAuth();
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
  }

  // Getters útiles
  get isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }

  get currentUser(): Usuario | null {
    return this.currentUserSubject.value;
  }

  get token(): string | null {
    return this.storage.getToken();
  }

  // Verificar si el usuario tiene un rol específico
  hasRole(role: string): boolean {
    const user = this.currentUser;
    return user ? user.roles.includes(role as any) : false;
  }

  // Verificar si el usuario tiene alguno de los roles
  hasAnyRole(roles: string[]): boolean {
    const user = this.currentUser;
    return user ? roles.some(role => user.roles.includes(role as any)) : false;
  }

  // Verificar si es administrador
  get isAdmin(): boolean {
    return this.hasRole('ADMINISTRADOR');
  }

  // Verificar si tiene permisos de operaciones
  get isOperations(): boolean {
    return this.hasAnyRole(['ADMINISTRADOR', 'OPERACIONES']);
  }

  // Verificar si tiene permisos financieros
  get isFinance(): boolean {
    return this.hasAnyRole(['ADMINISTRADOR', 'FINANZAS']);
  }
}
