import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SociosService } from '../../services/socios.service';
import { NotificationService } from '../../../../core/services/notification.service';
import { Socio } from '../../../../models';

@Component({
  selector: 'app-socio-detail',
  templateUrl: './socio-detail.component.html',
  styleUrls: ['./socio-detail.component.scss']
})
export class SocioDetailComponent implements OnInit {
  socio: Socio | null = null;
  isLoading = true;
  resumenFinanciero = {
    totalViajes: 15,
    ingresosBrutos: 45000,
    gastos: 12000,
    gananciaSocio: 23100
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private sociosService: SociosService,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.loadSocio(+id);
    }
  }

  private loadSocio(id: number): void {
    this.isLoading = true;
    this.sociosService.getById(id).subscribe({
      next: (socio) => {
        this.socio = socio;
        this.isLoading = false;
      },
      error: () => {
        // Mock data
        this.socio = {
          id: id,
          nombre: 'Juan',
          apellido: 'García',
          ci: '1234567',
          telefono: '77712345',
          email: 'juan@example.com',
          direccion: 'Av. Principal #123, Santa Cruz',
          participacion_tipo: 'NETO',
          participacion_valor: 70,
          porcentaje_ganancia: 70,
          saldo_anticipos: 0,
          banco: 'BNB',
          cuenta_bancaria: '1234567890',
          estado: 'ACTIVO',
          vehiculos: [
            { id: 1, placa: 'ABC-123', marca: 'Volvo', modelo: 'FH16', estado: 'ACTIVO' } as any,
            { id: 2, placa: 'XYZ-789', marca: 'Scania', modelo: 'R450', estado: 'ACTIVO' } as any
          ],
          created_at: new Date(),
          updated_at: new Date()
        };
        this.isLoading = false;
      }
    });
  }

  getInitials(): string {
    if (!this.socio) return '';
    const firstInitial = this.socio.nombre?.charAt(0) || '';
    const lastInitial = this.socio.apellido?.charAt(0) || '';
    return `${firstInitial}${lastInitial}`.toUpperCase();
  }

  goBack(): void {
    this.router.navigate(['/socios']);
  }
}
