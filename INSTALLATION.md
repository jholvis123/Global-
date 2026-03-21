# 📦 Guía de Instalación - Sistema de Gestión de Autotransporte

Esta guía te llevará paso a paso para instalar y configurar el sistema completo.

## 🎯 Opción 1: Instalación con Docker (Recomendada)

### Prerrequisitos
- **Docker Desktop** o **Docker Engine + Docker Compose**
- **Git** para clonar el repositorio
- **8GB RAM mínimo** (recomendado 16GB)
- **10GB espacio libre** en disco

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd srl
```

2. **Configurar variables de entorno**
```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar configuración (opcional, los valores por defecto funcionan)
nano .env
```

3. **Iniciar todos los servicios**
```bash
# Construir e iniciar contenedores
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f
```

4. **Verificar instalación**
```bash
# Verificar que todos los contenedores estén ejecutándose
docker-compose ps

# Debería mostrar algo así:
# NAME                           COMMAND                  STATUS
# gestion-transporte-db          /opt/mssql/bin/sqlservr  Up (healthy)
# gestion-transporte-backend     uvicorn app.main:app     Up (healthy)
# gestion-transporte-frontend    nginx -g daemon off;     Up (healthy)
```

5. **Acceder al sistema**
- **Frontend**: http://localhost
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Base de datos**: localhost:1433

6. **Credenciales iniciales**
```
Usuario: admin@transporte.bo
Contraseña: admin123
```

### Comandos Útiles Docker

```bash
# Ver logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs database

# Reiniciar servicio específico
docker-compose restart backend

# Detener todos los servicios
docker-compose down

# Eliminar volúmenes (⚠️ borra datos)
docker-compose down -v

# Reconstruir contenedores
docker-compose up -d --build --force-recreate
```

---

## 🔧 Opción 2: Instalación Manual (Desarrollo)

### Prerrequisitos

#### Sistema Operativo
- **Windows 10/11** con WSL2 (recomendado)
- **Ubuntu 20.04+** o **macOS 12+**

#### Software Base
- **Python 3.11+**
- **Node.js 18+** y **npm**
- **SQL Server 2019+** (LocalDB, Express o Full)
- **Git**

### Instalación del Backend (FastAPI)

1. **Instalar Python y dependencias**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# macOS (con Homebrew)
brew install python@3.11

# Windows - descargar desde python.org
```

2. **Configurar SQL Server**

**Windows:**
```bash
# Instalar SQL Server LocalDB
winget install Microsoft.SQLServer.2019.LocalDB

# O descargar SQL Server Express desde:
# https://www.microsoft.com/en-us/sql-server/sql-server-downloads
```

**Ubuntu/Linux:**
```bash
# Instalar SQL Server en Linux
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/20.04/mssql-server-2019.list)"
sudo apt-get update
sudo apt-get install -y mssql-server

# Configurar
sudo /opt/mssql/bin/mssql-conf setup

# Instalar herramientas cliente
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt-get update
sudo apt-get install mssql-tools unixodbc-dev
```

3. **Configurar base de datos**
```bash
# Conectar a SQL Server
sqlcmd -S localhost -U sa

# En el prompt de SQL Server:
CREATE DATABASE GestionTransporte;
GO
quit

# Ejecutar scripts de creación
cd database
sqlcmd -S localhost -U sa -d GestionTransporte -i schema.sql
sqlcmd -S localhost -U sa -d GestionTransporte -i seed_data.sql
```

4. **Configurar backend Python**
```bash
cd backend

# Crear entorno virtual
python3.11 -m venv venv

# Activar entorno virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con configuración de base de datos

# Verificar conexión a BD
python -c "from app.db.database import engine; print('✅ Conexión exitosa')"

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Instalación del Frontend (Angular)

1. **Instalar Node.js**
```bash
# Ubuntu (usando NodeSource)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS (con Homebrew)
brew install node@18

# Windows - descargar desde nodejs.org
```

2. **Instalar Angular CLI**
```bash
npm install -g @angular/cli@17
```

3. **Configurar frontend**
```bash
cd frontend

# Instalar dependencias
npm install

# Configurar environment (opcional)
# Editar src/environments/environment.ts si es necesario

# Iniciar servidor de desarrollo
ng serve --host 0.0.0.0 --port 4200
```

---

## 🌐 Verificación de la Instalación

### Health Checks

1. **Backend Health Check**
```bash
curl http://localhost:8000/health

# Respuesta esperada:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": 1699123456.789,
  "version": "1.0.0"
}
```

2. **Frontend**
- Navegar a http://localhost:4200
- Debería mostrar la página de login

3. **Base de Datos**
```bash
sqlcmd -S localhost -U sa -d GestionTransporte -Q "SELECT COUNT(*) as total_socios FROM socios"

# Debería mostrar 5 socios de prueba
```

### Pruebas de Funcionalidad

1. **Login**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@transporte.bo", "password": "admin123"}'
```

2. **Listar Socios**
```bash
# Obtener token del login anterior
curl -X GET http://localhost:8000/api/v1/socios \
  -H "Authorization: Bearer <TOKEN>"
```

---

## 🚀 Configuración para Producción

### Variables de Entorno Producción

```bash
# Backend (.env)
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=clave-super-segura-para-produccion-cambiar-obligatorio
DATABASE_URL=mssql+pyodbc://usuario:password@servidor-produccion/GestionTransporte?driver=ODBC+Driver+17+for+SQL+Server

# Configuración de seguridad
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### SSL/HTTPS

Para producción, configurar SSL usando Let's Encrypt:

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Configurar auto-renovación
sudo crontab -e
# Agregar línea:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Optimizaciones de Producción

```bash
# Aumentar límites del sistema
echo "fs.file-max = 65535" >> /etc/sysctl.conf

# Configurar firewall
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Configurar logrotate
sudo vim /etc/logrotate.d/gestion-transporte
```

---

## ❓ Solución de Problemas

### Error de Conexión a Base de Datos

```bash
# Verificar que SQL Server esté ejecutándose
sudo systemctl status mssql-server

# Ver logs de SQL Server
sudo journalctl -u mssql-server

# Reiniciar SQL Server
sudo systemctl restart mssql-server
```

### Error de CORS en Frontend

```bash
# Verificar configuración en backend/.env
CORS_ORIGINS=http://localhost:4200,http://localhost

# Reiniciar backend después del cambio
```

### Puerto en Uso

```bash
# Ver qué proceso usa el puerto
sudo netstat -tulpn | grep :8000

# Matar proceso si es necesario
sudo kill -9 <PID>
```

### Problemas de Permisos Docker

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Logout y login nuevamente
newgrp docker
```

### Logs para Debug

```bash
# Backend logs
tail -f backend/logs/app.log

# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

---

## 📞 Soporte

Si encuentras problemas durante la instalación:

1. **Revisar logs** detallados
2. **Verificar prerrequisitos** están instalados correctamente
3. **Consultar documentación** de cada tecnología
4. **Crear issue** en el repositorio con detalles del error
5. **Contactar soporte**: soporte@transporte.bo

---

¡Instalación completa! 🎉 Ya puedes comenzar a usar el sistema de gestión de transporte.