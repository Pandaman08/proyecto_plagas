import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas


@pytest.fixture
def sistema():
    return SistemaExpertoPlagas()


class TestCasosBorde:
    """Verifica comportamiento en situaciones límite para el cultivo de papa."""

    def test_sin_sintomas_diagnostico_vacio_o_generico(self, sistema):
        resultado = sistema.diagnosticar("papa", [])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] == 0.0 or "Sin plaga" in d["plaga"]

    def test_sintomas_inexistentes(self, sistema):
        resultado = sistema.diagnosticar("papa", ["sintoma_inexistente", "otro_falso"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] <= 0.5 or "Sin plaga" in d["plaga"]

    def test_un_solo_sintoma_parcial(self, sistema):
        # Usa un síntoma que aparece en una regla real (ej. parte del pulgón)
        resultado = sistema.diagnosticar("papa", ["hojas_amarillentas"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] < 1.0, "Un solo síntoma no debe dar certeza total"

    def test_cultivo_no_soportado(self, sistema):
        resultado = sistema.diagnosticar("mango", ["hojas_enrolladas"])
        assert "error" in resultado
        assert "no soportado" in resultado["error"].lower()

    def test_multiples_sintomas_varias_plagas(self, sistema):
        # Combina síntomas que activan distintas reglas del cultivo de papa
        sintomas = [
            "hojas_enrolladas", "hojas_amarillentas",          # Pulgón de la papa
            "tallos_perforados", "tuberculos_danados",         # Gorgojo andino
            "hojas_manchas_negras", "clima_humedo"             # Tizón tardío
        ]
        resultado = sistema.diagnosticar("papa", sintomas)
        assert len(resultado["diagnosticos"]) >= 2, "Debe activar más de una regla"
        certezas = [d["certeza"] for d in resultado["diagnosticos"]]
        assert certezas == sorted(certezas, reverse=True), "Los diagnósticos deben ordenarse por certeza"
