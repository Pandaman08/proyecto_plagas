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
            imagen="uva/filoxera.jpg"
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
        TEST(lambda s: "hojas_gris_plomizo" in s and not "tejido_araña" in s),
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
            imagen="uva/aranita_roja.webp"
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
            imagen="uva/aranita_roja.webp"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "hojas_abarquilladas" in s and not "brotacion_lenta" in s),
        NOT(Diagnostico(plaga="Ácaro hialino (Calipetrimerus vitis / Phyllocoptes vitis)"))
    )
    def acaro_hialino_parcial(self):
        self.declare(Diagnostico(
            plaga="Ácaro hialino – sospecha",
            certeza=0.5,
            umbral="Síntoma aislado",
            recomendaciones=[
                "Observar si la brotación es lenta en próximos días.",
                "Revisar brotes con deformaciones.",
                "Aplicar azufre preventivo."
            ],
            regla_activada="acaro_hialino_parcial",
            imagen="uva/aranita_roja.webp"
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
            imagen="uva/oidium.jpeg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "picaduras_racimos" in s and not "aves_presentes" in s and not "avispa_presencia" in s),
        NOT(Diagnostico(plaga="Aves (cuculíes, madrugadoras)"))
    )
    def picaduras_generales(self):
        self.declare(Diagnostico(
            plaga="Daño en racimos (causa a determinar)",
            certeza=0.5,
            umbral="Daño visible sin identificar agente",
            recomendaciones=[
                "Observar el campo en diferentes horas del día.",
                "Buscar presencia de aves, avispas o insectos.",
                "Instalar medidas de protección preventivas."
            ],
            regla_activada="picaduras_generales",
            imagen="uva/oidium.jpeg"
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
            imagen="uva/oidium_avispa.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "bayas_vacias" in s and not "avispa_presencia" in s),
        NOT(Diagnostico(plaga="Avispas y abejas (Polistes spp., Apis mellifera)"))
    )
    def bayas_vacias_parcial(self):
        self.declare(Diagnostico(
            plaga="Daño en uvas (posible avispas/aves)",
            certeza=0.6,
            umbral="Bayas vacías sin confirmar agente",
            recomendaciones=[
                "Revisar racimos en horas de la mañana y tarde.",
                "Buscar nidos de avispas cerca del viñedo.",
                "Instalar protecciones en racimos."
            ],
            regla_activada="bayas_vacias_parcial",
            imagen="uva/oidium_avispa.jpg"
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
            imagen="uva/oidium.jpeg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: ("racimos_consumidos" in s or "madrigueras" in s) and not ({"racimos_consumidos", "madrigueras"}.issubset(s))),
        NOT(Diagnostico(plaga="Ratas y ratones"))
    )
    def ratas_raton_parcial(self):
        self.declare(Diagnostico(
            plaga="Ratas y ratones – sospecha",
            certeza=0.7,
            umbral="Evidencia parcial de roedores",
            recomendaciones=[
                "Buscar heces, rastros o madrigueras adicionales.",
                "Revisar daños en tallos jóvenes.",
                "Colocar trampas para confirmar presencia."
            ],
            regla_activada="ratas_raton_parcial",
            imagen="uva/oidium.jpeg"
        ))

    # --- GUSANO CORNUDO ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_consumidas", "gusano_grande"}.issubset(s))
    )
    def gusano_cornudo_completa(self):
        self.declare(Diagnostico(
            plaga="Gusano cornudo (Pholus vitis)",
            certeza=1.0,
            umbral="Presencia visual de larvas >6 cm",
            recomendaciones=[
                "Recolección manual y destrucción.",
                "Aplicar Bacillus thuringiensis (Dipel) a 250 g/ha.",
                "Usar Trichlorfon (Dipterex 80) a 1.5 kg/ha si ataque severo."
            ],
            regla_activada="gusano_cornudo_completa",
            imagen="uva/gusano_cornudo.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "hojas_consumidas" in s and not "gusano_grande" in s),
        NOT(Diagnostico(plaga="Gusano cornudo (Pholus vitis)"))
    )
    def hojas_consumidas_parcial(self):
        self.declare(Diagnostico(
            plaga="Daño foliar por insecto (a identificar)",
            certeza=0.5,
            umbral="Hojas comidas sin identificar insecto",
            recomendaciones=[
                "Revisar plantas en horas de la tarde/noche.",
                "Buscar larvas, orugas o insectos grandes.",
                "Documentar características del insecto si lo encuentra."
            ],
            regla_activada="hojas_consumidas_parcial",
            imagen="uva/aranita_roja.webp"
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
            imagen="uva/nematodos.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "nódulos_redondeados_raíz" in s and not "plantas_debiles" in s),
        NOT(Diagnostico(plaga="Nematodos (Meloidogyne spp.)"))
    )
    def nematodos_parcial(self):
        self.declare(Diagnostico(
            plaga="Nematodos – sospecha",
            certeza=0.8,
            umbral="Nódulos en raíces detectados",
            recomendaciones=[
                "Observar desarrollo general de la planta.",
                "Enviar muestra de raíz y suelo a laboratorio.",
                "Implementar medidas preventivas con estiércol."
            ],
            regla_activada="nematodos_parcial",
            imagen="uva/nematodos.jpg"
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
            imagen="uva/oidium.jpeg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "polvillo_blanco" in s and not "aborto_flores" in s),
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
            imagen="uva/oidium.jpeg"
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
            imagen="uva/podredumbre_gris.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "moho_gris" in s and not "racimos_podridos" in s),
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
            imagen="uva/podredumbre_gris.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "racimos_podridos" in s and not "moho_gris" in s),
        NOT(Diagnostico(plaga="Podredumbre gris (Botrytis cinerea)"))
    )
    def racimos_podridos_general(self):
        self.declare(Diagnostico(
            plaga="Pudrición de racimos (causa a determinar)",
            certeza=0.5,
            umbral="Racimos podridos sin moho visible",
            recomendaciones=[
                "Revisar exceso de humedad y riego.",
                "Verificar ventilación de las plantas.",
                "Puede ser daño secundario por insectos o aves."
            ],
            regla_activada="racimos_podridos_general",
            imagen="uva/podredumbre_gris.jpg"
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
            imagen="uva/agalla_corona.jpg"
        ))

    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: "agallas_tallo" in s and not "plantas_pequeñas" in s),
        NOT(Diagnostico(plaga="Agalla de la corona (Agrobacterium vitis)"))
    )
    def agalla_corona_parcial(self):
        self.declare(Diagnostico(
            plaga="Agalla de la corona – sospecha",
            certeza=0.8,
            umbral="Tumores detectados",
            recomendaciones=[
                "Monitorear crecimiento de la planta.",
                "Desinfectar herramientas inmediatamente.",
                "Evitar propagar material de esta planta."
            ],
            regla_activada="agalla_corona_parcial",
            imagen="uva/agalla_corona.jpg"
        ))

    # --- DEFICIENCIA NUTRICIONAL ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"clorosis_hojas", "crecimiento_lento"}.issubset(s))
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
            imagen="uva/deficiencia.jpg"
        ))

    # --- ESTRÉS HÍDRICO ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_marchitas", "suelo_seco"}.issubset(s))
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
            imagen="uva/estres_hidrico.jpg"
        ))

    # --- PROBLEMA RADICULAR ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_amarrillentas", "raíces_dañadas"}.issubset(s))
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
            imagen="uva/problema_raices.jpg"
        ))

    # --- ESTRÉS AMBIENTAL ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"flores_no_cuajan", "temperatura_alta"}.issubset(s))
    )
    def estrés_ambiental(self):
        self.declare(Diagnostico(
            plaga="Estrés ambiental (alta temperatura)",
            certeza=0.8,
            umbral="Fallo en cuajado sin plaga",
            recomendaciones=[
                "Proporcionar sombra parcial en horas de calor extremo.",
                "Mantener humedad del suelo.",
                "Usar mulching para conservar agua."
            ],
            regla_activada="estrés_ambiental",
            imagen="uva/estres_ambiental.jpg"
        ))

    # --- MANEJO CULTURAL ---
    @Rule(
        Caso(cultivo="uva", sintomas=MATCH.s),
        TEST(lambda s: {"racimos_desiguales", "poda_inadecuada"}.issubset(s))
    )
    def manejo_cultivo(self):
        self.declare(Diagnostico(
            plaga="Manejo cultural inadecuado",
            certeza=0.9,
            umbral="Problemas estructurales en planta",
            recomendaciones=[
                "Implementar poda de formación y poda en verde.",
                "Reducir número de plantas por hoyo.",
                "Capacitarse en técnicas de manejo del viñedo."
            ],
            regla_activada="manejo_cultivo",
            imagen="uva/manejo_cultivo.jpg"
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