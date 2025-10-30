import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

def mostrar_diagnostico_uva(CULTIVOS):
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
                st.image(f"images/{diag['imagen']}", caption=f"Imagen de {diag['plaga']}", use_container_width=True)
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



