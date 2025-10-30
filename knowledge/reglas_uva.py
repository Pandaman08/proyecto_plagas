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

class ReglasUva(KnowledgeEngine):
    # --- FILÓXERA ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"verrugas_hojas", "nudosidades_raices"}.issubset(s))
    )
    def filoxera_completa(self):
        self.declare(Diagnostico(
            plaga="Filóxera (Phylloxera vitifoliae)",
            certeza=1.0,
            umbral="Presencia en raíces o hojas",
            recomendaciones=[
                "Injertar sobre porta-injertos resistentes: Poulsen, 1102, Riparia.",
                "Evitar plantas provenientes de zonas infestadas.",
                "Tratar yemas con insecticidas antes de injertar.",
                "Aplicar imidacloprid (Confidor) a 100 ml/200L si hay ataque."
            ],
            regla_activada="filoxera_completa",
            imagen="uva/filoxera.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "verrugas_hojas" in s or "nudosidades_raices" in s),
        NOT(Diagnostico(plaga="Filóxera (Phylloxera vitifoliae)"))
    )
    def filoxera_parcial(self):
        self.declare(Diagnostico(
            plaga="Filóxera (Phylloxera vitifoliae) – sospecha",
            certeza=0.7,
            umbral="Presencia parcial de síntomas",
            recomendaciones=[
                "Confirmar mediante inspección de raíces y hojas.",
                "Revisar origen de plantas e injertos.",
                "Implementar medidas preventivas inmediatas."
            ],
            regla_activada="filoxera_parcial",
            imagen="filoxera.jpg"
        ))

    # --- ARAÑITA ROJA ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_gris_plomizo", "tejido_araña"}.issubset(s))
    )
    def aranita_roja_completa(self):
        self.declare(Diagnostico(
            plaga="Arañita roja (Panonychus ulmi / Tetranynchus sp.)",
            certeza=1.0,
            umbral="Alta densidad visible a simple vista",
            recomendaciones=[
                "Mantener riego adecuado y humedad relativa.",
                "Aplicar azufre espolvoreado (30 kg/ha) o azufre mojable (1 kg/200L).",
                "Usar Propineb (Fitorraz) si hay daño severo.",
                "Rotar acaricidas: Dicofol, Abamectina, Azocyclotin."
            ],
            regla_activada="aranita_roja_completa",
            imagen="uva/aranita_roja.webp"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "hojas_gris_plomizo" in s),
        NOT(Diagnostico(plaga="Arañita roja (Panonychus ulmi / Tetranynchus sp.)"))
    )
    def aranita_roja_parcial(self):
        self.declare(Diagnostico(
            plaga="Arañita roja – sospecha",
            certeza=0.6,
            umbral="Síntoma inicial",
            recomendaciones=[
                "Inspeccionar cara inferior de hojas con lupa 10X.",
                "Verificar presencia de ácaros rojos pequeños.",
                "Iniciar control preventivo con azufre."
            ],
            regla_activada="aranita_roja_parcial",
            imagen="aranita_roja.jpg"
        ))

    # --- ACARO HIALINO ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"brotacion_lenta", "hojas_abarquilladas"}.issubset(s))
    )
    def acaro_hialino_completa(self):
        self.declare(Diagnostico(
            plaga="Ácaro hialino (Calipetrimerus vitis / Phyllocoptes vitis)",
            certeza=1.0,
            umbral="Deformación visible en brotes",
            recomendaciones=[
                "Quemar restos de poda.",
                "Aplicar azufre antes de la brotación (1 kg/200L).",
                "Usar aceite agrícola + Azocyclotin o Abamectina si hay ataque."
            ],
            regla_activada="acaro_hialino_completa",
            imagen="uva/aranita_roja.jpg"  # Reutilizar si no tienes imagen específica
        ))

    # --- AVES ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"picaduras_racimos", "aves_presentes"}.issubset(s))
    )
    def aves_completa(self):
        self.declare(Diagnostico(
            plaga="Aves (cuculíes, madrugadoras)",
            certeza=1.0,
            umbral="Daño estético en racimos",
            recomendaciones=[
                "Instalar cintas anti-aves (efectivas en Caravelí).",
                "Usar protectores de racimos (bolsas de papel).",
                "Aplicar Oiko Neem (1.2 L/200L) semanas previas a cosecha.",
                "Ahuyentar con espantapájaros o sonidos."
            ],
            regla_activada="aves_completa",
            imagen="uva/oidium.jpeg"  # Reutilizar o cambiar si tienes imagen de aves
        ))

    # --- AVISPAS Y ABEJAS ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"bayas_vacias", "avispa_presencia"}.issubset(s))
    )
    def avispas_abejas_completa(self):
        self.declare(Diagnostico(
            plaga="Avispas y abejas (Polistes spp., Apis mellifera)",
            certeza=1.0,
            umbral="Racimos con bayas solo piel",
            recomendaciones=[
                "Eliminar nidos silvestres cerca del viñedo.",
                "Usar cebos tóxicos: zumo de fruta + Trichlorfon (4g/L).",
                "Colocar bolsas de papel en racimos pequeños.",
                "Aplicar Malathion localizado si es necesario."
            ],
            regla_activada="avispas_abejas_completa",
            imagen="uva/oidium_avispa.jpg"  # Reutilizar o cambiar
        ))

    # --- RATAS Y RATONES ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"racimos_consumidos", "madrigueras"}.issubset(s))
    )
    def ratas_raton_completa(self):
        self.declare(Diagnostico(
            plaga="Ratas y ratones",
            certeza=1.0,
            umbral="Daño directo en racimos o tallos",
            recomendaciones=[
                "Fomentar enemigos naturales: zorros, aves rapaces, culebras.",
                "Destruir madrigueras y usar trampas mecánicas.",
                "Aplicar rodenticidas anticoagulantes (Cumatetralil, Difetialone) en cebos."
            ],
            regla_activada="ratas_raton_completa",
            imagen="uva/oidium.jpeg"  # Reutilizar o cambiar
        ))

    # --- GUSANO CORNUDO ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_consumidas", "gusano_grande"}.issubset(s))
    )
    def gusano_cornudo_completa(self):
        self.dedeclare(Diagnostico(
            plaga="Gusano cornudo (Pholus vitis)",
            certeza=1.0,
            umbral="Presencia visual de larvas >6 cm",
            recomendaciones=[
                "Recolección manual y destrucción.",
                "Aplicar Bacillus thuringiensis (Dipel) a 250 g/ha.",
                "Usar Trichlorfon (Dipterex 80) a 1.5 kg/ha si ataque severo."
            ],
            regla_activada="gusano_cornudo_completa",
            imagen="gusano_cornudo.jpg"
        ))

    # --- NEMATODOS ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"plantas_debiles", "nódulos_redondeados_raíz"}.issubset(s))
    )
    def nematodos_completa(self):
        self.declare(Diagnostico(
            plaga="Nematodos (Meloidogyne spp.)",
            certeza=1.0,
            umbral="Nódulos redondeados en raíces",
            recomendaciones=[
                "Injertar sobre patrones resistentes: Verlandieri, Riparia.",
                "Aplicar estiércol para promover hongos antagonistas.",
                "Favorecer lombrices de tierra (sus excretas son tóxicas para nematodos).",
                "Último recurso: nematicidas como Aldicarb (Temik) – alto riesgo."
            ],
            regla_activada="nematodos_completa",
            imagen="oidium.jpg"  # Reutilizar o cambiar
        ))

    # --- OIDIO (OIDIUM) ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"polvillo_blanco", "aborto_flores"}.issubset(s))
    )
    def oidium_completa(self):
        self.declare(Diagnostico(
            plaga="Oidio (Uncinula necator)",
            certeza=1.0,
            umbral="Polvillo blanco en hojas y racimos",
            recomendaciones=[
                "Mejorar aireación con poda en verde y distanciamiento de plantas.",
                "Aplicar azufre espolvoreado (30-40 kg/ha) o azufre mojable (1 kg/200L).",
                "Fungicidas: Tebuconazole (Silvacur), Triadimenol (Bayfidan) a 100 ml/200L.",
                "Tratamientos en: brotes 10cm, inicio floración, envero."
            ],
            regla_activada="oidium_completa",
            imagen="oidium.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "polvillo_blanco" in s),
        NOT(Diagnostico(plaga="Oidio (Uncinula necator)"))
    )
    def oidium_parcial(self):
        self.declare(Diagnostico(
            plaga="Oidio – sospecha",
            certeza=0.7,
            umbral="Primeros signos visibles",
            recomendaciones=[
                "Inspeccionar ambas caras de hojas y racimos.",
                "Iniciar tratamiento preventivo con azufre.",
                "Evitar riego excesivo y mantener ventilación."
            ],
            regla_activada="oidium_parcial",
            imagen="oidium.jpg"
        ))

    # --- PODREDUMBRE GRIS ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"moho_gris", "racimos_podridos"}.issubset(s))
    )
    def podredumbre_gris_completa(self):
        self.declare(Diagnostico(
            plaga="Podredumbre gris (Botrytis cinerea)",
            certeza=1.0,
            umbral="Moho gris en racimos en envero",
            recomendaciones=[
                "Poda en verde para mejorar aireación.",
                "Evitar riegos pesados; usar riegos ligeros.",
                "Fungicidas: Benomil (200 g/200L), Tebuconazole (200 ml/200L), Tolyfluanid (500 g/200L).",
                "Aplicar en: cuajado, grano guisante, inicio envero, 21 días pre-cosecha."
            ],
            regla_activada="podredumbre_gris_completa",
            imagen="podredumbre_gris.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "moho_gris" in s),
        NOT(Diagnostico(plaga="Podredumbre gris (Botrytis cinerea)"))
    )
    def podredumbre_gris_parcial(self):
        self.declare(Diagnostico(
            plaga="Podredumbre gris – sospecha",
            certeza=0.6,
            umbral="Primeras manchas marrón oscuro",
            recomendaciones=[
                "Inspeccionar racimos en floración y envero.",
                "Reducir humedad con poda y ventilación.",
                "Iniciar aplicación preventiva de fungicidas."
            ],
            regla_activada="podredumbre_gris_parcial",
            imagen="podredumbre_gris.jpg"
        ))

    # --- AGALLA DE LA CORONA ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"agallas_tallo", "plantas_pequeñas"}.issubset(s))
    )
    def agalla_corona_completa(self):
        self.declare(Diagnostico(
            plaga="Agalla de la corona (Agrobacterium vitis)",
            certeza=1.0,
            umbral="Tumores en cuello de planta",
            recomendaciones=[
                "Usar porta-injertos resistentes: Riparia Gloria, Rupestris du Lot.",
                "Desinfectar herramientas de poda con lejía (200 ml/L) o formol (50 ml/L).",
                "Quemar restos de poda y plantas enfermas.",
                "Extirpar tumores y aplicar cicatrizante vegetal (Skane M8)."
            ],
            regla_activada="agalla_corona_completa",
            imagen="agalla_corona.jpg"
        ))

    # --- REGLAS ADICIONALES (para completar 20) ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "clorosis_hojas" in s and "crecimiento_lento" in s)
    )
    def deficiencia_nutricional(self):
        self.declare(Diagnostico(
            plaga="Deficiencia nutricional (potasio/nitrógeno)",
            certeza=0.8,
            umbral="Síntomas generales sin plaga específica",
            recomendaciones=[
                "Realizar análisis de suelo y hojas.",
                "Aplicar fertilizantes equilibrados (N-P-K).",
                "Evitar exceso de nitrógeno que favorece plagas."
            ],
            regla_activada="deficiencia_nutricional",
            imagen="oidium.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "hojas_marchitas" in s and "suelo_seco" in s)
    )
    def estrés_hidrico(self):
        self.declare(Diagnostico(
            plaga="Estrés hídrico",
            certeza=0.9,
            umbral="Marchitez sin plaga visible",
            recomendaciones=[
                "Ajustar frecuencia de riego (no superar 30 días entre riegos).",
                "Usar riego gota a gota si es posible.",
                "Monitorear humedad del suelo."
            ],
            regla_activada="estrés_hidrico",
            imagen="oidium.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "hojas_amarrillentas" in s and "raíces_dañadas" in s)
    )
    def problema_raices(self):
        self.declare(Diagnostico(
            plaga="Problema radicular (drenaje/pH)",
            certeza=0.7,
            umbral="Síntomas sistémicos",
            recomendaciones=[
                "Verificar drenaje del suelo y pH (ideal 6.0-7.0).",
                "Aplicar enmiendas orgánicas.",
                "Evitar compactación del suelo."
            ],
            regla_activada="problema_raices",
            imagen="oidium.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "flores_no_cuajan" in s and "temperatura_alta" in s)
    )
    def estrés_ambiental(self):
        self.declare(Diagnostico(
            plaga="Estrés ambiental (alta temperatura)",
            certeza=0.6,
            umbral="Fallo en cuajado sin plaga",
            recomendaciones=[
                "Proporcionar sombra parcial en horas de calor extremo.",
                "Mantener humedad del suelo.",
                "Usar mulching para conservar agua."
            ],
            regla_activada="estrés_ambiental",
            imagen="oidium.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "racimos_desiguales" in s and "poda_inadecuada" in s)
    )
    def manejo_cultivo(self):
        self.declare(Diagnostico(
            plaga="Manejo cultural inadecuado",
            certeza=0.8,
            umbral="Problemas estructurales en planta",
            recomendaciones=[
                "Implementar poda de formación y poda en verde.",
                "Reducir número de plantas por hoyo.",
                "Capacitarse en técnicas de manejo del viñedo."
            ],
            regla_activada="manejo_cultivo",
            imagen="oidium.jpg"
        ))

    # --- SIN DIAGNÓSTICO ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        NOT(Diagnostico())
    )
    def sin_diagnostico(self):
        self.declare(Diagnostico(
            plaga="Sin plaga identificada",
            certeza=0.0,
            umbral="N/A",
            recomendaciones=[
                "No se detectaron síntomas compatibles con plagas principales en uva.",
                "Verifique condiciones de cultivo: riego, fertilización, poda.",
                "Consulte a un especialista o envíe muestras a laboratorio."
            ],
            regla_activada="sin_diagnostico",
            imagen=None
        ))