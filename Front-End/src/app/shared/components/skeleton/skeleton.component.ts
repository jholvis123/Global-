import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-skeleton',
  templateUrl: './skeleton.component.html',
  styleUrls: ['./skeleton.component.scss']
})
export class SkeletonComponent {
  @Input() type: 'text' | 'title' | 'avatar' | 'thumbnail' | 'card' | 'table-row' | 'stat-card' = 'text';
  @Input() width: string = '100%';
  @Input() height: string = 'auto';
  @Input() count: number = 1;
  @Input() animated: boolean = true;

  get items(): number[] {
    return Array(this.count).fill(0);
  }
}
