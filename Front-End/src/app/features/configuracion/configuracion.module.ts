import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatDividerModule } from '@angular/material/divider';

import { ConfiguracionPageComponent } from './pages/configuracion-page/configuracion-page.component';

const routes: Routes = [
  { path: '', component: ConfiguracionPageComponent }
];

@NgModule({
  declarations: [
    ConfiguracionPageComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes),
    MatIconModule,
    MatButtonModule,
    MatSlideToggleModule,
    MatDividerModule
  ]
})
export class ConfiguracionModule { }
