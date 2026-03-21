-- ========================================
-- DATOS SEMILLA PARA SISTEMA DE TRANSPORTE
-- ========================================

USE GestionTransporte;
GO

-- Limpiar datos existentes (solo para desarrollo)
DELETE FROM auditoria_logs;
DELETE FROM liquidaciones;
DELETE FROM gastos_viajes;
DELETE FROM anticipos;
DELETE FROM mantenimientos;
DELETE FROM viajes;
DELETE FROM remolques;
DELETE FROM vehiculos;
DELETE FROM choferes;
DELETE FROM clientes;
DELETE FROM socios;
DELETE FROM usuario_roles;
DELETE FROM usuarios;
DELETE FROM roles;

-- Resetear identities
DBCC CHECKIDENT ('auditoria_logs', RESEED, 0);
DBCC CHECKIDENT ('liquidaciones', RESEED, 0);
DBCC CHECKIDENT ('gastos_viajes', RESEED, 0);
DBCC CHECKIDENT ('anticipos', RESEED, 0);
DBCC CHECKIDENT ('mantenimientos', RESEED, 0);
DBCC CHECKIDENT ('viajes', RESEED, 0);
DBCC CHECKIDENT ('remolques', RESEED, 0);
DBCC CHECKIDENT ('vehiculos', RESEED, 0);
DBCC CHECKIDENT ('choferes', RESEED, 0);
DBCC CHECKIDENT ('clientes', RESEED, 0);
DBCC CHECKIDENT ('socios', RESEED, 0);
DBCC CHECKIDENT ('usuario_roles', RESEED, 0);
DBCC CHECKIDENT ('usuarios', RESEED, 0);
DBCC CHECKIDENT ('roles', RESEED, 0);

-- ========================================
-- ROLES DEL SISTEMA
-- ========================================
INSERT INTO roles (nombre, descripcion) VALUES
('ADMINISTRADOR', 'Acceso completo al sistema'),
('OPERACIONES', 'Gestión de viajes y vehículos'),
('FINANZAS', 'Liquidaciones y reportes financieros'),
('SOCIO', 'Vista de sus camiones y reportes'),
('CHOFER', 'Vista de sus viajes'),
('CLIENTE', 'Vista de sus órdenes');

-- ========================================
-- USUARIOS DEL SISTEMA
-- ========================================
-- Password: admin123 (hash bcrypt)
INSERT INTO usuarios (email, password_hash, nombre, apellido, telefono, estado) VALUES
('admin@transporte.bo', '$2b$12$LQv3c1yqBWVHxkd0LQ4YFOYznpXZ4uX5E5KvjFzmPNczSbaKF6V6u', 'Carlos', 'Rodriguez', '70123456', 'ACTIVO'),
('operaciones@transporte.bo', '$2b$12$LQv3c1yqBWVHxkd0LQ4YFOYznpXZ4uX5E5KvjFzmPNczSbaKF6V6u', 'Maria', 'Lopez', '70234567', 'ACTIVO'),
('finanzas@transporte.bo', '$2b$12$LQv3c1yqBWVHxkd0LQ4YFOYznpXZ4uX5E5KvjFzmPNczSbaKF6V6u', 'Juan', 'Perez', '70345678', 'ACTIVO'),
('socio1@transporte.bo', '$2b$12$LQv3c1yqBWVHxkd0LQ4YFOYznpXZ4uX5E5KvjFzmPNczSbaKF6V6u', 'Roberto', 'Silva', '70456789', 'ACTIVO'),
('socio2@transporte.bo', '$2b$12$LQv3c1yqBWVHxkd0LQ4YFOYznpXZ4uX5E5KvjFzmPNczSbaKF6V6u', 'Ana', 'Martinez', '70567890', 'ACTIVO');

-- Asignar roles a usuarios
INSERT INTO usuario_roles (usuario_id, rol_id) VALUES
(1, 1), -- Admin: ADMINISTRADOR
(2, 2), -- Operaciones: OPERACIONES
(3, 3), -- Finanzas: FINANZAS
(4, 4), -- Socio1: SOCIO
(5, 4); -- Socio2: SOCIO

-- ========================================
-- SOCIOS (5 socios)
-- ========================================
INSERT INTO socios (nombre, nit, ci, direccion, telefono, email, cuenta_bancaria, banco, participacion_tipo, participacion_valor, usuario_id) VALUES
('Roberto Silva Transportes', '1023456789001', '7890123', 'Av. Brasil 123, Santa Cruz', '70456789', 'socio1@transporte.bo', '1234567890', 'Banco Nacional', 'NETO', 65.00, 4),
('Ana Martinez S.R.L.', '2034567890001', '8901234', 'Calle Sucre 456, Cochabamba', '70567890', 'socio2@transporte.bo', '2345678901', 'Banco Unión', 'NETO', 60.00, 5),
('Transportes Oriente Ltda.', '3045678901001', '9012345', 'Zona Norte 789, La Paz', '70678901', 'oriente@empresa.bo', '3456789012', 'Banco Mercantil', 'BRUTO', 70.00, NULL),
('Flota Boliviana S.A.', '4056789012001', '0123456', 'Av. Pando 321, Santa Cruz', '70789012', 'boliviana@flota.bo', '4567890123', 'BCP', 'NETO', 58.00, NULL),
('Camiones del Sur', '5067890123001', '1234567', 'Calle Comercio 654, Tarija', '70890123', 'sur@camiones.bo', '5678901234', 'Banco Sol', 'NETO', 62.00, NULL);

-- ========================================
-- CHOFERES (10 choferes)
-- ========================================
INSERT INTO choferes (nombre, apellido, ci, licencia_numero, licencia_categoria, licencia_vencimiento, telefono, direccion, experiencia_anos) VALUES
('Pedro', 'Gonzalez', '12345678', 'LIC001', 'D', '2025-12-31', '71123456', 'Barrio San Pedro, Santa Cruz', 8),
('Luis', 'Fernandez', '23456789', 'LIC002', 'D', '2026-03-15', '71234567', 'Villa Primero de Mayo, Cochabamba', 5),
('Mario', 'Vargas', '34567890', 'LIC003', 'D', '2025-09-20', '71345678', 'Zona Sur, La Paz', 12),
('Carlos', 'Mendoza', '45678901', 'LIC004', 'D', '2026-01-10', '71456789', 'Barrio Equipetrol, Santa Cruz', 6),
('Jose', 'Morales', '56789012', 'LIC005', 'D', '2025-11-05', '71567890', 'Zona Norte, Cochabamba', 9),
('Ricardo', 'Torres', '67890123', 'LIC006', 'D', '2026-02-28', '71678901', 'El Alto, La Paz', 4),
('Miguel', 'Castro', '78901234', 'LIC007', 'D', '2025-10-15', '71789012', 'Plan Tres Mil, Santa Cruz', 7),
('Fernando', 'Rojas', '89012345', 'LIC008', 'D', '2026-04-12', '71890123', 'Quillacollo, Cochabamba', 3),
('Daniel', 'Herrera', '90123456', 'LIC009', 'D', '2025-08-30', '71901234', 'Sopocachi, La Paz', 10),
('Alejandro', 'Gutierrez', '01234567', 'LIC010', 'D', '2026-05-18', '71012345', 'Km 7 Doble Via, Santa Cruz', 6);

-- ========================================
-- CLIENTES (3 clientes)
-- ========================================
INSERT INTO clientes (razon_social, nit, contacto_nombre, contacto_telefono, contacto_email, direccion) VALUES
('Agroindustrial San Juan S.A.', '1011223344001', 'Maria Gutierrez', '72111222', 'compras@sanjuan.bo', 'Parque Industrial, Santa Cruz'),
('Cementos Bolivianos Ltda.', '2022334455001', 'Jorge Ramirez', '72222333', 'logistica@cementos.bo', 'Zona Industrial, Cochabamba'),
('Minerales del Altiplano S.R.L.', '3033445566001', 'Patricia Flores', '72333444', 'ventas@minerales.bo', 'Alto La Paz, La Paz');

-- ========================================
-- VEHÍCULOS (12 camiones)
-- ========================================
INSERT INTO vehiculos (placa, marca, modelo, año, capacidad_ton, socio_id, soat_vencimiento, itv_vencimiento, seguro_vencimiento) VALUES
-- Socio 1 (Roberto Silva) - 3 camiones
('SCZ-1001', 'Volvo', 'FH16', 2020, 30.0, 1, '2025-10-15', '2025-11-30', '2025-12-20'),
('SCZ-1002', 'Scania', 'R450', 2019, 28.5, 1, '2025-09-20', '2025-10-25', '2025-11-15'),
('SCZ-1003', 'Mercedes-Benz', 'Actros', 2021, 32.0, 1, '2025-11-10', '2025-12-15', '2026-01-05'),

-- Socio 2 (Ana Martinez) - 2 camiones
('CBB-2001', 'Iveco', 'Stralis', 2018, 25.0, 2, '2025-08-30', '2025-09-15', '2025-10-10'),
('CBB-2002', 'MAN', 'TGX', 2020, 27.5, 2, '2025-10-05', '2025-11-20', '2025-12-25'),

-- Socio 3 (Transportes Oriente) - 3 camiones
('LPZ-3001', 'Volvo', 'FM', 2017, 24.0, 3, '2025-09-10', '2025-10-05', '2025-11-01'),
('LPZ-3002', 'Scania', 'G410', 2019, 26.0, 3, '2025-10-20', '2025-11-15', '2025-12-10'),
('LPZ-3003', 'DAF', 'XF105', 2018, 28.0, 3, '2025-08-15', '2025-09-30', '2025-10-25'),

-- Socio 4 (Flota Boliviana) - 2 camiones
('SCZ-4001', 'Mercedes-Benz', 'Arocs', 2021, 35.0, 4, '2025-11-25', '2025-12-30', '2026-01-20'),
('SCZ-4002', 'Volvo', 'FMX', 2020, 33.0, 4, '2025-10-30', '2025-11-25', '2025-12-15'),

-- Socio 5 (Camiones del Sur) - 2 camiones
('TJA-5001', 'Scania', 'P320', 2019, 22.0, 5, '2025-09-25', '2025-10-20', '2025-11-30'),
('TJA-5002', 'Iveco', 'Trakker', 2020, 26.5, 5, '2025-10-15', '2025-11-10', '2025-12-05');

-- ========================================
-- REMOLQUES (algunos ejemplos)
-- ========================================
INSERT INTO remolques (placa, tipo, capacidad_ton, vehiculo_id) VALUES
('REM-001', 'Semirremolque Granelero', 25.0, 1),
('REM-002', 'Semirremolque Tolva', 22.0, 3),
('REM-003', 'Semirremolque Cisterna', 20.0, 9);

-- ========================================
-- VIAJES (30 viajes de ejemplo)
-- ========================================
INSERT INTO viajes (cliente_id, vehiculo_id, chofer_id, origen, destino, fecha_salida, fecha_llegada, tipo_carga, peso_ton, km_estimado, km_real, tarifa_tipo, tarifa_valor, estado, notas) VALUES
-- Soya (12 viajes)
(1, 1, 1, 'Santa Cruz', 'Puerto Aguirre', '2025-08-01 06:00:00', '2025-08-01 18:00:00', 'soya', 28.5, 320, 325, 'TON', 180.00, 'LIQUIDADO', 'Carga de soya para exportación'),
(1, 2, 2, 'Santa Cruz', 'Puerto Busch', '2025-08-02 05:30:00', '2025-08-02 19:30:00', 'soya', 27.0, 380, 385, 'TON', 180.00, 'LIQUIDADO', 'Soya premium calidad exportación'),
(1, 3, 3, 'Santa Cruz', 'Puerto Aguirre', '2025-08-03 06:15:00', '2025-08-03 18:45:00', 'soya', 30.0, 320, 320, 'TON', 185.00, 'LIQUIDADO', 'Carga completa de soya'),
(1, 4, 4, 'Santa Cruz', 'Puerto Busch', '2025-08-05 05:45:00', '2025-08-05 20:15:00', 'soya', 24.5, 380, 378, 'TON', 180.00, 'LIQUIDADO', 'Transporte soya grado A'),
(1, 5, 5, 'Santa Cruz', 'Puerto Aguirre', '2025-08-07 06:30:00', '2025-08-07 19:00:00', 'soya', 26.8, 320, 322, 'TON', 180.00, 'LIQUIDADO', 'Soya limpia y seca'),
(1, 6, 6, 'Santa Cruz', 'Puerto Busch', '2025-08-10 05:00:00', '2025-08-10 19:45:00', 'soya', 23.2, 380, 382, 'TON', 185.00, 'LIQUIDADO', 'Carga soya exportación'),
(1, 7, 7, 'Santa Cruz', 'Puerto Aguirre', '2025-08-12 06:00:00', '2025-08-12 18:30:00', 'soya', 25.5, 320, 318, 'TON', 180.00, 'ENTREGADO', 'Soya clasificada'),
(1, 8, 8, 'Santa Cruz', 'Puerto Busch', '2025-08-15 05:30:00', '2025-08-15 20:00:00', 'soya', 29.1, 380, 385, 'TON', 180.00, 'ENTREGADO', 'Transporte soya premium'),
(1, 9, 9, 'Santa Cruz', 'Puerto Aguirre', '2025-08-18 06:15:00', '2025-08-18 19:15:00', 'soya', 27.8, 320, 325, 'TON', 185.00, 'EN_RUTA', 'Soya para exportación'),
(1, 10, 10, 'Santa Cruz', 'Puerto Busch', '2025-08-20 05:45:00', NULL, 'soya', 26.3, 380, NULL, 'TON', 180.00, 'PLANIFICADO', 'Carga soya clasificada'),
(1, 11, 1, 'Santa Cruz', 'Puerto Aguirre', '2025-08-22 06:00:00', NULL, 'soya', 28.7, 320, NULL, 'TON', 180.00, 'PLANIFICADO', 'Soya grado exportación'),
(1, 12, 2, 'Santa Cruz', 'Puerto Busch', '2025-08-25 05:30:00', NULL, 'soya', 25.9, 380, NULL, 'TON', 185.00, 'PLANIFICADO', 'Transporte soya premium'),

-- Cemento (7 viajes)
(2, 1, 3, 'Cochabamba', 'Santa Cruz', '2025-08-03 07:00:00', '2025-08-03 16:30:00', 'cemento', 32.0, 210, 215, 'TON', 95.00, 'LIQUIDADO', 'Cemento Portland tipo I'),
(2, 2, 4, 'Cochabamba', 'La Paz', '2025-08-06 08:00:00', '2025-08-06 18:00:00', 'cemento', 30.5, 380, 375, 'TON', 95.00, 'LIQUIDADO', 'Cemento para construcción'),
(2, 3, 5, 'Cochabamba', 'Sucre', '2025-08-09 07:30:00', '2025-08-09 17:45:00', 'cemento', 28.0, 280, 285, 'TON', 100.00, 'LIQUIDADO', 'Cemento especial'),
(2, 4, 6, 'Cochabamba', 'Santa Cruz', '2025-08-13 07:15:00', '2025-08-13 16:45:00', 'cemento', 31.2, 210, 212, 'TON', 95.00, 'ENTREGADO', 'Cemento Portland'),
(2, 5, 7, 'Cochabamba', 'La Paz', '2025-08-16 08:30:00', '2025-08-16 19:00:00', 'cemento', 29.8, 380, 378, 'TON', 95.00, 'EN_RUTA', 'Cemento tipo II'),
(2, 6, 8, 'Cochabamba', 'Tarija', '2025-08-19 07:45:00', NULL, 'cemento', 26.5, 450, NULL, 'TON', 100.00, 'PLANIFICADO', 'Cemento especial Tarija'),
(2, 7, 9, 'Cochabamba', 'Santa Cruz', '2025-08-23 07:00:00', NULL, 'cemento', 30.0, 210, NULL, 'TON', 95.00, 'PLANIFICADO', 'Cemento Portland tipo I'),

-- Minerales (11 viajes adicionales)
(3, 8, 10, 'Oruro', 'Arica', '2025-08-04 05:00:00', '2025-08-05 20:00:00', 'minerales', 35.0, 580, 590, 'TON', 120.00, 'LIQUIDADO', 'Concentrado de zinc'),
(3, 9, 1, 'Potosí', 'Antofagasta', '2025-08-08 04:30:00', '2025-08-09 22:30:00', 'minerales', 33.5, 650, 645, 'TON', 125.00, 'LIQUIDADO', 'Concentrado de plata'),
(3, 10, 2, 'Oruro', 'Arica', '2025-08-11 05:15:00', '2025-08-12 19:45:00', 'minerales', 34.2, 580, 585, 'TON', 120.00, 'LIQUIDADO', 'Estaño en concentrado'),
(3, 11, 3, 'La Paz', 'Iquique', '2025-08-14 06:00:00', '2025-08-15 18:30:00', 'minerales', 31.8, 520, 525, 'TON', 130.00, 'ENTREGADO', 'Concentrado de cobre'),
(3, 12, 4, 'Potosí', 'Antofagasta', '2025-08-17 04:45:00', '2025-08-18 21:15:00', 'minerales', 32.5, 650, 648, 'TON', 125.00, 'EN_RUTA', 'Concentrado de plomo'),
(3, 1, 5, 'Oruro', 'Arica', '2025-08-21 05:30:00', NULL, 'minerales', 33.0, 580, NULL, 'TON', 120.00, 'PLANIFICADO', 'Zinc concentrado'),
(3, 2, 6, 'La Paz', 'Iquique', '2025-08-24 06:15:00', NULL, 'minerales', 30.5, 520, NULL, 'TON', 130.00, 'PLANIFICADO', 'Estaño refinado'),
(3, 3, 7, 'Potosí', 'Antofagasta', '2025-08-26 04:30:00', NULL, 'minerales', 34.8, 650, NULL, 'TON', 125.00, 'PLANIFICADO', 'Concentrado mixto'),
(3, 4, 8, 'Oruro', 'Arica', '2025-08-28 05:00:00', NULL, 'minerales', 32.2, 580, NULL, 'TON', 120.00, 'PLANIFICADO', 'Mineral de zinc'),
(3, 5, 9, 'La Paz', 'Iquique', '2025-08-30 06:00:00', NULL, 'minerales', 29.8, 520, NULL, 'TON', 130.00, 'PLANIFICADO', 'Cobre concentrado'),
(3, 6, 10, 'Potosí', 'Antofagasta', '2025-09-01 04:45:00', NULL, 'minerales', 33.7, 650, NULL, 'TON', 125.00, 'PLANIFICADO', 'Plomo concentrado');

-- ========================================
-- GASTOS DE VIAJES (ejemplos para algunos viajes)
-- ========================================
INSERT INTO gastos_viajes (viaje_id, tipo, monto_bs, descripcion, fecha) VALUES
-- Gastos del viaje 1 (soya)
(1, 'COMBUSTIBLE', 1200.00, 'Diesel para Santa Cruz - Puerto Aguirre', '2025-08-01 06:30:00'),
(1, 'PEAJE', 25.00, 'Peaje carretera', '2025-08-01 10:00:00'),
(1, 'VIATICO', 150.00, 'Viáticos chofer', '2025-08-01 06:00:00'),

-- Gastos del viaje 2 (soya)
(2, 'COMBUSTIBLE', 1380.00, 'Diesel para Santa Cruz - Puerto Busch', '2025-08-02 05:45:00'),
(2, 'PEAJE', 30.00, 'Peajes ruta', '2025-08-02 12:00:00'),
(2, 'VIATICO', 180.00, 'Viáticos chofer ruta larga', '2025-08-02 05:30:00'),

-- Gastos del viaje 13 (cemento)
(13, 'COMBUSTIBLE', 950.00, 'Diesel Cochabamba - Santa Cruz', '2025-08-03 07:15:00'),
(13, 'PEAJE', 20.00, 'Peaje autopista', '2025-08-03 11:00:00'),
(13, 'VIATICO', 120.00, 'Viáticos día completo', '2025-08-03 07:00:00'),
(13, 'TALLER', 280.00, 'Cambio de llanta en ruta', '2025-08-03 14:30:00'),

-- Gastos del viaje 21 (minerales)
(21, 'COMBUSTIBLE', 2100.00, 'Diesel Oruro - Arica', '2025-08-04 05:30:00'),
(21, 'PEAJE', 45.00, 'Peajes internacionales', '2025-08-04 16:00:00'),
(21, 'VIATICO', 350.00, 'Viáticos 2 días', '2025-08-04 05:00:00'),
(21, 'OTRO', 150.00, 'Trámites frontera', '2025-08-04 20:00:00');

-- ========================================
-- ANTICIPOS (ejemplos)
-- ========================================
INSERT INTO anticipos (viaje_id, socio_id, chofer_id, beneficiario_tipo, monto_bs, observacion) VALUES
-- Anticipos a socios
(1, 1, NULL, 'SOCIO', 2000.00, 'Anticipo para combustible viaje soya'),
(13, 2, NULL, 'SOCIO', 1500.00, 'Anticipo operativo cemento'),
(21, 3, NULL, 'SOCIO', 3000.00, 'Anticipo viaje internacional minerales'),

-- Anticipos a choferes
(NULL, NULL, 1, 'CHOFER', 500.00, 'Anticipo personal chofer Pedro'),
(NULL, NULL, 5, 'CHOFER', 400.00, 'Anticipo familiar chofer Jose'),
(2, NULL, 2, 'CHOFER', 300.00, 'Anticipo viáticos viaje Puerto Busch');

-- ========================================
-- LIQUIDACIONES (para viajes completados)
-- ========================================
INSERT INTO liquidaciones (viaje_id, ingreso_bs, gastos_bs, pago_socio_bs, saldo_socio_bs, saldo_chofer_bs) VALUES
-- Liquidación viaje 1 (soya): 28.5 * 180 = 5130 ingreso
(1, 5130.00, 1375.00, 2439.75, -439.75, 0.00), -- 65% de (5130-1375) = 2439.75, menos anticipo 2000 = -439.75

-- Liquidación viaje 2 (soya): 27 * 180 = 4860 ingreso
(2, 4860.00, 1590.00, 2125.50, 2125.50, 0.00), -- 65% de (4860-1590) = 2125.50

-- Liquidación viaje 13 (cemento): 32 * 95 = 3040 ingreso
(13, 3040.00, 1370.00, 1002.00, -498.00, 0.00), -- 60% de (3040-1370) = 1002, menos anticipo 1500 = -498

-- Liquidación viaje 21 (minerales): 35 * 120 = 4200 ingreso
(21, 4200.00, 2645.00, 1088.50, -1911.50, 0.00); -- 70% de (4200-2645) = 1088.50, menos anticipo 3000 = -1911.50

-- ========================================
-- MANTENIMIENTOS (ejemplos)
-- ========================================
INSERT INTO mantenimientos (vehiculo_id, tipo, descripcion, costo_bs, fecha, taller, proximo_km, proxima_fecha) VALUES
-- Mantenimientos preventivos
(1, 'PREVENTIVO', 'Cambio de aceite y filtros', 580.00, '2025-07-15', 'Taller Volvo Santa Cruz', 25000, '2025-10-15'),
(2, 'PREVENTIVO', 'Revisión general 10000 km', 1200.00, '2025-07-20', 'Scania Service', 30000, '2025-11-20'),
(3, 'PREVENTIVO', 'Cambio de pastillas de freno', 450.00, '2025-08-01', 'Mercedes Benz Service', NULL, '2025-11-01'),

-- Mantenimientos correctivos
(4, 'CORRECTIVO', 'Reparación sistema hidráulico', 2800.00, '2025-07-25', 'Taller Industrial CBB', NULL, NULL),
(5, 'CORRECTIVO', 'Cambio de embrague', 3500.00, '2025-08-10', 'MAN Service Center', NULL, NULL),
(6, 'CORRECTIVO', 'Reparación motor - junta de culata', 4200.00, '2025-08-05', 'Taller Diesel La Paz', NULL, NULL);

GO

-- Actualizar saldos de anticipos en socios
UPDATE socios SET saldo_anticipos = 2000.00 WHERE id = 1; -- Roberto Silva
UPDATE socios SET saldo_anticipos = 1500.00 WHERE id = 2; -- Ana Martinez
UPDATE socios SET saldo_anticipos = 3000.00 WHERE id = 3; -- Transportes Oriente

PRINT 'Datos semilla insertados correctamente';
PRINT 'Total Socios: 5';
PRINT 'Total Choferes: 10';
PRINT 'Total Vehículos: 12';
PRINT 'Total Clientes: 3';
PRINT 'Total Viajes: 30 (12 soya, 7 cemento, 11 minerales)';
PRINT 'Usuario admin: admin@transporte.bo / admin123';
GO