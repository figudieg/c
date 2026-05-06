import { Component, OnInit } from '@angular/core';
import { VentasService, OrdenVenta } from '../../services/ventas.service';

@Component({
  standalone: false,
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css'],
})
export class OrdersComponent implements OnInit {
  // Inicializamos con arrays vacíos para asegurar que la tabla sea "mantenible"
  orders: OrdenVenta[] = [];
  filteredOrders: OrdenVenta[] = [];
  isLoading = true;
  error = '';
  searchTerm = '';
  selectedOrder: OrdenVenta | null = null;

  constructor(private ventasService: VentasService) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  /**
   * Carga las órdenes desde el servicio de ventas.
   * Maneja el estado de carga y posibles errores de red.
   */
  // Nueva propiedad para distinguir entre "Carga inicial" y "Sin resultados"
isFirstLoad = true;

async loadOrders(): Promise<void> {
  this.isLoading = true;
  this.error = '';
  
  try {
    const data = await this.ventasService.getOrders();
    this.orders = data || [];
    this.filteredOrders = [...this.orders];
    this.isFirstLoad = false; // Ya sabemos que intentó cargar al menos una vez
  } catch (err: any) {
    console.error('Error profesional:', err);
    // Si es un error de autenticación (401), podrías redirigir al login
    this.error = err.status === 401 ? 'Sesión expirada' : 'Error de servidor';
    this.orders = [];
    this.filteredOrders = [];
  } finally {
    this.isLoading = false;
  }
}

  /**
   * Filtra las órdenes en tiempo real basándose en múltiples campos.
   */
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
      ? 'Fecha inválida' 
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
    const classes: { [key: string]: string } = {
      'Pendiente': 'bg-yellow-900/40 text-yellow-300 border-yellow-700/40',
      'Aprobada': 'bg-blue-900/40 text-blue-300 border-blue-700/40',
      'Completada': 'bg-emerald-900/40 text-emerald-300 border-emerald-700/40'
    };
    return classes[estado] || 'bg-gray-800 text-gray-400 border-gray-700';
  }
}