import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { OnboardingService, TourStep, Tour } from '../../../core/services/onboarding.service';

@Component({
  selector: 'app-tour-overlay',
  templateUrl: './tour-overlay.component.html',
  styleUrls: ['./tour-overlay.component.scss']
})
export class TourOverlayComponent implements OnInit, OnDestroy {
  isActive = false;
  currentStep: TourStep | null = null;
  currentStepIndex = 0;
  totalSteps = 0;
  tour: Tour | null = null;
  
  tooltipStyle: { [key: string]: string } = {};
  highlightStyle: { [key: string]: string } = {};
  
  private subscriptions = new Subscription();

  constructor(private onboardingService: OnboardingService) {}

  ngOnInit(): void {
    this.subscriptions.add(
      this.onboardingService.isActive$.subscribe(active => {
        this.isActive = active;
        if (active) {
          this.updatePosition();
        }
      })
    );

    this.subscriptions.add(
      this.onboardingService.currentTour$.subscribe(tour => {
        this.tour = tour;
        this.totalSteps = tour?.steps.length || 0;
      })
    );

    this.subscriptions.add(
      this.onboardingService.currentStep$.subscribe(stepIndex => {
        this.currentStepIndex = stepIndex;
        this.currentStep = this.onboardingService.getCurrentStep();
        if (this.isActive) {
          setTimeout(() => this.updatePosition(), 100);
        }
      })
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  updatePosition(): void {
    if (!this.currentStep) return;

    const element = document.querySelector(this.currentStep.target);
    if (!element) {
      console.warn(`Element not found: ${this.currentStep.target}`);
      return;
    }

    const rect = element.getBoundingClientRect();
    const padding = 8;

    // Highlight position
    this.highlightStyle = {
      top: `${rect.top - padding}px`,
      left: `${rect.left - padding}px`,
      width: `${rect.width + padding * 2}px`,
      height: `${rect.height + padding * 2}px`
    };

    // Tooltip position
    const tooltipWidth = 320;
    const tooltipHeight = 180;
    let top = 0;
    let left = 0;

    switch (this.currentStep.position) {
      case 'top':
        top = rect.top - tooltipHeight - 20;
        left = rect.left + (rect.width / 2) - (tooltipWidth / 2);
        break;
      case 'bottom':
        top = rect.bottom + 20;
        left = rect.left + (rect.width / 2) - (tooltipWidth / 2);
        break;
      case 'left':
        top = rect.top + (rect.height / 2) - (tooltipHeight / 2);
        left = rect.left - tooltipWidth - 20;
        break;
      case 'right':
        top = rect.top + (rect.height / 2) - (tooltipHeight / 2);
        left = rect.right + 20;
        break;
    }

    // Keep tooltip in viewport
    left = Math.max(20, Math.min(left, window.innerWidth - tooltipWidth - 20));
    top = Math.max(20, Math.min(top, window.innerHeight - tooltipHeight - 20));

    this.tooltipStyle = {
      top: `${top}px`,
      left: `${left}px`
    };
  }

  next(): void {
    this.onboardingService.nextStep();
  }

  previous(): void {
    this.onboardingService.previousStep();
  }

  skip(): void {
    this.onboardingService.skipTour();
  }

  get progress(): number {
    return this.totalSteps > 0 ? ((this.currentStepIndex + 1) / this.totalSteps) * 100 : 0;
  }
}
