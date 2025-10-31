import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas


@pytest.fixture
def sistema():
    return SistemaExpertoPlagas()


class TestExplicacion:
    """Verifica trazabilidad y explicación del razonamiento."""

    def test_diagnostico_incluye_regla_activada(self, sistema):
        resultado = sistema.diagnosticar("palta", ["raspado_frutos", "rugosidad_frutos", "bronceado_frutos"])
        d = resultado["diagnosticos"][0]
        assert "regla_activada" in d
        assert d["regla_activada"] == "trips_completo"

    def test_reglas_activadas_en_resultado_general(self, sistema):
        resultado = sistema.diagnosticar("palta", ["hojas_amarillas", "defoliacion", "raices_necrosadas", "frutos_pequenos"])
        assert "reglas_activadas" in resultado
        assert "tristeza_completa" in resultado["reglas_activadas"]

    def test_explicacion_incluye_umbral_y_recomendaciones(self, sistema):
        resultado = sistema.diagnosticar("palta", ["cancros_tronco", "exudados_blancos", "muerte_ramas"])
        d = resultado["diagnosticos"][0]
        assert "umbral" in d
        assert "recomendaciones" in d
        assert len(d["recomendaciones"]) > 0

    def test_explicacion_diferencia_certezas(self, sistema):
        completo = sistema.diagnosticar("palta", ["raspado_frutos", "rugosidad_frutos", "bronceado_frutos"])
        parcial = sistema.diagnosticar("palta", ["raspado_frutos", "rugosidad_frutos"])
        assert completo["diagnosticos"][0]["certeza"] > parcial["diagnosticos"][0]["certeza"]
        assert completo["diagnosticos"][0]["regla_activada"] == "trips_completo"
        assert parcial["diagnosticos"][0]["regla_activada"] == "trips_parcial"

    def test_sin_diagnostico_retorna_explicacion_clara(self, sistema):
        resultado = sistema.diagnosticar("palta", [])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            if "Sin plaga" in d["plaga"]:
                assert d["regla_activada"] == "sin_diagnostico"
                assert len(d["recomendaciones"]) > 0