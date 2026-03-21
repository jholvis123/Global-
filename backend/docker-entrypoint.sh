#!/bin/bash

# Script de entrada para el contenedor FastAPI
set -e

echo "🚀 Iniciando contenedor FastAPI..."

# Esperar que la base de datos esté disponible
echo "⏳ Esperando que SQL Server esté disponible..."
while ! python -c "
import pyodbc
import os
try:
    conn = pyodbc.connect(os.environ.get('DATABASE_URL', ''))
    conn.close()
    print('✅ Base de datos conectada')
except:
    raise Exception('❌ Base de datos no disponible')
"; do
    echo "⏳ Reintentando conexión a base de datos..."
    sleep 5
done

# Ejecutar migraciones si existen
echo "🔄 Ejecutando migraciones..."
if [ -d "alembic/versions" ]; then
    alembic upgrade head
    echo "✅ Migraciones completadas"
else
    echo "ℹ️  No hay migraciones para ejecutar"
fi

# Crear directorios necesarios
mkdir -p uploads/documents
mkdir -p uploads/images
mkdir -p logs

echo "✅ Contenedor listo para iniciar"

# Ejecutar comando
exec "$@"