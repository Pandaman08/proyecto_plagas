"""
Tests automáticos para el Sistema Experto de Plagas de Palta
Cumple con los requisitos:
1. Test de inferencia correcta (regla dispara lo esperado)
2. Test de caso borde (sin síntomas, síntomas contradictorios)
3. Test de explicación (el sistema puede decir "por qué decidió eso")
"""

import pytest
import collections.abc
import sys
import os

# Parche para compatibilidad con Python 3.10+
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.MutableSequence = collections.abc.MutableSequence
collections.Sequence = collections.abc.Sequence
collections.Iterable = collections.abc.Iterable
collections.Iterator = collections.abc.Iterator
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

# Agregar el path del proyecto al sys.path para importaciones
sys.path.insert(0, os.path.abspath('.'))

from engine.motor import SistemaExpertoPlagas


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sistema():
    """Instancia del sistema experto para reutilizar en tests."""
    return SistemaExpertoPlagas()


# ============================================================================
# 1. TESTS DE INFERENCIA CORRECTA
# ============================================================================

class TestInferenciaCorrecta:
    """Verifica que las reglas disparen el diagnóstico esperado."""
    
    def test_trips_completo_certeza_maxima(self, sistema):
        """Test: Trips con síntomas completos → certeza 1.0"""
        sintomas = ["raspado_frutos", "rugosidad_frutos", "bronceado_frutos"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        assert len(resultado["diagnosticos"]) > 0, "Debe retornar al menos 1 diagnóstico"
        diagnostico = resultado["diagnosticos"][0]
        
        assert "Trips del Palto" in diagnostico["plaga"]
        assert diagnostico["certeza"] == 1.0
        assert diagnostico["regla_activada"] == "trips_completo"
        assert len(diagnostico["recomendaciones"]) > 0
        
    def test_tristeza_completa_certeza_maxima(self, sistema):
        """Test: Tristeza con síntomas completos → certeza 1.0"""
        sintomas = ["hojas_amarillas", "defoliacion", "raices_necrosadas", "frutos_pequenos"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        diagnostico = resultado["diagnosticos"][0]
        
        assert "Tristeza del palto" in diagnostico["plaga"]
        assert diagnostico["certeza"] == 1.0
        assert "Phytophthora cinnamomi" in diagnostico["plaga"]
        assert diagnostico["regla_activada"] == "tristeza_completa"
        
    def test_sunblotch_completo_certeza_maxima(self, sistema):
        """Test: Sunblotch con síntomas completos → certeza 1.0"""
        sintomas = ["manchas_amarillas_fruto", "variegado_hojas", "crecimiento_horizontal"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        diagnostico = resultado["diagnosticos"][0]
        
        assert "Sunblotch" in diagnostico["plaga"]
        assert diagnostico["certeza"] == 1.0
        assert "viroide" in diagnostico["plaga"]
        assert "CRÍTICO" in diagnostico["recomendaciones"][0]
        
    def test_aranita_roja_parcial_certeza_reducida(self, sistema):
        """Test: Arañita con síntomas parciales → certeza 0.65"""
        sintomas = ["tostado_hojas", "hojas_rojizas"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        diagnostico = resultado["diagnosticos"][0]
        
        assert "Arañita" in diagnostico["plaga"]
        assert diagnostico["certeza"] == 0.65
        assert "sospecha" in diagnostico["plaga"]
        assert diagnostico["regla_activada"] == "aranita_roja_parcial"
        
    def test_brazo_negro_completo(self, sistema):
        """Test: Brazo negro con síntomas completos → identificación correcta"""
        sintomas = ["cancros_tronco", "exudados_blancos", "muerte_ramas"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        diagnostico = resultado["diagnosticos"][0]
        
        assert "Brazo negro" in diagnostico["plaga"]
        assert diagnostico["certeza"] == 1.0
        assert "Lasiodiplodia" in diagnostico["plaga"]
        assert any("Desinfectar" in rec for rec in diagnostico["recomendaciones"])


# ============================================================================
# 2. TESTS DE CASOS BORDE
# ============================================================================

class TestCasosBorde:
    """Verifica comportamiento en situaciones límite o extremas."""
    
    def test_sin_sintomas_diagnostico_vacio_o_generico(self, sistema):
        """Test: Sin síntomas → debe retornar diagnóstico de 'sin identificar' o vacío"""
        sintomas = []
        resultado = sistema.diagnosticar("palta", sintomas)
        
        # Puede retornar vacío o un diagnóstico genérico "sin plaga identificada"
        if len(resultado["diagnosticos"]) > 0:
            diagnostico = resultado["diagnosticos"][0]
            assert diagnostico["certeza"] == 0.0 or "Sin plaga" in diagnostico["plaga"]
        else:
            assert len(resultado["diagnosticos"]) == 0
            
    def test_sintomas_contradictorios_o_incompatibles(self, sistema):
        """Test: Síntomas que no pertenecen a ninguna plaga conocida"""
        sintomas = ["sintoma_inexistente", "otro_sintoma_falso"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        # Debe retornar diagnóstico de baja certeza o sin identificar
        if len(resultado["diagnosticos"]) > 0:
            diagnostico = resultado["diagnosticos"][0]
            assert diagnostico["certeza"] <= 0.5 or "Sin plaga" in diagnostico["plaga"]
            
    def test_un_solo_sintoma_parcial(self, sistema):
        """Test: Un solo síntoma → certeza muy reducida o sin diagnóstico"""
        sintomas = ["raspado_frutos"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        # Puede no disparar ninguna regla o disparar regla de baja confianza
        if len(resultado["diagnosticos"]) > 0:
            diagnostico = resultado["diagnosticos"][0]
            assert diagnostico["certeza"] < 1.0  # No puede ser certeza máxima con 1 síntoma
            
    def test_cultivo_no_soportado(self, sistema):
        """Test: Cultivo no implementado → debe retornar error explicativo"""
        resultado = sistema.diagnosticar("mango", ["sintoma_cualquiera"])
        
        assert "error" in resultado
        assert "no soportado" in resultado["error"].lower()
        
    def test_sintomas_de_multiples_plagas_devuelve_lista_ordenada(self, sistema):
        """Test: Síntomas que coinciden con múltiples plagas → lista ordenada por certeza"""
        # Síntomas mezclados: trips + arañita
        sintomas = [
            "raspado_frutos", "rugosidad_frutos",  # Trips (2 síntomas)
            "tostado_hojas", "hojas_rojizas"       # Arañita (2 síntomas)
        ]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        assert len(resultado["diagnosticos"]) >= 2
        # Verificar que estén ordenados por certeza descendente
        certezas = [d["certeza"] for d in resultado["diagnosticos"]]
        assert certezas == sorted(certezas, reverse=True)


# ============================================================================
# 3. TESTS DE EXPLICACIÓN (TRAZABILIDAD)
# ============================================================================

class TestExplicacion:
    """Verifica que el sistema pueda explicar por qué decidió un diagnóstico."""
    
    def test_diagnostico_incluye_regla_activada(self, sistema):
        """Test: El diagnóstico debe indicar qué regla se activó"""
        sintomas = ["raspado_frutos", "rugosidad_frutos", "bronceado_frutos"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        diagnostico = resultado["diagnosticos"][0]
        
        assert "regla_activada" in diagnostico
        assert diagnostico["regla_activada"] is not None
        assert len(diagnostico["regla_activada"]) > 0
        
    def test_reglas_activadas_en_resultado_general(self, sistema):
        """Test: El resultado debe listar todas las reglas activadas"""
        sintomas = ["hojas_amarillas", "defoliacion", "raices_necrosadas", "frutos_pequenos"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        assert "reglas_activadas" in resultado
        assert len(resultado["reglas_activadas"]) > 0
        assert resultado["reglas_activadas"][0] == "tristeza_completa"
        
    def test_explicacion_incluye_umbral_y_recomendaciones(self, sistema):
        """Test: La explicación debe incluir umbral de daño y recomendaciones"""
        sintomas = ["cancros_tronco", "exudados_blancos", "muerte_ramas"]
        resultado = sistema.diagnosticar("palta", sintomas)
        
        diagnostico = resultado["diagnosticos"][0]
        
        assert "umbral" in diagnostico
        assert "recomendaciones" in diagnostico
        assert len(diagnostico["recomendaciones"]) > 0
        assert diagnostico["umbral"] != ""
        
    def test_explicacion_diferencia_certezas(self, sistema):
        """Test: El sistema debe explicar por qué una certeza es 1.0 vs 0.7"""
        # Caso 1: Síntomas completos
        sintomas_completos = ["raspado_frutos", "rugosidad_frutos", "bronceado_frutos"]
        resultado_completo = sistema.diagnosticar("palta", sintomas_completos)
        diag_completo = resultado_completo["diagnosticos"][0]
        
        # Caso 2: Síntomas parciales
        sintomas_parciales = ["raspado_frutos", "rugosidad_frutos"]
        resultado_parcial = sistema.diagnosticar("palta", sintomas_parciales)
        diag_parcial = resultado_parcial["diagnosticos"][0]
        
        # Verificar que certezas sean diferentes y explicables
        assert diag_completo["certeza"] > diag_parcial["certeza"]
        assert diag_completo["regla_activada"] == "trips_completo"
        assert diag_parcial["regla_activada"] == "trips_parcial"
        assert "sospecha" in diag_parcial["plaga"]
        
    def test_sin_diagnostico_retorna_explicacion_clara(self, sistema):
        """Test: Cuando no hay diagnóstico, debe explicar por qué"""
        sintomas = []
        resultado = sistema.diagnosticar("palta", sintomas)
        
        if len(resultado["diagnosticos"]) > 0:
            diagnostico = resultado["diagnosticos"][0]
            # Debe haber una explicación del por qué no se identificó
            if "Sin plaga" in diagnostico["plaga"]:
                assert len(diagnostico["recomendaciones"]) > 0
                assert diagnostico["regla_activada"] == "sin_diagnostico"


# ============================================================================
# TEST DE INTEGRACIÓN
# ============================================================================

class TestIntegracion:
    """Tests que verifican el funcionamiento completo del sistema."""
    
    def test_flujo_completo_diagnostico_exitoso(self, sistema):
        """Test: Flujo completo desde síntomas hasta diagnóstico"""
        sintomas = ["manchas_amarillas_fruto", "variegado_hojas", "crecimiento_horizontal"]
        
        resultado = sistema.diagnosticar("palta", sintomas)
        
        # Verificar estructura completa del resultado
        assert "diagnosticos" in resultado
        assert "reglas_activadas" in resultado
        assert len(resultado["diagnosticos"]) > 0
        
        diagnostico = resultado["diagnosticos"][0]
        
        # Verificar todos los campos esperados
        campos_esperados = ["plaga", "certeza", "umbral", "recomendaciones", "regla_activada"]
        for campo in campos_esperados:
            assert campo in diagnostico, f"Falta el campo '{campo}' en el diagnóstico"
            
        # Verificar tipos de datos
        assert isinstance(diagnostico["plaga"], str)
        assert isinstance(diagnostico["certeza"], float)
        assert isinstance(diagnostico["umbral"], str)
        # recomendaciones puede ser list o frozenlist (por experta)
        assert hasattr(diagnostico["recomendaciones"], '__iter__')
        assert len(diagnostico["recomendaciones"]) > 0
        assert 0.0 <= diagnostico["certeza"] <= 1.0


# ============================================================================
# EJECUTAR TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])