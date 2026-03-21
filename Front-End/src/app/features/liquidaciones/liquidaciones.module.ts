import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';

import { LiquidacionesListComponent } from './pages/liquidaciones-list/liquidaciones-list.component';
import { LiquidacionFormComponent } from './pages/liquidacion-form/liquidacion-form.component';
import { LiquidacionDetailComponent } from './pages/liquidacion-detail/liquidacion-detail.component';

const routes: Routes = [
  { path: '', component: LiquidacionesListComponent },
  { path: 'nuevo', component: LiquidacionFormComponent },
  { path: ':id', component: LiquidacionDetailComponent },
  { path: ':id/editar', component: LiquidacionFormComponent }
];

@NgModule({
  declarations: [
    LiquidacionesListComponent,
    LiquidacionFormComponent,
    LiquidacionDetailComponent
  ],
  imports: [
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class LiquidacionesModule { }
