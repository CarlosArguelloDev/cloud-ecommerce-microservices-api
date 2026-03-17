# 🌿 Lirio del Valle — Backend Microservicios

Backend REST API para la tienda de plantas **Lirio del Valle**, construido con Flask, SQLAlchemy y PostgreSQL, orquestado con Docker Compose.

## Arquitectura

```
Frontend React (localhost:5173)
        │
        ▼
  api-gateway :5000   ← único punto de entrada (CORS habilitado)
  ┌──────────────────────────────────────────────────────┐
  │  products-service :5001  ←→  db-products (postgres)  │
  │  users-service    :5002  ←→  db-users    (postgres)  │
  │  orders-service   :5003  ←→  db-orders   (postgres)  │
  │  payments-service :5004  ←→  db-payments (postgres)  │
  └──────────────────────────────────────────────────────┘
```

## Inicio rápido

### Requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo

### Levantar todos los servicios

```bash
docker-compose up --build
```

El primer arranque descarga imágenes y construye los contenedores (~2–3 min).  
Los siguientes arranques son mucho más rápidos:

```bash
docker-compose up
```

### Apagar

```bash
docker-compose down
```

Para también eliminar los volúmenes de datos (borrar DBs):

```bash
docker-compose down -v
```

---

## Endpoints disponibles

Todos los endpoints se acceden a través del gateway en `http://localhost:5000`.

### 🌿 Productos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/products` | Lista todas las plantas |
| GET | `/products/<id>` | Detalle de una planta |

### 👤 Usuarios

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/users/register` | Registro de nuevo usuario |
| POST | `/users/login` | Login → retorna JWT |
| GET | `/users/profile` | Perfil (requiere JWT) |
| GET | `/users/wishlist` | Ver wishlist (requiere JWT) |
| POST | `/users/wishlist` | Añadir a wishlist (requiere JWT) |
| DELETE | `/users/wishlist/<product_id>` | Quitar de wishlist (requiere JWT) |

### 🛒 Órdenes

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/orders` | Crear orden desde el carrito |
| GET | `/orders/<id>` | Estado de una orden |
| GET | `/orders/user/<user_id>` | Historial de órdenes |

### 💳 Pagos

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/payments` | Procesar pago simulado |
| GET | `/payments/<id>` | Estado de un pago |

---


