from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class AuditoriaLog(BaseModel):
    """Modelo de auditoría de cambios"""
    __tablename__ = "auditoria_logs"
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    tabla = Column(String(50), nullable=False, index=True)
    registro_id = Column(Integer, nullable=False, index=True)
    operacion = Column(String(10), nullable=False)  # INSERT, UPDATE, DELETE
    valores_anteriores = Column(Text)
    valores_nuevos = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Constraints
    __table_args__ = (
        CheckConstraint("operacion IN ('INSERT', 'UPDATE', 'DELETE')", name="ck_auditoria_operacion"),
    )
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="auditoria_logs")
    
    @property
    def usuario_nombre(self):
        """Retorna el nombre del usuario que realizó la operación"""
        if self.usuario:
            return self.usuario.nombre_completo
        return "Sistema"
    
    @property
    def descripcion_operacion(self):
        """Retorna una descripción legible de la operación"""
        operaciones = {
            "INSERT": "Creación",
            "UPDATE": "Modificación", 
            "DELETE": "Eliminación"
        }
        return operaciones.get(self.operacion, self.operacion)
    
    @property
    def resumen_cambio(self):
        """Retorna un resumen del cambio realizado"""
        return f"{self.descripcion_operacion} en {self.tabla} (ID: {self.registro_id})"