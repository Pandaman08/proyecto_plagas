import streamlit as st
from ui.palta_interfaz import mostrar_diagnostico_palta
from ui.piña_interfaz import mostrar_diagnostico_piña
from ui.uva_interfaz import mostrar_diagnostico_uva
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
        color: #000000;
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
    "Palta": {
        "sintomas": [
            # PLAGAS - Trips
            "raspado_frutos", "rugosidad_frutos", "bronceado_frutos", "deformacion_frutos",
            # PLAGAS - Arañita Roja
            "tostado_hojas", "hojas_rojizas", "perdida_clorofila", "defoliacion_prematura",
            # PLAGAS - Mosca Blanca
            "perforacion_brotes", "fumagina", "debilitamiento_planta", "hojas_pegajosas",
            # ENFERMEDADES - Tristeza
            "hojas_amarillas", "defoliacion", "raices_necrosadas", "frutos_pequenos", "muerte_regresiva",
            # ENFERMEDADES - Brazo Negro
            "cancros_tronco", "exudados_blancos", "muerte_ramas", "pudricion_frutos_pedunculo",
            # ENFERMEDADES - Sunblotch
            "manchas_amarillas_fruto", "variegado_hojas", "moteado_hojas", "crecimiento_horizontal", "corteza_facil_desprender"
        ],
        "descripcion": "Diagnóstico basado en la Guía PortalFruticola (2023) para el cultivo de palta."
    },
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
        mostrar_diagnostico_piña(CULTIVOS)
    elif cultivo_seleccionado == "Uva":
        mostrar_diagnostico_uva(CULTIVOS)
    elif cultivo_seleccionado == "Palta":
        mostrar_diagnostico_palta(CULTIVOS)
    else:
        st.info(f"El módulo de diagnóstico para **{cultivo_seleccionado}** estará disponible en una próxima actualización.")
        st.image("https://placehold.co/600x200/e8f5e9/2e7d32?text=Próximamente", use_column_width=True)

    # Pie de página
    st.markdown("""
    <div class="footer">
        Desarrollado con fines académicos • Universidad Nacional de Trujillo
    </div>
    """, unsafe_allow_html=True)

