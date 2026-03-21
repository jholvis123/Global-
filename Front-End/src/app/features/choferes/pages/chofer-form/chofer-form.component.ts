import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { ChoferesService } from '../../services/choferes.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { CATEGORIAS_LICENCIA, ESTADOS_CHOFER } from '../../../../models';

@Component({
  selector: 'app-chofer-form',
  templateUrl: './chofer-form.component.html',
  styleUrls: ['./chofer-form.component.scss']
})
export class ChoferFormComponent implements OnInit {
  choferForm!: FormGroup;
  isEditing = false;
  isSubmitting = false;

  // Constantes para selects
  categoriasLicencia = CATEGORIAS_LICENCIA;
  estadosChofer = ESTADOS_CHOFER;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private choferesService: ChoferesService,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    this.initForm();
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.isEditing = true;
      this.loadChofer(+id);
    }
  }

  private initForm(): void {
    this.choferForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      ci: ['', Validators.required],
      telefono: [''],
      fecha_nacimiento: [null],
      direccion: [''],
      licencia_numero: ['', Validators.required],
      licencia_categoria: ['', Validators.required],
      licencia_vencimiento: [null, Validators.required],
      experiencia_anos: [0, [Validators.required, Validators.min(0)]],
      estado: ['ACTIVO'],
      observaciones: [''],
      contacto_emergencia_nombre: [''],
      contacto_emergencia_telefono: ['']
    });
  }

  private loadChofer(id: number): void {
    this.choferesService.getById(id).subscribe({
      next: (chofer) => this.choferForm.patchValue(chofer),
      error: () => {
        this.notification.error('Error al cargar el chofer');
        this.router.navigate(['/choferes']);
      }
    });
  }

  onSubmit(): void {
    if (this.choferForm.invalid) {
      this.choferForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    setTimeout(() => {
      this.isSubmitting = false;
      this.notification.success(this.isEditing ? 'Chofer actualizado' : 'Chofer creado');
      this.router.navigate(['/choferes']);
    }, 1000);
  }

  goBack(): void {
    this.router.navigate(['/choferes']);
  }
}
