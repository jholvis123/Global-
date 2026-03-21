import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { ClientesService } from '../../services/clientes.service';
import { NotificationService } from '../../../../core/services/notification.service';

@Component({
  selector: 'app-cliente-form',
  templateUrl: './cliente-form.component.html',
  styleUrls: ['./cliente-form.component.scss']
})
export class ClienteFormComponent implements OnInit {
  clienteForm!: FormGroup;
  isEditing = false;
  isSubmitting = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private clientesService: ClientesService,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    this.initForm();
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.isEditing = true;
      this.loadCliente(+id);
    }
  }

  private initForm(): void {
    this.clienteForm = this.fb.group({
      razon_social: ['', Validators.required],
      nit: [''],
      rubro: [''],
      ciudad: [''],
      direccion: [''],
      contacto_nombre: [''],
      telefono: [''],
      celular: [''],
      email: ['', Validators.email],
      dias_credito: [0],
      limite_credito: [0],
      estado: ['ACTIVO'],
      observaciones: ['']
    });
  }

  private loadCliente(id: number): void {
    this.clientesService.getById(id).subscribe({
      next: (cliente) => this.clienteForm.patchValue(cliente),
      error: () => {
        this.notification.error('Error al cargar el cliente');
        this.router.navigate(['/clientes']);
      }
    });
  }

  onSubmit(): void {
    if (this.clienteForm.invalid) {
      this.clienteForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    setTimeout(() => {
      this.isSubmitting = false;
      this.notification.success(this.isEditing ? 'Cliente actualizado' : 'Cliente creado');
      this.router.navigate(['/clientes']);
    }, 1000);
  }

  goBack(): void {
    this.router.navigate(['/clientes']);
  }
}
