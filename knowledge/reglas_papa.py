from experta import *
from knowledge.hechos import Caso, Diagnostico


class ReglasPapa(KnowledgeEngine):
    """
    Sistema experto para diagnóstico de plagas en cultivo de papa.
    Basado en el conjunto de síntomas seleccionados por el usuario.
    """

    # === 1. Pulgón de la papa (Myzus persicae)
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_pulgon(self, sintomas):
        if "hojas_enrolladas" in sintomas and "hojas_amarillentas" in sintomas:
            self.declare(Diagnostico(
                plaga="Pulgón de la papa (Myzus persicae)",
                imagen="papa/pulgon.jpg",
                certeza=0.9,
                descripcion="Insecto chupador que extrae savia, provocando hojas amarillentas y enrolladas.",
                recomendaciones=["Aplicar insecticida biológico (neem o jabón potásico) y eliminar hojas infestadas."],
                razon="El enrollamiento y amarilleo de hojas es característico de la succión de savia.",
                regla_activada="plaga_pulgon"
            ))

    # === 2. Polilla de la papa (Phthorimaea operculella)
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_polilla(self, sintomas):
        if "tuneles_en_hojas" in sintomas and "larvas_presentes" in sintomas:
            self.declare(Diagnostico(
                plaga="Polilla de la papa (Phthorimaea operculella)",
                imagen="papa/polilla.jpg",
                certeza=0.9,
                descripcion="Las larvas excavan galerías en hojas y tubérculos, generando pérdidas en almacenamiento.",
                recomendaciones=["Usar trampas con feromonas y eliminar hojas afectadas."],
                razon="La presencia de túneles y larvas es típica de la polilla.",
                regla_activada="plaga_polilla"
            ))

    # === 3. Gusano alambre (Agriotes spp.)
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_gusano_alambre(self, sintomas):
        if "raices_perforadas" in sintomas and "tuberculos_huecos" in sintomas:
            self.declare(Diagnostico(
                plaga="Gusano alambre (Agriotes spp.)",
                imagen="papa/gusano_alambre.jpg",
                certeza=0.6,
                descripcion="Larvas de escarabajos que perforan raíces y tubérculos, afectando el crecimiento.",
                recomendaciones=["Rotar cultivos y usar trampas con trozos de papa enterrados."],
                razon="Los orificios profundos en tubérculos indican gusano alambre.",
                regla_activada="plaga_gusano_alambre"
            ))

    # === 4. Nematodo dorado
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_nematodo_dorado(self, sintomas):
        if "plantas_debilitadas" in sintomas and "manchas_amarillas" in sintomas:
            self.declare(Diagnostico(
                plaga="Nematodo dorado (Globodera rostochiensis)",
                imagen="papa/nematodo_dorado.jpg",
                certeza=0.9,
                descripcion="Nematodos microscópicos que atacan raíces, formando manchas amarillas.",
                recomendaciones=["Aplicar solarización y sembrar variedades resistentes."],
                razon="Las manchas amarillas y el debilitamiento indican nematodo dorado.",
                regla_activada="plaga_nematodo_dorado"
            ))

    # === 5. Mosca minadora
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_mosca_minadora(self, sintomas):
        if "hojas_con_galerias" in sintomas and "insectos_pequenos_negros" in sintomas:
            self.declare(Diagnostico(
                plaga="Mosca minadora (Liriomyza huidobrensis)",
                imagen="papa/mosca_minadora.jpg",
                certeza=0.6,
                descripcion="Las larvas excavan galerías en el mesófilo de las hojas, reduciendo fotosíntesis.",
                recomendaciones=["Eliminar hojas afectadas y aplicar extracto de ajo o neem." ],
                razon="Las galerías visibles son síntoma clásico de mosca minadora.",
                regla_activada="plaga_mosca_minadora"
            ))

    # === 6. Gorgojo andino
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_gorgojo_andino(self, sintomas):
        if "tallos_perforados" in sintomas and "tuberculos_danados" in sintomas:
            self.declare(Diagnostico(
                plaga="Gorgojo andino (Premnotrypes spp.)",
                imagen="papa/gorgojo_andino.png",
                certeza=0.9,
                descripcion="Escarabajo que daña tallos y tubérculos. Las larvas excavan galerías internas.",
                recomendaciones=["Usar trampas con feromonas y control biológico (Beauveria bassiana)." ],
                razon="El daño en tallos y tubérculos es típico del gorgojo andino.",
                regla_activada="plaga_gorgojo_andino"
            ))

    # === 7. Trips
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_trips(self, sintomas):
        if "hojas_plateadas" in sintomas and "insectos_pequenos" in sintomas:
            self.declare(Diagnostico(
                plaga="Trips",
                imagen="papa/trips.jpg",
                certeza=0.6,
                descripcion="Insectos diminutos que raspan hojas, provocando decoloración plateada.",
                recomendaciones=["Aplicar extracto de ajo o jabón potásico."  ],
                razon="Las hojas plateadas y deformes se asocian al ataque de trips.",
                regla_activada="plaga_trips"
            ))

    # === 8. Ácaros
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_acaros(self, sintomas):
        if "hojas_arrugadas" in sintomas and "polvo_fino_blanco" in sintomas:
            self.declare(Diagnostico(
                plaga="Ácaros",
                imagen="papa/acaros.jpg",
                certeza=0.9,
                descripcion="Provocan arrugamiento de hojas y polvo blanco en su superficie.",
                recomendaciones=["Aplicar azufre mojable o acaricidas naturales."   ],
                razon="El polvo blanco y hojas arrugadas son señales de ácaros.",
                regla_activada="plaga_acaros"
            ))

    # === 9. Escarabajo de la papa
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_escarabajo(self, sintomas):
        if "hojas_devoradas" in sintomas and "insectos_amarillos_negros" in sintomas:
            self.declare(Diagnostico(
                plaga="Escarabajo de la papa (Leptinotarsa decemlineata)",
                imagen="papa/escarabajo.jpg",
                certeza=0.9,
                descripcion="Escarabajo rayado que devora completamente el follaje.",
                recomendaciones=["Recolectar manualmente y aplicar Bacillus thuringiensis." ],
                razon="Los escarabajos rayados amarillos y negros son característicos.",
                regla_activada="plaga_escarabajo"
            ))

    # === 10. Gusano cortador
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_gusano_cortador(self, sintomas):
        if "tallos_cortados" in sintomas and "plantas_caidas" in sintomas:
            self.declare(Diagnostico(
                plaga="Gusano cortador (Agrotis spp.)",
                imagen="papa/gusano_cortador.jpg",
                certeza=0.6,
                descripcion="Corta tallos jóvenes al nivel del suelo, afectando brotes.",
                recomendaciones=["Eliminar larvas y aplicar ceniza alrededor del tallo."],
                razon="El corte de tallos jóvenes indica gusano cortador.",
                regla_activada="plaga_gusano_cortador"
            ))

    # === 11. Mosca blanca
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_mosca_blanca(self, sintomas):
        if "hojas_amarillas" in sintomas and "insectos_mosca_blanca" in sintomas:
            self.declare(Diagnostico(
                plaga="Mosca blanca",
                imagen="papa/mosca_blanca.jpg",
                certeza=0.9,
                descripcion="Insectos que se alimentan de savia y excretan melaza, generando fumagina.",
                recomendaciones=["Aplicar trampas amarillas y extractos naturales repelentes."],
                razon="La presencia de moscas blancas en el envés de las hojas lo confirma.",
                regla_activada="plaga_mosca_blanca"
            ))

    # === 12. Minador del tubérculo
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_minador_tuberculo(self, sintomas):
        if "tuberculos_con_galerias" in sintomas and "larvas_internas" in sintomas:
            self.declare(Diagnostico(
                plaga="Minador del tubérculo",
                imagen="papa/minador_tuberculo.jpg",
                certeza=0.6,
                descripcion="Larvas que excavan galerías dentro de los tubérculos.",
                recomendaciones=["Eliminar tubérculos afectados y ventilar el almacenamiento."],
                razon="Las galerías internas son signo clásico de minador del tubérculo.",
                regla_activada="plaga_minador_tuberculo"
            ))

    # === 13. Gusano blanco
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_gusano_blanco(self, sintomas):
        if "suelo_humedo" in sintomas and "raices_mascadas" in sintomas:
            self.declare(Diagnostico(
                plaga="Gusano blanco",
                imagen="papa/gusano_blanco.jpg",
                certeza=0.6,
                descripcion="Larvas que mastican raíces en suelos húmedos.",
                recomendaciones=["Arar profundamente y usar hongos entomopatógenos."],
                razon="Las raíces mascadas en suelos húmedos indican gusano blanco.",
                regla_activada="plaga_gusano_blanco"
            ))

    # === 14. Nematodo del tallo
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_nematodo_tallo(self, sintomas):
        if "tallos_deformados" in sintomas and "hojas_abolladas" in sintomas:
            self.declare(Diagnostico(
                plaga="Nematodo del tallo",
                imagen="papa/nematodo_tallo.jpg",
                certeza=0.6,
                descripcion="Nematodo que deforma tallos y hojas.",
                recomendaciones=["Usar material de siembra certificado y solarizar el suelo."],
                razon="Los tallos deformes y hojas abolladas son típicos del nematodo del tallo.",
                regla_activada="plaga_nematodo_tallo"
            ))

    # === 15. Gusano rosado
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_gusano_rosado(self, sintomas):
        if "tuberculos_decolorados" in sintomas and "larvas_rosadas" in sintomas:
            self.declare(Diagnostico(
                plaga="Gusano rosado",
                imagen="papa/gusano_rosado.jpg",
                certeza=0.9,
                descripcion="Larvas rosadas que dañan los tubérculos, dejándolos blandos.",
                recomendaciones=["Eliminar tubérculos dañados y usar trampas luminosas."],
                razon="Las larvas rosadas son distintivas de esta plaga.",
                regla_activada="plaga_gusano_rosado"
            ))

    # === 16. Grillo topo
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_grillo_topo(self, sintomas):
        if "suelo_agrietado" in sintomas and "raices_mordidas" in sintomas:
            self.declare(Diagnostico(
                plaga="Grillo topo",
                imagen="papa/grillo_topo.jpg",
                certeza=0.6,
                descripcion="Insecto subterráneo que daña raíces al alimentarse de noche.",
                recomendaciones=["Usar trampas con agua y luz, mantener suelo húmedo."],
                razon="El suelo removido y agrietado indica presencia de grillo topo.",
                regla_activada="plaga_grillo_topo"
            ))

    # === 17. Gusano gris
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_gusano_gris(self, sintomas):
        if "tallos_mordidos" in sintomas and "ataque_nocturno" in sintomas:
            self.declare(Diagnostico(
                plaga="Gusano gris",
                imagen="papa/gusano_gris.jpg",
                certeza=0.9,
                descripcion="Larvas nocturnas que cortan tallos durante la noche.",
                recomendaciones=["Aplicar Bacillus thuringiensis o control manual nocturno."],
                razon="El ataque nocturno y mordidas confirman gusano gris.",
                regla_activada="plaga_gusano_gris"
            ))

    # === 18. Pulgón verde
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_pulgon_verde(self, sintomas):
        if "hojas_curvadas" in sintomas and "insectos_verdes" in sintomas:
            self.declare(Diagnostico(
                plaga="Pulgón verde",
                imagen="papa/pulgon_verde.jpg",
                certeza=0.6,
                descripcion="Variante del pulgón común, de color verde, transmisor de virus.",
                recomendaciones=["Aplicar jabón potásico o extracto de tabaco diluido."],
                razon="Los pulgones verdes curvan hojas por succión de savia.",
                regla_activada="plaga_pulgon_verde"
            ))

    # === 19. Caracoles o babosas
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_caracoles(self, sintomas):
        if "hojas_mordidas" in sintomas and "rastro_baboso" in sintomas:
            self.declare(Diagnostico(
                plaga="Caracoles o babosas",
                imagen="papa/caracoles.jpg",
                certeza=0.6,
                descripcion="Moluscos que raspan hojas y dejan rastros de baba brillante.",
                recomendaciones=["Colocar trampas de cerveza o aplicar cal alrededor."],
                razon="El rastro baboso brillante indica presencia de babosas.",
                regla_activada="plaga_caracoles"
            ))

    # === 20. Tizón tardío
    @Rule(Caso(cultivo='papa', sintomas=MATCH.sintomas))
    def plaga_tizon_tardio(self, sintomas):
        if "hojas_manchas_negras" in sintomas and "clima_humedo" in sintomas:
            self.declare(Diagnostico(
                plaga="Tizón tardío (Phytophthora infestans)",
                imagen="papa/tizon_tardio.png",
                certeza=0.9,
                descripcion="Hongo agresivo que provoca manchas negras y necrosis en hojas.",
                recomendaciones=["Aplicar fungicidas preventivos y eliminar hojas infectadas."],
                razon="Las manchas negras en clima húmedo son signo de tizón tardío.",
                regla_activada="plaga_tizon_tardio"
            ))
