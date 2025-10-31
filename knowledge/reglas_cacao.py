import collections.abc

# Parche para compatibilidad con Python 3.10+
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.MutableSequence = collections.abc.MutableSequence
collections.Sequence = collections.abc.Sequence
collections.Iterable = collections.abc.Iterable
collections.Iterator = collections.abc.Iterator
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

from experta import KnowledgeEngine, Rule, TEST, MATCH, NOT
from knowledge.hechos import Caso, Diagnostico

class ReglasCacao(KnowledgeEngine):
    """
    Sistema experto para diagnóstico de plagas en cacao (Theobroma cacao)
    Basado en:
    - INIAP Ecuador (Instituto Nacional de Investigaciones Agropecuarias)
    - AGROSAVIA Colombia (Corporación Colombiana de Investigación Agropecuaria)
    - SENASA Perú
    """

    # ==================== MONILIASIS ====================
    
    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: {"manchas_oscuras_mazorca", "polvo_blanco", "pudricion_fruto"}.issubset(s))
    )
    def moniliasis_completa(self):
        """Moniliasis con síntomas completos"""
        self.declare(Diagnostico(
            plaga="Moniliasis del cacao (Moniliophthora roreri)",
            certeza=1.0,
            umbral="Pérdidas potenciales 40-90%",
            recomendaciones=[
                "Remoción quincenal de mazorcas enfermas: cortar y enterrar o cubrir con hojarasca.",
                "Aplicar fungicidas: oxicloruro de cobre 860 g i.a./ha alternado con Mancozeb 347 g i.a./ha cada 15-30 días.",
                "Poda fitosanitaria: eliminar ramas improductivas, mejorar ventilación y penetración de luz.",
                "Uso de biofungicidas: Trichoderma spp o Bacillus spp 1.5 L/ha + podas.",
                "Sembrar materiales tolerantes: clones CCN-51, EET 544, EET 558.",
                "Monitorear mazorcas desde 40-80 días post-polinización (periodo crítico)."
            ],
            regla_activada="moniliasis_completa"
        ))

    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: len({"manchas_oscuras_mazorca", "polvo_blanco", "pudricion_fruto"} & s) >= 2),
        NOT(Diagnostico(plaga="Moniliasis del cacao (Moniliophthora roreri)"))
    )
    def moniliasis_parcial(self):
        """Moniliasis en etapa inicial"""
        self.declare(Diagnostico(
            plaga="Moniliasis del cacao (Moniliophthora roreri) – etapa inicial",
            certeza=0.8,
            umbral="Pérdidas potenciales 40-90%",
            recomendaciones=[
                "Inspeccionar TODAS las mazorcas semanalmente, incluso asintomáticas.",
                "Periodo de incubación: 40-80 días sin síntomas externos visibles.",
                "Buscar pequeñas manchas oscuras que preceden al polvo blanco.",
                "Alta humedad (>80%) + temperatura (21-27°C) favorecen dispersión.",
                "Actuar preventivamente: no esperar síntomas avanzados."
            ],
            regla_activada="moniliasis_parcial"
        ))

    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: "alta_humedad_ambiente" in s and "temperatura_optima" in s),
        NOT(Diagnostico())
    )
    def moniliasis_condiciones_riesgo(self):
        """Condiciones ambientales favorables para moniliasis"""
        self.declare(Diagnostico(
            plaga="Riesgo de Moniliasis – condiciones ambientales favorables",
            certeza=0.6,
            umbral="Prevención",
            recomendaciones=[
                "Condiciones de riesgo detectadas: alta humedad + temperatura favorable.",
                "Implementar monitoreo intensivo cada 7 días.",
                "Aplicar fungicidas preventivos: cobre + Mancozeb alternado.",
                "Intensificar remoción de mazorcas (incluir asintomáticas sospechosas).",
                "Amazonia ecuatoriana: zona de mayor riesgo (>40% pérdidas reportadas)."
            ],
            regla_activada="moniliasis_condiciones_riesgo"
        ))

    # ==================== ESCOBA DE BRUJA ====================
    
    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: {"brotes_anormales", "hipertrofia_cojines", "escobas_secas"}.issubset(s))
    )
    def escoba_bruja_completa(self):
        """Escoba de bruja con síntomas completos"""
        self.declare(Diagnostico(
            plaga="Escoba de bruja (Moniliophthora perniciosa)",
            certeza=1.0,
            umbral="Eliminar tejido infectado inmediatamente",
            recomendaciones=[
                "Poda fitosanitaria: cortar escobas 30 cm por debajo de síntoma visible.",
                "Quemar o enterrar tejido removido lejos de plantación.",
                "Aplicar pasta cúprica en cortes para proteger heridas.",
                "Control cultural: eliminar cojines florales y frutos infectados semanalmente.",
                "Aplicar fungicidas cúpricos en épocas de brotación y floración.",
                "Sembrar clones tolerantes: buscar material genético resistente."
            ],
            regla_activada="escoba_bruja_completa"
        ))

    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: "brotes_anormales" in s or "hipertrofia_cojines" in s),
        NOT(Diagnostico(plaga="Escoba de bruja (Moniliophthora perniciosa)"))
    )
    def escoba_bruja_parcial(self):
        """Escoba de bruja en etapa temprana"""
        self.declare(Diagnostico(
            plaga="Escoba de bruja (Moniliophthora perniciosa) – sospecha",
            certeza=0.75,
            umbral="Eliminar tejido infectado inmediatamente",
            recomendaciones=[
                "Inspeccionar: brotes verdes hinchados y deformados (fase verde).",
                "Escobas secas necróticas son fuente de basidiosporas (fase seca).",
                "Mayor impacto en Amazonía: Brasil reporta devastación histórica.",
                "Actuar rápido: enfermedad sistémica puede matar ramas enteras.",
                "Consultar con técnico para confirmación diagnóstica."
            ],
            regla_activada="escoba_bruja_parcial"
        ))

    # ==================== MAZORQUERO (CARMENTA SPP) ====================
    
    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: {"mazorcas_perforadas", "galerias_internas", "adulto_volador_presente"}.issubset(s))
    )
    def mazorquero_completo(self):
        """Mazorquero del cacao (barrenador)"""
        self.declare(Diagnostico(
            plaga="Mazorquero del cacao (Carmenta spp)",
            certeza=1.0,
            umbral="Umbral bajo: gran impacto en calidad",
            recomendaciones=[
                "Remoción semanal de mazorcas afectadas: cortar y destruir lejos del campo.",
                "Aplicar hongos entomopatógenos: Beauveria bassiana o Metarhizium anisopliae.",
                "Control biológico: proteger avispas parasitoides naturales.",
                "Monitorear adultos con trampas de feromonas (insecto volador).",
                "Cosecha oportuna: no dejar mazorcas maduras en árbol más de 7-10 días.",
                "Mejorar drenaje: larvas se desarrollan mejor en alta humedad."
            ],
            regla_activada="mazorquero_completo"
        ))

    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: "mazorcas_perforadas" in s or "galerias_internas" in s),
        NOT(Diagnostico(plaga="Mazorquero del cacao (Carmenta spp)"))
    )
    def mazorquero_parcial(self):
        """Mazorquero - daño inicial"""
        self.declare(Diagnostico(
            plaga="Mazorquero del cacao (Carmenta spp) – daño inicial",
            certeza=0.7,
            umbral="Umbral bajo: gran impacto en calidad",
            recomendaciones=[
                "Verificar perforaciones pequeñas en cáscara de mazorca.",
                "Al abrir: buscar galerías y larvas en pulpa/semillas.",
                "Adulto es polilla que perfora mazorca para oviposición.",
                "Cusco (Perú) reporta problema serio con esta plaga.",
                "Intensificar inspecciones semanales de mazorcas."
            ],
            regla_activada="mazorquero_parcial"
        ))

    # ==================== PHYTOPHTHORA (PUDRICIÓN NEGRA) ====================
    
    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: {"manchas_negras_mazorca", "pudricion_rapida", "lluvia_reciente"}.issubset(s))
    )
    def phytophthora_completa(self):
        """Pudrición negra de mazorca (Phytophthora)"""
        self.declare(Diagnostico(
            plaga="Pudrición negra de mazorca (Phytophthora palmivora)",
            certeza=0.95,
            umbral="Control preventivo crítico",
            recomendaciones=[
                "Mejorar drenaje: evitar encharcamientos (Phytophthora es oomiceto acuático).",
                "Aplicar fungicidas cúpricos: oxicloruro de cobre preventivamente en época lluviosa.",
                "Poda de mantenimiento: mejorar aireación del dosel.",
                "Elevar mazorcas: evitar contacto directo con suelo húmedo.",
                "Cosechar frecuentemente: no dejar mazorcas maduras en época lluviosa.",
                "Eliminar mazorcas infectadas: enterrar o alejar de plantación."
            ],
            regla_activada="phytophthora_completa"
        ))

    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        TEST(lambda s: "manchas_negras_mazorca" in s and "lluvia_reciente" in s),
        NOT(Diagnostico(plaga="Pudrición negra de mazorca (Phytophthora palmivora)"))
    )
    def phytophthora_inicial(self):
        """Phytophthora en etapa inicial"""
        self.declare(Diagnostico(
            plaga="Pudrición negra de mazorca (Phytophthora spp) – etapa inicial",
            certeza=0.8,
            umbral="Control preventivo crítico",
            recomendaciones=[
                "Síntomas aparecen 2-3 días después de lluvia intensa.",
                "Manchas negras con borde difuso que se expanden rápidamente.",
                "Diferencia con moniliasis: Phytophthora NO produce polvo blanco.",
                "Actuar preventivamente: aplicar cúpricos ANTES de lluvias.",
                "Enfermedad más importante del cacao a nivel global."
            ],
            regla_activada="phytophthora_inicial"
        ))

    # ==================== SIN DIAGNÓSTICO ====================
    
    @Rule(
        Caso(cultivo="cacao", sintomas=MATCH.s),
        NOT(Diagnostico())
    )
    def sin_diagnostico(self):
        """No se identificó plaga específica"""
        self.declare(Diagnostico(
            plaga="Sin plaga identificada",
            certeza=0.0,
            umbral="N/A",
            recomendaciones=[
                "Los síntomas no coinciden con plagas principales del cacao.",
                "Considerar otras plagas: chinches (Monalonion), trips, áfidos.",
                "Evaluar enfermedades menores: mal de machete, muerte súbita.",
                "Problemas nutricionales o de drenaje pueden simular síntomas de plagas.",
                "Contactar con INIAP, SENASA o centro de investigación local.",
                "Enviar muestra a laboratorio especializado para análisis."
            ],
            regla_activada="sin_diagnostico"

        ))
