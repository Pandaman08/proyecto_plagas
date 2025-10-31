import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas


@pytest.fixture
def sistema():
    return SistemaExpertoPlagas()


class TestInferenciaCorrecta:
    """Verifica que las reglas disparen el diagnóstico esperado."""

    def test_trips_completo_certeza_maxima(self, sistema):
        sintomas = ["raspado_frutos", "rugosidad_frutos", "bronceado_frutos"]
        resultado = sistema.diagnosticar("palta", sintomas)
        assert len(resultado["diagnosticos"]) > 0
        d = resultado["diagnosticos"][0]
        assert "Trips del Palto" in d["plaga"]
        assert d["certeza"] == 1.0
        assert d["regla_activada"] == "trips_completo"

    def test_tristeza_completa_certeza_maxima(self, sistema):
        sintomas = ["hojas_amarillas", "defoliacion", "raices_necrosadas", "frutos_pequenos"]
        resultado = sistema.diagnosticar("palta", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Tristeza del palto" in d["plaga"]
        assert "Phytophthora cinnamomi" in d["plaga"]
        assert d["certeza"] == 1.0
        assert d["regla_activada"] == "tristeza_completa"

    def test_sunblotch_completo_certeza_maxima(self, sistema):
        sintomas = ["manchas_amarillas_fruto", "variegado_hojas", "crecimiento_horizontal"]
        resultado = sistema.diagnosticar("palta", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Sunblotch" in d["plaga"]
        assert "viroide" in d["plaga"]
        assert d["certeza"] == 1.0

    def test_aranita_roja_parcial_certeza_reducida(self, sistema):
        sintomas = ["tostado_hojas", "hojas_rojizas"]
        resultado = sistema.diagnosticar("palta", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Arañita" in d["plaga"]
        assert "sospecha" in d["plaga"]
        assert d["certeza"] == 0.65
        assert d["regla_activada"] == "aranita_roja_parcial"

    def test_brazo_negro_completo(self, sistema):
        sintomas = ["cancros_tronco", "exudados_blancos", "muerte_ramas"]
        resultado = sistema.diagnosticar("palta", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Brazo negro" in d["plaga"]
        assert "Lasiodiplodia" in d["plaga"]
        assert d["certeza"] == 1.0