import { Component, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';
import { trigger, transition, style, animate } from '@angular/animations';
import { AuthService } from '../../../core/services/auth.service';

interface MenuItem {
  label: string;
  icon: string;
  route?: string;
  roles?: string[];
  children?: MenuItem[];
  expanded?: boolean;
}

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
  animations: [
    trigger('submenuAnimation', [
      transition(':enter', [
        style({ height: 0, opacity: 0 }),
        animate('200ms ease-out', style({ height: '*', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('200ms ease-in', style({ height: 0, opacity: 0 }))
      ])
    ])
  ]
})
export class SidebarComponent {
  @Output() menuItemClick = new EventEmitter<void>();

  menuItems: MenuItem[] = [
    { 
      label: 'Dashboard', 
      icon: 'dashboard', 
      route: '/app/dashboard' 
    },
    { 
      label: 'Viajes', 
      icon: 'route', 
      route: '/app/viajes'
    },
    { 
      label: 'Vehiculos', 
      icon: 'local_shipping', 
      route: '/app/vehiculos'
    },
    { 
      label: 'Choferes', 
      icon: 'badge', 
      route: '/app/choferes'
    },
    { 
      label: 'Socios', 
      icon: 'handshake', 
      route: '/app/socios'
    },
    { 
      label: 'Clientes', 
      icon: 'business', 
      route: '/app/clientes'
    },
    { 
      label: 'Anticipos', 
      icon: 'payments', 
      route: '/app/anticipos'
    },
    { 
      label: 'Liquidaciones', 
      icon: 'receipt_long', 
      route: '/app/liquidaciones'
    },
    { 
      label: 'Mantenimientos', 
      icon: 'build', 
      route: '/app/mantenimientos'
    },
    { 
      label: 'Reportes', 
      icon: 'analytics', 
      route: '/app/reportes'
    },
    { 
      label: 'Chatbot', 
      icon: 'chat', 
      route: '/app/chatbot'
    },
    { 
      label: 'Configuración', 
      icon: 'settings', 
      route: '/app/configuracion'
    }
  ];

  constructor(private authService: AuthService) {}

  hasAccess(roles?: string[]): boolean {
    // Si no hay roles definidos, acceso libre
    if (!roles || roles.length === 0) {
      return true;
    }
    
    // Si el usuario está autenticado, verificar roles
    const user = this.authService.currentUser;
    if (!user) {
      // En desarrollo, mostrar todos los menús si hay un token
      return !!localStorage.getItem('access_token');
    }
    
    // Obtener roles del usuario (manejar tanto array como string)
    let userRoles: string[] = [];
    if (Array.isArray(user.roles)) {
      userRoles = user.roles;
    } else if (typeof user.roles === 'string') {
      userRoles = [user.roles];
    } else if ((user as any).rol) {
      userRoles = Array.isArray((user as any).rol) ? (user as any).rol : [(user as any).rol];
    }
    
    // Si no tiene roles pero está autenticado, dar acceso (desarrollo)
    if (userRoles.length === 0) {
      return true;
    }
    
    return roles.some(role => userRoles.includes(role));
  }

  toggleSubmenu(item: MenuItem): void {
    item.expanded = !item.expanded;
  }

  onItemClick(): void {
    this.menuItemClick.emit();
  }
}
