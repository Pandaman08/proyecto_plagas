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