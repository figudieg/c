# 🚗 Sistema de Gestión de Concesionario (Backend API)

Este proyecto es una API robusta desarrollada en **Django 5.2** y **Django Rest Framework**, diseñada para automatizar el flujo operativo de un concesionario de vehículos. El sistema centraliza la gestión de inventario, perfiles de usuario, catálogos geográficos y el proceso final de facturación y ventas.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.11
* **Framework:** Django 5.2.13 / DRF
* **Base de Datos:** PostgreSQL (Managed = False para control total de SQL)
* **Servidor:** Apache con XAMPP (Entorno de desarrollo)

---

## 🚀 Proceso de Venta (Flujo de Trabajo)

El sistema sigue una lógica de negocio estricta para garantizar la integridad de los datos y la disponibilidad del inventario:

### 1. Preparación del Catálogo e Inventario

Antes de realizar una venta, el sistema debe tener pobladas las siguientes entidades:

* **Marcas y Versiones:** Definición técnica de los vehículos.
* **Equipamiento Base:** Características específicas por versión (anidadas en la respuesta del inventario).
* **Inventario (Vehículo Nuevo):** Registro físico mediante VIN, número de motor y chasis. El vehículo debe estar en estado `Disponible`.

### 2. Gestión de Usuarios y Roles

El sistema utiliza una arquitectura de perfil extendido vinculada a `auth_user` de Django:

* **Autenticación:** Manejada por el sistema nativo de Django.
* **Perfil de Usuario:** Extiende la cuenta con identificación (cédula/RIF), teléfono y **Cargo**.
* **Roles:** Solo los usuarios con el cargo de `Vendedor` o `Administrador` pueden figurar como responsables en una orden de venta.

### 3. Registro del Cliente

Se capturan los datos fiscales del cliente, incluyendo su ubicación geográfica vinculada al catálogo de **Estados de Venezuela**.

### 4. Ejecución de la Orden de Venta

El proceso de venta consolida la transacción:

1. **Selección:** Se vincula un `Cliente`, un `Vehículo` y un `Vendedor`.
2. **Validación:** El sistema verifica que el vehículo no haya sido vendido previamente (relación `OneToOne`).
3. **Cierre:** Al registrar la `OrdenVenta`, se dispara un flujo lógico (vía señales o triggers) que actualiza el estado del vehículo en el inventario a `Vendido`, retirándolo automáticamente de la oferta comercial.

---

## 📂 Estructura del Proyecto (Apps)

* **`apps.users`**: Gestión de cuentas de usuario y perfiles de empleados (Cargos).
* **`apps.vehiculos`**: Control de inventario, marcas, versiones y equipamiento técnico.
* **`apps.clientes`**: Registro de compradores y datos de contacto.
* **`apps.catalogos`**: Tablas maestras (Países, Estados de Venezuela, Tipos de moneda, etc.).
* **`apps.ventas`**: Motor de transacciones y órdenes de venta.

---

## 📋 Endpoints Principales

| Recurso                        | Método  | Descripción                                              |
| :----------------------------- | :------- | :-------------------------------------------------------- |
| `/api/vehiculos/inventario/` | `GET`  | Lista de vehículos disponibles con equipamiento anidado. |
| `/api/users/vendedores/`     | `GET`  | Lista de personal activo con cargo de vendedor.           |
| `/api/clientes/lista/`       | `POST` | Registro de nuevos clientes.                              |
| `/api/ventas/orden/`         | `POST` | Creación de orden de venta y actualización de stock.    |
