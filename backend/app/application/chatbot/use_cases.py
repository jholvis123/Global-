from app.domain.chatbot.entities import SolicitudCotizacion, TipoCarga
from app.domain.chatbot.interfaces import RepositorioTarifas, ServicioPLN
from app.application.chatbot.strategies import FabricaEstrategiasTarifa

class GenerarCotizacionCasoUso:
    def __init__(self, repositorio_tarifas: RepositorioTarifas, servicio_pln: ServicioPLN):
        """Inyección de dependencias estricta a través de constructores"""
        self.repositorio_tarifas = repositorio_tarifas
        self.servicio_pln = servicio_pln

    def ejecutar(self, texto_usuario: str) -> SolicitudCotizacion:
        # 1. Extraer entidades del lenguaje natural utilizando la Interfaz PLN
        datos_extraidos = self.servicio_pln.extraer_datos_cotizacion(texto_usuario)
        
        origen = datos_extraidos.get("origen")
        destino = datos_extraidos.get("destino")
        tipo_carga_str = datos_extraidos.get("tipo_carga", "general").lower()
        peso_kg = datos_extraidos.get("peso_kg", 0.0)

        if not origen or not destino:
            raise ValueError("No se detectó un origen y destino claros en tu solicitud.")

        # 2. Conversión estricta al Enum de Dominio
        try:
            tipo_carga = TipoCarga(tipo_carga_str)
        except ValueError:
            tipo_carga = TipoCarga.GENERAL

        # 3. Recuperar tarifa base desde Repositorio (Interfaz)
        tarifa_ruta = self.repositorio_tarifas.buscar_tarifa(origen, destino)
        if not tarifa_ruta:
            raise ValueError(f"Lo sentimos, no cubrimos la ruta: {origen} -> {destino}")

        # 4. Cálculo de tarifa utilizando el Patrón Strategy
        estrategia = FabricaEstrategiasTarifa.obtener_estrategia(tipo_carga)
        precio_final = estrategia.calcular(
            precio_base_ruta=tarifa_ruta.precio_base, 
            peso_kg=peso_kg
        )

        # 5. Crear la entidad de Dominio final
        cotizacion = SolicitudCotizacion(
            texto_original=texto_usuario,
            origen=origen,
            destino=destino,
            tipo_carga=tipo_carga,
            peso_kg=peso_kg,
            precio_calculado=precio_final
        )

        # 6. Almacenar el registro para auditoría/historial
        return self.repositorio_tarifas.guardar_solicitud(cotizacion)
