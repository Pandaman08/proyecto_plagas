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
        resultado = sistema.diagnosticar("café", ["frutos_perforados", "granos_dañados", "cerezas_caidas"])
        d = resultado["diagnosticos"][0]
        assert "regla_activada" in d
        assert d["regla_activada"] == "broca_completa"

    def test_reglas_activadas_en_resultado_general(self, sistema):
        resultado = sistema.diagnosticar("café", ["manchas_amarillas_envés", "caida_hojas", "polvo_naranja"])
        assert "reglas_activadas" in resultado
        assert "roya_completa" in resultado["reglas_activadas"]

    def test_explicacion_incluye_umbral_y_recomendaciones(self, sistema):
        resultado = sistema.diagnosticar("café", ["hojas_bronceadas", "telaraña_envés", "epoca_seca"])
        d = resultado["diagnosticos"][0]
        assert "umbral" in d
        assert "recomendaciones" in d
        assert len(d["recomendaciones"]) > 0
        # Verificar que las recomendaciones sean específicas
        assert any("spiromesifen" in rec.lower() or "depredador" in rec.lower() for rec in d["recomendaciones"])

    def test_explicacion_diferencia_certezas(self, sistema):
        completo = sistema.diagnosticar("café", ["frutos_perforados", "granos_dañados", "cerezas_caidas"])
        parcial = sistema.diagnosticar("café", ["frutos_perforados", "granos_dañados"])
        assert completo["diagnosticos"][0]["certeza"] > parcial["diagnosticos"][0]["certeza"]
        assert completo["diagnosticos"][0]["regla_activada"] == "broca_completa"
        assert parcial["diagnosticos"][0]["regla_activada"] == "broca_parcial"

    def test_sin_diagnostico_retorna_explicacion_clara(self, sistema):
        resultado = sistema.diagnosticar("café", [])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            if "Sin plaga" in d["plaga"]:
                assert d["regla_activada"] == "sin_diagnostico"
                assert len(d["recomendaciones"]) > 0
                # Debe sugerir contactar técnicos o laboratorio
                assert any("técnico" in rec.lower() or "laboratorio" in rec.lower() for rec in d["recomendaciones"])

    def test_reglas_parciales_vs_completas_explicadas(self, sistema):
        # Roya inicial vs completa
        inicial = sistema.diagnosticar("café", ["manchas_amarillas_envés"])
        completa = sistema.diagnosticar("café", ["manchas_amarillas_envés", "caida_hojas", "polvo_naranja"])
        
        d_inicial = inicial["diagnosticos"][0]
        d_completa = completa["diagnosticos"][0]
        
        # Ambas deben ser roya pero con diferentes certezas
        assert "Roya" in d_inicial["plaga"]
        assert "Roya" in d_completa["plaga"]
        assert d_completa["certeza"] > d_inicial["certeza"]
        assert "inicial" in d_inicial["plaga"] or "inicial" in d_inicial["regla_activada"]

    def test_explicacion_umbral_especifico_por_plaga(self, sistema):
        # Broca tiene umbral del 5%
        broca = sistema.diagnosticar("café", ["frutos_perforados", "granos_dañados", "cerezas_caidas"])
        assert "5%" in broca["diagnosticos"][0]["umbral"]
        
        # Roya tiene umbral del 10%
        roya = sistema.diagnosticar("café", ["manchas_amarillas_envés", "caida_hojas", "polvo_naranja"])
        assert "10%" in roya["diagnosticos"][0]["umbral"]

    def test_recomendaciones_especificas_por_plaga(self, sistema):
        # Broca debe recomendar Beauveria bassiana
        broca = sistema.diagnosticar("café", ["frutos_perforados", "granos_dañados", "cerezas_caidas"])
        recomendaciones_broca = " ".join(broca["diagnosticos"][0]["recomendaciones"]).lower()
        assert "beauveria bassiana" in recomendaciones_broca
        
        # Roya debe recomendar fungicidas cúpricos
        roya = sistema.diagnosticar("café", ["manchas_amarillas_envés", "caida_hojas", "polvo_naranja"])
        recomendaciones_roya = " ".join(roya["diagnosticos"][0]["recomendaciones"]).lower()
        assert "cúprico" in recomendaciones_roya or "cobre" in recomendaciones_roya

    def test_cochinilla_por_hormigas_explica_relacion(self, sistema):
        resultado = sistema.diagnosticar("café", ["hormigas_cuello_tallo", "amarillamiento_hojas"])
        d = resultado["diagnosticos"][0]
        if "Cochinilla" in d["plaga"]:
            assert d["regla_activada"] == "cochinilla_por_hormigas"
            recomendaciones = " ".join(d["recomendaciones"]).lower()
            # Debe explicar la relación hormigas-cochinillas
            assert "hormiga" in recomendaciones

    def test_trazabilidad_completa_multiples_sintomas(self, sistema):
        # Caso complejo con varios síntomas
        sintomas = ["amarillamiento_hojas", "defoliacion", "manchas_necroticas_hojas"]
        resultado = sistema.diagnosticar("café", sintomas)
        
        # Debe haber trazabilidad completa
        assert "reglas_activadas" in resultado
        assert len(resultado["reglas_activadas"]) > 0
        
        # Cada diagnóstico debe tener su regla
        for d in resultado["diagnosticos"]:
            assert "regla_activada" in d
            assert d["regla_activada"] is not None