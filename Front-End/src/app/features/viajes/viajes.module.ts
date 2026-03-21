import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';

import { ViajesListComponent } from './pages/viajes-list/viajes-list.component';
import { ViajeFormComponent } from './pages/viaje-form/viaje-form.component';
import { ViajeDetailComponent } from './pages/viaje-detail/viaje-detail.component';
import { GastoDialogComponent } from './components/gasto-dialog/gasto-dialog.component';

import { ViajesService } from './services/viajes.service';

const routes: Routes = [
  { path: '', component: ViajesListComponent },
  { path: 'nuevo', component: ViajeFormComponent },
  { path: ':id', component: ViajeDetailComponent },
  { path: ':id/editar', component: ViajeFormComponent }
];

@NgModule({
  declarations: [
    ViajesListComponent,
    ViajeFormComponent,
    ViajeDetailComponent,
    GastoDialogComponent
  ],
  imports: [
    SharedModule,
    RouterModule.forChild(routes)
  ],
  providers: [ViajesService]
})
export class ViajesModule { }
