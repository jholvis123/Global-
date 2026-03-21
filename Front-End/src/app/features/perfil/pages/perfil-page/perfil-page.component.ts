import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../../core/services/auth.service';
import { NotificationService } from '../../../../core/services/notification.service';

@Component({
  selector: 'app-perfil-page',
  templateUrl: './perfil-page.component.html',
  styleUrls: ['./perfil-page.component.scss']
})
export class PerfilPageComponent implements OnInit {
  perfilForm!: FormGroup;
  passwordForm!: FormGroup;
  isLoading = false;
  isSaving = false;
  hideCurrentPassword = true;
  hideNewPassword = true;
  hideConfirmPassword = true;
  
  user: any;
  avatarInitials = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    this.user = this.authService.currentUser;
    this.avatarInitials = this.getInitials(this.user?.nombre || 'Usuario');
    
    this.perfilForm = this.fb.group({
      nombre: [this.user?.nombre || '', [Validators.required, Validators.minLength(3)]],
      email: [this.user?.email || '', [Validators.required, Validators.email]],
      telefono: [this.user?.telefono || ''],
      cargo: [{ value: this.user?.rol || '', disabled: true }]
    });

    this.passwordForm = this.fb.group({
      currentPassword: ['', [Validators.required]],
      newPassword: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });
  }

  getInitials(name: string): string {
    return name.split(' ')
      .map(n => n[0])
      .join('')
      .substring(0, 2)
      .toUpperCase();
  }

  passwordMatchValidator(form: FormGroup) {
    const newPassword = form.get('newPassword')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    
    if (newPassword !== confirmPassword) {
      form.get('confirmPassword')?.setErrors({ mismatch: true });
      return { mismatch: true };
    }
    return null;
  }

  saveProfile(): void {
    if (this.perfilForm.invalid) return;

    this.isSaving = true;
    
    // Simular guardado (conectar con backend real)
    setTimeout(() => {
      this.isSaving = false;
      this.notification.success('Perfil actualizado correctamente');
    }, 1000);
  }

  changePassword(): void {
    if (this.passwordForm.invalid) return;

    this.isSaving = true;

    // Simular cambio de contraseña (conectar con backend real)
    setTimeout(() => {
      this.isSaving = false;
      this.passwordForm.reset();
      this.notification.success('Contraseña cambiada correctamente');
    }, 1000);
  }

  getRoleBadgeClass(): string {
    const role = this.user?.rol?.toLowerCase();
    switch (role) {
      case 'admin': return 'badge--admin';
      case 'operador': return 'badge--operator';
      case 'contador': return 'badge--accountant';
      default: return 'badge--default';
    }
  }
}
