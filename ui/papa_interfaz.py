import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

# ====== MAPEOS DE SÍNTOMAS A TEXTO LEGIBLE ======
SINTOMAS_LEGIBLES = {
    "hojas_enrolladas": "Hojas enrolladas",
    "hojas_amarillentas": "Hojas amarillentas",
    "tuneles_en_hojas": "Túneles en las hojas",
    "larvas_presentes": "Larvas presentes",
    "raices_perforadas": "Raíces perforadas",
    "tuberculos_huecos": "Tubérculos huecos",
    "plantas_debilitadas": "Plantas debilitadas",
    "manchas_amarillas": "Manchas amarillas en hojas",
    "hojas_con_galerias": "Galerías en hojas",
    "insectos_pequenos_negros": "Insectos pequeños negros",
    "tallos_perforados": "Tallos perforados",
    "tuberculos_danados": "Tubérculos dañados",
    "hojas_plateadas": "Hojas plateadas",
    "insectos_pequenos": "Insectos pequeños visibles",
    "hojas_arrugadas": "Hojas arrugadas",
    "polvo_fino_blanco": "Polvo fino blanco sobre hojas",
    "hojas_devoradas": "Hojas devoradas",
    "insectos_amarillos_negros": "Insectos amarillos con negro",
    "tallos_cortados": "Tallos cortados",
    "plantas_caidas": "Plantas caídas",
    "hojas_amarillas": "Hojas amarillas",
    "insectos_mosca_blanca": "Insectos tipo mosca blanca",
    "tuberculos_con_galerias": "Tubérculos con galerías",
    "larvas_internas": "Larvas dentro del tubérculo",
    "suelo_humedo": "Suelo húmedo o lodoso",
    "raices_mascadas": "Raíces mascadas",
    "tallos_deformados": "Tallos deformados",
    "hojas_abolladas": "Hojas abolladas o deformadas",
    "tuberculos_decolorados": "Tubérculos decolorados",
    "larvas_rosadas": "Larvas rosadas visibles",
    "suelo_agrietado": "Suelo agrietado",
    "raices_mordidas": "Raíces mordidas",
    "tallos_mordidos": "Tallos mordidos",
    "ataque_nocturno": "Daño visible solo de noche",
    "hojas_curvadas": "Hojas curvadas hacia adentro",
    "insectos_verdes": "Insectos verdes pequeños",
    "hojas_mordidas": "Hojas mordidas",
    "rastro_baboso": "Rastro baboso en hojas o suelo",
    "hojas_manchas_negras": "Manchas negras en hojas",
    "clima_humedo": "Clima húmedo o lluvioso reciente"
}

# ====== AGRUPACIÓN DE SÍNTOMAS ======
CATEGORIAS_SINTOMAS = {
    "🍃 Hojas": [
        "hojas_enrolladas", "hojas_amarillentas", "tuneles_en_hojas", 
        "hojas_con_galerias", "hojas_plateadas", "hojas_arrugadas", 
        "hojas_devoradas", "hojas_curvadas", "hojas_manchas_negras", "hojas_mordidas"
    ],
    "🌿 Tallos y raíces": [
        "tallos_perforados", "tallos_cortados", "tallos_deformados", 
        "raices_perforadas", "raices_mascadas", "raices_mordidas"
    ],
    "🥔 Tubérculos": [
        "tuberculos_huecos", "tuberculos_danados", 
        "tuberculos_con_galerias", "tuberculos_decolorados"
    ],
    "🐛 Insectos visibles": [
        "larvas_presentes", "insectos_pequenos_negros", "insectos_pequenos", 
        "insectos_amarillos_negros", "insectos_mosca_blanca", 
        "larvas_internas", "larvas_rosadas", "insectos_verdes"
    ],
    "🌱 Planta completa": [
        "plantas_debilitadas", "manchas_amarillas", "plantas_caidas"
    ],
    "🌾 Suelo y ambiente": [
        "suelo_humedo", "suelo_agrietado", "ataque_nocturno", "clima_humedo"
    ],
    "🐌 Otros": [
        "polvo_fino_blanco", "rastro_baboso"
    ]
}

# ====== INTERFAZ ======
def mostrar_diagnostico_papa(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Papa"]["sintomas"]

    st.title("🥔 Diagnóstico de Plagas en Papa")
    st.markdown("Selecciona los síntomas que observas en tu cultivo:")

    sintomas_seleccionados = []

    for categoria, sintomas_cat in CATEGORIAS_SINTOMAS.items():
        with st.expander(categoria):
            cols = st.columns(2)
            for idx, sintoma_clave in enumerate(sintomas_cat):
                if sintoma_clave in sintomas_disponibles:
                    col = cols[idx % 2]
                    texto = SINTOMAS_LEGIBLES.get(sintoma_clave, sintoma_clave)
                    if col.checkbox(texto, key=sintoma_clave):
                        sintomas_seleccionados.append(sintoma_clave)

    st.markdown("---")

    if st.button("🔍 Diagnosticar", use_container_width=True, type="primary"):
        if not sintomas_seleccionados:
            st.warning("⚠️ Debes seleccionar al menos un síntoma.")
            return

        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("papa", sintomas_seleccionados)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        diagnosticos = resultado["diagnosticos"]
        if not diagnosticos:
            st.info("🤔 No se encontró una plaga con esos síntomas. Intenta seleccionar más.")
            return

        diag = diagnosticos[0]
        certeza_pct = int(diag['certeza'] * 100)
        st.success(f"### 🪲 Plaga identificada: **{diag['plaga']}**")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**Nivel de certeza:** {certeza_pct}%")
            st.markdown("#### ✅ Recomendaciones:")
            for rec in diag['recomendaciones']:
                st.markdown(f"- {rec}")

        with col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=certeza_pct,
                title={'text': "Confianza"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#4CAF50"},
                    'steps': [
                        {'range': [0, 60], 'color': "#ffebee"},
                        {'range': [60, 85], 'color': "#c8e6c9"},
                        {'range': [85, 100], 'color': "#81c784"}
                    ],
                }
            ))
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)

        # Mostrar imagen asociada
        if diag.get("imagen"):
            ruta_imagen = f"images/papa/{diag['imagen']}"
            try:
                st.image(ruta_imagen, caption=f"{diag['plaga']}", use_column_width=True)
            except Exception:
                st.warning(f"No se encontró imagen: {ruta_imagen}")

        # Diagnósticos secundarios
        if len(diagnosticos) > 1:
            with st.expander("🔄 Posibles alternativas"):
                for d in diagnosticos[1:]:
                    st.markdown(f"- **{d['plaga']}** ({int(d['certeza']*100)}%)")

        # Mostrar síntomas marcados
        with st.expander("🧠 Síntomas seleccionados"):
            for s in sintomas_seleccionados:
                st.markdown(f"- {SINTOMAS_LEGIBLES.get(s, s)}")

