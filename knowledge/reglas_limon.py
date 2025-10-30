from experta import KnowledgeEngine, Rule, TEST, MATCH, NOT
from .hechos import Caso, Diagnostico

class ReglasLimon(KnowledgeEngine):

    # ═══════════════════════════════════════════════════════════════
    # REGLA 1: Minador de hojas de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_con_minas_serpentinas", "hojas_enrolladas", "hojas_plateadas"}.issubset(s))
    )
    def minador_hojas_completo(self):
        self.declare(Diagnostico(
            plaga="Minador de hojas de los cítricos (Phyllocnistis citrella)",
            certeza=1.0,
            umbral="Más del 25% de brotes infestados",
            recomendaciones=[
                "Inspeccionar brotes tiernos en busca de minas serpenteantes.",
                "Aplicar aceite agrícola al 0.5-1% durante brotación.",
                "Liberar parasitoides: Ageniaspis citricola o Citrostichus phyllocnistoides.",
                "Usar insecticidas: abamectina (300-500 ml/ha) o imidacloprid (0.03-0.05%)."
            ],
            regla_activada="minador_hojas_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 2: Pulgón negro de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"pulgones_brotes", "hojas_enrolladas", "mielada", "fumagina"}.issubset(s))
    )
    def pulgon_negro_completo(self):
        self.declare(Diagnostico(
            plaga="Pulgón negro de los cítricos (Toxoptera aurantii)",
            certeza=1.0,
            umbral="5% de brotes con colonias",
            recomendaciones=[
                "Revisar envés de hojas tiernas y brotes en floración.",
                "Aplicar jabón potásico al 1% o aceite mineral al 0.5%.",
                "Liberar depredadores: Cycloneda sanguinea, Paraneda pallidula.",
                "Usar imidacloprid (0.05%) o thiamethoxam (50-75 g/200L) si es necesario."
            ],
            regla_activada="pulgon_negro_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 3: Ácaro del tostado
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"frutos_plateados", "cáscara_agrietada", "frutos_pequeños"}.issubset(s))
    )
    def acaro_tostado_completo(self):
        self.declare(Diagnostico(
            plaga="Ácaro del tostado (Phyllocoptruta oleivora)",
            certeza=1.0,
            umbral="3-5 ácaros por cm² de fruto",
            recomendaciones=[
                "Inspeccionar frutos jóvenes cerca del pedúnculo.",
                "Aplicar azufre mojable o aceite agrícola al 0.5-1%.",
                "Usar acaricidas: abamectina (50-100 ml/200L) o fenpyroximate (200 ml/200L).",
                "Fomentar presencia del hongo Hirsutella thompsonii."
            ],
            regla_activada="acaro_tostado_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 4: Arañita roja de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_con_puntos_amarillos", "hojas_plateadas", "debilitamiento_planta"}.issubset(s))
    )
    def aranita_roja_completo(self):
        self.declare(Diagnostico(
            plaga="Arañita roja de los cítricos (Panonychus citri)",
            certeza=1.0,
            umbral="5-8 ácaros móviles por hoja",
            recomendaciones=[
                "Revisar haz de hojas con lupa (10x) en busca de ácaros rojos.",
                "Aplicar azufre mojable o aceite mineral al 1%.",
                "Liberar ácaros depredadores: Amblyseius chungas, Phytoseiulus persimilis.",
                "Usar acaricidas: spirodiclofen (0.04%) o spiromesifen (0.5-0.6 L/ha)."
            ],
            regla_activada="aranita_roja_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 5: Queresa coma (escama púrpura)
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_marrones_hojas", "hojas_amarillentas", "muerte_brotes"}.issubset(s))
    )
    def queresa_coma_completo(self):
        self.declare(Diagnostico(
            plaga="Queresa coma o escama púrpura (Lepidosaphes beckii)",
            certeza=1.0,
            umbral="Más de 10 escamas por hoja",
            recomendaciones=[
                "Inspeccionar nervadura central de hojas y ramas.",
                "Podar ramas muy infestadas y quemarlas.",
                "Aplicar aceite agrícola al 1% o buprofezin (200 g/cilindro).",
                "Liberar parasitoides: Aphytis lepidosaphes."
            ],
            regla_activada="queresa_coma_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 6: Queresa redonda de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_marrones_hojas", "frutos_con_manchas_oscuras", "debilitamiento_planta"}.issubset(s))
    )
    def queresa_redonda_completo(self):
        self.declare(Diagnostico(
            plaga="Queresa redonda de los cítricos (Selenaspidus articulatus)",
            certeza=1.0,
            umbral="Más de 2 mm de diámetro por escama",
            recomendaciones=[
                "Revisar hojas, ramas y frutos en busca de escamas circulares.",
                "Aplicar metidation (0.1-0.2%) o imidacloprid (140 ml/cilindro).",
                "Liberar parasitoide Aphytis roseni (1 colonia/ha).",
                "Usar aceite mineral al 1% en épocas de brotación."
            ],
            regla_activada="queresa_redonda_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 7: Piojo blanco de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_blancas_hojas", "mielada", "fumagina"}.issubset(s))
    )
    def piojo_blanco_completo(self):
        self.declare(Diagnostico(
            plaga="Piojo blanco de los cítricos (Pinnaspis aspidistrae)",
            certeza=1.0,
            umbral="Presencia visible en más del 10% de hojas",
            recomendaciones=[
                "Inspeccionar envés de hojas y base de frutos.",
                "Aplicar aceite mineral al 1% o metidation (0.1-0.2%).",
                "Liberar coccinélidos depredadores: Azya orbigera, Cryptognatha auriculata.",
                "Realizar podas de ventilación para reducir humedad."
            ],
            regla_activada="piojo_blanco_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 8: Mosca blanca lanuda de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"moscas_blancas_envés", "mielada", "fumagina", "hojas_amarillentas"}.issubset(s))
    )
    def mosca_blanca_lanuda_completo(self):
        self.declare(Diagnostico(
            plaga="Mosca blanca lanuda de los cítricos (Aleurothrixus floccosus)",
            certeza=1.0,
            umbral="Más de 5 ninfas por hoja",
            recomendaciones=[
                "Revisar envés de hojas en busca de ninfas con filamentos cerosos.",
                "Aplicar lavados con detergente + agua a presión.",
                "Liberar parasitoides: Cales noacki o Amitus spiniferus.",
                "Usar buprofezin (100 g/200L) o aceite agrícola al 0.5-1%."
            ],
            regla_activada="mosca_blanca_lanuda_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 9: Mosca negra de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"moscas_blancas_envés", "fumagina", "frutos_decolorados"}.issubset(s))
    )
    def mosca_negra_completo(self):
        self.declare(Diagnostico(
            plaga="Mosca negra de los cítricos (Aleurocanthus woglumi)",
            certeza=1.0,
            umbral="Más de 10 ninfas por hoja",
            recomendaciones=[
                "Inspeccionar envés de hojas por ninfas negras brillantes.",
                "Liberar parasitoide Encarsia perplexa (altamente eficiente).",
                "Aplicar aceite agrícola al 1% + detergente.",
                "Realizar podas de saneamiento en focos de infestación."
            ],
            regla_activada="mosca_negra_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 10: Cochinilla harinosa de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"insectos_algodonosos", "mielada", "frutos_deformados"}.issubset(s))
    )
    def cochinilla_harinosa_completo(self):
        self.declare(Diagnostico(
            plaga="Cochinilla harinosa de los cítricos (Planococcus citri)",
            certeza=1.0,
            umbral="Presencia en frutos o cáliz",
            recomendaciones=[
                "Revisar cáliz de frutos y zona de contacto entre frutos.",
                "Aplicar buprofezin (200 g/200L) o aceite mineral al 1%.",
                "Liberar parasitoides: Coccidoxenoides peregrinus o Leptomastidea abnormis.",
                "Fomentar presencia de Cryptolaemus montrouzieri (coccinélido depredador)."
            ],
            regla_activada="cochinilla_harinosa_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 11: Ácaro hialino
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"frutos_plateados", "hojas_deformadas", "frutos_deformados"}.issubset(s))
    )
    def acaro_hialino_completo(self):
        self.declare(Diagnostico(
            plaga="Ácaro hialino (Polyphagotarsonemus latus)",
            certeza=1.0,
            umbral="Presencia de ácaro en brotes tiernos",
            recomendaciones=[
                "Inspeccionar base de frutos pequeños (1 pulgada de diámetro).",
                "Aplicar spirodiclofen (Envidor 240 SC al 0.03%).",
                "Usar spiromesifen (Oberon 240 SC, 300-500 ml/ha).",
                "Realizar aplicaciones preventivas durante fructificación temprana."
            ],
            regla_activada="acaro_hialino_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 12: Queresa verde
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_marrones_hojas", "mielada", "debilitamiento_planta"}.issubset(s))
    )
    def queresa_verde_completo(self):
        self.declare(Diagnostico(
            plaga="Queresa verde (Coccus viridis)",
            certeza=0.9,
            umbral="Más de 5 escamas por hoja",
            recomendaciones=[
                "Revisar ramas, brotes y hojas por escamas verdes ovaladas.",
                "Aplicar aceite agrícola al 1% durante brotación-floración.",
                "Liberar parasitoides: Metaphycus luteolus (2 colonias/ha).",
                "Fomentar larvas de sirfidos Eosalpingogaster nigriventris (depredador)."
            ],
            regla_activada="queresa_verde_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 13: Gusano perro del naranjo (Heraclides thoas)
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"hojas_deformadas", "debilitamiento_planta"}.issubset(s))
    )
    def gusano_perro_completo(self):
        self.declare(Diagnostico(
            plaga="Gusano perro del naranjo (Heraclides thoas nealces)",
            certeza=0.85,
            umbral="Presencia de larvas en viveros o plantas jóvenes",
            recomendaciones=[
                "Realizar recolección manual de larvas grandes.",
                "Aplicar Bacillus thuringiensis (500 g/ha).",
                "Usar triflumuron (Alsystin 480 SC, 50 ml/cilindro).",
                "Monitorear presencia de parasitoide Pteromalus sp. en pupas."
            ],
            regla_activada="gusano_perro_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 14: Queresa cerosa
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_blancas_hojas", "fumagina", "mielada"}.issubset(s))
    )
    def queresa_cerosa_completo(self):
        self.declare(Diagnostico(
            plaga="Queresa cerosa (Ceroplastes floridensis)",
            certeza=0.9,
            umbral="Más de 3 escamas por hoja",
            recomendaciones=[
                "Inspeccionar hojas y ramillas por escamas blancas en forma de estrella.",
                "Aplicar aceite agrícola al 1% en plantas muy infestadas.",
                "Liberar parasitoides: Coccophagus caridei o Anicetus quintanai.",
                "Fomentar presencia de Scutellista cyanea (depredador de huevos)."
            ],
            regla_activada="queresa_cerosa_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 15: Queresa blanca algodonosa (cochinilla acanalada)
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"insectos_algodonosos", "fumagina", "hojas_amarillentas"}.issubset(s))
    )
    def cochinilla_acanalada_completo(self):
        self.declare(Diagnostico(
            plaga="Cochinilla acanalada (Icerya purchasi)",
            certeza=0.95,
            umbral="Presencia de ovisacos visibles",
            recomendaciones=[
                "Revisar ramas y tronco por ovisacos algodonosos blancos.",
                "Liberar coccinélido Rodolia cardinalis (muy eficiente).",
                "Aplicar aceite agrícola al 1% en focos específicos.",
                "Evitar uso de insecticidas de amplio espectro."
            ],
            regla_activada="cochinilla_acanalada_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 16: Pulgón verde de los cítricos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"pulgones_brotes", "hojas_enrolladas", "mielada"}.issubset(s))
    )
    def pulgon_verde_completo(self):
        self.declare(Diagnostico(
            plaga="Pulgón verde de los cítricos (Aphis spiraecola)",
            certeza=0.9,
            umbral="Colonias en más del 5% de brotes",
            recomendaciones=[
                "Revisar brotes tiernos y flores por pulgones verde amarillentos.",
                "Aplicar jabón potásico al 1% o aceite mineral al 0.5%.",
                "Liberar depredadores: Cycloneda sanguinea, Paraneda pallidula.",
                "Usar imidacloprid (0.05%) o thiamethoxam (50-75 g/200L)."
            ],
            regla_activada="pulgon_verde_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 17: Queresa negra del olivo
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_marrones_hojas", "fumagina", "muerte_brotes"}.issubset(s))
    )
    def queresa_negra_completo(self):
        self.declare(Diagnostico(
            plaga="Queresa negra del olivo (Saissetia oleae)",
            certeza=0.85,
            umbral="Más de 5 escamas por hoja con forma de H",
            recomendaciones=[
                "Inspeccionar hojas, ramas y tronco por escamas con crestas en H.",
                "Aplicar aceite agrícola al 1% en plantas infestadas.",
                "Liberar parasitoides: Metaphycus helvolus o Metaphycus lounsburyi.",
                "Fomentar presencia de Scutellista cyanea (depredador de huevos)."
            ],
            regla_activada="queresa_negra_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 18: Ortézidos (queresa blanca)
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"escamas_blancas_hojas", "fumagina", "debilitamiento_planta"}.issubset(s))
    )
    def ortezidos_completo(self):
        self.declare(Diagnostico(
            plaga="Ortézidos (Praelongaorthezia praelonga)",
            certeza=0.9,
            umbral="Presencia de ovisacos blancos pulverulentos",
            recomendaciones=[
                "Revisar envés de hojas, ramas y tronco.",
                "Eliminar malezas alrededor del cultivo (reservorio).",
                "Aplicar buprofezin (Applaud, 200 g/200L).",
                "Liberar depredadores: Eosalpingogaster sp. (sirfido)."
            ],
            regla_activada="ortezidos_completo"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 19: Mosca mediterránea de la fruta (ocasional en limón)
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"frutos_con_manchas_oscuras", "frutos_deformados"}.issubset(s))
    )
    def mosca_mediterranea_parcial(self):
        self.declare(Diagnostico(
            plaga="Mosca mediterránea de la fruta (Ceratitis capitata)",
            certeza=0.7,
            umbral="Más de 0.5 moscas/trampa/día (MTD)",
            recomendaciones=[
                "Colocar trampas Jackson con Trimledure (1 trampa/4 ha).",
                "Recoger y enterrar frutos caídos.",
                "Aplicar cebos tóxicos: buminal + malathion (4 por mil).",
                "Usar trampas McPhail con atrayentes alimenticios."
            ],
            regla_activada="mosca_mediterranea_parcial"
        ))

    # ═══════════════════════════════════════════════════════════════
    # REGLA 20: Síntomas generales inespecíficos
    # ═══════════════════════════════════════════════════════════════
    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"debilitamiento_planta", "hojas_amarillentas"}.issubset(s) and len(s) <= 2)
    )
    def sintomas_generales(self):
        self.declare(Diagnostico(
            plaga="Diagnóstico inconcluso - síntomas generales",
            certeza=0.5,
            umbral="No aplicable",
            recomendaciones=[
                "Realizar inspección detallada en busca de insectos o ácaros.",
                "Verificar si hay presencia de mielada, fumagina o escamas.",
                "Revisar condiciones de riego, nutrición y pH del suelo.",
                "Consultar con un técnico agrónomo para diagnóstico preciso."
            ],
            regla_activada="sintomas_generales"
        ))
