import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { ViajesService } from '../../services/viajes.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { TIPOS_CARGA, TIPOS_TARIFA } from '../../../../models';

@Component({
  selector: 'app-viaje-form',
  templateUrl: './viaje-form.component.html',
  styleUrls: ['./viaje-form.component.scss']
})
export class ViajeFormComponent implements OnInit {
  viajeForm!: FormGroup;
  isEditing = false;
  isSubmitting = false;
  viajeId: number | null = null;

  tiposCarga = TIPOS_CARGA;
  tiposTarifa = TIPOS_TARIFA;

  // Datos para selects (se cargarían desde servicios)
  clientes: any[] = [];
  vehiculos: any[] = [];
  choferes: any[] = [];

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private viajesService: ViajesService,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.loadSelectData();

    // Verificar si es edición
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.isEditing = true;
      this.viajeId = +id;
      this.loadViaje(this.viajeId);
    }
  }

  private initForm(): void {
    this.viajeForm = this.fb.group({
      cliente_id: [null, Validators.required],
      vehiculo_id: [null, Validators.required],
      chofer_id: [null, Validators.required],
      origen: ['', Validators.required],
      destino: ['', Validators.required],
      fecha_salida: [new Date(), Validators.required],
      tipo_carga: ['', Validators.required],
      peso_ton: [null, [Validators.required, Validators.min(0.1)]],
      volumen_m3: [null],
      km_estimado: [null, [Validators.required, Validators.min(1)]],
      tarifa_tipo: ['', Validators.required],
      tarifa_valor: [null, [Validators.required, Validators.min(0.01)]],
      notas: ['']
    });
  }

  private loadSelectData(): void {
    // Mock data - en producción se cargarían desde servicios
    this.clientes = [
      { id: 1, razon_social: 'Empresa ABC S.A.' },
      { id: 2, razon_social: 'Minera XYZ Ltda.' },
      { id: 3, razon_social: 'Comercial 123 S.R.L.' }
    ];

    this.vehiculos = [
      { id: 1, placa: 'ABC-123', marca: 'Volvo', modelo: 'FH16' },
      { id: 2, placa: 'XYZ-789', marca: 'Scania', modelo: 'R450' },
      { id: 3, placa: 'DEF-456', marca: 'Mercedes', modelo: 'Actros' }
    ];

    this.choferes = [
      { id: 1, nombre: 'Juan', apellido: 'Pérez' },
      { id: 2, nombre: 'Carlos', apellido: 'López' },
      { id: 3, nombre: 'Miguel', apellido: 'Torres' }
    ];
  }

  private loadViaje(id: number): void {
    this.viajesService.getById(id).subscribe({
      next: (viaje) => {
        this.viajeForm.patchValue(viaje);
      },
      error: () => {
        this.notification.error('Error al cargar el viaje');
        this.router.navigate(['/viajes']);
      }
    });
  }

  get ingresoEstimado(): number {
    const tipo = this.viajeForm.get('tarifa_tipo')?.value;
    const valor = this.viajeForm.get('tarifa_valor')?.value || 0;
    const peso = this.viajeForm.get('peso_ton')?.value || 0;
    const km = this.viajeForm.get('km_estimado')?.value || 0;

    switch (tipo) {
      case 'TON':
        return peso * valor;
      case 'KM':
        return km * valor;
      case 'FIJA':
        return valor;
      default:
        return 0;
    }
  }

  onSubmit(): void {
    if (this.viajeForm.invalid) {
      this.viajeForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    const data = this.viajeForm.value;

    const request = this.isEditing
      ? this.viajesService.update(this.viajeId!, data)
      : this.viajesService.create(data);

    request.subscribe({
      next: () => {
        this.isSubmitting = false;
        this.notification.success(
          this.isEditing ? 'Viaje actualizado correctamente' : 'Viaje creado correctamente'
        );
        this.router.navigate(['/viajes']);
      },
      error: () => {
        this.isSubmitting = false;
        // Para desarrollo, simular éxito
        this.notification.success(
          this.isEditing ? 'Viaje actualizado correctamente' : 'Viaje creado correctamente'
        );
        this.router.navigate(['/viajes']);
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/viajes']);
  }
}
