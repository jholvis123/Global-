"""
Domain Services - Lógica de negocio pura que no pertenece a una entidad específica
"""
from decimal import Decimal
from typing import Dict, Any, List
from datetime import datetime

from app.domain.value_objects import Dinero, Tarifa, Porcentaje


class CalculadoraTarifa:
    """
    Domain Service para calcular tarifas e ingresos de viajes.
    Centraliza TODA la lógica de cálculo de tarifas.
    """
    
    def calcular_ingreso(
        self,
        tarifa_tipo: str,
        tarifa_valor: Decimal,
        peso_ton: Decimal,
        km: int
    ) -> Dinero:
        """
        Calcular el ingreso de un viaje basado en la tarifa.
        
        Args:
            tarifa_tipo: Tipo de tarifa (KM, TON, FIJA)
            tarifa_valor: Valor unitario de la tarifa
            peso_ton: Peso en toneladas
            km: Kilómetros del viaje
            
        Returns:
            Dinero con el ingreso calculado
        """
        tarifa = Tarifa(tarifa_tipo, tarifa_valor)
        return tarifa.calcular_ingreso(peso_ton, km)
    
    def calcular_con_recargos(
        self,
        ingreso_base: Dinero,
        recargos: List[Dict[str, Any]]
    ) -> Dinero:
        """
        Calcular ingreso con recargos adicionales.
        
        Args:
            ingreso_base: Ingreso base del viaje
            recargos: Lista de recargos [{tipo, valor, es_porcentaje}]
            
        Returns:
            Dinero con el total incluyendo recargos
        """
        total = ingreso_base
        
        for recargo in recargos:
            if recargo.get("es_porcentaje", False):
                porcentaje = Porcentaje(Decimal(str(recargo["valor"])))
                total = total + porcentaje.aplicar_a(ingreso_base)
            else:
                total = total + Dinero(Decimal(str(recargo["valor"])))
        
        return total.redondear()


class CalculadoraLiquidacion:
    """
    Domain Service para calcular liquidaciones de viajes.
    TODA la lógica de liquidación está aquí.
    """
    
    def calcular(
        self,
        ingreso_bs: Decimal,
        gastos: List[Dict[str, Any]],
        porcentaje_socio: Decimal,
        anticipos_pendientes: Decimal = Decimal("0")
    ) -> Dict[str, Any]:
        """
        Calcular liquidación completa de un viaje.
        
        Args:
            ingreso_bs: Ingreso bruto del viaje
            gastos: Lista de gastos [{tipo, monto_bs}]
            porcentaje_socio: Porcentaje de participación del socio
            anticipos_pendientes: Anticipos a descontar
            
        Returns:
            Dict con todos los cálculos de la liquidación
        """
        # Convertir a objetos de dominio
        ingreso = Dinero(ingreso_bs)
        total_gastos = Dinero(sum(Decimal(str(g["monto_bs"])) for g in gastos))
        
        # Calcular margen bruto
        margen_bruto = ingreso - total_gastos
        
        # Calcular pago al socio
        porcentaje = Porcentaje(porcentaje_socio)
        pago_socio = porcentaje.aplicar_a(margen_bruto)
        
        # Descontar anticipos
        anticipos = Dinero(anticipos_pendientes)
        saldo_socio = pago_socio - anticipos
        
        # Comisión de la empresa
        comision_empresa = margen_bruto - pago_socio
        
        # Calcular rentabilidad
        rentabilidad = self._calcular_rentabilidad(ingreso, margen_bruto)
        
        return {
            "ingreso_bs": ingreso.valor,
            "gastos_bs": total_gastos.valor,
            "margen_bruto_bs": margen_bruto.valor,
            "porcentaje_socio": porcentaje_socio,
            "pago_socio_bs": pago_socio.redondear().valor,
            "anticipos_descontados_bs": anticipos.valor,
            "saldo_socio_bs": saldo_socio.redondear().valor,
            "comision_empresa_bs": comision_empresa.redondear().valor,
            "rentabilidad_pct": rentabilidad,
            "detalles_gastos": self._agrupar_gastos(gastos),
            "fecha_calculo": datetime.utcnow()
        }
    
    def _calcular_rentabilidad(self, ingreso: Dinero, margen: Dinero) -> Decimal:
        """Calcular porcentaje de rentabilidad"""
        if ingreso.es_cero:
            return Decimal("0")
        return ((margen.valor / ingreso.valor) * 100).quantize(Decimal("0.01"))
    
    def _agrupar_gastos(self, gastos: List[Dict[str, Any]]) -> Dict[str, Decimal]:
        """Agrupar gastos por tipo"""
        agrupados = {}
        for gasto in gastos:
            tipo = gasto.get("tipo", "OTRO")
            monto = Decimal(str(gasto["monto_bs"]))
            agrupados[tipo] = agrupados.get(tipo, Decimal("0")) + monto
        return agrupados


class ValidadorViaje:
    """
    Domain Service para validar reglas de negocio de viajes.
    Centraliza TODAS las validaciones de viajes.
    """
    
    ESTADOS_VALIDOS = ["PLANIFICADO", "EN_RUTA", "ENTREGADO", "LIQUIDADO", "CANCELADO"]
    TIPOS_CARGA = ["GENERAL", "GRANEL", "LIQUIDOS", "REFRIGERADO", "PELIGROSO", "CONTENEDOR"]
    
    def validar_creacion(
        self,
        origen: str,
        destino: str,
        peso_ton: Decimal,
        km_estimado: int,
        tarifa_tipo: str,
        tarifa_valor: Decimal,
        tipo_carga: str
    ) -> List[str]:
        """
        Validar datos para crear un viaje.
        
        Returns:
            Lista vacía si es válido, lista de errores si no
        """
        errores = []
        
        # Validar origen y destino
        if not origen or len(origen.strip()) < 2:
            errores.append("El origen debe tener al menos 2 caracteres")
        
        if not destino or len(destino.strip()) < 2:
            errores.append("El destino debe tener al menos 2 caracteres")
        
        if origen and destino and origen.strip().lower() == destino.strip().lower():
            errores.append("El origen y destino no pueden ser iguales")
        
        # Validar peso
        if peso_ton <= 0:
            errores.append("El peso debe ser mayor a 0 toneladas")
        
        if peso_ton > Decimal("100"):
            errores.append("El peso no puede exceder 100 toneladas")
        
        # Validar kilómetros
        if km_estimado <= 0:
            errores.append("Los kilómetros estimados deben ser mayores a 0")
        
        if km_estimado > 5000:
            errores.append("Los kilómetros no pueden exceder 5000 km")
        
        # Validar tarifa
        if tarifa_tipo not in ["KM", "TON", "FIJA"]:
            errores.append("Tipo de tarifa debe ser KM, TON o FIJA")
        
        if tarifa_valor <= 0:
            errores.append("El valor de la tarifa debe ser mayor a 0")
        
        # Validar tipo de carga
        if tipo_carga and tipo_carga not in self.TIPOS_CARGA:
            errores.append(f"Tipo de carga debe ser: {', '.join(self.TIPOS_CARGA)}")
        
        return errores
    
    def puede_cambiar_estado(self, estado_actual: str, estado_nuevo: str) -> bool:
        """
        Validar si una transición de estado es válida.
        
        Transiciones permitidas:
        PLANIFICADO -> EN_RUTA, CANCELADO
        EN_RUTA -> ENTREGADO, CANCELADO
        ENTREGADO -> LIQUIDADO
        LIQUIDADO -> (ninguno, es estado final)
        CANCELADO -> (ninguno, es estado final)
        """
        transiciones = {
            "PLANIFICADO": ["EN_RUTA", "CANCELADO"],
            "EN_RUTA": ["ENTREGADO", "CANCELADO"],
            "ENTREGADO": ["LIQUIDADO"],
            "LIQUIDADO": [],
            "CANCELADO": []
        }
        
        return estado_nuevo in transiciones.get(estado_actual, [])
    
    def validar_finalizacion(
        self,
        estado_actual: str,
        km_real: int = None
    ) -> List[str]:
        """Validar requisitos para finalizar un viaje"""
        errores = []
        
        if estado_actual != "EN_RUTA":
            errores.append("Solo se pueden finalizar viajes EN_RUTA")
        
        if km_real is None or km_real <= 0:
            errores.append("Debe especificar los kilómetros reales")
        
        return errores
    
    def validar_liquidacion(
        self,
        estado_actual: str,
        tiene_chofer: bool,
        tiene_vehiculo: bool,
        ingreso: Decimal
    ) -> List[str]:
        """Validar requisitos para liquidar un viaje"""
        errores = []
        
        if estado_actual != "ENTREGADO":
            errores.append("Solo se pueden liquidar viajes ENTREGADOS")
        
        if not tiene_chofer:
            errores.append("El viaje debe tener un chofer asignado")
        
        if not tiene_vehiculo:
            errores.append("El viaje debe tener un vehículo asignado")
        
        if ingreso <= 0:
            errores.append("El viaje debe tener ingresos mayores a 0")
        
        return errores


class CalculadoraEstadisticas:
    """
    Domain Service para calcular estadísticas y reportes.
    """
    
    def calcular_resumen_viajes(self, viajes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcular resumen estadístico de una lista de viajes"""
        if not viajes:
            return self._resumen_vacio()
        
        total_ingresos = sum(Decimal(str(v.get("ingreso_bs", 0))) for v in viajes)
        total_gastos = sum(Decimal(str(v.get("gastos_bs", 0))) for v in viajes)
        total_km = sum(v.get("km_real", v.get("km_estimado", 0)) for v in viajes)
        total_ton = sum(Decimal(str(v.get("peso_ton", 0))) for v in viajes)
        
        margen = total_ingresos - total_gastos
        
        # Contar por estado
        estados = {}
        for v in viajes:
            estado = v.get("estado", "DESCONOCIDO")
            estados[estado] = estados.get(estado, 0) + 1
        
        return {
            "total_viajes": len(viajes),
            "ingresos_bs": float(total_ingresos),
            "gastos_bs": float(total_gastos),
            "margen_bs": float(margen),
            "rentabilidad_pct": float(
                (margen / total_ingresos * 100) if total_ingresos > 0 else 0
            ),
            "km_totales": total_km,
            "toneladas_totales": float(total_ton),
            "promedio_ingreso_bs": float(total_ingresos / len(viajes)),
            "promedio_km": total_km // len(viajes),
            "por_estado": estados
        }
    
    def _resumen_vacio(self) -> Dict[str, Any]:
        """Retornar resumen vacío cuando no hay datos"""
        return {
            "total_viajes": 0,
            "ingresos_bs": 0.0,
            "gastos_bs": 0.0,
            "margen_bs": 0.0,
            "rentabilidad_pct": 0.0,
            "km_totales": 0,
            "toneladas_totales": 0.0,
            "promedio_ingreso_bs": 0.0,
            "promedio_km": 0,
            "por_estado": {}
        }
