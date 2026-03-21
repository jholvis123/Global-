from app.db.database import SessionLocal
from app.domain.chatbot.entities import SolicitudCotizacion

db = SessionLocal()
solicitudes = db.query(SolicitudCotizacion).order_by(SolicitudCotizacion.id.desc()).limit(10).all()

print("╔════════════════════════════════════════════════════════════════╗")
print("║  PERSISTENCIA EN BD: Últimas 10 solicitudes                   ║")
print("╚════════════════════════════════════════════════════════════════╝\n")

if solicitudes:
    for s in solicitudes:
        print(f"ID: {s.id:3} | {s.origen:12} → {s.destino:12} | {s.peso_kg:8.1f}kg | {s.tipo_carga:12} | ${s.precio_calculado:7.2f} Bs")
    print(f"\nTOTAL en BD: {db.query(SolicitudCotizacion).count()} solicitudes")
else:
    print("No hay solicitudes")

db.close()
