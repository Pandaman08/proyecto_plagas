import streamlit as st
from ui.palta_interfaz import mostrar_diagnostico_palta
from ui.piña_interfaz import mostrar_diagnostico_piña
from ui.uva_interfaz import mostrar_diagnostico_uva
from ui.limon_interfaz import mostrar_diagnostico_limon
from ui.cafe_interfaz import mostrar_diagnostico_cafe
from ui.cacao_interfaz import mostrar_diagnostico_cacao
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

    /* Sidebar - usa variable de Streamlit */
    [data-testid="stSidebar"] {
        color: var(--textColor);
        background-color: var(--secondaryBackgroundColor);
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
        color: var(--textColor);
        font-weight: 600;
    }

    /* Botones - usa primaryColor */
    .stButton>button {
        background-color: var(--primaryColor);
        color: #2e7d32;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #388e3c; /* Puedes ajustar este hover si quieres mantenerlo fijo */
        color: white;
    }

    /* Tarjetas de diagnóstico */
    .diagnostic-card {
        color: var(--textColor);
        background: var(--backgroundColor);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 20px;
        border-left: 4px solid var(--primaryColor);
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

    /* Modo oscuro: ajusta colores específicos si es necesario */
    @media (prefers-color-scheme: dark) {
        .main-header {
            color: #bbdefb;
        }
        .main-subheader {
            color: #81c784;
        }
        .footer {
            color: #aaa;
            border-top: 1px solid #444;
        }
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
    "Palta": {
        "sintomas": [            
            # 1. Trips del Palto (4 síntomas)
            "raspado_frutos",
            "rugosidad_frutos",
            "bronceado_frutos",
            "deformacion_frutos",
            
            # 2. Arañita Roja/Marrón (5 síntomas)
            "tostado_hojas",
            "hojas_rojizas",
            "perdida_clorofila",
            "bronceado_hojas",
            "defoliacion_prematura",
            
            # 3. Mosca Blanca de los Brotes (4 síntomas)
            "perforacion_brotes",
            "fumagina",
            "debilitamiento_planta",
            "hojas_pegajosas",
            
            # 4. Queresas Fiorinia (3 síntomas)
            "escamas_marron_frutos",
            "escamas_marron_hojas",
            "secamiento_hojas",
            
            # 5. Queresas Hemiberlesia (2 síntomas)
            "escamas_blancas_pedunculo",
            "escamas_circulares_frutos",
            
            # 6. Mosca Blanca Espiral (3 síntomas)
            "espirales_cera_hojas",
            "huevos_desordenados_enves",
            "cobertura_cera_hojas",
            
            # 7. Bicho del Cesto (3 síntomas)
            "cestos_colgantes_hojas",
            "raspado_epidermis_hojas",
            "larvas_con_refugio",
            
            # 8. Tristeza del Palto (5 síntomas)
            "hojas_amarillas",
            "defoliacion",
            "raices_necrosadas",
            "frutos_pequenos",
            "muerte_regresiva",
            
            # 9. Brazo Negro (4 síntomas)
            "cancros_tronco",
            "exudados_blancos",
            "muerte_ramas",
            "pudricion_frutos_pedunculo",
            
            # 10. Sunblotch (5 síntomas)
            "manchas_amarillas_fruto",
            "variegado_hojas",
            "moteado_hojas",
            "crecimiento_horizontal",
            "corteza_facil_desprender"
        ],
        "descripcion": "Diagnóstico basado en guías técnicas oficiales: PortalFruticola (2023) y Solagro (2024) para el cultivo de palta."
    },
    "Café": {
        "sintomas": [
            "frutos_perforados",
            "granos_dañados",
            "cerezas_caidas",
            "manchas_amarillas_envés",
            "caida_hojas",
            "polvo_naranja",
            "amarillamiento_hojas",
            "marchitez_plantas",
            "muerte_plantas",
            "hormigas_cuello_tallo",
            "minas_serpentinas_hojas",
            "defoliacion",
            "hojas_necroticas",
            "hojas_bronceadas",
            "telaraña_envés",
            "epoca_seca",
            "manchas_necroticas_hojas",
            "plantulas_debiles"
        ],
        "descripcion": "Diagnóstico basado en CENICAFE Colombia, SENASA Perú e INIA (2022)."
    },
    "Cacao": {
        "sintomas": [
            "manchas_oscuras_mazorca",
            "polvo_blanco",
            "pudricion_fruto",
            "alta_humedad_ambiente",
            "temperatura_optima",
            "brotes_anormales",
            "hipertrofia_cojines",
            "escobas_secas",
            "mazorcas_perforadas",
            "galerias_internas",
            "adulto_volador_presente",
            "manchas_negras_mazorca",
            "pudricion_rapida",
            "lluvia_reciente"
        ],
        "descripcion": "Diagnóstico basado en INIAP Ecuador y AGROSAVIA Colombia (2014-2022)."
    },
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
    elif cultivo_seleccionado == "Limon":
        mostrar_diagnostico_limon(CULTIVOS)
    elif cultivo_seleccionado == "Palta":
        mostrar_diagnostico_palta(CULTIVOS)
    elif cultivo_seleccionado == "Café":
        mostrar_diagnostico_cafe(CULTIVOS)
    elif cultivo_seleccionado == "Cacao":
        mostrar_diagnostico_cacao(CULTIVOS)
    else:
        st.info(f"El módulo de diagnóstico para **{cultivo_seleccionado}** estará disponible en una próxima actualización.")
        st.image("https://placehold.co/600x200/e8f5e9/2e7d32?text=Próximamente", use_column_width=True)

    # Pie de página
    st.markdown("""
    <div class="footer">
        Desarrollado con fines académicos • Universidad Nacional de Trujillo
    </div>
    """, unsafe_allow_html=True)


