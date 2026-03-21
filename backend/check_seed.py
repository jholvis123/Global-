from app.db.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Verificar zonas geográficas
    result = conn.execute(text("SELECT id, nombre, tarifa_base_km FROM zonageografica"))
    print('Zonas geográficas:')
    for row in result:
        print(f'  ID: {row[0]}, Nombre: {row[1]}, Tarifa base: {row[2]}')

    print()

    # Verificar tarifas
    result = conn.execute(text("""
        SELECT t.id, zo.nombre as origen, zd.nombre as destino, t.distancia_km, t.precio_base
        FROM tarifa t
        JOIN zonageografica zo ON t.zona_origen_id = zo.id
        JOIN zonageografica zd ON t.zona_destino_id = zd.id
    """))
    print('Tarifas:')
    for row in result:
        print(f'  {row[1]} -> {row[2]}: {row[3]}km, ${row[4]}')