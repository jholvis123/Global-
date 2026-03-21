import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'currencyBs'
})
export class CurrencyBsPipe implements PipeTransform {
  transform(value: number | string | null | undefined, showSymbol: boolean = true): string {
    if (value === null || value === undefined) {
      return showSymbol ? 'Bs 0.00' : '0.00';
    }

    const numValue = typeof value === 'string' ? parseFloat(value) : value;
    
    if (isNaN(numValue)) {
      return showSymbol ? 'Bs 0.00' : '0.00';
    }

    const formatted = numValue.toLocaleString('es-BO', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });

    return showSymbol ? `Bs ${formatted}` : formatted;
  }
}
