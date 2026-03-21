import pytest
from typing import Dict, Any, Optional
from app.domain.chatbot.entities import Tarifa, SolicitudCotizacion, TipoCarga
from app.domain.chatbot.interfaces import RepositorioTarifas, ServicioPLN
from app.application.chatbot.use_cases import GenerarCotizacionCasoUso

# ------------- MOCKS DE INFRAESTRUCTURA -------------

class FakeServicioPLN(ServicioPLN):
    """Simula el motor spaCy dictando que el PLN extrajo 'X' datos exáctos"""
    def __init__(self, datos_simulados: Dict[str, Any]):
        self.datos_simulados = datos_simulados

    def extraer_datos_cotizacion(self, texto: str) -> Dict[str, Any]:
        return self.datos_simulados

class FakeRepositorioTarifas(RepositorioTarifas):
    """Simula la Base de Datos de PostgreSQL en SQLModel"""
    def __init__(self, tarifa_simulada: Optional[Tarifa] = None):
        self.tarifa_simulada = tarifa_simulada
        self.solicitud_guardada = None

    def buscar_tarifa(self, origen: str, destino: str) -> Optional[Tarifa]:
        return self.tarifa_simulada

    def guardar_solicitud(self, solicitud: SolicitudCotizacion) -> SolicitudCotizacion:
        solicitud.id = 999  # Simulamos id autogenerado por BD
        self.solicitud_guardada = solicitud
        return solicitud

# ------------- SUITE DE PRUEBAS -------------

class TestGenerarCotizacionCasoUso:
    
    def test_flujo_feliz_cotizacion_general(self):
        """Prueba que el caso de uso orquesta correctamente todo si los datos son perfectos"""
        
        # 1. Arrange (Preparar)
        datos_pln = {
            "origen": "Santa Cruz",
            "destino": "La Paz",
            "tipo_carga": "general",
            "peso_kg": 100.0
        }
        tarifa_db = Tarifa(id=1, zona_origen_id=1, zona_destino_id=2, distancia_km=850, precio_base=1000.0)
        
        mock_pln = FakeServicioPLN(datos_pln)
        mock_repo = FakeRepositorioTarifas(tarifa_simulada=tarifa_db)
        
        caso_uso = GenerarCotizacionCasoUso(repositorio_tarifas=mock_repo, servicio_pln=mock_pln)
        texto_usuario = "Lleva 100 kilos de papas de santa cruz a la paz"

        # 2. Act (Actuar)
        resultado = caso_uso.ejecutar(texto_usuario)

        # 3. Assert (Afirmar)
        assert resultado.id == 999
        assert resultado.origen == "Santa Cruz"
        assert resultado.destino == "La Paz"
        assert resultado.tipo_carga == TipoCarga.GENERAL
        
        # Matemáticas para general: 1000 base + (100kg * 0.5) = 1050
        assert resultado.precio_calculado == 1050.0
        
        # Verificamos que el repositorio intentó guardarlo
        assert mock_repo.solicitud_guardada is not None

    def test_error_cuando_pln_no_encuentra_origen_o_destino(self):
        """Verifica que el Backend rechace la solicitud si el usuario habla confuso"""
        
        datos_pln_incompletos = {
            "origen": None,  # Faltan datos!
            "destino": "La Paz",
            "tipo_carga": "general",
            "peso_kg": 0.0
        }
        mock_pln = FakeServicioPLN(datos_pln_incompletos)
        mock_repo = FakeRepositorioTarifas()  # BD vacía no importa, fallará antes
        
        caso_uso = GenerarCotizacionCasoUso(repositorio_tarifas=mock_repo, servicio_pln=mock_pln)

        # Usamos pytest.raises para asegurar que lance un Error
        with pytest.raises(ValueError, match="No se detectó un origen y destino claros"):
            caso_uso.ejecutar("hola quiero un viaje a la paz")

    def test_error_cuando_ruta_no_existe_en_db(self):
        """Verifica que rechace la solicitud si la ruta no tiene tarifa en Base de Datos"""
        
        datos_pln = {
            "origen": "Madrid", # Destino fuera de cobertura
            "destino": "Paris",
            "tipo_carga": "general",
            "peso_kg": 100.0
        }
        mock_pln = FakeServicioPLN(datos_pln)
        # Repo retorna None porque no existe la tarifa
        mock_repo = FakeRepositorioTarifas(tarifa_simulada=None) 
        
        caso_uso = GenerarCotizacionCasoUso(repositorio_tarifas=mock_repo, servicio_pln=mock_pln)

        with pytest.raises(ValueError, match="Lo sentimos, no cubrimos la ruta: Madrid -> Paris"):
            caso_uso.ejecutar("Lleva esto de madrid a paris")
