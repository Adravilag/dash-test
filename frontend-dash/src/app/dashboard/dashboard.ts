import { Component, signal, OnInit, inject, ChangeDetectionStrategy } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { SalesTableComponent } from './sales-table.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, SalesTableComponent],
  templateUrl: './dashboard.html',
  // OnPush reduce drásticamente la carga de CPU al ignorar ciclos de detección innecesarios
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    'ngSkipHydration': 'true'
  }
})
export class Dashboard implements OnInit {
  private http = inject(HttpClient);
  private sanitizer = inject(DomSanitizer);
  
  // Base URL para evitar hardcoding en múltiples sitios
  // private readonly baseUrl = 'http://localhost:8050';
  private readonly baseUrl = 'https://dash-test-b9tv.onrender.com';

  // Signals para un manejo de estado reactivo y eficiente
  dashUrl = signal<SafeResourceUrl>(this.sanitizer.bypassSecurityTrustResourceUrl(`${this.baseUrl}/ventas`));
  pathActual = signal('/ventas'); 
  
  loading = signal(true);
  vistaActual = signal<'graficos' | 'tabla'>('graficos');
  dashboardsDisponibles = signal<any[]>([]);

  ngOnInit() {
    this.cargarConfiguracion();
  }

  cargarConfiguracion() {
    this.http.get<any>(`${this.baseUrl}/api/config`).subscribe({
      next: (data) => this.dashboardsDisponibles.set(data.dashboards),
      error: (err) => console.error('Error de conexión con Dash:', err)
    });
  }

  cambiarVista(path: string) {
    // Evita recargar el iframe si el usuario pulsa el botón del gráfico activo
    if (this.pathActual() === path && this.vistaActual() === 'graficos') return;

    this.vistaActual.set('graficos');
    this.loading.set(true); // El loader se quita en onIframeLoad()
    this.pathActual.set(path);
    
    // Actualización directa del Signal de URL
    this.dashUrl.set(this.sanitizer.bypassSecurityTrustResourceUrl(`${this.baseUrl}${path}`));
  }

  mostrarTabla() {
    if (this.vistaActual() === 'tabla') return;
    this.vistaActual.set('tabla');
  }

  /**
   * Se dispara cuando el iframe termina de recibir el contenido.
   * Eliminamos cualquier retraso artificial para una sensación de velocidad pura.
   */
  onIframeLoad() {
    this.loading.set(false);
  }
}