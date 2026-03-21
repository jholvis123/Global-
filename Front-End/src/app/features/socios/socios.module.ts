import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';

import { SociosListComponent } from './pages/socios-list/socios-list.component';
import { SocioFormComponent } from './pages/socio-form/socio-form.component';
import { SocioDetailComponent } from './pages/socio-detail/socio-detail.component';
import { SociosService } from './services/socios.service';

const routes: Routes = [
  { path: '', component: SociosListComponent },
  { path: 'nuevo', component: SocioFormComponent },
  { path: ':id', component: SocioDetailComponent },
  { path: ':id/editar', component: SocioFormComponent }
];

@NgModule({
  declarations: [SociosListComponent, SocioFormComponent, SocioDetailComponent],
  imports: [SharedModule, RouterModule.forChild(routes)],
  providers: [SociosService]
})
export class SociosModule { }
