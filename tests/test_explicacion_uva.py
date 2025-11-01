import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas


@pytest.fixture
def sistema():
    return SistemaExpertoPlagas()

class TestExplicacionUva:
    """Verifica trazabilidad y explicación del razonamiento para el cultivo de uva."""

    @pytest.fixture
    def sistema(self):
        return SistemaExpertoPlagas()

    def test_diagnostico_incluye_regla_activada_filoxera(self, sistema):
        """Debe activar la regla de filóxera completa."""
        resultado = sistema.diagnosticar("uva", ["verrugas_hojas", "nudosidades_raices"])
        d = resultado["diagnosticos"][0]
        assert "regla_activada" in d
        assert d["regla_activada"] == "filoxera_completa"

    def test_diagnostico_incluye_regla_activada_oidio(self, sistema):
        """Debe activar la regla de oidio completo."""
        resultado = sistema.diagnosticar("uva", ["polvillo_blanco", "aborto_flores"])
        d = resultado["diagnosticos"][0]
        assert "regla_activada" in d
        assert d["regla_activada"] == "oidium_completa"

    def test_reglas_activadas_en_resultado_general(self, sistema):
        """Debe registrar las reglas activadas en el resultado global."""
        resultado = sistema.diagnosticar("uva", ["moho_gris", "racimos_podridos"])
        assert "reglas_activadas" in resultado
        assert any("podredumbre" in r for r in resultado["reglas_activadas"])

    def test_explicacion_incluye_recomendaciones_aranita(self, sistema):
        """Cada diagnóstico debe incluir recomendaciones."""
        resultado = sistema.diagnosticar("uva", ["hojas_gris_plomizo", "tejido_araña"])
        assert resultado["diagnosticos"], "No se generó ningún diagnóstico"
        d = resultado["diagnosticos"][0]
        assert "recomendaciones" in d
        assert len(d["recomendaciones"]) > 0
        assert any("azufre" in r.lower() for r in d["recomendaciones"])

    def test_explicacion_diferencia_certezas_completo_vs_parcial(self, sistema):
        """Síntomas completos deben generar mayor certeza que parciales."""
        completo = sistema.diagnosticar("uva", ["verrugas_hojas", "nudosidades_raices"])
        parcial = sistema.diagnosticar("uva", ["verrugas_hojas"])
        assert completo["diagnosticos"], "Diagnóstico completo vacío"
        assert parcial["diagnosticos"], "Diagnóstico parcial vacío"
        assert completo["diagnosticos"][0]["certeza"] > parcial["diagnosticos"][0]["certeza"]

    def test_sin_diagnostico_retorna_explicacion_clara(self, sistema):
        """Debe devolver mensaje cuando no hay coincidencias."""
        resultado = sistema.diagnosticar("uva", [])
        if resultado["diagnosticos"]:
            d = resultado["diagnosticos"][0]
            if "Sin plaga" in d["plaga"]:
                assert d["regla_activada"] == "sin_diagnostico"
                assert len(d["recomendaciones"]) > 0
                assert any("laboratorio" in r.lower() or "especialista" in r.lower() 
                          for r in d["recomendaciones"])

    def test_multiples_diagnosticos_ordenados_por_certeza(self, sistema):
        """Múltiples diagnósticos deben estar ordenados por certeza."""
        sintomas = [
            "polvillo_blanco",           #oidio parcial
            "moho_gris",                 #podredumbre parcial
            "clorosis_hojas"             #deficiencia nutricional
        ]
        resultado = sistema.diagnosticar("uva", sintomas)
        if len(resultado["diagnosticos"]) >= 2:
            certezas = [d["certeza"] for d in resultado["diagnosticos"]]
            assert certezas == sorted(certezas, reverse=True)

    def test_imagen_incluida_en_diagnostico(self, sistema):
        """Los diagnósticos deben incluir referencia a imagen."""
        resultado = sistema.diagnosticar("uva", ["verrugas_hojas", "nudosidades_raices"])
        d = resultado["diagnosticos"][0]
        assert "imagen" in d
        assert d["imagen"] is not None
        assert "uva/" in d["imagen"]

    def test_umbral_incluido_en_diagnostico(self, sistema):
        """Cada diagnóstico debe especificar su umbral de detección."""
        resultado = sistema.diagnosticar("uva", ["hojas_gris_plomizo", "tejido_araña"])
        d = resultado["diagnosticos"][0]
        assert "umbral" in d
        assert len(d["umbral"]) > 0

    def test_explicacion_regla_parcial_vs_completa(self, sistema):
        """Las reglas parciales deben tener nombres diferentes a las completas."""
        completo = sistema.diagnosticar("uva", ["bayas_vacias", "avispa_presencia"])
        parcial = sistema.diagnosticar("uva", ["bayas_vacias"])
        
        assert completo["diagnosticos"][0]["regla_activada"] == "avispas_abejas_completa"
        assert parcial["diagnosticos"][0]["regla_activada"] == "bayas_vacias_parcial"

    def test_recomendaciones_especificas_por_plaga(self, sistema):
        """Cada plaga debe tener recomendaciones específicas y relevantes."""

        resultado_filoxera = sistema.diagnosticar("uva", ["verrugas_hojas", "nudosidades_raices"])
        assert any("porta-injerto" in r.lower() or "injert" in r.lower() 
                  for r in resultado_filoxera["diagnosticos"][0]["recomendaciones"])
        
        resultado_oidio = sistema.diagnosticar("uva", ["polvillo_blanco", "aborto_flores"])
        assert any("azufre" in r.lower() or "fungicida" in r.lower() 
                  for r in resultado_oidio["diagnosticos"][0]["recomendaciones"])
        
        resultado_ratas = sistema.diagnosticar("uva", ["racimos_consumidos", "madrigueras"])
        assert any("rodenticida" in r.lower() or "trampa" in r.lower() 
                  for r in resultado_ratas["diagnosticos"][0]["recomendaciones"])