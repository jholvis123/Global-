import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';
import { NotificationService } from '../../../../core/services/notification.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  hidePassword = true;
  isLoading = false;
  emailFocused = false;
  passwordFocused = false;

  features = [
    { icon: 'local_shipping', title: 'Gestión de Flota', desc: 'Control total de tus vehículos' },
    { icon: 'route', title: 'Tracking de Viajes', desc: 'Seguimiento en tiempo real' },
    { icon: 'analytics', title: 'Reportes Avanzados', desc: 'Métricas y análisis detallados' },
    { icon: 'payments', title: 'Liquidaciones', desc: 'Gestión financiera automatizada' }
  ];

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private notification: NotificationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
      rememberMe: [false]
    });
  }

  fillTestUser(email: string, password: string): void {
    this.loginForm.patchValue({ email, password });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.isLoading = true;

    this.authService.login(this.loginForm.value).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.notification.success(`Bienvenido, ${response.usuario.nombre}!`);
        
        // Redirigir a la URL guardada o al dashboard
        const redirectUrl = sessionStorage.getItem('redirectUrl') || '/app/dashboard';
        sessionStorage.removeItem('redirectUrl');
        this.router.navigate([redirectUrl]);
      },
      error: (error) => {
        this.isLoading = false;
        // El error ya se muestra por el interceptor
      }
    });
  }
}
