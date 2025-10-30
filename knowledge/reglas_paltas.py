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

class ReglasPalta(KnowledgeEngine):
    
    # PLAGAS
    
    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"raspado_frutos", "rugosidad_frutos", "bronceado_frutos"}.issubset(s))
    )
    def trips_completo(self):
        self.declare(Diagnostico(
            plaga="Trips del Palto (Heliothrips haemorrhoidalis)",
            certeza=1.0,
            umbral="Presencia de trips en floración y cuajado",
            recomendaciones=[
                "Aplicar productos antes del inicio de floración y al inicio del cuajado.",
                "Principios activos recomendados: Metomil, Clorpirifos o Benfuracard.",
                "Consultar con especialista para dosis adecuada según nivel de infestación.",
                "Monitorear especialmente durante brotamiento, floración y cuajado de frutos."
            ],
            regla_activada="trips_completo"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: len({"raspado_frutos", "rugosidad_frutos", "bronceado_frutos", "deformacion_frutos"} & s) >= 2),
        NOT(Diagnostico(plaga="Trips del Palto (Heliothrips haemorrhoidalis)"))
    )
    def trips_parcial(self):
        self.declare(Diagnostico(
            plaga="Trips del Palto (Heliothrips haemorrhoidalis) — sospecha",
            certeza=0.7,
            umbral="Presencia de trips en floración y cuajado",
            recomendaciones=[
                "Síntomas incompletos. Inspeccionar frutos recién cuajados en busca de raspado.",
                "Buscar pequeños insectos alargados en flores y frutos.",
                "El daño por ovoposición forma pequeñas concavidades en los tejidos.",
                "Verificar presencia de rugosidad y plateado en hojas jóvenes."
            ],
            regla_activada="trips_parcial"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"tostado_hojas", "hojas_rojizas", "defoliacion_prematura"}.issubset(s))
    )
    def aranita_roja_completa(self):
        self.declare(Diagnostico(
            plaga="Arañita roja (Oligonychus yothersi / O. punicae)",
            certeza=1.0,
            umbral="Presencia de ácaros en casi todas las plantas",
            recomendaciones=[
                "Realizar lavado a presión con detergente agrícola (150 ml/200 litros) para eliminar ácaros del haz de hojas.",
                "Control químico con: Spirodiclofen, Cyexatín, Propargite, Abamectina o aceite agrícola vegetal.",
                "Prevención post-control: azufre micronizado (1.0 kg/200 lt de agua).",
                "Regar días antes de aplicar insecticidas. Evitar mezclas de agroquímicos.",
                "Aplicar cuando la planta no esté estresada para mejor efectividad."
            ],
            regla_activada="aranita_roja_completa"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: "tostado_hojas" in s and ("hojas_rojizas" in s or "perdida_clorofila" in s)),
        NOT(Diagnostico(plaga="Arañita roja (Oligonychus yothersi / O. punicae)"))
    )
    def aranita_roja_parcial(self):
        self.declare(Diagnostico(
            plaga="Arañita roja (Oligonychus yothersi / O. punicae) — sospecha",
            certeza=0.6,
            umbral="Presencia de ácaros en casi todas las plantas",
            recomendaciones=[
                "Inspeccionar el haz de las hojas con lupa en busca de ácaros pequeños.",
                "Buscar raspado y puntos rojizos en hojas maduras.",
                "El color rojizo es la respuesta de la planta al sellar heridas del raspado.",
                "Monitorear pérdida de actividad fotosintética y rendimiento."
            ],
            regla_activada="aranita_roja_parcial"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"perforacion_brotes", "fumagina", "debilitamiento_planta"}.issubset(s))
    )
    def mosca_blanca_completa(self):
        self.declare(Diagnostico(
            plaga="Mosca blanca de los brotes (Bemisia sp.)",
            certeza=1.0,
            umbral="Ataques severos en brotes",
            recomendaciones=[
                "Control preventivo: lavar con detergente agrícola (150 ml/200 lt).",
                "Realizar podas sanitarias para eliminar brotes afectados.",
                "Ataques severos: aplicar Acetamiprid, Imidacloprid, Clorpirifos o Buprofezin.",
                "Monitorear formación de fumagina (hongo negro sobre melaza secretada).",
                "Inspeccionar envés de hojas jóvenes en busca de adultos blancos."
            ],
            regla_activada="mosca_blanca_completa"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: len({"perforacion_brotes", "fumagina", "debilitamiento_planta", "hojas_pegajosas"} & s) >= 2),
        NOT(Diagnostico(plaga="Mosca blanca de los brotes (Bemisia sp.)"))
    )
    def mosca_blanca_parcial(self):
        self.declare(Diagnostico(
            plaga="Mosca blanca de los brotes (Bemisia sp.) — sospecha",
            certeza=0.65,
            umbral="Ataques severos en brotes",
            recomendaciones=[
                "Buscar insectos blancos pequeños en el envés de hojas jóvenes.",
                "Verificar presencia de melaza (sustancia pegajosa) en hojas.",
                "La fumagina (hongo negro) es indicador indirecto de mosca blanca.",
                "Realizar podas sanitarias preventivas."
            ],
            regla_activada="mosca_blanca_parcial"
        ))

    # ENFERMEDADES

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_amarillas", "defoliacion", "raices_necrosadas", "frutos_pequenos"}.issubset(s))
    )
    def tristeza_completa(self):
        self.declare(Diagnostico(
            plaga="Tristeza del palto (Phytophthora cinnamomi)",
            certeza=1.0,
            umbral="Presencia de raicillas podridas o necrosadas",
            recomendaciones=[
                "Emplear patrones tolerantes: Topa Topa y Duke.",
                "Aplicar riegos ligeros y frecuentes (evitar encharcamiento).",
                "Incorporar materia orgánica descompuesta (compost) al suelo.",
                "Si daño inicial: aplicar fungicida a base de Metalaxyl al cuello en forma de drench.",
                "Usar fosfonatos sistémicos: Aliete (Fosetil de aluminio) o ácido fosfórico.",
                "Mejorar drenaje en suelos arcillosos o pesados."
            ],
            regla_activada="tristeza_completa"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: len({"hojas_amarillas", "defoliacion", "raices_necrosadas", "muerte_regresiva"} & s) >= 2),
        NOT(Diagnostico(plaga="Tristeza del palto (Phytophthora cinnamomi)"))
    )
    def tristeza_parcial(self):
        self.declare(Diagnostico(
            plaga="Tristeza del palto (Phytophthora cinnamomi) — sospecha",
            certeza=0.7,
            umbral="Presencia de raicillas podridas o necrosadas",
            recomendaciones=[
                "Inspeccionar raíces en busca de pudrición o necrosis.",
                "La enfermedad prospera en suelos arcillosos con mal drenaje.",
                "En ataques leves: algunas ramas defoliadas.",
                "En ataques severos: árbol con fuerte defoliación que lleva a la muerte.",
                "Realizar análisis de suelo y evaluar condiciones de humedad."
            ],
            regla_activada="tristeza_parcial"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"cancros_tronco", "exudados_blancos", "muerte_ramas"}.issubset(s))
    )
    def brazo_negro_completo(self):
        self.declare(Diagnostico(
            plaga="Brazo negro (Lasiodiplodia theobromae)",
            certeza=1.0,
            umbral="Presencia de cancros con exudados blanquecinos",
            recomendaciones=[
                "Desinfectar semillas desde el inicio del cultivo.",
                "Pulverizar preventivamente dos veces al año con Benomil o Thiabendazol.",
                "Desinfectar herramientas de injerto y poda con lejía entre planta y planta.",
                "Eliminar ramas afectadas mediante poda sanitaria.",
                "Aplicar fungicida al observar primera secreción blanquecina en cancros.",
                "Evitar heridas abiertas durante podas e injertos."
            ],
            regla_activada="brazo_negro_completo"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: len({"cancros_tronco", "exudados_blancos", "muerte_ramas", "pudricion_frutos_pedunculo"} & s) >= 2),
        NOT(Diagnostico(plaga="Brazo negro (Lasiodiplodia theobromae)"))
    )
    def brazo_negro_parcial(self):
        self.declare(Diagnostico(
            plaga="Brazo negro (Lasiodiplodia theobromae) — sospecha",
            certeza=0.65,
            umbral="Presencia de cancros con exudados blanquecinos",
            recomendaciones=[
                "Buscar cancros con exudados blanquecinos y grumosos en tronco y ramas.",
                "Verificar necrosis del follaje y ramillas con muerte total del tejido.",
                "En frutos: pudrición en zona de inserción del pedúnculo.",
                "El hongo se disemina por herramientas sin desinfectar.",
                "Inspeccionar cortes longitudinales de frutos afectados."
            ],
            regla_activada="brazo_negro_parcial"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"manchas_amarillas_fruto", "variegado_hojas", "crecimiento_horizontal"}.issubset(s))
    )
    def sunblotch_completo(self):
        self.declare(Diagnostico(
            plaga="Sunblotch - Mancha de sol (ASBVD viroide)",
            certeza=1.0,
            umbral="Presencia de síntomas en frutos y hojas",
            recomendaciones=[
                "CRÍTICO: Los viroides NO se pueden controlar una vez en la planta.",
                "Eliminar plantas infectadas desde la raíz y quemar completamente.",
                "Prevención: desinfectar herramientas de poda y cosecha con agua+jabón o lejía.",
                "No usar semillas, yemas o plumas de plantas enfermas para propagación.",
                "Desinfectar tijeras de podar entre planta y planta durante cosecha.",
                "Adquirir material vegetal certificado libre de viroides."
            ],
            regla_activada="sunblotch_completo"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: len({"manchas_amarillas_fruto", "variegado_hojas", "moteado_hojas", "corteza_facil_desprender"} & s) >= 2),
        NOT(Diagnostico(plaga="Sunblotch - Mancha de sol (ASBVD viroide)"))
    )
    def sunblotch_parcial(self):
        self.declare(Diagnostico(
            plaga="Sunblotch - Mancha de sol (ASBVD viroide) — sospecha",
            certeza=0.75,
            umbral="Presencia de síntomas en frutos y hojas",
            recomendaciones=[
                "Lesión en forma de vagina en frutos con bordes indefinidos.",
                "Color: amarillo pálido (general), verde claro (Fuerte), rojizo (Hass).",
                "Moteado rosa o blanco en hojas.",
                "Líneas longitudinales amarillentas cuando se desprende corteza.",
                "Síntomas aparecen a partir del 3er año en plantas injertadas.",
                "Consultar con especialista para confirmación del diagnóstico."
            ],
            regla_activada="sunblotch_parcial"
        ))

    # SIN DIAGNÓSTICO

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        NOT(Diagnostico())
    )
    def sin_diagnostico(self):
        self.declare(Diagnostico(
            plaga="Sin plaga o enfermedad identificada",
            certeza=0.0,
            umbral="N/A",
            recomendaciones=[
                "No se detectaron síntomas compatibles con plagas o enfermedades principales en palta.",
                "Considerar deficiencias nutricionales (N, P, K, B, Ca, Mg, Zn) según síntomas foliares.",
                "Verificar estado fenológico: algunas plagas atacan en etapas específicas.",
                "Evaluar condiciones de drenaje, riego y fertilización.",
                "Consultar con especialista en cultivo de palto para diagnóstico detallado.",
                "Considerar análisis de suelo y foliar para detectar deficiencias."
            ],
            regla_activada="sin_diagnostico"
        ))