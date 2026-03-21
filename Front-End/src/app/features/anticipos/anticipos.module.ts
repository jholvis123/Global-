import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';

import { AnticiposListComponent } from './pages/anticipos-list/anticipos-list.component';
import { AnticipoFormComponent } from './pages/anticipo-form/anticipo-form.component';

const routes: Routes = [
  { path: '', component: AnticiposListComponent },
  { path: 'nuevo', component: AnticipoFormComponent },
  { path: ':id/editar', component: AnticipoFormComponent }
];

@NgModule({
  declarations: [
    AnticiposListComponent,
    AnticipoFormComponent
  ],
  imports: [
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class AnticiposModule { }
