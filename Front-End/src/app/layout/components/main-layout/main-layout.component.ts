import { Component, OnInit, ViewChild } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { MatSidenav } from '@angular/material/sidenav';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { LoadingService } from '../../../core/services/loading.service';

@Component({
  selector: 'app-main-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.scss']
})
export class MainLayoutComponent implements OnInit {
  @ViewChild('drawer') drawer!: MatSidenav;
  
  isHandset$: Observable<boolean>;
  loading$: Observable<boolean>;

  constructor(
    private breakpointObserver: BreakpointObserver,
    private loadingService: LoadingService
  ) {
    this.isHandset$ = this.breakpointObserver.observe(Breakpoints.Handset)
      .pipe(
        map(result => result.matches),
        shareReplay()
      );
    
    this.loading$ = this.loadingService.loading$;
  }

  ngOnInit(): void {}

  onMenuItemClick(): void {
    this.isHandset$.subscribe(isHandset => {
      if (isHandset) {
        this.drawer.close();
      }
    });
  }
}
