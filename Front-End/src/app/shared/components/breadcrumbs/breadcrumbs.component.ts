import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { filter, distinctUntilChanged } from 'rxjs/operators';

export interface Breadcrumb {
  label: string;
  url: string;
  icon?: string;
}

@Component({
  selector: 'app-breadcrumbs',
  templateUrl: './breadcrumbs.component.html',
  styleUrls: ['./breadcrumbs.component.scss']
})
export class BreadcrumbsComponent implements OnInit {
  breadcrumbs: Breadcrumb[] = [];

  private routeLabels: { [key: string]: { label: string; icon: string } } = {
    'app': { label: 'Inicio', icon: 'home' },
    'dashboard': { label: 'Dashboard', icon: 'dashboard' },
    'viajes': { label: 'Viajes', icon: 'local_shipping' },
    'vehiculos': { label: 'Vehículos', icon: 'directions_car' },
    'choferes': { label: 'Choferes', icon: 'badge' },
    'socios': { label: 'Socios', icon: 'groups' },
    'clientes': { label: 'Clientes', icon: 'business' },
    'anticipos': { label: 'Anticipos', icon: 'payments' },
    'liquidaciones': { label: 'Liquidaciones', icon: 'receipt_long' },
    'mantenimientos': { label: 'Mantenimientos', icon: 'build' },
    'reportes': { label: 'Reportes', icon: 'assessment' },
    'usuarios': { label: 'Usuarios', icon: 'manage_accounts' },
    'perfil': { label: 'Mi Perfil', icon: 'person' },
    'configuracion': { label: 'Configuración', icon: 'settings' },
    'nuevo': { label: 'Nuevo', icon: 'add' },
    'editar': { label: 'Editar', icon: 'edit' },
    'detalle': { label: 'Detalle', icon: 'visibility' }
  };

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.buildBreadcrumbs();
    
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd),
      distinctUntilChanged()
    ).subscribe(() => {
      this.buildBreadcrumbs();
    });
  }

  private buildBreadcrumbs(): void {
    const url = this.router.url;
    const segments = url.split('/').filter(segment => segment && !segment.startsWith('?'));
    
    this.breadcrumbs = [];
    let currentPath = '';

    segments.forEach((segment, index) => {
      currentPath += `/${segment}`;
      
      const routeInfo = this.routeLabels[segment.toLowerCase()];
      
      // Si es un ID (número o UUID), usar etiqueta genérica
      const isId = /^[0-9]+$/.test(segment) || /^[a-f0-9-]{36}$/i.test(segment);
      
      if (routeInfo || isId) {
        this.breadcrumbs.push({
          label: isId ? `#${segment.substring(0, 8)}` : routeInfo.label,
          url: currentPath,
          icon: isId ? 'tag' : routeInfo?.icon
        });
      }
    });
  }

  navigateTo(breadcrumb: Breadcrumb): void {
    if (breadcrumb.url !== this.router.url) {
      this.router.navigateByUrl(breadcrumb.url);
    }
  }
}
