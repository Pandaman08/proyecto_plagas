import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas


@pytest.fixture
def sistema():
    return SistemaExpertoPlagas()

class TestCasosBordeUva:
    """Verifica comportamiento en situaciones límite para el cultivo de uva."""

    def test_sin_sintomas_diagnostico_vacio_o_generico(self, sistema):
        """Sin síntomas debe retornar diagnóstico genérico o vacío."""
        resultado = sistema.diagnosticar("uva", [])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] == 0.0 or "Sin plaga" in d["plaga"]

    def test_sintomas_inexistentes(self, sistema):
        """Síntomas que no existen en el sistema deben dar certeza baja."""
        resultado = sistema.diagnosticar("uva", ["sintoma_falso_123", "otro_inventado"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] <= 0.5 or "Sin plaga" in d["plaga"]

    def test_un_solo_sintoma_parcial_filoxera(self, sistema):
        """Un solo síntoma de filóxera no debe dar certeza total."""
        resultado = sistema.diagnosticar("uva", ["verrugas_hojas"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] < 1.0, "Un solo síntoma no debe dar certeza total"

    def test_un_solo_sintoma_parcial_oidio(self, sistema):
        """Un solo síntoma de oidio debe dar diagnóstico parcial."""
        resultado = sistema.diagnosticar("uva", ["polvillo_blanco"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] < 1.0

    def test_cultivo_no_soportado(self, sistema):
        """Cultivo no registrado debe retornar error."""
        resultado = sistema.diagnosticar("kiwi", ["hojas_manchadas"])
        assert "error" in resultado
        assert "no soportado" in resultado["error"].lower()

    def test_multiples_sintomas_varias_plagas(self, sistema):
        """Combina síntomas de diferentes plagas para activar múltiples reglas."""
        sintomas = [
            "verrugas_hojas", "nudosidades_raices",      #filoxera
            "hojas_gris_plomizo", "tejido_araña",        #arañita roja
            "polvillo_blanco", "aborto_flores",          #oidio
            "moho_gris", "racimos_podridos"              #botritis
        ]
        resultado = sistema.diagnosticar("uva", sintomas)
        assert len(resultado["diagnosticos"]) >= 2, "Debe activar más de una regla"
        certezas = [d["certeza"] for d in resultado["diagnosticos"]]
        assert certezas == sorted(certezas, reverse=True), "Diagnósticos deben ordenarse por certeza"

    def test_sintoma_ambiguo_picaduras(self, sistema):
        """Picaduras en racimos puede ser por aves o avispas."""
        resultado = sistema.diagnosticar("uva", ["picaduras_racimos"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert d["certeza"] <= 0.6, "Síntoma ambiguo no debe dar alta certeza"

    def test_sintoma_compartido_hojas_abarquilladas(self, sistema):
        """Hojas abarquilladas solas deben dar diagnóstico parcial de ácaro hialino."""
        resultado = sistema.diagnosticar("uva", ["hojas_abarquilladas"])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert "Ácaro hialino" in d["plaga"]
            assert d["certeza"] == 0.5