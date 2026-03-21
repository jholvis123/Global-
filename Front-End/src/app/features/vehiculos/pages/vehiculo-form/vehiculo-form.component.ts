import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { VehiculosService } from '../../services/vehiculos.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { MARCAS_VEHICULO, ESTADOS_VEHICULO } from '../../../../models';

@Component({
  selector: 'app-vehiculo-form',
  templateUrl: './vehiculo-form.component.html',
  styleUrls: ['./vehiculo-form.component.scss']
})
export class VehiculoFormComponent implements OnInit {
  vehiculoForm!: FormGroup;
  isEditing = false;
  isSubmitting = false;
  vehiculoId: number | null = null;
  socios: any[] = [];

  // Constantes para selects
  marcasVehiculo = MARCAS_VEHICULO;
  estadosVehiculo = ESTADOS_VEHICULO;
  tiposCombustible = [
    { value: 'DIESEL', label: 'Diesel' },
    { value: 'GASOLINA', label: 'Gasolina' },
    { value: 'GNV', label: 'GNV' }
  ];

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private vehiculosService: VehiculosService,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.loadSocios();

    const id = this.route.snapshot.params['id'];
    if (id) {
      this.isEditing = true;
      this.vehiculoId = +id;
      this.loadVehiculo(this.vehiculoId);
    }
  }

  private initForm(): void {
    this.vehiculoForm = this.fb.group({
      placa: ['', [Validators.required, Validators.pattern(/^[A-Z]{3}-\d{3}$/)]],
      marca: ['', Validators.required],
      modelo: ['', Validators.required],
      anio: [new Date().getFullYear(), [Validators.required, Validators.min(1990), Validators.max(new Date().getFullYear() + 1)]],
      capacidad_ton: [null, [Validators.required, Validators.min(1)]],
      tipo_combustible: ['DIESEL'],
      socio_id: [null, Validators.required],
      numero_motor: [''],
      numero_chasis: [''],
      soat_vencimiento: [null],
      inspeccion_vencimiento: [null],
      estado: ['ACTIVO'],
      observaciones: ['']
    });
  }

  private loadSocios(): void {
    // Mock data
    this.socios = [
      { id: 1, nombre: 'Juan', apellido: 'Garcia' },
      { id: 2, nombre: 'Maria', apellido: 'Lopez' },
      { id: 3, nombre: 'Pedro', apellido: 'Martinez' }
    ];
  }

  private loadVehiculo(id: number): void {
    this.vehiculosService.getById(id).subscribe({
      next: (vehiculo) => this.vehiculoForm.patchValue(vehiculo),
      error: () => {
        this.notification.error('Error al cargar el vehículo');
        this.router.navigate(['/vehiculos']);
      }
    });
  }

  onSubmit(): void {
    if (this.vehiculoForm.invalid) {
      this.vehiculoForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    const data = this.vehiculoForm.value;
    data.placa = data.placa.toUpperCase();

    // Simular guardado
    setTimeout(() => {
      this.isSubmitting = false;
      this.notification.success(this.isEditing ? 'Vehículo actualizado' : 'Vehículo creado');
      this.router.navigate(['/vehiculos']);
    }, 1000);
  }

  goBack(): void {
    this.router.navigate(['/vehiculos']);
  }
}
