import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

def mostrar_diagnostico_cafe(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Café"]["sintomas"]
    
    with st.expander("🔍 Guía de síntomas observables", expanded=False):
        st.markdown("""
        ### Plagas del Café (Coffea arabica)
        
        **Broca del café (Hypothenemus hampei)**
        - **frutos_perforados**: Perforación circular en disco del fruto (parte central)
        - **granos_dañados**: Granos con galerías internas, polvo café
        - **cerezas_caidas**: Caída prematura de frutos verdes/maduros
        
        **Roya amarilla (Hemileia vastatrix)**
        - **manchas_amarillas_envés**: Manchas cloróticas en envés de hojas
        - **caida_hojas**: Defoliación progresiva del cafetal
        - **polvo_naranja**: Polvillo amarillo-naranja (uredosporas) en envés
        
        **Cochinillas de raíces (Puto barberi, Dysmicoccus)**
        - **amarillamiento_hojas**: Clorosis general de follaje
        - **marchitez_plantas**: Pérdida de turgencia, plantas débiles
        - **muerte_plantas**: Muerte de plantas jóvenes y en producción
        - **hormigas_cuello_tallo**: Presencia de hormigas en base del tallo
        
        **Minador de hojas (Leucoptera coffeella)**
        - **minas_serpentinas_hojas**: Galerías sinuosas entre epidermis
        - **defoliacion**: Caída de hojas minadas
        - **hojas_necroticas**: Hojas con tejido muerto por minas
        
        **Arañita roja (Oligonychus yothersi)**
        - **hojas_bronceadas**: Coloración bronceada/amarillenta en hojas
        - **telaraña_envés**: Finas telas de araña en envés
        - **epoca_seca**: Síntomas evidentes en periodo seco
        
        **Mancha de hierro (Cercospora coffeicola)**
        - **manchas_necroticas_hojas**: Manchas necróticas circulares
        - **plantulas_debiles**: Plantas debilitadas en vivero/crecimiento
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
        resultado = motor.diagnosticar("café", seleccion)

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
        
        # Información adicional sobre fuentes
        with st.expander("📚 Fuentes consultadas", expanded=False):
            st.markdown("""
            **Fuentes técnicas utilizadas:**
            - CENICAFE (Centro Nacional de Investigaciones del Café, Colombia)
            - SENASA Perú (Servicio Nacional de Sanidad Agraria)
            - INIA Perú (Instituto Nacional de Innovación Agraria) - Manejo Integrado de Plagas (2022)
            - Café de Colombia - Federación Nacional de Cafeteros
            - Perfect Daily Grind - Guía de plagas comunes del café
            
            **Referencias clave:**
            - Control biológico de broca del café con *Beauveria bassiana*
            - Manejo Integrado de Plagas (MIP) en caficultura colombiana
            - Guías SENASA para vigilancia fitosanitaria en café
            """)