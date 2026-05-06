import { Component, OnInit } from '@angular/core';
import { VentasService, OrdenVenta } from '../../services/ventas.service';

@Component({
  standalone: false,
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css'],
})
export class OrdersComponent implements OnInit {
  orders: OrdenVenta[] = [];
  filteredOrders: OrdenVenta[] = [];
  isLoading = true;
  isFirstLoad = true;
  error = '';
  searchTerm = '';
  selectedOrder: OrdenVenta | null = null;

  constructor(private ventasService: VentasService) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  async loadOrders(): Promise<void> {
    this.isLoading = true;
    this.error = '';

    try {
      const data = await this.ventasService.getOrders();
      this.orders = data || [];
      this.filteredOrders = [...this.orders];
    } catch (err: any) {
      console.error('Error cargando órdenes:', err);
      this.error = 'No se pudieron cargar las órdenes. Verifica tu conexión.';
      this.orders = [];
      this.filteredOrders = [];
    } finally {
      this.isLoading = false;
      this.isFirstLoad = false;
    }
  }

  onSearch(term: string): void {
    this.searchTerm = term;
    if (!term.trim()) {
      this.filteredOrders = [...this.orders];
      return;
    }
    const q = term.toLowerCase();
    this.filteredOrders = this.orders.filter(o =>
      (o.referencia?.toLowerCase() || '').includes(q) ||
      (o.cliente_nombre?.toLowerCase() || '').includes(q) ||
      (o.modelo_vehiculo?.toLowerCase() || '').includes(q) ||
      (o.vendedor_nombre?.toLowerCase() || '').includes(q)
    );
  }

  openDetail(order: OrdenVenta): void {
    this.selectedOrder = order;
  }

  closeDetail(): void {
    this.selectedOrder = null;
  }

  formatDate(dateStr: string): string {
    if (!dateStr) return '—';
    const date = new Date(dateStr);
    return isNaN(date.getTime())
      ? '—'
      : date.toLocaleDateString('es-VE', { day: '2-digit', month: 'short', year: 'numeric' });
  }

  formatPrice(price: string | number): string {
    const n = typeof price === 'string' ? parseFloat(price) : price;
    if (isNaN(n)) return '—';
    return new Intl.NumberFormat('en-US', {
      style: 'currency', currency: 'USD', minimumFractionDigits: 2
    }).format(n);
  }

  getEstadoLabel(estado: string): string {
    return estado || 'Pendiente';
  }

  getEstadoClass(estado: string): string {
    const classes: Record<string, string> = {
      'Pendiente':  'bg-yellow-900/40 text-yellow-300 border-yellow-700/40',
      'Aprobada':   'bg-blue-900/40 text-blue-300 border-blue-700/40',
      'Completada': 'bg-emerald-900/40 text-emerald-300 border-emerald-700/40',
      'Cancelada':  'bg-red-900/40 text-red-300 border-red-700/40',
    };
    return classes[estado] || 'bg-gray-800 text-gray-400 border-gray-700';
  }
}