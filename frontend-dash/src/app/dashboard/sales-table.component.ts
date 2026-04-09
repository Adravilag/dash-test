// src/app/dashboard/sales-table.component.ts
import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SalesService } from '../services/sales.service';

@Component({
  selector: 'app-sales-table',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="overflow-x-auto bg-white rounded-2xl shadow-xl border border-slate-200">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-50 border-b border-slate-200">
            <th class="p-4 text-sm font-semibold text-slate-600 uppercase tracking-wider">Producto</th>
            <th class="p-4 text-sm font-semibold text-slate-600 uppercase tracking-wider">Categoría</th>
            <th class="p-4 text-sm font-semibold text-slate-600 uppercase tracking-wider text-right">Ventas</th>
            <th class="p-4 text-sm font-semibold text-slate-600 uppercase tracking-wider">Fecha</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr *ngFor="let venta of salesData()" class="hover:bg-indigo-50/30 transition-colors group">
            <td class="p-4 text-slate-700 font-medium">{{ venta.Producto }}</td>
            <td class="p-4">
              <span class="px-3 py-1 rounded-full text-xs font-semibold" 
                [ngClass]="venta.Categoria === 'Electrónica' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'">
                {{ venta.Categoria }}
              </span>
            </td>
            <td class="p-4 text-right font-mono font-bold text-slate-900">
              {{ venta.Ventas | currency:'EUR':'symbol':'1.2-2' }}
            </td>
            <td class="p-4 text-slate-500 text-sm">{{ venta.Fecha }}</td>
          </tr>
        </tbody>
      </table>
      
      <div *ngIf="salesData().length === 0" class="p-12 text-center text-slate-400">
        <p>No hay datos disponibles en este momento.</p>
      </div>
    </div>
  `
})
export class SalesTableComponent implements OnInit {
  private salesService = inject(SalesService);
  salesData = signal<any[]>([]);

  ngOnInit() {
    this.salesService.getVentas().subscribe({
      next: (data) => this.salesData.set(data),
      error: (err) => console.error('Error cargando ventas:', err)
    });
  }
}