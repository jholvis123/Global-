import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { TIPOS_GASTO, GastoViaje, GastoViajeCreate, TipoGasto } from '../../../../models';

export interface GastoDialogData {
  viaje_id: number;
  gasto?: GastoViaje; // Para edición
}

@Component({
  selector: 'app-gasto-dialog',
  templateUrl: './gasto-dialog.component.html',
  styleUrls: ['./gasto-dialog.component.scss']
})
export class GastoDialogComponent implements OnInit {
  gastoForm!: FormGroup;
  tiposGasto = TIPOS_GASTO;
  isEditing = false;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<GastoDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: GastoDialogData
  ) {}

  ngOnInit(): void {
    this.isEditing = !!this.data.gasto;
    this.initForm();
    
    if (this.isEditing && this.data.gasto) {
      this.gastoForm.patchValue(this.data.gasto);
    }
  }

  private initForm(): void {
    this.gastoForm = this.fb.group({
      tipo: ['COMBUSTIBLE', Validators.required],
      monto_bs: [null, [Validators.required, Validators.min(0.01)]],
      descripcion: [''],
      fecha: [new Date(), Validators.required],
      ubicacion: ['']
    });
  }

  onSubmit(): void {
    if (this.gastoForm.invalid) {
      this.gastoForm.markAllAsTouched();
      return;
    }

    const formData = this.gastoForm.value;
    
    // Crear el objeto de gasto
    const gasto: GastoViaje = {
      id: this.data.gasto?.id || Date.now(), // ID temporal para demo
      viaje_id: this.data.viaje_id,
      tipo: formData.tipo,
      monto_bs: formData.monto_bs,
      descripcion: formData.descripcion,
      fecha: formData.fecha,
      ubicacion: formData.ubicacion,
      created_at: new Date()
    };

    this.dialogRef.close(gasto);
  }

  cancel(): void {
    this.dialogRef.close();
  }

  getTipoIcon(tipo: string): string {
    const found = this.tiposGasto.find(t => t.value === tipo);
    return found ? found.icon : 'receipt';
  }
}
