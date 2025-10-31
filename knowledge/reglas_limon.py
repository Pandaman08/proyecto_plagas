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

class ReglasLimon(KnowledgeEngine):

    # PLAGAS DEL LIMÓN (10 PLAGAS CON 20 REGLAS)

    # 1. MINADOR DE HOJAS DE LOS CÍTRICOS

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
                "Inspeccionar brotes tiernos en busca de minas serpenteantes características.",
                "Aplicar aceite agrícola al 0.5-1% durante brotación para sofocar larvas.",
                "Liberar parasitoides: Ageniaspis citricola o Citrostichus phyllocnistoides.",
                "Control químico: abamectina (300-500 ml/ha) o imidacloprid (0.03-0.05%).",
                "Las galerías serpentinas son dejadas por larvas que se alimentan entre epidermis."
            ],
            regla_activada="minador_hojas_completo",
            imagen="limon/minador.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"hojas_con_minas_serpentinas", "hojas_enrolladas", "hojas_plateadas", "hojas_deformadas"} & s) >= 2),
        NOT(Diagnostico(plaga="Minador de hojas de los cítricos (Phyllocnistis citrella)"))
    )
    def minador_hojas_parcial(self):
        self.declare(Diagnostico(
            plaga="Minador de hojas de los cítricos (Phyllocnistis citrella) — sospecha",
            certeza=0.7,
            umbral="Más del 25% de brotes infestados",
            recomendaciones=[
                "Buscar galerías serpenteantes en hojas jóvenes y brotes tiernos.",
                "Las minas son túneles plateados que serpentean por la lámina foliar.",
                "Ataca principalmente en periodos de brotación intensa.",
                "Verificar presencia de pequeñas pupas en bordes de hojas enrolladas."
            ],
            regla_activada="minador_hojas_parcial",
            imagen="limon/minador.jpg"
        ))

    # 2. PULGÓN NEGRO DE LOS CÍTRICOS

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"pulgones_brotes", "hojas_enrolladas", "mielada"}.issubset(s))
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
                "Control químico: imidacloprid (0.05%) o thiamethoxam (50-75 g/200L).",
                "La mielada favorece aparición de fumagina (hongo negro)."
            ],
            regla_activada="pulgon_negro_completo",
            imagen="limon/pulgon_negro.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"pulgones_brotes", "hojas_enrolladas", "mielada", "fumagina"} & s) >= 2),
        NOT(Diagnostico(plaga="Pulgón negro de los cítricos (Toxoptera aurantii)"))
    )
    def pulgon_negro_parcial(self):
        self.declare(Diagnostico(
            plaga="Pulgón negro de los cítricos (Toxoptera aurantii) — sospecha",
            certeza=0.7,
            umbral="5% de brotes con colonias",
            recomendaciones=[
                "Buscar colonias de pulgones negros en brotes tiernos y envés de hojas.",
                "Pueden transmitir el virus de la tristeza de los cítricos.",
                "Los pulgones secretan mielada que atrae hormigas y favorece fumagina.",
                "Monitorear especialmente durante brotación y floración."
            ],
            regla_activada="pulgon_negro_parcial",
            imagen="limon/pulgon_negro.jpg"
        ))

    # 3. ÁCARO DEL TOSTADO

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
                "Inspeccionar frutos jóvenes cerca del pedúnculo con lupa (10x).",
                "Aplicar azufre mojable o aceite agrícola al 0.5-1%.",
                "Control químico: abamectina (50-100 ml/200L) o fenpyroximate (200 ml/200L).",
                "Fomentar presencia del hongo Hirsutella thompsonii.",
                "El daño en cáscara reduce calidad comercial pero no afecta pulpa."
            ],
            regla_activada="acaro_tostado_completo",
            imagen="limon/acaro_tostado.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"frutos_plateados", "cáscara_agrietada", "frutos_pequeños", "frutos_decolorados"} & s) >= 2),
        NOT(Diagnostico(plaga="Ácaro del tostado (Phyllocoptruta oleivora)"))
    )
    def acaro_tostado_parcial(self):
        self.declare(Diagnostico(
            plaga="Ácaro del tostado (Phyllocoptruta oleivora) — sospecha",
            certeza=0.7,
            umbral="3-5 ácaros por cm² de fruto",
            recomendaciones=[
                "Buscar ácaros microscópicos de color amarillo pálido en frutos.",
                "El daño aparece como plateado o bronceado en cáscara.",
                "Ataques severos causan agrietamiento y caída prematura de frutos.",
                "Realizar monitoreo desde cuajado hasta 8-10 semanas después."
            ],
            regla_activada="acaro_tostado_parcial",
            imagen="limon/acaro_tostado.jpg"
        ))

    # 4. ARAÑITA ROJA DE LOS CÍTRICOS

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
                "Revisar HAZ de hojas con lupa (10x) en busca de ácaros rojos.",
                "Aplicar azufre mojable o aceite mineral al 1%.",
                "Liberar ácaros depredadores: Amblyseius chungas, Phytoseiulus persimilis.",
                "Control químico: spirodiclofen (0.04%) o spiromesifen (0.5-0.6 L/ha).",
                "Las poblaciones aumentan en épocas secas y calurosas."
            ],
            regla_activada="aranita_roja_completo",
            imagen="limon/aranita_roja.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"hojas_con_puntos_amarillos", "hojas_plateadas", "debilitamiento_planta", "hojas_amarillentas"} & s) >= 2),
        NOT(Diagnostico(plaga="Arañita roja de los cítricos (Panonychus citri)"))
    )
    def aranita_roja_parcial(self):
        self.declare(Diagnostico(
            plaga="Arañita roja de los cítricos (Panonychus citri) — sospecha",
            certeza=0.65,
            umbral="5-8 ácaros móviles por hoja",
            recomendaciones=[
                "Buscar ácaros rojos pequeños en el HAZ (cara superior) de hojas.",
                "Los ácaros succionan savia causando punteado amarillo.",
                "Ataques severos causan defoliación y debilitamiento del árbol.",
                "Verificar presencia de telarañas finas en hojas afectadas."
            ],
            regla_activada="aranita_roja_parcial",
            imagen="limon/aranita_roja.jpg"
        ))

    # 5. QUERESA COMA (ESCAMA PÚRPURA)

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
                "Liberar parasitoides: Aphytis lepidosaphes.",
                "Las escamas tienen forma de coma o mejillón (2-3 mm)."
            ],
            regla_activada="queresa_coma_completo",
            imagen="limon/queresa_coma.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"escamas_marrones_hojas", "hojas_amarillentas", "muerte_brotes", "debilitamiento_planta"} & s) >= 2),
        NOT(Diagnostico(plaga="Queresa coma o escama púrpura (Lepidosaphes beckii)"))
    )
    def queresa_coma_parcial(self):
        self.declare(Diagnostico(
            plaga="Queresa coma o escama púrpura (Lepidosaphes beckii) — sospecha",
            certeza=0.7,
            umbral="Más de 10 escamas por hoja",
            recomendaciones=[
                "Buscar escamas con forma de coma en hojas, ramas y frutos.",
                "Color marrón púrpura oscuro, alargadas y curvas.",
                "Se localizan preferentemente en nervadura central de hojas.",
                "Altas infestaciones causan amarillamiento y muerte de brotes."
            ],
            regla_activada="queresa_coma_parcial",
            imagen="limon/queresa_coma.jpg"
        ))

    # 6. QUERESA REDONDA DE LOS CÍTRICOS

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
                "Control químico: metidation (0.1-0.2%) o imidacloprid (140 ml/cilindro).",
                "Liberar parasitoide Aphytis roseni (1 colonia/ha).",
                "Aplicar aceite mineral al 1% en épocas de brotación.",
                "Las escamas son circulares, convexas, de color marrón oscuro."
            ],
            regla_activada="queresa_redonda_completo",
            imagen="limon/queresa_redonda.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"escamas_marrones_hojas", "frutos_con_manchas_oscuras", "debilitamiento_planta", "hojas_amarillentas"} & s) >= 2),
        NOT(Diagnostico(plaga="Queresa redonda de los cítricos (Selenaspidus articulatus)"))
    )
    def queresa_redonda_parcial(self):
        self.declare(Diagnostico(
            plaga="Queresa redonda de los cítricos (Selenaspidus articulatus) — sospecha",
            certeza=0.7,
            umbral="Más de 2 mm de diámetro por escama",
            recomendaciones=[
                "Buscar escamas circulares de 2-3 mm de diámetro en hojas y frutos.",
                "Color marrón oscuro con centro más claro (punto excéntrico).",
                "Causan manchas oscuras en frutos afectando calidad comercial.",
                "Succionan savia causando debilitamiento general del árbol."
            ],
            regla_activada="queresa_redonda_parcial",
            imagen="limon/queresa_redonda.jpg"
        ))

    # 7. PIOJO BLANCO DE LOS CÍTRICOS

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
                "Realizar podas de ventilación para reducir humedad.",
                "Las escamas blancas son alargadas con forma de pera."
            ],
            regla_activada="piojo_blanco_completo",
            imagen="limon/piojo_blanco.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"escamas_blancas_hojas", "mielada", "fumagina", "hojas_amarillentas"} & s) >= 2),
        NOT(Diagnostico(plaga="Piojo blanco de los cítricos (Pinnaspis aspidistrae)"))
    )
    def piojo_blanco_parcial(self):
        self.declare(Diagnostico(
            plaga="Piojo blanco de los cítricos (Pinnaspis aspidistrae) — sospecha",
            certeza=0.7,
            umbral="Presencia visible en más del 10% de hojas",
            recomendaciones=[
                "Buscar escamas blancas alargadas en envés de hojas.",
                "Secretan mielada que favorece desarrollo de fumagina.",
                "Se distribuyen preferentemente en ramas sombreadas.",
                "Altas infestaciones causan amarillamiento de hojas."
            ],
            regla_activada="piojo_blanco_parcial",
            imagen="limon/piojo_blanco.jpg"
        ))

    # 8. MOSCA BLANCA LANUDA DE LOS CÍTRICOS

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"moscas_blancas_envés", "mielada", "fumagina"}.issubset(s))
    )
    def mosca_blanca_lanuda_completo(self):
        self.declare(Diagnostico(
            plaga="Mosca blanca lanuda de los cítricos (Aleurothrixus floccosus)",
            certeza=1.0,
            umbral="Más de 5 ninfas por hoja",
            recomendaciones=[
                "Revisar envés de hojas en busca de ninfas con filamentos cerosos.",
                "Aplicar lavados con detergente + agua a presión.",
                "Liberar parasitoide Cales noacki (muy eficiente).",
                "Control químico: imidacloprid (0.05%) o buprofezin (200 g/200L).",
                "Las ninfas están cubiertas por cera blanca algodonosa."
            ],
            regla_activada="mosca_blanca_lanuda_completo",
            imagen="limon/mosca_blanca_lanuda.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"moscas_blancas_envés", "mielada", "fumagina", "hojas_amarillentas"} & s) >= 2),
        NOT(Diagnostico(plaga="Mosca blanca lanuda de los cítricos (Aleurothrixus floccosus)"))
    )
    def mosca_blanca_lanuda_parcial(self):
        self.declare(Diagnostico(
            plaga="Mosca blanca lanuda de los cítricos (Aleurothrixus floccosus) — sospecha",
            certeza=0.7,
            umbral="Más de 5 ninfas por hoja",
            recomendaciones=[
                "Buscar ninfas con filamentos cerosos blancos en envés de hojas.",
                "Los adultos son pequeñas moscas blancas que levantan vuelo al sacudir hojas.",
                "Secretan abundante mielada que favorece fumagina.",
                "La fumagina reduce fotosíntesis y afecta calidad de frutos."
            ],
            regla_activada="mosca_blanca_lanuda_parcial",
            imagen="limon/mosca_blanca_lanuda.jpg"
        ))

    # 9. TRIPS DE LOS CÍTRICOS

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"frutos_deformados", "frutos_plateados", "cáscara_agrietada"}.issubset(s))
    )
    def trips_citricos_completo(self):
        self.declare(Diagnostico(
            plaga="Trips de los cítricos (Scirtothrips citri)",
            certeza=1.0,
            umbral="Presencia en floración y cuajado",
            recomendaciones=[
                "Inspeccionar flores y frutos pequeños en busca de trips.",
                "Aplicar aceite agrícola al 0.5% durante floración.",
                "Control químico: spinosad (48%) 100-150 ml/200L o imidacloprid.",
                "Monitorear con trampas adhesivas azules.",
                "El daño en frutos jóvenes causa cicatrices plateadas permanentes."
            ],
            regla_activada="trips_citricos_completo",
            imagen="limon/trips.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"frutos_deformados", "frutos_plateados", "cáscara_agrietada", "frutos_decolorados"} & s) >= 2),
        NOT(Diagnostico(plaga="Trips de los cítricos (Scirtothrips citri)"))
    )
    def trips_citricos_parcial(self):
        self.declare(Diagnostico(
            plaga="Trips de los cítricos (Scirtothrips citri) — sospecha",
            certeza=0.65,
            umbral="Presencia en floración y cuajado",
            recomendaciones=[
                "Buscar pequeños insectos alargados (1-2 mm) de color amarillo pálido.",
                "Atacan flores, frutos recién cuajados y brotes tiernos.",
                "El daño aparece como plateado o bronceado en cáscara.",
                "Periodo crítico: desde floración hasta 6-8 semanas post-cuajado."
            ],
            regla_activada="trips_citricos_parcial",
            imagen="limon/trips.jpg"
        ))

    # 10. COCHINILLA ACANALADA (QUERESA BLANCA ALGODONOSA)

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: {"insectos_algodonosos", "fumagina", "hojas_amarillentas"}.issubset(s))
    )
    def cochinilla_acanalada_completo(self):
        self.declare(Diagnostico(
            plaga="Cochinilla acanalada (Icerya purchasi)",
            certeza=1.0,
            umbral="Presencia de ovisacos visibles",
            recomendaciones=[
                "Revisar ramas y tronco por ovisacos algodonosos blancos.",
                "Liberar coccinélido Rodolia cardinalis (control biológico muy eficiente).",
                "Aplicar aceite agrícola al 1% solo en focos específicos.",
                "EVITAR insecticidas de amplio espectro que afectan Rodolia.",
                "Los ovisacos son acanalados, blancos y contienen hasta 1000 huevos."
            ],
            regla_activada="cochinilla_acanalada_completo",
            imagen="limon/cochinilla_acanalada.jpg"
        ))

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        TEST(lambda s: len({"insectos_algodonosos", "fumagina", "hojas_amarillentas", "debilitamiento_planta"} & s) >= 2),
        NOT(Diagnostico(plaga="Cochinilla acanalada (Icerya purchasi)"))
    )
    def cochinilla_acanalada_parcial(self):
        self.declare(Diagnostico(
            plaga="Cochinilla acanalada (Icerya purchasi) — sospecha",
            certeza=0.75,
            umbral="Presencia de ovisacos visibles",
            recomendaciones=[
                "Buscar ovisacos blancos acanalados en ramas y tronco.",
                "Las hembras son rojizas con patas y antenas negras.",
                "Secretan abundante mielada que favorece fumagina.",
                "Rodolia cardinalis es el control biológico más efectivo del mundo."
            ],
            regla_activada="cochinilla_acanalada_parcial",
            imagen="limon/cochinilla_acanalada.jpg"
        ))

    # SIN DIAGNÓSTICO (REGLA 21)

    @Rule(
        Caso(cultivo="limon", sintomas=MATCH.s),
        NOT(Diagnostico())
    )
    def sin_diagnostico(self):
        self.declare(Diagnostico(
            plaga="Sin plaga o enfermedad identificada",
            certeza=0.0,
            umbral="N/A",
            recomendaciones=[
                "No se detectaron síntomas compatibles con plagas principales en limón.",
                "Considerar deficiencias nutricionales: N (hojas amarillas), Fe (clorosis), Zn (hojas pequeñas).",
                "Verificar condiciones de riego: exceso causa pudrición de raíces, déficit causa estrés.",
                "Evaluar pH del suelo: limón prefiere pH 5.5-6.5.",
                "Consultar con especialista en cítricos para diagnóstico detallado.",
                "Considerar análisis foliar y de suelo para detectar deficiencias.",
                "Revisar la guía técnica de plagas en cítricos (Carrillo, 2020)."
            ],
            regla_activada="sin_diagnostico",
            imagen=None
        ))