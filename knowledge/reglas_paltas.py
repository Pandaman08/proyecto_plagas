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

    # PLAGAS (10 PLAGAS CON 20 REGLAS)

    # 1. TRIPS DEL PALTO

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

    # 2. ARAÑITA ROJA / ARAÑITA MARRÓN

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"tostado_hojas", "hojas_rojizas", "defoliacion_prematura"}.issubset(s))
    )
    def aranita_roja_completa(self):
        self.declare(Diagnostico(
            plaga="Arañita roja/marrón (Oligonychus yothersi / O. punicae)",
            certeza=1.0,
            umbral="300 ácaros/hoja o 70 hembras adultas/hoja en sequía",
            recomendaciones=[
                "Realizar lavado a presión con detergente agrícola (150 ml/200 litros) para eliminar ácaros del haz de hojas.",
                "Control químico con: Spirodiclofen, Cyexatín, Propargite, Abamectina o aceite agrícola vegetal.",
                "Prevención post-control: azufre micronizado (1.0 kg/200 lt de agua).",
                "Regar días antes de aplicar insecticidas. Evitar mezclas de agroquímicos.",
                "Los ácaros se encuentran en la cara SUPERIOR de las hojas (diferente a otras especies).",
                "Monitorear: 300 ácaros/hoja causa bronceado y defoliación parcial."
            ],
            regla_activada="aranita_roja_completa"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: "tostado_hojas" in s and ("hojas_rojizas" in s or "perdida_clorofila" in s or "bronceado_hojas" in s)),
        NOT(Diagnostico(plaga="Arañita roja/marrón (Oligonychus yothersi / O. punicae)"))
    )
    def aranita_roja_parcial(self):
        self.declare(Diagnostico(
            plaga="Arañita roja/marrón (Oligonychus yothersi / O. punicae) — sospecha",
            certeza=0.65,
            umbral="300 ácaros/hoja o 70 hembras adultas/hoja en sequía",
            recomendaciones=[
                "Inspeccionar el HAZ (cara superior) de las hojas con lupa en busca de ácaros pequeños.",
                "Buscar reducción en actividad fotosintética por succión de savia.",
                "El bronceado de hojas es signo de alta densidad de ácaros.",
                "Periodos de sequía favorecen la defoliación con menos ácaros (70 hembras/hoja)."
            ],
            regla_activada="aranita_roja_parcial"
        ))

    # 3. MOSCA BLANCA DE LOS BROTES

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

    # 4. QUERESAS FIORINIA

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_marron_frutos", "secamiento_hojas", "defoliacion"}.issubset(s))
    )
    def queresas_fiorinia_completa(self):
        self.declare(Diagnostico(
            plaga="Queresas Fiorinia (Fiorinia fiorinae)",
            certeza=1.0,
            umbral="Poblaciones que cubren casi la totalidad de hojas",
            recomendaciones=[
                "Daño cosmético particularmente cuando poblaciones se localizan sobre frutos.",
                "Inspeccionar escamas alargadas de color marrón amarillento con pliegue central (carina).",
                "Escamas de forma 'pupilarial' formadas por dos exuvias solamente.",
                "Control químico: aceites minerales o insecticidas sistémicos.",
                "Monitoreo crítico: cuando cubren casi toda la hoja provocan secamiento y defoliación.",
                "En frutos: afecta calidad cosmética reduciendo valor comercial."
            ],
            regla_activada="queresas_fiorinia_completa"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: len({"escamas_marron_frutos", "escamas_marron_hojas", "secamiento_hojas"} & s) >= 2),
        NOT(Diagnostico(plaga="Queresas Fiorinia (Fiorinia fiorinae)"))
    )
    def queresas_fiorinia_parcial(self):
        self.declare(Diagnostico(
            plaga="Queresas Fiorinia (Fiorinia fiorinae) — sospecha",
            certeza=0.7,
            umbral="Poblaciones que cubren casi la totalidad de hojas",
            recomendaciones=[
                "Buscar escamas pequeñas alargadas de color marrón amarillento.",
                "Verificar presencia de pliegue central (carina longitudinal) en la escama.",
                "Escamas del macho son más pequeñas y de color blancuzco.",
                "Inspeccionar hojas y frutos en busca de cobertura de escamas.",
                "El daño económico es mayor cuando afecta la calidad cosmética del fruto."
            ],
            regla_activada="queresas_fiorinia_parcial"
        ))

    # 5. QUERESAS HEMIBERLESIA

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_blancas_pedunculo", "escamas_circulares_frutos"}.issubset(s))
    )
    def queresas_hemiberlesia_completa(self):
        self.declare(Diagnostico(
            plaga="Queresas Hemiberlesia (Hemiberlesia lataniae)",
            certeza=1.0,
            umbral="Presencia en zona peduncular del fruto",
            recomendaciones=[
                "Especie cosmopolita frecuentemente interceptada en cuarentena.",
                "Principal daño: presencia en frutos afectando exportación.",
                "Se establece preferentemente en zona peduncular (difícil remoción en post-cosecha).",
                "Escama circular u ovalada, convexa, gruesa, color blanco rosado.",
                "Exuvias sub-centrales oscuras a casi negras (diferenciación diagnóstica).",
                "Control: tratamientos pre-cosecha con aceites o insecticidas sistémicos.",
                "Crítico para exportación: requiere certificación fitosanitaria."
            ],
            regla_activada="queresas_hemiberlesia_completa"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: "escamas_blancas_pedunculo" in s or "escamas_circulares_frutos" in s),
        NOT(Diagnostico(plaga="Queresas Hemiberlesia (Hemiberlesia lataniae)"))
    )
    def queresas_hemiberlesia_parcial(self):
        self.declare(Diagnostico(
            plaga="Queresas Hemiberlesia (Hemiberlesia lataniae) — sospecha",
            certeza=0.7,
            umbral="Presencia en zona peduncular del fruto",
            recomendaciones=[
                "Inspeccionar zona peduncular del fruto (sitio preferencial).",
                "Buscar escamas circulares u ovaladas bien adheridas a la planta.",
                "Color blanco algo rosado con exuvias centrales oscuras.",
                "Difícil remoción durante proceso de post-cosecha.",
                "Problema crítico para frutos de exportación."
            ],
            regla_activada="queresas_hemiberlesia_parcial"
        ))

    # 6. MOSCA BLANCA ESPIRAL

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"espirales_cera_hojas", "huevos_desordenados_enves", "cobertura_cera_hojas"}.issubset(s))
    )
    def mosca_blanca_espiral_completa(self):
        self.declare(Diagnostico(
            plaga="Mosca blanca espiral (Aleurodicus cocois)",
            certeza=1.0,
            umbral="Ataques intensos con cobertura de cera acentuada",
            recomendaciones=[
                "Característica diagnóstica: grandes espirales de secreciones céreas en envés de hojas.",
                "Huevos alargados dispuestos en forma desordenada dentro de las espirales.",
                "Secreta menor cantidad de melaza comparada con otras especies de moscas blancas.",
                "En ataques intensos: cobertura de cera muy acentuada en hojas.",
                "Control: detergentes agrícolas, aceites minerales o insecticidas sistémicos.",
                "Monitorear envés de hojas regularmente."
            ],
            regla_activada="mosca_blanca_espiral_completa"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: len({"espirales_cera_hojas", "huevos_desordenados_enves", "cobertura_cera_hojas"} & s) >= 2),
        NOT(Diagnostico(plaga="Mosca blanca espiral (Aleurodicus cocois)"))
    )
    def mosca_blanca_espiral_parcial(self):
        self.declare(Diagnostico(
            plaga="Mosca blanca espiral (Aleurodicus cocois) — sospecha",
            certeza=0.65,
            umbral="Ataques intensos con cobertura de cera acentuada",
            recomendaciones=[
                "Inspeccionar envés de hojas en busca de espirales céreas características.",
                "Buscar huevos alargados en disposición desordenada.",
                "Verificar cobertura de cera blanca sobre las hojas.",
                "Diferente a otras moscas blancas por patrón espiral de oviposición."
            ],
            regla_activada="mosca_blanca_espiral_parcial"
        ))

    # 7. BICHO DEL CESTO

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: {"cestos_colgantes_hojas", "raspado_epidermis_hojas", "defoliacion"}.issubset(s))
    )
    def bicho_cesto_completo(self):
        self.declare(Diagnostico(
            plaga="Bicho del cesto (Oiketicus kirbyi)",
            certeza=1.0,
            umbral="Presencia de cestos en follaje",
            recomendaciones=[
                "Característica única: larva construye 'cesto' con restos de follaje pegados con saliva.",
                "Al eclosionar, larvas raspan epidermis del follaje inmediatamente.",
                "Cesto se amplía con pedazos de follaje, ramitas y nervaduras a medida que crece.",
                "Control manual: recolectar y destruir cestos visibles.",
                "Control biológico: avispas parasitoides naturales.",
                "Control químico: Bacillus thuringiensis o insecticidas en estadios tempranos.",
                "Monitorear antes de que las larvas completen el cesto protector."
            ],
            regla_activada="bicho_cesto_completo"
        ))

    @Rule(
        Caso(cultivo="palta", sintomas=MATCH.s),
        TEST(lambda s: len({"cestos_colgantes_hojas", "raspado_epidermis_hojas", "larvas_con_refugio"} & s) >= 2),
        NOT(Diagnostico(plaga="Bicho del cesto (Oiketicus kirbyi)"))
    )
    def bicho_cesto_parcial(self):
        self.declare(Diagnostico(
            plaga="Bicho del cesto (Oiketicus kirbyi) — sospecha",
            certeza=0.7,
            umbral="Presencia de cestos en follaje",
            recomendaciones=[
                "Buscar estructuras en forma de 'cesto' colgando de las hojas.",
                "El cesto está formado por pedazos de hojas, ramitas y nervaduras.",
                "Verificar raspado superficial en epidermis de hojas.",
                "Las larvas se protegen dentro del cesto mientras se alimentan.",
                "Fácil de detectar visualmente por los cestos característicos."
            ],
            regla_activada="bicho_cesto_parcial"
        ))

    # ENFERMEDADES (3 ENFERMEDADES CON 6 REGLAS)

    # 8. TRISTEZA DEL PALTO

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
                "Mejorar drenaje en suelos arcillosos o pesados.",
                "La enfermedad prospera cuando el suelo es arcilloso o pesado."
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

    # 9. BRAZO NEGRO

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
                "Evitar heridas abiertas durante podas e injertos.",
                "El hongo se disemina por herramientas no desinfectadas."
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

    # 10. SUNBLOTCH (MANCHA DE SOL)

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
                "Adquirir material vegetal certificado libre de viroides.",
                "Disminuye rendimientos y produce frutas sin valor comercial."
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
                "Los paltos no desarrollan en altura, tienen crecimiento horizontal.",
                "Consultar con especialista para confirmación del diagnóstico."
            ],
            regla_activada="sunblotch_parcial"
        ))

    # SIN DIAGNÓSTICO (REGLA 21)

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
                "Considerar análisis de suelo y foliar para detectar deficiencias.",
                "Revisar la guía fotográfica oficial para comparar síntomas visuales."
            ],
            regla_activada="sin_diagnostico"
        ))