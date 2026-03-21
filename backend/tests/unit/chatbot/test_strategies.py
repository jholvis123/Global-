import pytest
from app.application.chatbot.strategies import FabricaEstrategiasTarifa
from app.domain.chatbot.entities import TipoCarga

class TestEstrategiasTarifa:
    """Suite de Pruebas para validar matemáticamente el coste por tipo de carga"""

    @pytest.mark.parametrize("precio_base, peso, esperado", [
        (100.0, 10.0, 105.0),   # 100 + (10 * 0.5) = 105.0
        (500.0, 100.0, 550.0),  # 500 + (100 * 0.5) = 550.0
        (0.0, 50.0, 25.0),      # 0 + (50 * 0.5) = 25.0
    ])
    def test_carga_general_calculo_correcto(self, precio_base, peso, esperado):
        estrategia = FabricaEstrategiasTarifa.obtener_estrategia(TipoCarga.GENERAL)
        resultado = estrategia.calcular(precio_base, peso)
        assert resultado == esperado

    @pytest.mark.parametrize("precio_base, peso, esperado", [
        (100.0, 10.0, 162.0),   # (100 + (10 * 0.8)) * 1.5 = (108) * 1.5 = 162.0
    ])
    def test_carga_peligrosa_calculo_correcto(self, precio_base, peso, esperado):
        estrategia = FabricaEstrategiasTarifa.obtener_estrategia(TipoCarga.PELIGROSA)
        resultado = estrategia.calcular(precio_base, peso)
        assert resultado == esperado

    @pytest.mark.parametrize("precio_base, peso, esperado", [
        (100.0, 10.0, 137.8),   # (100 + (10 * 0.6)) * 1.3 = (106) * 1.3 = 137.8
    ])
    def test_carga_refrigerada_calculo_correcto(self, precio_base, peso, esperado):
        estrategia = FabricaEstrategiasTarifa.obtener_estrategia(TipoCarga.REFRIGERADA)
        resultado = estrategia.calcular(precio_base, peso)
        assert resultado == esperado
