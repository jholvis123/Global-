-- ========================================
-- SISTEMA DE GESTIÓN DE AUTOTRANSPORTE PESADO
-- Base de Datos SQL Server 2019+
-- Zona Horaria: America/La_Paz
-- Moneda: Bolivianos (Bs)
-- ========================================

USE master;
GO

-- Crear base de datos si no existe
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'GestionTransporte')
BEGIN
    CREATE DATABASE GestionTransporte
    COLLATE SQL_Latin1_General_CP1_CI_AS;
END
GO

USE GestionTransporte;
GO

-- ========================================
-- TABLAS PRINCIPALES
-- ========================================

-- Tabla de roles del sistema
CREATE TABLE roles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL UNIQUE,
    descripcion NVARCHAR(200),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL
);

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(100) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    telefono NVARCHAR(15),
    estado NVARCHAR(20) DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO', 'INACTIVO', 'BLOQUEADO')),
    intentos_fallidos INT DEFAULT 0,
    ultimo_login DATETIME2,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1
);

-- Tabla de roles de usuarios
CREATE TABLE usuario_roles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario_id INT NOT NULL,
    rol_id INT NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (rol_id) REFERENCES roles(id),
    UNIQUE(usuario_id, rol_id)
);

-- Tabla de socios
CREATE TABLE socios (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    nit NVARCHAR(20) UNIQUE,
    ci NVARCHAR(15),
    direccion NVARCHAR(200),
    telefono NVARCHAR(15),
    email NVARCHAR(100),
    cuenta_bancaria NVARCHAR(50),
    banco NVARCHAR(50),
    participacion_tipo NVARCHAR(10) DEFAULT 'NETO' CHECK (participacion_tipo IN ('NETO', 'BRUTO')),
    participacion_valor DECIMAL(5,2) NOT NULL, -- Porcentaje o monto fijo
    saldo_anticipos DECIMAL(12,2) DEFAULT 0.00,
    estado NVARCHAR(20) DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO', 'INACTIVO')),
    usuario_id INT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de choferes
CREATE TABLE choferes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    ci NVARCHAR(15) NOT NULL UNIQUE,
    licencia_numero NVARCHAR(20) NOT NULL,
    licencia_categoria NVARCHAR(10) NOT NULL,
    licencia_vencimiento DATE NOT NULL,
    telefono NVARCHAR(15),
    direccion NVARCHAR(200),
    experiencia_anos INT DEFAULT 0,
    estado NVARCHAR(20) DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO', 'INACTIVO', 'SUSPENDIDO')),
    usuario_id INT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de clientes
CREATE TABLE clientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    razon_social NVARCHAR(150) NOT NULL,
    nit NVARCHAR(20) UNIQUE,
    contacto_nombre NVARCHAR(100),
    contacto_telefono NVARCHAR(15),
    contacto_email NVARCHAR(100),
    direccion NVARCHAR(200),
    estado NVARCHAR(20) DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO', 'INACTIVO')),
    usuario_id INT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de vehículos (camiones)
CREATE TABLE vehiculos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    placa NVARCHAR(10) NOT NULL UNIQUE,
    marca NVARCHAR(50) NOT NULL,
    modelo NVARCHAR(50) NOT NULL,
    año INT NOT NULL,
    capacidad_ton DECIMAL(6,2) NOT NULL,
    socio_id INT NOT NULL,
    estado NVARCHAR(20) DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO', 'MANTENIMIENTO', 'BAJA')),
    soat_vencimiento DATE,
    itv_vencimiento DATE,
    seguro_vencimiento DATE,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (socio_id) REFERENCES socios(id)
);

-- Tabla de remolques (opcional)
CREATE TABLE remolques (
    id INT IDENTITY(1,1) PRIMARY KEY,
    placa NVARCHAR(10) NOT NULL UNIQUE,
    tipo NVARCHAR(50) NOT NULL,
    capacidad_ton DECIMAL(6,2) NOT NULL,
    vehiculo_id INT NULL,
    estado NVARCHAR(20) DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO', 'MANTENIMIENTO', 'BAJA')),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
);

-- Tabla de viajes
CREATE TABLE viajes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cliente_id INT NOT NULL,
    vehiculo_id INT NOT NULL,
    chofer_id INT NOT NULL,
    origen NVARCHAR(100) NOT NULL,
    destino NVARCHAR(100) NOT NULL,
    fecha_salida DATETIME2 NOT NULL,
    fecha_llegada DATETIME2 NULL,
    tipo_carga NVARCHAR(50) NOT NULL,
    peso_ton DECIMAL(8,2) NOT NULL,
    volumen_m3 DECIMAL(8,2) NULL,
    km_estimado INT NOT NULL,
    km_real INT NULL,
    tarifa_tipo NVARCHAR(10) NOT NULL CHECK (tarifa_tipo IN ('KM', 'TON', 'FIJA')),
    tarifa_valor DECIMAL(10,2) NOT NULL,
    ingreso_total_bs DECIMAL(12,2) AS (
        CASE 
            WHEN tarifa_tipo = 'TON' THEN peso_ton * tarifa_valor
            WHEN tarifa_tipo = 'KM' THEN ISNULL(km_real, km_estimado) * tarifa_valor
            WHEN tarifa_tipo = 'FIJA' THEN tarifa_valor
        END
    ) PERSISTED,
    estado NVARCHAR(20) DEFAULT 'PLANIFICADO' CHECK (estado IN ('PLANIFICADO', 'EN_RUTA', 'ENTREGADO', 'LIQUIDADO')),
    notas NVARCHAR(500),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id),
    FOREIGN KEY (chofer_id) REFERENCES choferes(id)
);

-- Tabla de gastos de viajes
CREATE TABLE gastos_viajes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    viaje_id INT NOT NULL,
    tipo NVARCHAR(30) NOT NULL CHECK (tipo IN ('COMBUSTIBLE', 'PEAJE', 'VIATICO', 'TALLER', 'OTRO')),
    monto_bs DECIMAL(10,2) NOT NULL,
    descripcion NVARCHAR(200),
    soporte_url NVARCHAR(300),
    fecha DATETIME2 DEFAULT GETDATE(),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (viaje_id) REFERENCES viajes(id)
);

-- Tabla de anticipos
CREATE TABLE anticipos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    viaje_id INT NULL,
    socio_id INT NULL,
    chofer_id INT NULL,
    beneficiario_tipo NVARCHAR(10) NOT NULL CHECK (beneficiario_tipo IN ('SOCIO', 'CHOFER')),
    monto_bs DECIMAL(10,2) NOT NULL,
    fecha DATETIME2 DEFAULT GETDATE(),
    observacion NVARCHAR(300),
    estado NVARCHAR(20) DEFAULT 'PENDIENTE' CHECK (estado IN ('PENDIENTE', 'LIQUIDADO')),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (viaje_id) REFERENCES viajes(id),
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (chofer_id) REFERENCES choferes(id)
);

-- Tabla de liquidaciones
CREATE TABLE liquidaciones (
    id INT IDENTITY(1,1) PRIMARY KEY,
    viaje_id INT NOT NULL UNIQUE,
    ingreso_bs DECIMAL(12,2) NOT NULL,
    gastos_bs DECIMAL(12,2) NOT NULL,
    margen_bs AS (ingreso_bs - gastos_bs) PERSISTED,
    pago_socio_bs DECIMAL(12,2) NOT NULL,
    saldo_socio_bs DECIMAL(12,2) NOT NULL,
    saldo_chofer_bs DECIMAL(12,2) DEFAULT 0.00,
    fecha DATETIME2 DEFAULT GETDATE(),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (viaje_id) REFERENCES viajes(id)
);

-- Tabla de mantenimientos
CREATE TABLE mantenimientos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    vehiculo_id INT NOT NULL,
    tipo NVARCHAR(20) NOT NULL CHECK (tipo IN ('PREVENTIVO', 'CORRECTIVO')),
    descripcion NVARCHAR(300) NOT NULL,
    costo_bs DECIMAL(10,2) NOT NULL,
    fecha DATETIME2 NOT NULL,
    taller NVARCHAR(100),
    proximo_km INT NULL,
    proxima_fecha DATE NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    deleted_at DATETIME2 NULL,
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
);

-- Tabla de auditoría
CREATE TABLE auditoria_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario_id INT NULL,
    tabla NVARCHAR(50) NOT NULL,
    registro_id INT NOT NULL,
    operacion NVARCHAR(10) NOT NULL CHECK (operacion IN ('INSERT', 'UPDATE', 'DELETE')),
    valores_anteriores NVARCHAR(MAX) NULL,
    valores_nuevos NVARCHAR(MAX) NULL,
    ip_address NVARCHAR(45),
    user_agent NVARCHAR(500),
    created_at DATETIME2 DEFAULT GETDATE(),
    tenant_id INT DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- ========================================
-- ÍNDICES PARA RENDIMIENTO
-- ========================================

-- Índices en fechas
CREATE INDEX IX_viajes_fecha_salida ON viajes(fecha_salida);
CREATE INDEX IX_viajes_fecha_llegada ON viajes(fecha_llegada);
CREATE INDEX IX_gastos_viajes_fecha ON gastos_viajes(fecha);
CREATE INDEX IX_anticipos_fecha ON anticipos(fecha);
CREATE INDEX IX_liquidaciones_fecha ON liquidaciones(fecha);
CREATE INDEX IX_mantenimientos_fecha ON mantenimientos(fecha);

-- Índices en llaves foráneas
CREATE INDEX IX_viajes_cliente_id ON viajes(cliente_id);
CREATE INDEX IX_viajes_vehiculo_id ON viajes(vehiculo_id);
CREATE INDEX IX_viajes_chofer_id ON viajes(chofer_id);
CREATE INDEX IX_gastos_viajes_viaje_id ON gastos_viajes(viaje_id);
CREATE INDEX IX_vehiculos_socio_id ON vehiculos(socio_id);
CREATE INDEX IX_anticipos_socio_id ON anticipos(socio_id);
CREATE INDEX IX_anticipos_chofer_id ON anticipos(chofer_id);
CREATE INDEX IX_mantenimientos_vehiculo_id ON mantenimientos(vehiculo_id);

-- Índices en campos de búsqueda frecuente
CREATE INDEX IX_viajes_tipo_carga ON viajes(tipo_carga);
CREATE INDEX IX_viajes_estado ON viajes(estado);
CREATE INDEX IX_vehiculos_placa ON vehiculos(placa);
CREATE INDEX IX_choferes_licencia_vencimiento ON choferes(licencia_vencimiento);
CREATE INDEX IX_usuarios_email ON usuarios(email);

-- Índices compuestos
CREATE INDEX IX_viajes_fecha_estado ON viajes(fecha_salida, estado);
CREATE INDEX IX_auditoria_tabla_registro ON auditoria_logs(tabla, registro_id);

-- ========================================
-- VISTAS DE REPORTE
-- ========================================

-- Vista de resumen diario
CREATE VIEW vw_resumen_diario AS
SELECT 
    CAST(fecha_salida AS DATE) as fecha,
    COUNT(*) as total_viajes,
    SUM(ingreso_total_bs) as ingresos_bs,
    SUM(ISNULL(gv.gastos_bs, 0)) as gastos_bs,
    SUM(ingreso_total_bs) - SUM(ISNULL(gv.gastos_bs, 0)) as ganancia_bs
FROM viajes v
LEFT JOIN (
    SELECT viaje_id, SUM(monto_bs) as gastos_bs
    FROM gastos_viajes
    WHERE deleted_at IS NULL
    GROUP BY viaje_id
) gv ON v.id = gv.viaje_id
WHERE v.deleted_at IS NULL
GROUP BY CAST(fecha_salida AS DATE);

-- Vista de resumen mensual
CREATE VIEW vw_resumen_mensual AS
SELECT 
    YEAR(fecha_salida) as año,
    MONTH(fecha_salida) as mes,
    COUNT(*) as total_viajes,
    SUM(ingreso_total_bs) as ingresos_bs,
    SUM(ISNULL(gv.gastos_bs, 0)) as gastos_bs,
    SUM(ingreso_total_bs) - SUM(ISNULL(gv.gastos_bs, 0)) as ganancia_bs
FROM viajes v
LEFT JOIN (
    SELECT viaje_id, SUM(monto_bs) as gastos_bs
    FROM gastos_viajes
    WHERE deleted_at IS NULL
    GROUP BY viaje_id
) gv ON v.id = gv.viaje_id
WHERE v.deleted_at IS NULL
GROUP BY YEAR(fecha_salida), MONTH(fecha_salida);

-- Vista por tipo de carga
CREATE VIEW vw_por_tipo_carga AS
SELECT 
    tipo_carga,
    COUNT(*) as total_viajes,
    SUM(peso_ton) as peso_total_ton,
    SUM(ingreso_total_bs) as ingreso_total_bs,
    SUM(ISNULL(gv.gastos_bs, 0)) as gasto_total_bs,
    SUM(ingreso_total_bs) - SUM(ISNULL(gv.gastos_bs, 0)) as margen_bs
FROM viajes v
LEFT JOIN (
    SELECT viaje_id, SUM(monto_bs) as gastos_bs
    FROM gastos_viajes
    WHERE deleted_at IS NULL
    GROUP BY viaje_id
) gv ON v.id = gv.viaje_id
WHERE v.deleted_at IS NULL
GROUP BY tipo_carga;

-- Vista de vehículos con documentos próximos a vencer
CREATE VIEW vw_documentos_vencimiento AS
SELECT 
    v.id,
    v.placa,
    v.marca,
    v.modelo,
    s.nombre as socio_nombre,
    v.soat_vencimiento,
    v.itv_vencimiento,
    v.seguro_vencimiento,
    CASE 
        WHEN v.soat_vencimiento <= DATEADD(day, 30, GETDATE()) THEN 'SOAT'
        WHEN v.itv_vencimiento <= DATEADD(day, 30, GETDATE()) THEN 'ITV'
        WHEN v.seguro_vencimiento <= DATEADD(day, 30, GETDATE()) THEN 'SEGURO'
    END as documento_vencimiento
FROM vehiculos v
INNER JOIN socios s ON v.socio_id = s.id
WHERE v.deleted_at IS NULL
AND (v.soat_vencimiento <= DATEADD(day, 30, GETDATE())
     OR v.itv_vencimiento <= DATEADD(day, 30, GETDATE())
     OR v.seguro_vencimiento <= DATEADD(day, 30, GETDATE()));

-- Vista de choferes con licencias próximas a vencer
CREATE VIEW vw_licencias_vencimiento AS
SELECT 
    id,
    nombre,
    apellido,
    ci,
    licencia_numero,
    licencia_categoria,
    licencia_vencimiento,
    DATEDIFF(day, GETDATE(), licencia_vencimiento) as dias_restantes
FROM choferes
WHERE deleted_at IS NULL
AND licencia_vencimiento <= DATEADD(day, 30, GETDATE());

GO