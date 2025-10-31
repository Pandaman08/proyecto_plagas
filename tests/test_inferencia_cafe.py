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

    def test_broca_completa_certeza_maxima(self, sistema):
        sintomas = ["frutos_perforados", "granos_dañados", "cerezas_caidas"]
        resultado = sistema.diagnosticar("café", sintomas)
        assert len(resultado["diagnosticos"]) > 0
        d = resultado["diagnosticos"][0]
        assert "Broca del café" in d["plaga"]
        assert "Hypothenemus hampei" in d["plaga"]
        assert d["certeza"] == 1.0
        assert d["regla_activada"] == "broca_completa"

    def test_roya_completa_certeza_maxima(self, sistema):
        sintomas = ["manchas_amarillas_envés", "caida_hojas", "polvo_naranja"]
        resultado = sistema.diagnosticar("café", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Roya amarilla del café" in d["plaga"]
        assert "Hemileia vastatrix" in d["plaga"]
        assert d["certeza"] == 1.0
        assert d["regla_activada"] == "roya_completa"

    def test_cochinilla_raices_completa_certeza_alta(self, sistema):
        sintomas = ["amarillamiento_hojas", "marchitez_plantas", "muerte_plantas"]
        resultado = sistema.diagnosticar("café", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Cochinillas de raíces" in d["plaga"]
        assert "Puto barberi" in d["plaga"] or "Dysmicoccus" in d["plaga"]
        assert d["certeza"] == 0.9
        assert d["regla_activada"] == "cochinilla_raices_completa"

    def test_broca_parcial_certeza_reducida(self, sistema):
        sintomas = ["frutos_perforados", "granos_dañados"]
        resultado = sistema.diagnosticar("café", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Broca del café" in d["plaga"]
        assert "sospecha" in d["plaga"]
        assert d["certeza"] == 0.7
        assert d["regla_activada"] == "broca_parcial"

    def test_arañita_roja_completa(self, sistema):
        sintomas = ["hojas_bronceadas", "telaraña_envés", "epoca_seca"]
        resultado = sistema.diagnosticar("café", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Arañita roja del café" in d["plaga"]
        assert "Oligonychus yothersi" in d["plaga"]
        assert d["certeza"] == 1.0
        assert d["regla_activada"] == "arañita_roja_completa"

    def test_minador_completo_certeza_maxima(self, sistema):
        sintomas = ["minas_serpentinas_hojas", "defoliacion", "hojas_necroticas"]
        resultado = sistema.diagnosticar("café", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Minador de hojas" in d["plaga"]
        assert "Leucoptera coffeella" in d["plaga"]
        assert d["certeza"] == 1.0
        assert d["regla_activada"] == "minador_completo"

    def test_mancha_hierro(self, sistema):
        sintomas = ["manchas_necroticas_hojas", "defoliacion", "plantulas_debiles"]
        resultado = sistema.diagnosticar("café", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Mancha de hierro" in d["plaga"]
        assert "Cercospora coffeicola" in d["plaga"]
        assert d["certeza"] == 0.9
        assert d["regla_activada"] == "mancha_hierro"