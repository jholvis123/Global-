import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NotificationService } from '../../../../core/services/notification.service';

@Component({
  selector: 'app-anticipo-form',
  templateUrl: './anticipo-form.component.html',
  styleUrls: ['./anticipo-form.component.scss']
})
export class AnticipoFormComponent implements OnInit {
  form!: FormGroup;
  isEditing = false;
  isLoading = false;
  anticipoId: number | null = null;

  choferes = [
    { id: 1, nombre: 'Juan Pérez' },
    { id: 2, nombre: 'Carlos Mendoza' },
    { id: 3, nombre: 'Miguel Rodríguez' },
    { id: 4, nombre: 'Pedro Sánchez' }
  ];

  viajes = [
    { id: 1, codigo: 'VJ-2026-001', ruta: 'Santa Cruz - La Paz' },
    { id: 2, codigo: 'VJ-2026-002', ruta: 'Cochabamba - Oruro' },
    { id: 3, codigo: 'VJ-2026-003', ruta: 'Sucre - Potosí' }
  ];

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    this.initForm();
    
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.isEditing = true;
      this.anticipoId = +id;
      this.loadAnticipo(this.anticipoId);
    }
  }

  initForm(): void {
    this.form = this.fb.group({
      choferId: [null, Validators.required],
      viajeId: [null],
      monto: [null, [Validators.required, Validators.min(1)]],
      motivo: ['', [Validators.required, Validators.maxLength(500)]],
      observaciones: ['']
    });
  }

  loadAnticipo(id: number): void {
    // Simular carga de datos
    this.isLoading = true;
    setTimeout(() => {
      this.form.patchValue({
        choferId: 1,
        viajeId: 1,
        monto: 500,
        motivo: 'Gastos de combustible',
        observaciones: ''
      });
      this.isLoading = false;
    }, 500);
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    
    setTimeout(() => {
      this.isLoading = false;
      this.notification.success(
        this.isEditing ? 'Anticipo actualizado correctamente' : 'Anticipo creado correctamente'
      );
      this.router.navigate(['/app/anticipos']);
    }, 1000);
  }

  cancel(): void {
    this.router.navigate(['/app/anticipos']);
  }
}
