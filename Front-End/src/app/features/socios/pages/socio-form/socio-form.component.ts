import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { SociosService } from '../../services/socios.service';
import { NotificationService } from '../../../../core/services/notification.service';

@Component({
  selector: 'app-socio-form',
  templateUrl: './socio-form.component.html',
  styleUrls: ['./socio-form.component.scss']
})
export class SocioFormComponent implements OnInit {
  socioForm!: FormGroup;
  isEditing = false;
  isSubmitting = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private sociosService: SociosService,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    this.initForm();
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.isEditing = true;
      this.loadSocio(+id);
    }
  }

  private initForm(): void {
    this.socioForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      ci: ['', Validators.required],
      telefono: ['', Validators.required],
      direccion: [''],
      email: ['', Validators.email],
      porcentaje_ganancia: [70, [Validators.required, Validators.min(0), Validators.max(100)]],
      banco: [''],
      cuenta_bancaria: [''],
      estado: ['ACTIVO'],
      fecha_ingreso: [new Date()],
      observaciones: ['']
    });
  }

  private loadSocio(id: number): void {
    this.sociosService.getById(id).subscribe({
      next: (socio) => this.socioForm.patchValue(socio),
      error: () => {
        this.notification.error('Error al cargar el socio');
        this.router.navigate(['/socios']);
      }
    });
  }

  onSubmit(): void {
    if (this.socioForm.invalid) {
      this.socioForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    setTimeout(() => {
      this.isSubmitting = false;
      this.notification.success(this.isEditing ? 'Socio actualizado' : 'Socio creado');
      this.router.navigate(['/socios']);
    }, 1000);
  }

  goBack(): void {
    this.router.navigate(['/socios']);
  }
}
