import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas

@pytest.fixture
def sistema():
    return SistemaExpertoPlagas()

class TestInferenciaCorrectaUva:

    @pytest.fixture
    def sistema(self):
        return SistemaExpertoPlagas()

    def test_filoxera_completa_certeza_maxima(self, sistema):
        sintomas = ["verrugas_hojas", "nudosidades_raices"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Filóxera (Phylloxera vitifoliae)"
        assert d["certeza"] == 1.0

    def test_filoxera_parcial_certeza_media(self, sistema):
        sintomas = ["nudosidades_raices"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Filóxera" in d["plaga"]
        assert d["certeza"] == 0.7

    def test_aranita_roja_completa(self, sistema):
        sintomas = ["hojas_gris_plomizo", "tejido_araña"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Arañita roja (Panonychus ulmi / Tetranynchus sp.)"
        assert d["certeza"] == 1.0

    def test_aranita_roja_parcial(self, sistema):
        sintomas = ["tejido_araña"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Arañita roja" in d["plaga"]
        assert d["certeza"] == 0.6

    def test_acaro_hialino_completo(self, sistema):
        sintomas = ["brotacion_lenta", "hojas_abarquilladas"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Ácaro hialino (Calipetrimerus vitis / Phyllocoptes vitis)"
        assert d["certeza"] == 1.0

    def test_aves_completo(self, sistema):
        sintomas = ["picaduras_racimos", "aves_presentes"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Aves (cuculíes, madrugadoras)"
        assert d["certeza"] == 1.0

    def test_avispas_abejas_completo(self, sistema):
        sintomas = ["bayas_vacias", "avispa_presencia"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Avispas y abejas (Polistes spp., Apis mellifera)"
        assert d["certeza"] == 1.0

    def test_bayas_vacias_parcial(self, sistema):
        sintomas = ["bayas_vacias"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Daño en uvas" in d["plaga"]
        assert d["certeza"] == 0.6

    def test_ratas_raton_completo(self, sistema):
        sintomas = ["racimos_consumidos", "madrigueras"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Ratas y ratones"
        assert d["certeza"] == 1.0

    def test_ratas_raton_parcial(self, sistema):
        sintomas = ["madrigueras"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Ratas y ratones" in d["plaga"]
        assert d["certeza"] == 0.7

    def test_gusano_cornudo_completo(self, sistema):
        sintomas = ["hojas_consumidas", "gusano_grande"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Gusano cornudo (Pholus vitis)"
        assert d["certeza"] == 1.0

    def test_nematodos_completo(self, sistema):
        sintomas = ["plantas_debiles", "nódulos_redondeados_raíz"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Nematodos (Meloidogyne spp.)"
        assert d["certeza"] == 1.0

    def test_nematodos_parcial(self, sistema):
        sintomas = ["nódulos_redondeados_raíz"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Nematodos" in d["plaga"]
        assert d["certeza"] == 0.8

    def test_oidio_completo(self, sistema):
        sintomas = ["polvillo_blanco", "aborto_flores"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Oidio (Uncinula necator)"
        assert d["certeza"] == 1.0

    def test_oidio_parcial(self, sistema):
        sintomas = ["polvillo_blanco"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Oidio" in d["plaga"]
        assert d["certeza"] == 0.7

    def test_podredumbre_gris_completa(self, sistema):
        sintomas = ["moho_gris", "racimos_podridos"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Podredumbre gris (Botrytis cinerea)"
        assert d["certeza"] == 1.0

    def test_podredumbre_gris_parcial(self, sistema):
        sintomas = ["moho_gris"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Podredumbre gris" in d["plaga"]
        assert d["certeza"] == 0.6

    def test_agalla_corona_completa(self, sistema):
        sintomas = ["agallas_tallo", "plantas_pequeñas"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Agalla de la corona (Agrobacterium vitis)"
        assert d["certeza"] == 1.0

    def test_agalla_corona_parcial(self, sistema):
        sintomas = ["agallas_tallo"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Agalla de la corona" in d["plaga"]
        assert d["certeza"] == 0.8

    def test_deficiencia_nutricional(self, sistema):
        sintomas = ["clorosis_hojas", "crecimiento_lento"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Deficiencia nutricional" in d["plaga"]
        assert d["certeza"] == 0.8

    def test_estres_hidrico(self, sistema):
        sintomas = ["hojas_marchitas", "suelo_seco"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Estrés hídrico" in d["plaga"]
        assert d["certeza"] == 0.9

    def test_problema_raices(self, sistema):
        sintomas = ["hojas_amarrillentas", "raíces_dañadas"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Problema radicular" in d["plaga"]
        assert d["certeza"] == 0.7

    def test_estres_ambiental(self, sistema):
        sintomas = ["flores_no_cuajan", "temperatura_alta"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Estrés ambiental" in d["plaga"]
        assert d["certeza"] == 0.8

    def test_manejo_cultivo(self, sistema):
        sintomas = ["racimos_desiguales", "poda_inadecuada"]
        resultado = sistema.diagnosticar("uva", sintomas)
        d = resultado["diagnosticos"][0]
        assert "Manejo cultural" in d["plaga"]
        assert d["certeza"] == 0.9

    def test_sin_diagnostico(self, sistema):
        sintomas = []
        resultado = sistema.diagnosticar("uva", sintomas)
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            assert "Sin plaga" in d["plaga"]
            assert d["certeza"] == 0.0