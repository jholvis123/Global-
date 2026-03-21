import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

// Angular Material Modules
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatMenuModule } from '@angular/material/menu';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatRadioModule } from '@angular/material/radio';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule } from '@angular/material/chips';
import { MatBadgeModule } from '@angular/material/badge';
import { MatTabsModule } from '@angular/material/tabs';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatDividerModule } from '@angular/material/divider';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

// Components
import { LoadingSpinnerComponent } from './components/loading-spinner/loading-spinner.component';
import { ConfirmDialogComponent } from './components/confirm-dialog/confirm-dialog.component';
import { PageHeaderComponent } from './components/page-header/page-header.component';
import { EmptyStateComponent } from './components/empty-state/empty-state.component';
import { StatusBadgeComponent } from './components/status-badge/status-badge.component';
import { FormModalComponent } from './components/form-modal/form-modal.component';
import { BreadcrumbsComponent } from './components/breadcrumbs/breadcrumbs.component';
import { SkeletonComponent } from './components/skeleton/skeleton.component';
import { GlobalSearchComponent } from './components/global-search/global-search.component';
import { TourOverlayComponent } from './components/tour-overlay/tour-overlay.component';

// Pipes
import { CurrencyBsPipe } from './pipes/currency-bs.pipe';
import { DateFormatPipe } from './pipes/date-format.pipe';
import { TruncatePipe } from './pipes/truncate.pipe';

// Directives
import { HasRoleDirective } from './directives/has-role.directive';

const MATERIAL_MODULES = [
  MatButtonModule,
  MatIconModule,
  MatInputModule,
  MatFormFieldModule,
  MatCardModule,
  MatTableModule,
  MatPaginatorModule,
  MatSortModule,
  MatDialogModule,
  MatSnackBarModule,
  MatProgressSpinnerModule,
  MatProgressBarModule,
  MatMenuModule,
  MatToolbarModule,
  MatSidenavModule,
  MatListModule,
  MatSelectModule,
  MatDatepickerModule,
  MatNativeDateModule,
  MatCheckboxModule,
  MatRadioModule,
  MatTooltipModule,
  MatChipsModule,
  MatBadgeModule,
  MatTabsModule,
  MatExpansionModule,
  MatDividerModule,
  MatAutocompleteModule,
  MatSlideToggleModule
];

const COMPONENTS = [
  LoadingSpinnerComponent,
  ConfirmDialogComponent,
  PageHeaderComponent,
  EmptyStateComponent,
  StatusBadgeComponent,
  FormModalComponent,
  BreadcrumbsComponent,
  SkeletonComponent,
  GlobalSearchComponent,
  TourOverlayComponent
];

const PIPES = [
  CurrencyBsPipe,
  DateFormatPipe,
  TruncatePipe
];

const DIRECTIVES = [
  HasRoleDirective
];

@NgModule({
  declarations: [
    ...COMPONENTS,
    ...PIPES,
    ...DIRECTIVES
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    ...MATERIAL_MODULES
  ],
  exports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    ...MATERIAL_MODULES,
    ...COMPONENTS,
    ...PIPES,
    ...DIRECTIVES
  ]
})
export class SharedModule { }
