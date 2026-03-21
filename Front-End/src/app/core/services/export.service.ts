import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ExportService {

  constructor() { }

  /**
   * Exporta datos a un archivo Excel (.xlsx)
   * Requiere la librería xlsx: npm install xlsx
   */
  async exportToExcel(data: any[], filename: string, sheetName: string = 'Datos'): Promise<void> {
    try {
      // Importación dinámica de xlsx
      const XLSX = await import('xlsx' as any).catch(() => null);
      
      if (!XLSX) {
        console.warn('xlsx no está instalado. Exportando a CSV como alternativa.');
        this.exportToCSV(data, filename);
        return;
      }
      
      // Crear worksheet desde los datos
      const worksheet = XLSX.utils.json_to_sheet(data);
      
      // Crear workbook
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);
      
      // Ajustar ancho de columnas automáticamente
      const maxWidths: number[] = [];
      data.forEach(row => {
        Object.keys(row).forEach((key, index) => {
          const value = String(row[key] || '');
          const len = Math.max(value.length, key.length);
          maxWidths[index] = Math.max(maxWidths[index] || 10, len);
        });
      });
      worksheet['!cols'] = maxWidths.map(w => ({ wch: Math.min(w + 2, 50) }));
      
      // Generar y descargar el archivo
      XLSX.writeFile(workbook, `${filename}.xlsx`);
      
      console.log(`✅ Archivo ${filename}.xlsx exportado exitosamente`);
    } catch (error) {
      console.error('Error al exportar a Excel:', error);
      // Fallback a CSV si xlsx no está disponible
      this.exportToCSV(data, filename);
    }
  }

  /**
   * Exporta datos a un archivo CSV
   */
  exportToCSV(data: any[], filename: string): void {
    if (!data || data.length === 0) {
      console.warn('No hay datos para exportar');
      return;
    }

    // Obtener cabeceras
    const headers = Object.keys(data[0]);
    
    // Crear contenido CSV
    const csvContent = [
      headers.join(','),
      ...data.map(row => 
        headers.map(header => {
          let cell = row[header] ?? '';
          // Escapar comillas y comas
          if (typeof cell === 'string' && (cell.includes(',') || cell.includes('"'))) {
            cell = `"${cell.replace(/"/g, '""')}"`;
          }
          return cell;
        }).join(',')
      )
    ].join('\n');

    // Crear blob y descargar
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    this.downloadBlob(blob, `${filename}.csv`);
  }

  /**
   * Exporta datos a un archivo PDF
   * Requiere la librería jspdf y jspdf-autotable
   */
  async exportToPDF(
    data: any[], 
    filename: string, 
    title: string = 'Reporte',
    options: PDFExportOptions = {}
  ): Promise<void> {
    try {
      // Importación dinámica de jspdf
      const jspdfModule = await import('jspdf' as any).catch(() => null);
      const autoTableModule = await import('jspdf-autotable' as any).catch(() => null);
      
      if (!jspdfModule || !autoTableModule) {
        console.warn('jspdf o jspdf-autotable no están instalados. Por favor instale: npm install jspdf jspdf-autotable');
        alert('Exportar a PDF requiere instalar: npm install jspdf jspdf-autotable');
        return;
      }
      
      const { jsPDF } = jspdfModule;
      const autoTable = autoTableModule.default;
      
      // Crear documento PDF
      const doc = new jsPDF({
        orientation: options.orientation || 'landscape',
        unit: 'mm',
        format: 'a4'
      });

      // Título
      doc.setFontSize(18);
      doc.setTextColor(40, 40, 40);
      doc.text(title, 14, 22);

      // Fecha de generación
      doc.setFontSize(10);
      doc.setTextColor(100, 100, 100);
      doc.text(`Generado: ${new Date().toLocaleDateString('es-PE')} ${new Date().toLocaleTimeString('es-PE')}`, 14, 30);

      // Preparar datos para la tabla
      const headers = Object.keys(data[0] || {});
      const tableData = data.map(row => headers.map(h => row[h] ?? ''));

      // Generar tabla
      autoTable(doc, {
        head: [headers],
        body: tableData,
        startY: 35,
        theme: 'striped',
        headStyles: {
          fillColor: [59, 130, 246],
          textColor: 255,
          fontStyle: 'bold'
        },
        alternateRowStyles: {
          fillColor: [245, 247, 250]
        },
        styles: {
          fontSize: 8,
          cellPadding: 3
        },
        margin: { top: 35 }
      });

      // Número de página
      const pageCount = doc.internal.pages.length - 1;
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150);
        doc.text(
          `Página ${i} de ${pageCount}`,
          doc.internal.pageSize.getWidth() - 30,
          doc.internal.pageSize.getHeight() - 10
        );
      }

      // Guardar PDF
      doc.save(`${filename}.pdf`);
      
      console.log(`✅ Archivo ${filename}.pdf exportado exitosamente`);
    } catch (error) {
      console.error('Error al exportar a PDF:', error);
      alert('Error al generar PDF. Asegúrese de tener las librerías instaladas: npm install jspdf jspdf-autotable');
    }
  }

  /**
   * Imprime una tabla HTML directamente
   */
  printTable(elementId: string, title: string = 'Reporte'): void {
    const element = document.getElementById(elementId);
    if (!element) {
      console.error(`Elemento con ID "${elementId}" no encontrado`);
      return;
    }

    const printWindow = window.open('', '', 'height=600,width=800');
    if (!printWindow) {
      console.error('No se pudo abrir la ventana de impresión');
      return;
    }

    printWindow.document.write(`
      <html>
        <head>
          <title>${title}</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { color: #333; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #3b82f6; color: white; }
            tr:nth-child(even) { background-color: #f9fafb; }
            .print-date { color: #666; font-size: 12px; margin-bottom: 10px; }
          </style>
        </head>
        <body>
          <h1>${title}</h1>
          <p class="print-date">Generado: ${new Date().toLocaleDateString('es-PE')} ${new Date().toLocaleTimeString('es-PE')}</p>
          ${element.outerHTML}
        </body>
      </html>
    `);

    printWindow.document.close();
    printWindow.focus();
    
    setTimeout(() => {
      printWindow.print();
      printWindow.close();
    }, 250);
  }

  /**
   * Helper para descargar blob
   */
  private downloadBlob(blob: Blob, filename: string): void {
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    URL.revokeObjectURL(url);
  }
}

export interface PDFExportOptions {
  orientation?: 'portrait' | 'landscape';
  pageSize?: 'a4' | 'letter' | 'legal';
  margins?: {
    top?: number;
    right?: number;
    bottom?: number;
    left?: number;
  };
}
