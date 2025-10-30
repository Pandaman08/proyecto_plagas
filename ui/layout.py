import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

# ───────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS
# ───────────────────────────────────────────────
def inject_custom_css():
    st.markdown("""
    <style>
    /* Fuente principal */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Encabezado principal */
    .main-header {
        text-align: center;
        color: #1b5e20;
        margin-bottom: 5px;
    }
    .main-subheader {
        text-align: center;
        color: #388e3c;
        font-size: 1.1em;
        margin-bottom: 25px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        color: #000000;
        background-color: #f1f8e9;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] h2 {
        color: #2e7d32;
        font-weight: 600;
        text-transform: uppercase;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #000000;
        font-weight: 600;
    }

    /* Botones */
    .stButton>button {
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #388e3c;
        color: white;
    }

    /* Tarjetas de diagnóstico */
    .diagnostic-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 20px;
        border-left: 4px solid #4caf50;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.9em;
        border-top: 1px solid #eee;
        margin-top: 40px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

# ───────────────────────────────────────────────
# CONFIGURACIÓN DE CULTIVOS Y SÍNTOMAS
# ───────────────────────────────────────────────
CULTIVOS = {
    #tatito uwu
    "Limon": {
        "sintomas": [
            # Daños en hojas
            "hojas_enrolladas",
            "hojas_plateadas",
            "hojas_amarillentas",
            "hojas_deformadas",
            "hojas_con_minas_serpentinas",
            "hojas_con_puntos_amarillos",
            "hojas_con_manchas_negras",
        
            # Presencia de insectos/ácaros
            "escamas_blancas_hojas",
            "escamas_marrones_hojas",
            "insectos_algodonosos",
            "moscas_blancas_envés",
            "pulgones_brotes",
        
            # Secreciones
            "mielada",
            "fumagina",
            
            # Daños en frutos
            "frutos_decolorados",
            "frutos_con_manchas_oscuras",
            "frutos_plateados",
            "frutos_deformados",
            "frutos_pequeños",
            "cáscara_agrietada",
            
            # Daños en ramas/tronco
            "escamas_tronco",
            "debilitamiento_planta",
            "muerte_brotes"
        ],
        "descripcion": "Carrillo, P. S. C. (2020). Insectos y ácaros plagas de cítricos con énfasis en el cultivo de limón sutil. Editorial Académica Española."
    },
    "Piña": {
        "sintomas": [
            "marchitez",
            "enrojecimiento_foliar",
            "raices_dañadas",
            "retraso_crecimiento",
            "colonias_algodonosas",
            "enrollamiento_hojas",
            "hormigas"
        ],
        "descripcion": "Diagnóstico basado en la Guía SENASA (2020) para el cultivo de piña."
    },
    "Palta": {"sintomas": ["manchas_folares", "caida_prematura", "frutos_manchados"], "descripcion": "Próximamente disponible."},
    "Pitahaya": {"sintomas": ["clorosis", "necrosis", "deformacion_fruto"], "descripcion": "Próximamente disponible."},
    "Café": {"sintomas": ["ojos_de_gallo", "roya", "broca"], "descripcion": "Próximamente disponible."},
    "Cacao": {"sintomas": ["monilia", "escoba_de_bruja", "mal_de_macho"], "descripcion": "Próximamente disponible."},
    "Papa": {"sintomas": ["tizón_tardio", "nematodos", "pulgones"], "descripcion": "Próximamente disponible."},
    "Arroz": {"sintomas": ["hoja_blanca", "piricularia", "gusano_cogollero"], "descripcion": "Próximamente disponible."},
     "Uva": {
        "sintomas": [
            "verrugas_hojas",
            "nudosidades_raices",
            "hojas_gris_plomizo",
            "tejido_araña",
            "brotacion_lenta",
            "hojas_abarquilladas",
            "picaduras_racimos",
            "aves_presentes",
            "bayas_vacias",
            "avispa_presencia",
            "racimos_consumidos",
            "madrigueras",
            "hojas_consumidas",
            "gusano_grande",
            "plantas_debiles",
            "nódulos_redondeados_raíz",
            "polvillo_blanco",
            "aborto_flores",
            "moho_gris",
            "racimos_podridos",
            "agallas_tallo",
            "plantas_pequeñas",
            "clorosis_hojas",
            "crecimiento_lento",
            "hojas_marchitas",
            "suelo_seco",
            "hojas_amarrillentas",
            "raíces_dañadas",
            "flores_no_cuajan",
            "temperatura_alta",
            "racimos_desiguales",
            "poda_inadecuada"
        ],
        "descripcion": "Diagnóstico basado en el Manual Regional Sur - Control de Plagas y Enfermedades en el Cultivo de la Vid (desco, 2004)."
    },
    
}

# ───────────────────────────────────────────────
# FUNCIÓN PRINCIPAL DE LA INTERFAZ
# ───────────────────────────────────────────────
def mostrar_interfaz():
    inject_custom_css()

    # Encabezado
    st.markdown('<h1 class="main-header">🌱 Sistema Experto en Plagas Agrícolas</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subheader">Diagnóstico técnico basado en guías oficiales</p>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("🧭 Navegación")
    cultivo_seleccionado = st.sidebar.selectbox(
        "Seleccione un cultivo:",
        options=list(CULTIVOS.keys())
    )

    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Consejo**: Seleccione todos los síntomas observables en el campo para un diagnóstico preciso.")

    # Cuerpo principal
    info = CULTIVOS[cultivo_seleccionado]
    st.subheader(f"🪴 {cultivo_seleccionado}")
    st.caption(info["descripcion"])

    if cultivo_seleccionado == "Piña":
        mostrar_diagnostico_piña()
    elif cultivo_seleccionado == "Uva":
        mostrar_diagnostico_uva()
    elif cultivo_seleccionado == "Limon":
        mostrar_diagnostico_limon()
    else:
        st.info(f"El módulo de diagnóstico para **{cultivo_seleccionado}** estará disponible en una próxima actualización.")
        st.image("https://placehold.co/600x200/e8f5e9/2e7d32?text=Próximamente", use_column_width=True)

    # Pie de página
    st.markdown("""
    <div class="footer">
        Desarrollado con fines académicos • Universidad Nacional de Trujillo
    </div>
    """, unsafe_allow_html=True)

# ───────────────────────────────────────────────
# INTERFAZ ESPECÍFICA PARA PIÑA
# ───────────────────────────────────────────────
def mostrar_diagnostico_piña():
    sintomas_disponibles = CULTIVOS["Piña"]["sintomas"]
    
    with st.expander("🔍 Guía de síntomas observables", expanded=False):
        st.markdown("""
        - **marchitez**: pérdida de turgencia en hojas.
        - **enrojecimiento_foliar**: coloración rojiza en hojas adultas.
        - **raices_dañadas**: raíces cortadas, mordidas o con tejido necrótico.
        - **colonias_algodonosas**: masa blanca algodonosa en base de hojas/frutos.
        - **hormigas**: presencia activa de hormigas en la base de la planta.
        """)

    seleccion = st.multiselect(
        "Seleccione los síntomas observados en el campo:",
        options=sintomas_disponibles,
        default=[]
    )

    if st.button("🔍 Diagnosticar Plaga"):
        if not seleccion:
            st.warning("⚠️ Por favor, seleccione al menos un síntoma.")
            return

        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("piña", seleccion)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        diagnosticos = resultado["diagnosticos"]
        if not diagnosticos:
            st.warning("❌ No se encontró un diagnóstico compatible con los síntomas ingresados.")
            return

        # Mostrar diagnóstico principal
        diag = diagnosticos[0]
        st.markdown(f"""
        <div class="diagnostic-card">
            <h3>✅ Diagnóstico: {diag['plaga']}</h3>
            <p><strong>Certeza:</strong> {int(diag['certeza'] * 100)}%</p>
            <p><strong>Umbral de daño económico:</strong> {diag['umbral']}</p>
            <p><strong>Recomendaciones:</strong></p>
            <ul>
                {''.join(f'<li>{r}</li>' for r in diag['recomendaciones'])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Gráfico de certeza
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=diag['certeza'] * 100,
            title={'text': "Nivel de Confianza"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4caf50"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffcdd2"},
                    {'range': [50, 80], 'color': "#a5d6a7"},
                    {'range': [80, 100], 'color': "#4caf50"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Diagnósticos secundarios (si existen)
        if len(diagnosticos) > 1:
            with st.expander("📋 Diagnósticos alternativos", expanded=False):
                for d in diagnosticos[1:]:
                    if d['certeza'] > 0.5:
                        st.write(f"- **{d['plaga']}** (certeza: {int(d['certeza']*100)}%)")

        # Trazabilidad
        with st.expander("🔍 Trazabilidad de la inferencia", expanded=False):
            st.write("**Reglas activadas:**")
            for r in resultado["reglas_activadas"]:
                st.code(r, language="python")

# ───────────────────────────────────────────────
# INTERFAZ ESPECÍFICA PARA UVA
# ───────────────────────────────────────────────
def mostrar_diagnostico_uva():
    sintomas_disponibles = CULTIVOS["Uva"]["sintomas"]
    
    with st.expander("🔍 Guía de síntomas observables", expanded=False):
        st.markdown("""
        - **verrugas_hojas**: protuberancias en la cara superior de las hojas.
        - **nudosidades_raices**: deformaciones en raíces.
        - **hojas_gris_plomizo**: coloración grisácea.
        - **tejido_araña**: telarañas en hojas.
        - **brotacion_lenta**: desarrollo tardío de brotes.
        - **hojas_abarquilladas**: hojas enrolladas.
        - **picaduras_racimos**: marcas en bayas.
        - **aves_presentes**: presencia de palomas o cuculíes.
        - **bayas_vacias**: solo piel de baya.
        - **avispa_presencia**: avispas volando alrededor de racimos.
        - **racimos_consumidos**: racimos comidos.
        - **madrigueras**: hoyos en el suelo.
        - **hojas_consumidas**: hojas devoradas.
        - **gusano_grande**: larva de 6-8 cm con cuerno.
        - **plantas_debiles**: crecimiento pobre.
        - **nódulos_redondeados_raíz**: bultos redondos en raíces.
        - **polvillo_blanco**: polvo ceniciento en hojas/racimos.
        - **aborto_flores**: flores caen sin cuajar.
        - **moho_gris**: moho en racimos.
        - **racimos_podridos**: frutos pudridos.
        - **agallas_tallo**: tumores en cuello de planta.
        - **plantas_pequeñas**: tamaño reducido.
        - **clorosis_hojas**: amarilleamiento.
        - **crecimiento_lento**: desarrollo bajo.
        - **hojas_marchitas**: pérdida de turgencia.
        - **suelo_seco**: falta de humedad.
        - **hojas_amarrillentas**: color amarillo.
        - **raíces_dañadas**: raíces cortadas o necróticas.
        - **flores_no_cuajan**: sin fruto.
        - **temperatura_alta**: calor extremo.
        - **racimos_desiguales**: tamaño irregular.
        - **poda_inadecuada**: poda excesiva o nula.
        """)

    seleccion = st.multiselect(
        "Seleccione los síntomas observados en el campo:",
        options=sintomas_disponibles,
        default=[]
    )

    if st.button("🔍 Diagnosticar Plaga"):
        if not seleccion:
            st.warning("⚠️ Por favor, seleccione al menos un síntoma.")
            return

        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("uva", seleccion)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        diagnosticos = resultado["diagnosticos"]
        if not diagnosticos:
            st.warning("❌ No se encontró un diagnóstico compatible con los síntomas ingresados.")
            return

        # Mostrar diagnóstico principal
        diag = diagnosticos[0]
        st.markdown(f"""
        <div class="diagnostic-card">
            <h3>✅ Diagnóstico: {diag['plaga']}</h3>
            <p><strong>Certeza:</strong> {int(diag['certeza'] * 100)}%</p>
            <p><strong>Umbral de daño económico:</strong> {diag['umbral']}</p>
            <p><strong>Recomendaciones:</strong></p>
            <ul>
                {''.join(f'<li>{r}</li>' for r in diag['recomendaciones'])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar imagen si existe
        if diag.get("imagen"):
            try:
                st.image(f"images/{diag['imagen']}", caption=f"Imagen de {diag['plaga']}", use_column_width=True)
            except Exception:
                st.warning("Imagen no disponible. Asegúrese de tener la carpeta 'images' con el archivo correspondiente.")

        # Gráfico de certeza
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=diag['certeza'] * 100,
            title={'text': "Nivel de Confianza"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4caf50"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffcdd2"},
                    {'range': [50, 80], 'color': "#a5d6a7"},
                    {'range': [80, 100], 'color': "#4caf50"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Diagnósticos secundarios (si existen)
        if len(diagnosticos) > 1:
            with st.expander("📋 Diagnósticos alternativos", expanded=False):
                for d in diagnosticos[1:]:
                    st.write(f"- **{d['plaga']}** (certeza: {int(d['certeza']*100)}%)")

        # Trazabilidad
        with st.expander("🔍 Trazabilidad de la inferencia", expanded=False):
            st.write("**Reglas activadas:**")
            for r in resultado["reglas_activadas"]:
                st.code(r, language="python")

# ───────────────────────────────────────────────
# INTERFAZ ESPECÍFICA PARA LIMÓN CON CARRUSEL COMPACTO
# ───────────────────────────────────────────────
def mostrar_diagnostico_limon():
    sintomas_disponibles = CULTIVOS["Limon"]["sintomas"]

    # Inicializar el estado de la página si no existe
    if 'pagina_actual' not in st.session_state:
        st.session_state.pagina_actual = 0

    # Mostramos imágenes y descripciones de síntomas en carrusel
    with st.expander("🔍 Guía de síntomas observables", expanded=True):
        sintomas_info = {
            # Daños en hojas
            "hojas_enrolladas": "Hojas retorcidas o encrespadas, típicamente por pulgones o ácaros.",
            "hojas_plateadas": "Apariencia plateada o blanquecina en el haz, causada por ácaro del tostado.",
            "hojas_amarillentas": "Clorosis general, puede indicar queresas o moscas blancas.",
            "hojas_deformadas": "Hojas distorsionadas, arrugadas o con crecimiento anormal.",
            "hojas_con_minas_serpentinas": "Túneles serpenteantes plateados, daño de minador de hojas.",
            "hojas_con_puntos_amarillos": "Pequeños puntos amarillos dispersos por alimentación de ácaros.",
            "hojas_con_manchas_negras": "Manchas oscuras o negras, posible fumagina asociada a insectos chupadores.",
            
            # Presencia de insectos/ácaros
            "escamas_blancas_hojas": "Costras blancas en hojas, piojos blancos o queresas.",
            "escamas_marrones_hojas": "Escamas marrones circulares o alargadas, queresas diaspididas.",
            "insectos_algodonosos": "Masas blancas algodonosas, cochinilla harinosa o acanalada.",
            "moscas_blancas_envés": "Pequeños insectos blancos voladores en envés de hojas.",
            "pulgones_brotes": "Colonias de pulgones verdes, negros o marrones en brotes tiernos.",
            
            # Secreciones
            "mielada": "Sustancia pegajosa brillante en hojas/ramas, producida por insectos chupadores.",
            "fumagina": "Hongo negro hollín sobre mielada, reduce fotosíntesis.",
            
            # Daños en frutos
            "frutos_decolorados": "Frutos con manchas amarillas, grises o marrones.",
            "frutos_con_manchas_oscuras": "Manchas negras o marrones en cáscara, por queresas o ácaros.",
            "frutos_plateados": "Área plateada o bronceada en frutos por ácaro del tostado.",
            "frutos_deformados": "Frutos con forma irregular o desarrollo asimétrico.",
            "frutos_pequeños": "Frutos más pequeños de lo normal, por estrés de plagas.",
            "cáscara_agrietada": "Grietas superficiales en cáscara por daño temprano de ácaros.",
            
            # Daños en ramas/tronco
            "escamas_tronco": "Costras marrones o blancas en tronco y ramas principales.",
            "debilitamiento_planta": "Pérdida de vigor general, amarillamiento progresivo.",
            "muerte_brotes": "Brotes secos o muertos, por queresas o moscas blancas severas."
        }

        # Configuración del carrusel
        items_por_pagina = 3
        total_sintomas = len(sintomas_disponibles)
        total_paginas = (total_sintomas + items_por_pagina - 1) // items_por_pagina
        
        # Calcular índices para la página actual
        inicio = st.session_state.pagina_actual * items_por_pagina
        fin = min(inicio + items_por_pagina, total_sintomas)
        sintomas_pagina = sintomas_disponibles[inicio:fin]

        # Mostrar imágenes de la página actual con altura reducida
        cols = st.columns(3)
        for i, sintoma in enumerate(sintomas_pagina):
            with cols[i]:
                ruta_imagen = f"images/limon/sintomas/{sintoma}.jpg"
                try:
                    st.image(ruta_imagen, use_container_width=True)
                    st.markdown(f"""
                        <div style='margin-top: -10px; margin-bottom: 5px;'>
                            <p style='font-size: 0.9em; font-weight: 600; margin-bottom: 3px;'>
                                🟢 {sintoma.replace('_',' ').capitalize()}
                            </p>
                            <p style='font-size: 0.75em; color: #666; line-height: 1.3; margin: 0;'>
                                {sintomas_info.get(sintoma, "Descripción no disponible.")}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception:
                    st.warning(f"⚠️ {sintoma.replace('_',' ').capitalize()}")

        # Controles de navegación del carrusel - MÁS COMPACTOS
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if st.button("⬅️", disabled=(st.session_state.pagina_actual == 0), use_container_width=True, key="prev_btn"):
                st.session_state.pagina_actual -= 1
                st.rerun()
        
        with col_info:
            st.markdown(f"""
                <div style='text-align: center; padding: 2px; font-size: 0.85em; color: #555;'>
                    Página {st.session_state.pagina_actual + 1} de {total_paginas}
                </div>
            """, unsafe_allow_html=True)
        
        with col_next:
            if st.button("➡️", disabled=(st.session_state.pagina_actual >= total_paginas - 1), use_container_width=True, key="next_btn"):
                st.session_state.pagina_actual += 1
                st.rerun()

    # Selector de síntomas
    seleccion = st.multiselect(
        "Seleccione los síntomas observados en el campo:",
        options=sintomas_disponibles,
        default=[]
    )

    # Botón de diagnóstico
    if st.button("🔍 Diagnosticar Plaga"):
        if not seleccion:
            st.warning("⚠️ Por favor, seleccione al menos un síntoma.")
            return

        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("limon", seleccion)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        diagnosticos = resultado["diagnosticos"]
        if not diagnosticos:
            st.warning("❌ No se encontró un diagnóstico compatible con los síntomas ingresados.")
            return

        diag = diagnosticos[0]
        st.markdown(f"""
        <div class="diagnostic-card">
            <h3>✅ Diagnóstico: {diag['plaga']}</h3>
            <p><strong>Certeza:</strong> {int(diag['certeza'] * 100)}%</p>
            <p><strong>Umbral de daño económico:</strong> {diag['umbral']}</p>
            <p><strong>Recomendaciones:</strong></p>
            <ul>
                {''.join(f'<li>{r}</li>' for r in diag['recomendaciones'])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Gráfico de certeza
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=diag['certeza'] * 100,
            title={'text': "Nivel de Confianza"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4caf50"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffcdd2"},
                    {'range': [50, 80], 'color': "#a5d6a7"},
                    {'range': [80, 100], 'color': "#4caf50"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Diagnósticos secundarios (si existen)
        if len(diagnosticos) > 1:
            with st.expander("📋 Diagnósticos alternativos", expanded=False):
                for d in diagnosticos[1:]:
                    if d['certeza'] > 0.5:
                        st.write(f"- **{d['plaga']}** (certeza: {int(d['certeza']*100)}%)")

        # Trazabilidad
        with st.expander("🔍 Trazabilidad de la inferencia", expanded=False):
            st.write("**Reglas activadas:**")
            for r in resultado["reglas_activadas"]:
                st.code(r, language="python")