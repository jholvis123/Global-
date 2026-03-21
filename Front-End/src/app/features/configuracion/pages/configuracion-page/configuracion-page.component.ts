import { Component, OnInit } from '@angular/core';
import { ThemeService } from '../../../../core/services/theme.service';

@Component({
  selector: 'app-configuracion-page',
  templateUrl: './configuracion-page.component.html',
  styleUrls: ['./configuracion-page.component.scss']
})
export class ConfiguracionPageComponent implements OnInit {
  isDarkMode = false;
  
  settings = {
    notifications: {
      email: true,
      push: false,
      weekly: true,
      alerts: true
    },
    display: {
      compactMode: false,
      animations: true,
      showAvatars: true
    },
    privacy: {
      showOnline: true,
      publicProfile: false
    }
  };

  constructor(private themeService: ThemeService) {}

  ngOnInit(): void {
    this.isDarkMode = this.themeService.isDarkMode();
  }

  toggleDarkMode(): void {
    this.isDarkMode = !this.isDarkMode;
    this.themeService.setDarkMode(this.isDarkMode);
  }

  saveSettings(): void {
    // Guardar en localStorage o backend
    localStorage.setItem('app_settings', JSON.stringify(this.settings));
  }
}
