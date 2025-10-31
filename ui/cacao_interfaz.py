import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

def mostrar_diagnostico_cacao(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Cacao"]["sintomas"]
    
    st.warning("""
    ⚠️ **AVISO IMPORTANTE**: Este sistema es una herramienta de asistencia para diagnóstico preliminar.
    **La decisión final debe ser tomada por un ingeniero agrónomo, fitopatólogo o técnico agrícola calificado.**
    No usar directamente en producción sin validación profesional.
    """)
    
    with st.expander("🔍 Guía de síntomas observables", expanded=False):
        st.markdown("""
        ### Plagas y Enfermedades del Cacao (Theobroma cacao)
        
        **Moniliasis (Moniliophthora roreri)**
        - **manchas_oscuras_mazorca**: Pequeñas manchas oscuras en superficie de mazorca
        - **polvo_blanco**: Polvo blanco característico (millones de conidias)
        - **pudricion_fruto**: Pudrición interna del fruto, mazorca momificada
        - **alta_humedad_ambiente**: Humedad relativa >80%
        - **temperatura_optima**: Temperatura 21-27°C favorable
        
        **Escoba de bruja (Moniliophthora perniciosa)**
        - **brotes_anormales**: Brotes hinchados, deformados (fase verde)
        - **hipertrofia_cojines**: Cojines florales hinchados anormalmente
        - **escobas_secas**: Brotes secos necróticos (fase seca - fuente de esporas)
        
        **Mazorquero (Carmenta spp)**
        - **mazorcas_perforadas**: Perforaciones pequeñas en cáscara
        - **galerias_internas**: Galerías en pulpa y semillas
        - **adulto_volador_presente**: Observación de polillas adultas
        
        **Pudrición negra (Phytophthora palmivora)**
        - **manchas_negras_mazorca**: Manchas negras con borde difuso
        - **pudricion_rapida**: Pudrición acelerada en 3-5 días
        - **lluvia_reciente**: Síntomas evidentes después de lluvias
        
        ### Notas Importantes
        - Periodo de incubación moniliasis: 40-80 días sin síntomas visibles
        - Diferencia clave: Moniliasis = polvo blanco; Phytophthora = sin polvo, solo manchas negras
        - Escoba de bruja: enfermedad sistémica, afecta todo el tejido vascular
        """)

    seleccion = st.multiselect(
        "Seleccione los síntomas observados en el campo:",
        options=sintomas_disponibles,
        default=[],
        help="Seleccione todos los síntomas visibles para un diagnóstico más preciso"
    )

    if st.button("🔍 Diagnosticar Plaga", type="primary"):
        if not seleccion:
            st.warning("⚠️ Por favor, seleccione al menos un síntoma.")
            return

        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("cacao", seleccion)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        diagnosticos = resultado["diagnosticos"]
        if not diagnosticos:
            st.warning("❌ No se encontró un diagnóstico compatible con los síntomas ingresados.")
            return

        diag = diagnosticos[0]
        
        if diag['certeza'] == 0.0:
            st.error("❌ **Sin plaga identificada**: Los síntomas no coinciden con las plagas principales del cacao.")
            st.info("📋 **Recomendación**: Consulte con un técnico agrícola para análisis adicional.")
        else:
            # Alerta para enfermedades devastadoras
            if "Moniliasis" in diag['plaga'] or "Escoba de bruja" in diag['plaga']:
                st.error(f"""
                🚨 **ALERTA**: {diag['plaga'].split('(')[0]} es una enfermedad devastadora.
                Puede causar pérdidas del 40-90% de la producción. 
                **Acción inmediata requerida.**
                """)
            
            # Color según certeza
            if diag['certeza'] >= 0.95:
                color_borde = "#d32f2f"
            elif diag['certeza'] >= 0.8:
                color_borde = "#ff9800"
            else:
                color_borde = "#4caf50"
            
            st.markdown(f"""
            <div class="diagnostic-card" style="border-left: 4px solid {color_borde}">
                <h3>✅ Diagnóstico: {diag['plaga']}</h3>
                <p><strong>Certeza:</strong> {int(diag['certeza'] * 100)}%</p>
                <p><strong>Umbral de daño económico:</strong> {diag['umbral']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Gráfico de certeza
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=diag['certeza'] * 100,
                title={'text': "Nivel de Confianza"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color_borde},
                    'steps': [
                        {'range': [0, 50], 'color': "#ffcdd2"},
                        {'range': [50, 80], 'color': "#fff9c4"},
                        {'range': [80, 100], 'color': "#c8e6c9"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

            # Recomendaciones
            st.subheader("🌾 Recomendaciones de Manejo Integrado")
            for i, rec in enumerate(diag['recomendaciones'], 1):
                st.markdown(f"**{i}.** {rec}")

        # Explicabilidad
        with st.expander("🧠 Explicación del Razonamiento (Trazabilidad)", expanded=True):
            st.markdown("### 📋 Cómo el sistema llegó a esta conclusión")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Síntomas ingresados:**")
                for sintoma in seleccion:
                    st.markdown(f"- `{sintoma}`")
            
            with col2:
                st.markdown("**Reglas activadas:**")
                if resultado["reglas_activadas"]:
                    for regla in resultado["reglas_activadas"]:
                        if regla:
                            st.code(regla, language="python")
                
            - Colombia: origen probable de Moniliasis (mayor diversidad genética)
            - Pérdidas anuales en Santander (Colombia): 40% = 33 millones USD
            - Amazonia ecuatoriana: >40% pérdidas por Moniliasis

            """)
