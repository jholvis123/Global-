import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dateFormat'
})
export class DateFormatPipe implements PipeTransform {
  transform(value: Date | string | null | undefined, format: string = 'short'): string {
    if (!value) {
      return '-';
    }

    const date = typeof value === 'string' ? new Date(value) : value;
    
    if (isNaN(date.getTime())) {
      return '-';
    }

    const options: Intl.DateTimeFormatOptions = this.getFormatOptions(format);
    
    return date.toLocaleDateString('es-BO', options);
  }

  private getFormatOptions(format: string): Intl.DateTimeFormatOptions {
    switch (format) {
      case 'short':
        return { day: '2-digit', month: '2-digit', year: 'numeric' };
      case 'medium':
        return { day: '2-digit', month: 'short', year: 'numeric' };
      case 'long':
        return { day: '2-digit', month: 'long', year: 'numeric' };
      case 'full':
        return { weekday: 'long', day: '2-digit', month: 'long', year: 'numeric' };
      case 'datetime':
        return { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        };
      case 'time':
        return { hour: '2-digit', minute: '2-digit' };
      default:
        return { day: '2-digit', month: '2-digit', year: 'numeric' };
    }
  }
}
