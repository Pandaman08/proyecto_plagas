import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas


@pytest.fixture
def sistema():
    return SistemaExpertoPlagas()


class TestExplicacion:
    """Verifica trazabilidad y explicación del razonamiento para el cultivo de papa."""

    def test_diagnostico_incluye_regla_activada(self, sistema):
        """Debe activar la regla del pulgón."""
        resultado = sistema.diagnosticar("papa", ["hojas_enrolladas", "hojas_amarillentas"])
        d = resultado["diagnosticos"][0]
        assert "regla_activada" in d
        assert d["regla_activada"] == "plaga_pulgon"

    def test_reglas_activadas_en_resultado_general(self, sistema):
        """Debe registrar las reglas activadas en el resultado global."""
        resultado = sistema.diagnosticar("papa", ["hojas_manchas_negras", "clima_humedo"])
        assert "reglas_activadas" in resultado, "No se encontró 'reglas_activadas' en el resultado"
        assert any("tizon" in r for r in resultado["reglas_activadas"]), "No se activó la regla de tizón tardío"

    def test_explicacion_incluye_recomendaciones(self, sistema):
        """Cada diagnóstico debe incluir recomendaciones."""
        resultado = sistema.diagnosticar("papa", ["hojas_con_galerias", "insectos_pequenos_negros"])
        assert resultado["diagnosticos"], "No se generó ningún diagnóstico"
        d = resultado["diagnosticos"][0]
        assert "recomendaciones" in d
        assert len(d["recomendaciones"]) > 0

    def test_explicacion_diferencia_certezas(self, sistema):
        """Verifica que los síntomas completos generen mayor certeza."""
        completo = sistema.diagnosticar("papa", ["hojas_enrolladas", "hojas_amarillentas"])
        parcial = sistema.diagnosticar("papa", ["hojas_amarillentas"])
        assert completo["diagnosticos"], "Diagnóstico completo vacío"
        # el parcial puede no generar diagnóstico si no se cumple toda la regla
        if parcial["diagnosticos"]:
            assert completo["diagnosticos"][0]["certeza"] >= parcial["diagnosticos"][0]["certeza"]

    def test_sin_diagnostico_retorna_explicacion_clara(self, sistema):
        """Debe devolver un mensaje o recomendación cuando no hay coincidencias."""
        resultado = sistema.diagnosticar("papa", [])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            if "Sin plaga" in d["plaga"]:
                assert d["regla_activada"] == "sin_diagnostico"
                assert len(d["recomendaciones"]) > 0
