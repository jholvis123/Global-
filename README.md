# 🚛 Sistema de Gestión de Autotransporte Pesado

Sistema integral de gestión para empresa de autotransporte pesado desarrollado con **Angular 17+** (frontend), **FastAPI** (backend) y **SQL Server** (base de datos).

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Documentation](#api-documentation)
- [Despliegue](#despliegue)
- [Contribución](#contribución)
- [Licencia](#licencia)

## ✨ Características

### 🏢 Gestión de Socios
- Registro de socios (personas naturales y jurídicas)
- Configuración de contratos y participaciones
- Control de anticipos y liquidaciones
- Reportes financieros por socio

### 👨‍💼 Gestión de Choferes
- Registro completo de choferes
- Control de licencias y vencimientos
- Asignación a vehículos
- Seguimiento de viajes y rendimiento

### 🚚 Gestión de Vehículos
- Inventario de camiones y remolques
- Control de documentación (SOAT, ITV, seguros)
- Alertas de vencimiento
- Historial de mantenimientos

### 📦 Gestión de Viajes
- Planificación y seguimiento de viajes
- Control de cargas (soya, cemento, minerales)
- Cálculo automático de tarifas
- Estados: Planificado → En Ruta → Entregado → Liquidado

### 💰 Gestión Económica
- Liquidaciones automáticas por viaje
- Control de gastos operativos
- Anticipos a socios y choferes
- Cálculos de participación y márgenes

### 📊 Reportes y Analytics
- Dashboard con KPIs principales
- Reportes diarios, mensuales y por período
- Análisis por tipo de carga
- Exportación a PDF y Excel

### 🔐 Seguridad
- Autenticación JWT con tokens de acceso y refresh
- 6 roles de usuario: Admin, Operaciones, Finanzas, Socio, Chofer, Cliente
- Auditoría de cambios
- Control granular de permisos

## 🛠 Tecnologías

### Backend
- **FastAPI 0.104+** - Framework web moderno para APIs
- **SQLAlchemy 2.0** - ORM para Python
- **SQL Server 2019+** - Base de datos principal
- **PyODBC** - Conector para SQL Server
- **Pydantic** - Validación de datos
- **JWT** - Autenticación y autorización
- **Alembic** - Migraciones de base de datos

### Frontend
- **Angular 17+** - Framework frontend
- **TypeScript** - Lenguaje tipado
- **Angular Material** - Componentes UI
- **RxJS** - Programación reactiva
- **Chart.js** - Gráficos y visualizaciones
- **Tailwind CSS** - Framework CSS utilitario

### Infraestructura
- **Docker & Docker Compose** - Containerización
- **Nginx** - Servidor web y proxy reverso
- **Redis** - Cache y sesiones (opcional)

### Localización
- **Idioma**: Español (Bolivia)
- **Zona horaria**: America/La_Paz
- **Moneda**: Bolivianos (Bs)

## 🏗 Arquitectura

```
srl/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Esquemas Pydantic
│   │   ├── controllers/    # Lógica de negocio
│   │   ├── routes/         # Rutas de la API
│   │   ├── services/       # Servicios especializados
│   │   ├── repositories/   # Acceso a datos
│   │   ├── core/          # Configuración y seguridad
│   │   └── db/            # Base de datos
│   └── requirements.txt
├── frontend/               # Angular Frontend
│   ├── src/app/
│   │   ├── core/          # Servicios core
│   │   ├── shared/        # Componentes compartidos
│   │   └── modules/       # Módulos por funcionalidad
│   └── package.json
├── database/              # Scripts SQL Server
│   ├── schema.sql         # DDL y estructura
│   └── seed_data.sql      # Datos iniciales
└── docker-compose.yml     # Orquestación
```

## 🚀 Instalación

### Prerrequisitos
- **Docker & Docker Compose** (recomendado)
- **Node.js 18+** y **npm** (desarrollo frontend)
- **Python 3.11+** (desarrollo backend)
- **SQL Server 2019+** (base de datos)

### Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repo-url>
cd srl
```

2. **Iniciar servicios con Docker Compose**
```bash
docker-compose up -d
```

3. **Verificar servicios**
```bash
docker-compose ps
```

Los servicios estarán disponibles en:
- **Frontend**: http://localhost (Puerto 80)
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Base de datos**: localhost:1433

### Instalación Manual

#### Backend
```bash
cd backend
pip install -r requirements.txt
```

Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con configuración local
```

Ejecutar migraciones:
```bash
# Crear base de datos en SQL Server
sqlcmd -S localhost -U sa -P <password> -Q "CREATE DATABASE GestionTransporte"

# Ejecutar scripts
sqlcmd -S localhost -U sa -P <password> -d GestionTransporte -i database/schema.sql
sqlcmd -S localhost -U sa -P <password> -d GestionTransporte -i database/seed_data.sql
```

Iniciar backend:
```bash
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
ng serve
```

## ⚙️ Configuración

### Variables de Entorno Backend

```bash
# Base de datos
DATABASE_URL=mssql+pyodbc://user:pass@server/db?driver=ODBC+Driver+17+for+SQL+Server
DB_SERVER=localhost
DB_NAME=GestionTransporte
DB_USER=sa
DB_PASSWORD=password

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Aplicación
DEBUG=True
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:4200
```

### Configuración Frontend

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',
  locale: 'es-BO',
  timezone: 'America/La_Paz',
  currency: 'BOB'
};
```

## 📖 Uso

### Usuarios por Defecto

Después de ejecutar los datos semilla:

| Usuario | Email | Password | Rol |
|---------|-------|----------|-----|
| Admin | admin@transporte.bo | admin123 | Administrador |
| Operaciones | operaciones@transporte.bo | admin123 | Operaciones |
| Finanzas | finanzas@transporte.bo | admin123 | Finanzas |

### Flujo Básico

1. **Login** con credenciales de administrador
2. **Configurar socios** y vehículos
3. **Registrar choferes** y asignar licencias
4. **Crear viajes** con cargas específicas
5. **Registrar gastos** durante los viajes
6. **Cerrar viajes** y generar liquidaciones
7. **Revisar reportes** y análisis

### Roles y Permisos

- **Administrador**: Acceso completo al sistema
- **Operaciones**: Gestión de viajes, vehículos y choferes
- **Finanzas**: Liquidaciones, anticipos y reportes financieros
- **Socio**: Vista de sus vehículos y reportes
- **Chofer**: Vista de sus viajes y gastos
- **Cliente**: Vista de sus órdenes de transporte

## 📚 API Documentation

La documentación interactiva de la API está disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

```
POST   /api/v1/auth/login          # Iniciar sesión
GET    /api/v1/socios             # Listar socios
POST   /api/v1/viajes             # Crear viaje
GET    /api/v1/reportes/diario    # Reporte diario
```

## 🚀 Despliegue

### Docker Production

```bash
# Usar configuración de producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Variables de Producción

```bash
# Backend
SECRET_KEY=production-secret-key
DEBUG=False
ENVIRONMENT=production
DATABASE_URL=production-database-url

# Frontend
API_URL=https://api.yourdomain.com
```

### SSL/HTTPS

Para producción, configure SSL usando:
- **Let's Encrypt** con Nginx
- **CloudFlare** como proxy
- **Load balancer** con terminación SSL

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
ng e2e
```

## 🤝 Contribución

1. Fork el repositorio
2. Crear branch de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código

- **Backend**: PEP 8, type hints, docstrings
- **Frontend**: Angular style guide, TypeScript strict mode
- **Commits**: Conventional commits
- **Testing**: Cobertura mínima 80%

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Para soporte técnico:
- **Issues**: Crear issue en GitHub
- **Email**: soporte@transporte.bo
- **Documentación**: Wiki del proyecto

## 🎯 Roadmap

- [ ] **v1.1**: GPS tracking de vehículos
- [ ] **v1.2**: App móvil para choferes
- [ ] **v1.3**: Integración con sistemas contables
- [ ] **v1.4**: BI y analytics avanzados
- [ ] **v2.0**: Multiempresa y sucursales

---

**Desarrollado con ❤️ para el transporte pesado boliviano**