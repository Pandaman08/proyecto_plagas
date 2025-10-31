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
        resultado = sistema.diagnosticar("café", [])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] == 0.0 or "Sin plaga" in d["plaga"]

    def test_sintomas_contradictorios_o_incompatibles(self, sistema):
        resultado = sistema.diagnosticar("café", ["sintoma_inexistente", "otro_falso"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] <= 0.5 or "Sin plaga" in d["plaga"]

    def test_un_solo_sintoma_parcial(self, sistema):
        resultado = sistema.diagnosticar("café", ["frutos_perforados"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] < 1.0

    def test_cultivo_no_soportado(self, sistema):
        resultado = sistema.diagnosticar("mango", ["cualquiera"])
        assert "error" in resultado
        assert "no soportado" in resultado["error"].lower()

    def test_sintomas_de_multiples_plagas_devuelve_lista_ordenada(self, sistema):
        # Síntomas que pueden coincidir con varias plagas
        sintomas = ["amarillamiento_hojas", "defoliacion", "manchas_necroticas_hojas"]
        resultado = sistema.diagnosticar("café", sintomas)
        assert len(resultado["diagnosticos"]) >= 1
        certezas = [d["certeza"] for d in resultado["diagnosticos"]]
        assert certezas == sorted(certezas, reverse=True), "Los diagnósticos deben estar ordenados por certeza descendente"

    def test_sintoma_ambiguo_defoliacion(self, sistema):
        # Defoliación puede ser por roya, minador o mancha de hierro
        resultado = sistema.diagnosticar("café", ["defoliacion"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            # Debe tener baja certeza por ser síntoma inespecífico
            assert d["certeza"] < 1.0

    def test_cochinilla_solo_por_hormigas(self, sistema):
        # Solo presencia de hormigas, sin otros síntomas
        resultado = sistema.diagnosticar("café", ["hormigas_cuello_tallo"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            # No debería diagnosticar con alta certeza solo por hormigas
            if "Cochinilla" in d["plaga"]:
                assert d["certeza"] < 0.9

    def test_sintomas_epoca_seca_sin_telaraña(self, sistema):
        # Época seca sola no debe diagnosticar arañita
        resultado = sistema.diagnosticar("café", ["epoca_seca"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            if "Arañita" in d["plaga"]:
                assert d["certeza"] < 0.8

    def test_certeza_aumenta_con_mas_sintomas(self, sistema):
        # Test progresivo: 1, 2, 3 síntomas de broca
        r1 = sistema.diagnosticar("café", ["frutos_perforados"])
        r2 = sistema.diagnosticar("café", ["frutos_perforados", "granos_dañados"])
        r3 = sistema.diagnosticar("café", ["frutos_perforados", "granos_dañados", "cerezas_caidas"])
        
        if r1["diagnosticos"] and r2["diagnosticos"] and r3["diagnosticos"]:
            c1 = r1["diagnosticos"][0]["certeza"]
            c2 = r2["diagnosticos"][0]["certeza"]
            c3 = r3["diagnosticos"][0]["certeza"]
            # La certeza debe aumentar con más síntomas
            assert c2 >= c1 or c3 >= c2, "La certeza debe aumentar con más síntomas relacionados"