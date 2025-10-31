import pytest
from engine.motor import SistemaExpertoPlagas

class TestInferenciaCorrecta:

    @pytest.fixture
    def sistema(self):
        return SistemaExpertoPlagas()

    # === 1. Pulgón de la papa (Myzus persicae)
    def test_pulgon_completo_certeza_maxima(self, sistema):
        sintomas = ["hojas_enrolladas", "hojas_amarillentas"]
        resultado = sistema.diagnosticar("papa", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Pulgón de la papa (Myzus persicae)"
        assert d["certeza"] == 0.9
        assert "enrolladas" in d["descripcion"]

    # === 2. Gusano cortador (Agrotis spp.)
    def test_gusano_cortador_completo(self, sistema):
        sintomas = ["tallos_cortados", "plantas_caidas"]
        resultado = sistema.diagnosticar("papa", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Gusano cortador (Agrotis spp.)"
        assert d["certeza"] == 0.6
        assert "tallos jóvenes" in d["descripcion"]

    # === 3. Mosca minadora (Liriomyza huidobrensis)
    def test_mosca_minadora_completo(self, sistema):
        sintomas = ["hojas_con_galerias", "insectos_pequenos_negros"]
        resultado = sistema.diagnosticar("papa", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Mosca minadora (Liriomyza huidobrensis)"
        assert d["certeza"] == 0.6
        assert "galerías" in d["descripcion"]

    # === 4. Tizón tardío (Phytophthora infestans)
    def test_tizon_tardio_completo(self, sistema):
        sintomas = ["hojas_manchas_negras", "clima_humedo"]
        resultado = sistema.diagnosticar("papa", sintomas)
        d = resultado["diagnosticos"][0]
        assert d["plaga"] == "Tizón tardío (Phytophthora infestans)"
        assert d["certeza"] == 0.9
        assert "manchas negras" in d["descripcion"]

    # === 5. Caso borde (sin síntomas)
    def test_sin_sintomas_diagnostico_vacio(self, sistema):
        sintomas = []
        resultado = sistema.diagnosticar("papa", sintomas)
        assert len(resultado["diagnosticos"]) == 0
