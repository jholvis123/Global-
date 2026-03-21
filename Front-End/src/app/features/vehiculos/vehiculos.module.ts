import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';

import { VehiculosListComponent } from './pages/vehiculos-list/vehiculos-list.component';
import { VehiculoFormComponent } from './pages/vehiculo-form/vehiculo-form.component';
import { VehiculosService } from './services/vehiculos.service';

const routes: Routes = [
  { path: '', component: VehiculosListComponent },
  { path: 'nuevo', component: VehiculoFormComponent },
  { path: ':id/editar', component: VehiculoFormComponent }
];

@NgModule({
  declarations: [
    VehiculosListComponent,
    VehiculoFormComponent
  ],
  imports: [
    SharedModule,
    RouterModule.forChild(routes)
  ],
  providers: [VehiculosService]
})
export class VehiculosModule { }
