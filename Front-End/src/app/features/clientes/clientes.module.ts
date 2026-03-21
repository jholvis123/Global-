import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';

import { ClientesListComponent } from './pages/clientes-list/clientes-list.component';
import { ClienteFormComponent } from './pages/cliente-form/cliente-form.component';
import { ClientesService } from './services/clientes.service';

const routes: Routes = [
  { path: '', component: ClientesListComponent },
  { path: 'nuevo', component: ClienteFormComponent },
  { path: ':id/editar', component: ClienteFormComponent }
];

@NgModule({
  declarations: [ClientesListComponent, ClienteFormComponent],
  imports: [SharedModule, RouterModule.forChild(routes)],
  providers: [ClientesService]
})
export class ClientesModule { }
