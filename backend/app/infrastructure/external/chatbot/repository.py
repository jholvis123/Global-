from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import Optional
from app.domain.chatbot.interfaces import RepositorioTarifas
from app.domain.chatbot.entities import Tarifa, SolicitudCotizacion, ZonaGeografica

class PostgresRepositorioTarifas(RepositorioTarifas):
    def __init__(self, session: Session):
        self.session = session

    def buscar_tarifa(self, origen: str, destino: str) -> Optional[Tarifa]:
        zona_origen = self.session.query(ZonaGeografica).filter(
            ZonaGeografica.nombre == origen
        ).first()
        
        zona_destino = self.session.query(ZonaGeografica).filter(
            ZonaGeografica.nombre == destino
        ).first()

        if not zona_origen or not zona_destino:
            return None

        tarifa = self.session.query(Tarifa).filter(
            and_(
                Tarifa.zona_origen_id == zona_origen.id,
                Tarifa.zona_destino_id == zona_destino.id
            )
        ).first()

        return tarifa

    def guardar_solicitud(self, solicitud: SolicitudCotizacion) -> SolicitudCotizacion:
        self.session.add(solicitud)
        self.session.commit()
        self.session.refresh(solicitud)
        return solicitud
