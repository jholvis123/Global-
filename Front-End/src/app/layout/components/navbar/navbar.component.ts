import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { AuthService } from '../../../core/services/auth.service';
import { ThemeService } from '../../../core/services/theme.service';
import { Usuario } from '../../../models';

interface Notification {
  id: number;
  title: string;
  message: string;
  type: 'info' | 'warning' | 'success' | 'error';
  time: string;
  read: boolean;
  icon: string;
}

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  @Output() toggleSidebar = new EventEmitter<void>();
  
  searchQuery = '';
  searchOpen = false;
  isDarkMode = false;

  notifications: Notification[] = [
    {
      id: 1,
      title: 'Viaje completado',
      message: 'El viaje #VJ-2024-001 ha sido completado exitosamente',
      type: 'success',
      time: 'Hace 5 min',
      read: false,
      icon: 'check_circle'
    },
    {
      id: 2,
      title: 'Mantenimiento programado',
      message: 'El vehículo ABC-123 requiere mantenimiento preventivo',
      type: 'warning',
      time: 'Hace 1 hora',
      read: false,
      icon: 'build'
    },
    {
      id: 3,
      title: 'Nuevo anticipo solicitado',
      message: 'Juan Pérez ha solicitado un anticipo de Bs. 500',
      type: 'info',
      time: 'Hace 2 horas',
      read: true,
      icon: 'payments'
    }
  ];

  pageTitle = 'Dashboard';

  private routeTitles: { [key: string]: string } = {
    '/app/dashboard': 'Dashboard',
    '/app/viajes': 'Gestión de Viajes',
    '/app/vehiculos': 'Gestión de Vehículos',
    '/app/choferes': 'Gestión de Choferes',
    '/app/socios': 'Gestión de Socios',
    '/app/clientes': 'Gestión de Clientes',
    '/app/anticipos': 'Anticipos',
    '/app/liquidaciones': 'Liquidaciones',
    '/app/mantenimientos': 'Mantenimientos',
    '/app/reportes': 'Reportes',
    '/app/usuarios': 'Gestión de Usuarios',
    '/app/perfil': 'Mi Perfil',
    '/app/configuracion': 'Configuración'
  };

  constructor(
    private authService: AuthService,
    private themeService: ThemeService,
    private router: Router
  ) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.updatePageTitle(event.urlAfterRedirects);
    });
  }

  ngOnInit(): void {
    this.themeService.darkMode$.subscribe(isDark => {
      this.isDarkMode = isDark;
    });
  }

  private updatePageTitle(url: string): void {
    // Buscar coincidencia exacta primero
    if (this.routeTitles[url]) {
      this.pageTitle = this.routeTitles[url];
      return;
    }
    // Buscar por prefijo
    for (const route of Object.keys(this.routeTitles)) {
      if (url.startsWith(route)) {
        this.pageTitle = this.routeTitles[route];
        return;
      }
    }
    this.pageTitle = 'Dashboard';
  }

  get currentUser(): Usuario | null {
    return this.authService.currentUser;
  }

  get unreadCount(): number {
    return this.notifications.filter(n => !n.read).length;
  }

  getUserInitials(): string {
    if (!this.currentUser) return '?';
    const nombre = this.currentUser.nombre || '';
    const apellido = this.currentUser.apellido || '';
    return (nombre.charAt(0) + apellido.charAt(0)).toUpperCase();
  }

  getPrimaryRole(): string {
    if (!this.currentUser?.roles?.length) return 'Usuario';
    const role = this.currentUser.roles[0];
    const roleNames: { [key: string]: string } = {
      'ADMINISTRADOR': 'Administrador',
      'OPERACIONES': 'Operaciones',
      'FINANZAS': 'Finanzas',
      'CONSULTA': 'Consulta'
    };
    return roleNames[role] || role;
  }

  toggleSearch(): void {
    this.searchOpen = !this.searchOpen;
    if (!this.searchOpen) {
      this.searchQuery = '';
    }
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      // Implementar búsqueda global
      console.log('Buscando:', this.searchQuery);
      // Por ahora, navegar a una página de búsqueda o filtrar
    }
  }

  toggleDarkMode(): void {
    this.themeService.toggleDarkMode();
  }

  markAsRead(notification: Notification): void {
    notification.read = true;
  }

  markAllAsRead(): void {
    this.notifications.forEach(n => n.read = true);
  }

  deleteNotification(notification: Notification, event: Event): void {
    event.stopPropagation();
    this.notifications = this.notifications.filter(n => n.id !== notification.id);
  }

  getNotificationIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'success': 'check_circle',
      'warning': 'warning',
      'error': 'error',
      'info': 'info'
    };
    return icons[type] || 'notifications';
  }

  logout(): void {
    this.authService.logout();
  }
}
