from sqlalchemy.orm import Session
from sqlalchemy import text
from app.infrastructure.database.database import get_db
import logging

logger = logging.getLogger(__name__)

def crear_datos_semilla_chatbot():
    """Seed data para el sistema de cotizaciones del chatbot"""
    
    db = next(get_db())
    
    try:
        # Verificar si ya existe data
        result = db.execute(text("SELECT COUNT(*) FROM zonageografica"))
        zonas_count = result.scalar()
        if zonas_count > 0:
            logger.info("Data de chatbot ya existe, saltando seed...")
            return
        
        logger.info("Creando data semilla para chatbot...")
        
        # Crear zonas geográficas de Bolivia
        zonas_data = [
            ("Santa Cruz", 0.5),
            ("La Paz", 0.6),
            ("Cochabamba", 0.55),
            ("Sucre", 0.58),
            ("Oruro", 0.52),
            ("Potosí", 0.53),
            ("Tarija", 0.51),
            ("Beni", 0.49),
            ("Pando", 0.48),
            ("El Alto", 0.57),
        ]
        
        for nombre, tarifa in zonas_data:
            db.execute(text("INSERT INTO zonageografica (nombre, tarifa_base_km) VALUES (:nombre, :tarifa)"), 
                      {"nombre": nombre, "tarifa": tarifa})
        
        # Crear rutas y tarifas entre zonas principales
        rutas_data = [
            ("Santa Cruz", "La Paz", 800, 400),
            ("Santa Cruz", "Cochabamba", 400, 200),
            ("Santa Cruz", "Sucre", 600, 300),
            ("La Paz", "Cochabamba", 200, 100),
            ("La Paz", "Oruro", 250, 125),
            ("Cochabamba", "Sucre", 300, 150),
            ("Cochabamba", "Oruro", 150, 75),
            ("Sucre", "Potosí", 200, 100),
            ("Oruro", "Potosí", 250, 125),
            ("Santa Cruz", "Tarija", 500, 250),
        ]
        
        for origen, destino, distancia, precio in rutas_data:
            # Obtener IDs de zonas
            origen_result = db.execute(text("SELECT id FROM zonageografica WHERE nombre = :nombre"), {"nombre": origen})
            origen_id = origen_result.scalar()
            
            destino_result = db.execute(text("SELECT id FROM zonageografica WHERE nombre = :nombre"), {"nombre": destino})
            destino_id = destino_result.scalar()
            
            if origen_id and destino_id:
                db.execute(text("""
                    INSERT INTO tarifa (zona_origen_id, zona_destino_id, distancia_km, precio_base) 
                    VALUES (:origen_id, :destino_id, :distancia, :precio)
                """), {
                    "origen_id": origen_id,
                    "destino_id": destino_id,
                    "distancia": distancia,
                    "precio": precio
                })
        
        db.commit()
        logger.info("Data semilla para chatbot creada exitosamente!")
        
    except Exception as e:
        logger.error(f"Error creando data semilla: {e}")
        db.rollback()
    finally:
        db.close()
