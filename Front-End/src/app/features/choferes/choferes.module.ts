import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';

import { ChoferesListComponent } from './pages/choferes-list/choferes-list.component';
import { ChoferFormComponent } from './pages/chofer-form/chofer-form.component';
import { ChoferesService } from './services/choferes.service';

const routes: Routes = [
  { path: '', component: ChoferesListComponent },
  { path: 'nuevo', component: ChoferFormComponent },
  { path: ':id/editar', component: ChoferFormComponent }
];

@NgModule({
  declarations: [ChoferesListComponent, ChoferFormComponent],
  imports: [SharedModule, RouterModule.forChild(routes)],
  providers: [ChoferesService]
})
export class ChoferesModule { }
