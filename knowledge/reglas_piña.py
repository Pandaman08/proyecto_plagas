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
from .hechos import Caso, Diagnostico

class ReglasPiña(KnowledgeEngine):

    @Rule(
        Caso(cultivo="piña", sintomas=MATCH.s),
        TEST(lambda s: {"marchitez", "enrojecimiento_foliar", "raices_dañadas"}.issubset(s))
    )
    def gallina_ciega_completa(self):
        self.declare(Diagnostico(
            plaga="Gallina ciega (Phyllophaga sp.)",
            certeza=1.0,
            umbral="1 larva/metro lineal",
            recomendaciones=[
                "Excavar 10 cm de profundidad en 1 m lineal para conteo de larvas.",
                "Aplicar Metarhizium anisopliae o Beauveria bassiana si se supera el umbral.",
                "Evaluar presencia de depredador Phileurus didymus."
            ],
            regla_activada="gallina_ciega_completa"
        ))

    @Rule(
        Caso(cultivo="piña", sintomas=MATCH.s),
        TEST(lambda s: len({"marchitez", "enrojecimiento_foliar", "raices_dañadas"} & s) >= 2),
        NOT(Diagnostico(plaga="Gallina ciega (Phyllophaga sp.)"))
    )
    def gallina_ciega_parcial(self):
        self.declare(Diagnostico(
            plaga="Gallina ciega (Phyllophaga sp.) – sospecha",
            certeza=0.6,
            umbral="1 larva/metro lineal",
            recomendaciones=[
                "Síntomas incompletos. Realizar muestreo de suelo en 5 sectores.",
                "Buscar larvas en raíces a 2–10 cm de profundidad.",
                "Verificar presencia de larvas en forma de 'C', cabeza pardo-amarillenta."
            ],
            regla_activada="gallina_ciega_parcial"
        ))

    @Rule(
        Caso(cultivo="piña", sintomas=MATCH.s),
        TEST(lambda s: {"retraso_crecimiento", "colonias_algodonosas", "enrollamiento_hojas"}.issubset(s))
    )
    def cochinilla_harinosa_completa(self):
        self.declare(Diagnostico(
            plaga="Cochinilla harinosa (Dysmicoccus brevipes)",
            certeza=1.0,
            umbral="6–10 cochinillas/hoja",
            recomendaciones=[
                "Inspeccionar base de hojas y frutos en busca de colonias algodonosas.",
                "Buscar presencia de hormigas (Solenopsis, Pheidole) como indicador indirecto.",
                "Aplicar Cryptolaemus montrouzieri o Leptomastix dactylopii si se supera el umbral.",
                "Evaluar síntomas del virus PMWaV: marchitez roja, enrollamiento apical."
            ],
            regla_activada="cochinilla_harinosa_completa"
        ))

    @Rule(
        Caso(cultivo="piña", sintomas=MATCH.s),
        TEST(lambda s: "colonias_algodonosas" in s and "hormigas" in s),
        NOT(Diagnostico(plaga="Cochinilla harinosa (Dysmicoccus brevipes)")),
        NOT(Diagnostico(plaga="Cochinilla harinosa (Dysmicoccus brevipes) – sospecha"))
    )
    def cochinilla_por_hormigas(self):
        self.declare(Diagnostico(
            plaga="Cochinilla harinosa (Dysmicoccus brevipes) – indicio indirecto",
            certeza=0.7,
            umbral="6–10 cochinillas/hoja",
            recomendaciones=[
                "Presencia de hormigas asociadas a cochinillas es un fuerte indicador.",
                "Inspeccionar base de tallo y pedúnculo de frutos.",
                "Contar cochinillas en 5 plantas por sector (25 plantas total)."
            ],
            regla_activada="cochinilla_por_hormigas"
        ))

    @Rule(
        Caso(cultivo="piña", sintomas=MATCH.s),
        NOT(Diagnostico())
    )
    def sin_diagnostico(self):
        self.declare(Diagnostico(
            plaga="Sin plaga identificada",
            certeza=0.0,
            umbral="N/A",
            recomendaciones=[
                "No se detectaron síntomas compatibles con plagas principales en piña.",
                "Verificar estado fenológico: algunas plagas atacan solo en floración/fructificación.",
                "Considerar otras plagas no cubiertas: Thecla basilides, Melanoma canopilosum.",
                "Evaluar condiciones de drenaje: Phytophthora puede causar síntomas similares."
            ],
            regla_activada="sin_diagnostico"
        ))

