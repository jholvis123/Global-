import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { NgChartsModule } from 'ng2-charts';

import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { KpiCardComponent } from './components/kpi-card/kpi-card.component';
import { ChartCardComponent } from './components/chart-card/chart-card.component';
import { RecentTripsComponent } from './components/recent-trips/recent-trips.component';
import { AlertsWidgetComponent } from './components/alerts-widget/alerts-widget.component';

import { DashboardService } from './services/dashboard.service';

const routes: Routes = [
  { path: '', component: DashboardComponent }
];

@NgModule({
  declarations: [
    DashboardComponent,
    KpiCardComponent,
    ChartCardComponent,
    RecentTripsComponent,
    AlertsWidgetComponent
  ],
  imports: [
    SharedModule,
    NgChartsModule,
    RouterModule.forChild(routes)
  ],
  providers: [DashboardService]
})
export class DashboardModule { }
