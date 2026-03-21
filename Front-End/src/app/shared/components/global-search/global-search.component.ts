import { Component, OnInit, OnDestroy, ElementRef, ViewChild, HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { Subject, Subscription } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { SearchService, SearchResult } from '../../../core/services/search.service';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-global-search',
  templateUrl: './global-search.component.html',
  styleUrls: ['./global-search.component.scss'],
  animations: [
    trigger('slideDown', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(-10px)' }),
        animate('200ms ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
      ]),
      transition(':leave', [
        animate('150ms ease-in', style({ opacity: 0, transform: 'translateY(-10px)' }))
      ])
    ])
  ]
})
export class GlobalSearchComponent implements OnInit, OnDestroy {
  @ViewChild('searchInput') searchInput!: ElementRef<HTMLInputElement>;
  
  isOpen = false;
  searchTerm = '';
  results: SearchResult[] = [];
  isLoading = false;
  selectedIndex = -1;
  
  private searchSubject = new Subject<string>();
  private subscriptions = new Subscription();

  constructor(
    private searchService: SearchService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Suscribirse a los cambios de búsqueda
    this.subscriptions.add(
      this.searchSubject.pipe(
        debounceTime(300),
        distinctUntilChanged(),
        switchMap(term => {
          this.isLoading = true;
          return this.searchService.search(term);
        })
      ).subscribe(results => {
        this.results = results;
        this.isLoading = false;
        this.selectedIndex = -1;
      })
    );

    // Suscribirse al estado del search
    this.subscriptions.add(
      this.searchService.isOpen$.subscribe(isOpen => {
        this.isOpen = isOpen;
        if (isOpen) {
          setTimeout(() => this.searchInput?.nativeElement?.focus(), 100);
        }
      })
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  @HostListener('document:keydown', ['$event'])
  handleKeydown(event: KeyboardEvent): void {
    // Ctrl+K o Cmd+K para abrir búsqueda
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
      event.preventDefault();
      this.toggleSearch();
    }

    // Escape para cerrar
    if (event.key === 'Escape' && this.isOpen) {
      this.closeSearch();
    }

    // Navegación con flechas
    if (this.isOpen && this.results.length > 0) {
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        this.selectedIndex = Math.min(this.selectedIndex + 1, this.results.length - 1);
      } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
      } else if (event.key === 'Enter' && this.selectedIndex >= 0) {
        event.preventDefault();
        this.selectResult(this.results[this.selectedIndex]);
      }
    }
  }

  toggleSearch(): void {
    this.searchService.toggleSearch();
  }

  openSearch(): void {
    this.searchService.openSearch();
  }

  closeSearch(): void {
    this.searchService.closeSearch();
    this.searchTerm = '';
    this.results = [];
    this.selectedIndex = -1;
  }

  onSearchInput(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.searchTerm = target.value;
    this.searchSubject.next(this.searchTerm);
  }

  selectResult(result: SearchResult): void {
    this.router.navigate([result.route]);
    this.closeSearch();
  }

  getTypeLabel(type: SearchResult['type']): string {
    return this.searchService.getTypeLabel(type);
  }

  getTypeColor(type: SearchResult['type']): string {
    return this.searchService.getTypeColor(type);
  }

  onBackdropClick(): void {
    this.closeSearch();
  }
}
