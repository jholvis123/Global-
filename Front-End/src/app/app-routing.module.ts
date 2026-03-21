import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainLayoutComponent } from './layout/components/main-layout/main-layout.component';
import { AuthGuard } from './core/guards/auth.guard';

const routes: Routes = [
  // Landing Page (página principal pública)
  {
    path: '',
    pathMatch: 'full',
    loadChildren: () => import('./features/landing/landing.module').then(m => m.LandingModule)
  },

  // Rutas públicas (login)
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.module').then(m => m.AuthModule)
  },

  // Rutas protegidas con AuthGuard
  {
    path: 'app',
    component: MainLayoutComponent,
    canActivate: [AuthGuard],
    canActivateChild: [AuthGuard],
    children: [
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      },
      {
        path: 'dashboard',
        loadChildren: () => import('./features/dashboard/dashboard.module').then(m => m.DashboardModule)
      },
      {
        path: 'viajes',
        loadChildren: () => import('./features/viajes/viajes.module').then(m => m.ViajesModule)
      },
      {
        path: 'vehiculos',
        loadChildren: () => import('./features/vehiculos/vehiculos.module').then(m => m.VehiculosModule)
      },
      {
        path: 'choferes',
        loadChildren: () => import('./features/choferes/choferes.module').then(m => m.ChoferesModule)
      },
      {
        path: 'clientes',
        loadChildren: () => import('./features/clientes/clientes.module').then(m => m.ClientesModule)
      },
      {
        path: 'socios',
        loadChildren: () => import('./features/socios/socios.module').then(m => m.SociosModule)
      },
      {
        path: 'anticipos',
        loadChildren: () => import('./features/anticipos/anticipos.module').then(m => m.AnticiposModule)
      },
      {
        path: 'liquidaciones',
        loadChildren: () => import('./features/liquidaciones/liquidaciones.module').then(m => m.LiquidacionesModule)
      },
      {
        path: 'mantenimientos',
        loadChildren: () => import('./features/mantenimientos/mantenimientos.module').then(m => m.MantenimientosModule)
      },
      {
        path: 'reportes',
        loadChildren: () => import('./features/reportes/reportes.module').then(m => m.ReportesModule)
      },
      {
        path: 'perfil',
        loadChildren: () => import('./features/perfil/perfil.module').then(m => m.PerfilModule)
      },
      {
        path: 'configuracion',
        loadChildren: () => import('./features/configuracion/configuracion.module').then(m => m.ConfiguracionModule)
      },
      {
        path: 'chatbot',
        loadChildren: () => import('./features/chatbot/chatbot.module').then(m => m.ChatbotModule)
      }
    ]
  },

  // Página 404
  {
    path: '**',
    loadChildren: () => import('./features/not-found/not-found.module').then(m => m.NotFoundModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
    anchorScrolling: 'enabled'
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
