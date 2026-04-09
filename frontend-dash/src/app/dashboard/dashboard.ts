import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SafePipe } from './safe.pipe';
import { SalesTableComponent } from './sales-table.component'; // <-- Importante

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, SafePipe, SalesTableComponent], // <-- Añadido aquí
  templateUrl: './dashboard.html', // Asegúrate de que el nombre coincida (dashboard.html o dashboard.component.html)
  host: {
    'ngSkipHydration': 'true'
  }
})
export class Dashboard {
  // dashUrl = signal('http://localhost:8050/ventas');
  dashUrl = signal('https://dash-test-b9tv.onrender.com/ventas');
  loading = signal(true);

  // --- NUEVAS PROPIEDADES PARA CORREGIR LOS ERRORES ---
  
  // Controla qué vista mostrar: 'graficos' (Dash) o 'tabla' (Angular)
  vistaActual = signal<'graficos' | 'tabla'>('graficos');

  cambiarVista(ruta: string) {
    this.vistaActual.set('graficos'); // Cambiamos a modo gráficos
    this.loading.set(true);
    // this.dashUrl.set(`http://localhost:8050/${ruta}`);
    this.dashUrl.set(`https://dash-test-b9tv.onrender.com/${ruta}`);
  }

  mostrarTabla() {
    this.vistaActual.set('tabla'); // Cambiamos a modo tabla nativa
  }

  onIframeLoad() {
    setTimeout(() => this.loading.set(false), 300);
  }
}