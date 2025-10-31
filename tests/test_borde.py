import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas


@pytest.fixture
def sistema():
    return SistemaExpertoPlagas()


class TestCasosBorde:
    """Verifica comportamiento en situaciones límite."""

    def test_sin_sintomas_diagnostico_vacio_o_generico(self, sistema):
        resultado = sistema.diagnosticar("palta", [])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] == 0.0 or "Sin plaga" in d["plaga"]

    def test_sintomas_contradictorios_o_incompatibles(self, sistema):
        resultado = sistema.diagnosticar("palta", ["sintoma_inexistente", "otro_falso"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] <= 0.5 or "Sin plaga" in d["plaga"]

    def test_un_solo_sintoma_parcial(self, sistema):
        resultado = sistema.diagnosticar("palta", ["raspado_frutos"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] < 1.0

    def test_cultivo_no_soportado(self, sistema):
        resultado = sistema.diagnosticar("mango", ["cualquiera"])
        assert "error" in resultado
        assert "no soportado" in resultado["error"].lower()

    def test_sintomas_de_multiples_plagas_devuelve_lista_ordenada(self, sistema):
        sintomas = ["raspado_frutos", "rugosidad_frutos", "tostado_hojas", "hojas_rojizas"]
        resultado = sistema.diagnosticar("palta", sintomas)
        assert len(resultado["diagnosticos"]) >= 2
        certezas = [d["certeza"] for d in resultado["diagnosticos"]]
        assert certezas == sorted(certezas, reverse=True)