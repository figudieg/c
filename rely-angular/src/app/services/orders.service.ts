import { Injectable } from '@angular/core';
import { ApiClientService } from './api-client.service';

export interface TransaccionPago {
  id: number;
  monto: string;
  monto_inicial: string;
  monto_restante: string;
  moneda: string;
  metodo_pago: number;
  referencia: string;
  fecha_pago: string;
  estado_pago: number;
}

interface OrdenVentaAPI {
  id: number;
  codigo_orden: string;
  precio_final_venta: string;
  fecha_creacion: string;
  cliente_nombre: string;
  cliente_email: string;
  cliente_telefono: string;
  vendedor_nombre: string;
  vehiculo_vin: string;
  vehiculo_color: string;
  vehiculo_modelo: string;
  transaccion_info: TransaccionPago | null;
  estado_orden: number;
}

export interface OrdenVenta {
  id: number;
  referencia: string;
  precio: string;
  estado: string;
  estadoId: number;
  created_at: string;
  cliente_nombre: string;
  cliente_email: string;
  cliente_telefono: string;
  vendedor_nombre: string;
  vin_vehiculo: string;
  color_vehiculo: string;
  modelo_vehiculo: string;
  transaccion: TransaccionPago | null;
}

export interface CreateOrdenPayload {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  reference_number: string;
  price: number;
  vehicleModel: string;
  vehicleYear?: number;
  vehicleColor: string;
  paymentMethod: string;
  notes?: string;
}

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  errors?: any;
  detail?: string;
  message?: string;
  total?: number;
}

const ESTADO_LABELS: Record<number, string> = {
  1: 'Pendiente',
  2: 'Aprobada',
  3: 'Completada',
  4: 'Cancelada',
};

@Injectable({ providedIn: 'root' })
export class VentasService {
  constructor(private api: ApiClientService) {}

  private mapEstado(estado: number): string {
    return ESTADO_LABELS[estado] || 'Pendiente';
  }

  private mapOrden(apiOrden: OrdenVentaAPI): OrdenVenta {
    return {
      id: apiOrden.id,
      referencia: apiOrden.codigo_orden,
      precio: apiOrden.precio_final_venta,
      estado: this.mapEstado(apiOrden.estado_orden),
      estadoId: apiOrden.estado_orden,
      created_at: apiOrden.fecha_creacion,
      cliente_nombre: apiOrden.cliente_nombre,
      cliente_email: apiOrden.cliente_email,
      cliente_telefono: apiOrden.cliente_telefono,
      vendedor_nombre: apiOrden.vendedor_nombre,
      vin_vehiculo: apiOrden.vehiculo_vin,
      color_vehiculo: apiOrden.vehiculo_color,
      modelo_vehiculo: apiOrden.vehiculo_modelo,
      transaccion: apiOrden.transaccion_info,
    };
  }

  async getOrders(): Promise<OrdenVenta[]> {
    const res = await this.api.apiFetch('/api/ventas/ordenes/');
    const response: ApiResponse<OrdenVentaAPI[]> = await res.json();
    if (!res.ok || !response.success) {
      throw new Error(response.detail || 'Error al cargar las órdenes');
    }
    return (response.data || []).map(item => this.mapOrden(item));
  }

  async getOrderById(id: number): Promise<OrdenVenta> {
    const res = await this.api.apiFetch(`/api/ventas/ordenes/${id}/`);
    const response: ApiResponse<OrdenVentaAPI> = await res.json();
    if (!res.ok || !response.success || !response.data) {
      throw new Error(response.detail || 'Orden no encontrada');
    }
    return this.mapOrden(response.data);
  }

  async updateOrderStatus(id: number, estadoOrden: number): Promise<OrdenVenta> {
    const res = await this.api.apiFetch(`/api/ventas/ordenes/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ estado_orden: estadoOrden }),
    });
    const response: ApiResponse<OrdenVentaAPI> = await res.json();
    if (!res.ok || !response.success || !response.data) {
      throw new Error(response.detail || 'Error al actualizar la orden');
    }
    return this.mapOrden(response.data);
  }

  async createOrder(payload: CreateOrdenPayload): Promise<OrdenVenta> {
    const res = await this.api.apiFetch('/api/ventas/ordenes/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      const message =
        data.reference_number?.[0] ||
        data.non_field_errors?.[0] ||
        data.detail ||
        'Error al registrar la venta';
      throw new Error(message);
    }
    return data as OrdenVenta;
  }
}
