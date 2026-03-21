# 📡 API Endpoints Reference

## Base URL
```
http://localhost:8000/api/v1
```

## 🔐 Autenticación
Todas las rutas (excepto `/auth/login`) requieren header:
```
Authorization: Bearer <token>
```

---

## 📋 Endpoints por Módulo

### 🔑 Auth
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/login` | Iniciar sesión |
| POST | `/auth/refresh` | Renovar token |
| GET | `/auth/me` | Usuario actual |

### 👥 Socios
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/socios` | Listar con paginación |
| GET | `/socios/activos` | Listar activos (select) |
| GET | `/socios/{id}` | Detalle de socio |
| POST | `/socios` | Crear socio (admin) |
| PUT | `/socios/{id}` | Actualizar socio (admin) |
| DELETE | `/socios/{id}` | Eliminar socio (admin) |

### 🚚 Vehículos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/vehiculos` | Listar con filtros |
| GET | `/vehiculos/disponibles` | Vehículos disponibles |
| GET | `/vehiculos/{id}` | Detalle de vehículo |
| POST | `/vehiculos` | Crear vehículo |
| PUT | `/vehiculos/{id}` | Actualizar vehículo |
| DELETE | `/vehiculos/{id}` | Eliminar vehículo |

### 👨‍✈️ Choferes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/choferes` | Listar con filtros |
| GET | `/choferes/disponibles` | Choferes disponibles |
| GET | `/choferes/{id}` | Detalle de chofer |
| POST | `/choferes` | Crear chofer |
| PUT | `/choferes/{id}` | Actualizar chofer |
| DELETE | `/choferes/{id}` | Eliminar chofer |

### 🏢 Clientes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clientes` | Listar con filtros |
| GET | `/clientes/activos` | Clientes activos |
| GET | `/clientes/{id}` | Detalle de cliente |
| POST | `/clientes` | Crear cliente |
| PUT | `/clientes/{id}` | Actualizar cliente |
| DELETE | `/clientes/{id}` | Eliminar cliente |

### 🛣️ Viajes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/viajes` | Listar con filtros |
| GET | `/viajes/{id}` | Detalle de viaje |
| POST | `/viajes` | Crear viaje |
| PUT | `/viajes/{id}` | Actualizar viaje |
| POST | `/viajes/{id}/iniciar` | Iniciar viaje |
| POST | `/viajes/{id}/finalizar` | Finalizar viaje |
| DELETE | `/viajes/{id}` | Cancelar viaje |

### 💵 Anticipos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/anticipos` | Listar con filtros |
| GET | `/anticipos/{id}` | Detalle de anticipo |
| GET | `/anticipos/chofer/{id}/pendientes` | Pendientes de chofer |
| POST | `/anticipos` | Crear anticipo |
| DELETE | `/anticipos/{id}` | Eliminar anticipo |

### 📊 Liquidaciones
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/liquidaciones` | Listar con filtros |
| GET | `/liquidaciones/pendientes` | Viajes pendientes |
| GET | `/liquidaciones/{id}` | Detalle de liquidación |
| POST | `/liquidaciones/viaje/{id}` | Generar liquidación |

### 🔧 Mantenimientos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/mantenimientos` | Listar con filtros |
| GET | `/mantenimientos/proximos` | Próximos (30 días) |
| GET | `/mantenimientos/vehiculo/{id}/historial` | Historial vehículo |
| GET | `/mantenimientos/{id}` | Detalle |
| POST | `/mantenimientos` | Crear mantenimiento |
| PUT | `/mantenimientos/{id}` | Actualizar |
| POST | `/mantenimientos/{id}/completar` | Completar |

### 📈 Dashboard
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/dashboard` | Estadísticas generales |
| GET | `/dashboard/resumen` | Resumen por período |

---

## 🔍 Parámetros Comunes

### Paginación
```
?page=1&limit=20
```

### Filtros de fecha
```
?fecha_inicio=2024-01-01&fecha_fin=2024-12-31
```

### Estado
```
?estado=ACTIVO
```

### Búsqueda
```
?busqueda=texto
```

---

## 📦 Formato de Respuestas

### Lista paginada
```json
{
  "data": [...],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

### Detalle
```json
{
  "data": { ... }
}
```

### Acción exitosa
```json
{
  "data": { ... },
  "message": "Operación exitosa"
}
```

### Error
```json
{
  "detail": "Descripción del error",
  "code": "ERROR_CODE"
}
```
