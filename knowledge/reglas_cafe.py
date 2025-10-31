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

class ReglasCafe(KnowledgeEngine):
    """
    Sistema experto para diagnóstico de plagas en café (Coffea arabica)
    Basado en:
    - CENICAFE Colombia (Centro Nacional de Investigaciones del Café)
    - SENASA Perú (Servicio Nacional de Sanidad Agraria)
    - INIA Perú (Instituto Nacional de Innovación Agraria)
    """

    # ==================== BROCA DEL CAFÉ ====================
    
    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: {"frutos_perforados", "granos_dañados", "cerezas_caidas"}.issubset(s))
    )
    def broca_completa(self):
        """Broca del café con síntomas completos"""
        self.declare(Diagnostico(
            plaga="Broca del café (Hypothenemus hampei)",
            certeza=1.0,
            umbral="5% de frutos brocados",
            recomendaciones=[
                "Realizar repase: recolectar frutos secos, sobremaduros y maduros del árbol y suelo.",
                "Aplicar Beauveria bassiana (hongo entomopatógeno) 3x10^8 esporas/gramo.",
                "Liberar parasitoides: Cephalonomia stephanoderis y Prorops nasuta.",
                "Uso de trampas cebadas con alcohol-metanol (20 trampas/ha) en periodo intercosecha.",
                "Mantener cafetal limpio: no dejar frutos en el suelo después de cosecha."
            ],
            regla_activada="broca_completa"
        ))

    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: len({"frutos_perforados", "granos_dañados", "cerezas_caidas"} & s) >= 2),
        NOT(Diagnostico(plaga="Broca del café (Hypothenemus hampei)"))
    )
    def broca_parcial(self):
        """Broca del café con síntomas parciales"""
        self.declare(Diagnostico(
            plaga="Broca del café (Hypothenemus hampei) – sospecha",
            certeza=0.7,
            umbral="5% de frutos brocados",
            recomendaciones=[
                "Inspeccionar 30 frutos por planta en 20 plantas/lote.",
                "Buscar perforaciones en disco del fruto (parte central).",
                "Verificar presencia de adultos negros de 1.7mm dentro de granos.",
                "Si se confirma, implementar control cultural inmediato."
            ],
            regla_activada="broca_parcial"
        ))

    # ==================== ROYA AMARILLA ====================
    
    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: {"manchas_amarillas_envés", "caida_hojas", "polvo_naranja"}.issubset(s))
    )
    def roya_completa(self):
        """Roya amarilla con síntomas completos"""
        self.declare(Diagnostico(
            plaga="Roya amarilla del café (Hemileia vastatrix)",
            certeza=1.0,
            umbral="10% de hojas con lesiones",
            recomendaciones=[
                "Sembrar variedades resistentes: Catimor, Colombia, Costa Rica 95.",
                "Aplicar fungicidas cúpricos: oxicloruro de cobre 3-4 kg/ha.",
                "Aplicar azoxystrobina + tebuconazol en periodos críticos (floración).",
                "Mejorar nutrición: aplicar fertilización balanceada NPK.",
                "Regular sombra del cafetal: 30-40% de cobertura óptima."
            ],
            regla_activada="roya_completa"
        ))

    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: "manchas_amarillas_envés" in s or "polvo_naranja" in s),
        NOT(Diagnostico(plaga="Roya amarilla del café (Hemileia vastatrix)"))
    )
    def roya_inicial(self):
        """Roya amarilla en etapa inicial"""
        self.declare(Diagnostico(
            plaga="Roya amarilla del café (Hemileia vastatrix) – etapa inicial",
            certeza=0.8,
            umbral="10% de hojas con lesiones",
            recomendaciones=[
                "Monitorear semanalmente: revisar envés de hojas en tercio medio.",
                "El polvo amarillo-naranja son uredosporas del hongo.",
                "Actuar preventivamente antes de alcanzar 10% de incidencia.",
                "Evaluar condiciones de alta humedad que favorecen el hongo."
            ],
            regla_activada="roya_inicial"
        ))

    # ==================== COCHINILLAS DE RAÍCES ====================
    
    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: {"amarillamiento_hojas", "marchitez_plantas", "muerte_plantas"}.issubset(s))
    )
    def cochinilla_raices_completa(self):
        """Cochinillas de raíces con síntomas severos"""
        self.declare(Diagnostico(
            plaga="Cochinillas de raíces del café (Puto barberi, Dysmicoccus spp)",
            certeza=0.9,
            umbral="Presencia confirmada en raíces",
            recomendaciones=[
                "Revisar almácigos mensualmente (1.5 meses después de chapolas).",
                "Aplicar Silex™ 3g/L o Engeo® 0.5 cm³/L: 50cm³/planta en almácigo.",
                "En campo: Silex™ 0.30g/planta o Verdadero® 0.031g/planta (100cm³/árbol).",
                "Aplicar con suelo húmedo (capacidad de campo) para mejor distribución.",
                "Buscar asociación con hormigas (Solenopsis, Pheidole) como indicador."
            ],
            regla_activada="cochinilla_raices_completa"
        ))

    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: "hormigas_cuello_tallo" in s and len({"amarillamiento_hojas", "marchitez_plantas"} & s) >= 1)
    )
    def cochinilla_por_hormigas(self):
        """Cochinillas detectadas por presencia de hormigas"""
        self.declare(Diagnostico(
            plaga="Cochinillas de raíces – indicio por hormigas",
            certeza=0.75,
            umbral="Presencia confirmada en raíces",
            recomendaciones=[
                "Presencia de hormigas en cuello/raíces es fuerte indicador de cochinillas.",
                "Excavar cuidadosamente alrededor del cuello y raíces principales.",
                "Buscar insectos blancos algodonosos o enquistados en raíces.",
                "Sembrar 30 plantas indicadoras/lote en establecimiento (0-18 meses)."
            ],
            regla_activada="cochinilla_por_hormigas"
        ))

    # ==================== MINADOR DE HOJAS ====================
    
    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: {"minas_serpentinas_hojas", "defoliacion", "hojas_necroticas"}.issubset(s))
    )
    def minador_completo(self):
        """Minador de hojas con daño severo"""
        self.declare(Diagnostico(
            plaga="Minador de hojas del café (Leucoptera coffeella)",
            certeza=1.0,
            umbral="Control natural generalmente suficiente",
            recomendaciones=[
                "Proteger enemigos naturales: NO aplicar insecticidas de amplio espectro.",
                "Controles naturales: Closterocerus coffeellae, Horismenus, Cirrospilus.",
                "Solo si supera umbral: aplicar control biológico por conservación.",
                "Monitorear después de épocas secas cuando aumentan poblaciones.",
                "Mantener diversidad vegetal en cafetal para refugio de parasitoides."
            ],
            regla_activada="minador_completo"
        ))

    # ==================== ARAÑITA ROJA ====================
    
    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_bronceadas", "telaraña_envés", "epoca_seca"}.issubset(s))
    )
    def arañita_roja_completa(self):
        """Arañita roja en época seca"""
        self.declare(Diagnostico(
            plaga="Arañita roja del café (Oligonychus yothersi)",
            certeza=1.0,
            umbral="Focos visibles en época seca",
            recomendaciones=[
                "Aplicar spiromesifen 1.5 cm³/L SOLO en focos iniciales, no todo el lote.",
                "Ataque es agregado: tratar solo árboles con daño visible.",
                "Proteger depredadores: Stethorus sp., Harmonia sp., Cycloneda sanguinea.",
                "Población disminuye naturalmente con llegada de lluvias.",
                "Control localizado preserva enemigos naturales del cafetal."
            ],
            regla_activada="arañita_roja_completa"
        ))

    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: "hojas_bronceadas" in s and "epoca_seca" in s),
        NOT(Diagnostico(plaga="Arañita roja del café (Oligonychus yothersi)"))
    )
    def arañita_roja_inicial(self):
        """Arañita roja en etapa inicial"""
        self.declare(Diagnostico(
            plaga="Arañita roja del café (Oligonychus yothersi) – focos iniciales",
            certeza=0.8,
            umbral="Focos visibles en época seca",
            recomendaciones=[
                "Monitorear inicio de época seca: revisar envés de hojas.",
                "Buscar puntos bronceados/amarillentos en hojas expuestas al sol.",
                "Con lupa (10x) verificar presencia de ácaros y telarañas finas.",
                "Marcar focos para tratamiento localizado si se expanden."
            ],
            regla_activada="arañita_roja_inicial"
        ))

    # ==================== MANCHA DE HIERRO ====================
    
    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        TEST(lambda s: {"manchas_necroticas_hojas", "defoliacion", "plantulas_debiles"}.issubset(s))
    )
    def mancha_hierro(self):
        """Mancha de hierro (Cercospora coffeicola)"""
        self.declare(Diagnostico(
            plaga="Mancha de hierro (Cercospora coffeicola)",
            certeza=0.9,
            umbral="15% de incidencia foliar",
            recomendaciones=[
                "Mejorar nutrición: deficiencia de nitrógeno favorece la enfermedad.",
                "Aplicar fungicidas cúpricos preventivamente en vivero y plantación joven.",
                "Regular sombra: exceso favorece humedad y desarrollo del hongo.",
                "Eliminar hojas severamente afectadas para reducir inóculo.",
                "Mayor incidencia en plantas en crecimiento y viveros."
            ],
            regla_activada="mancha_hierro"
        ))

    # ==================== SIN DIAGNÓSTICO ====================
    
    @Rule(
        Caso(cultivo="café", sintomas=MATCH.s),
        NOT(Diagnostico())
    )
    def sin_diagnostico(self):
        """No se identificó plaga específica"""
        self.declare(Diagnostico(
            plaga="Sin plaga identificada",
            certeza=0.0,
            umbral="N/A",
            recomendaciones=[
                "Los síntomas no coinciden con plagas principales del café.",
                "Considerar otras plagas: chinche de chamusquina (Monalonion velezangeli).",
                "Evaluar deficiencias nutricionales o problemas de drenaje.",
                "Contactar con técnico de SENASA o centro de investigación local.",
                "Enviar muestra a laboratorio de fitopatología para análisis."
            ],
            regla_activada="sin_diagnostico"
        ))
