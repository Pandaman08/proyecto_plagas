import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

def mostrar_diagnostico_cafe(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Café"]["sintomas"]
    
    # DESCARGO DE RESPONSABILIDAD - REQUISITO ACADÉMICO
    st.warning("""
    ⚠️ **AVISO IMPORTANTE**: Este sistema es una herramienta de asistencia para diagnóstico preliminar.
    **La decisión final debe ser tomada por un ingeniero agrónomo, fitopatólogo o técnico agrícola calificado.**
    """)
    
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
        default=[],
        help="Seleccione todos los síntomas visibles para un diagnóstico más preciso"
    )

    if st.button("🔍 Diagnosticar Plaga", type="primary"):
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

        # DIAGNÓSTICO PRINCIPAL
        diag = diagnosticos[0]
        
        # Alerta si no hay diagnóstico
        if diag['certeza'] == 0.0:
            st.error("❌ **Sin diagnóstico identificado**: Los síntomas no coinciden con las plagas principales del café.")
            st.info("📋 **Recomendación**: Consulte con un técnico agrícola para análisis adicional.")
        else:
            # Color según certeza
            if diag['certeza'] >= 0.9:
                color_alerta = "success"
                icono = "✅"
            elif diag['certeza'] >= 0.7:
                color_alerta = "info"
                icono = "⚠️"
            else:
                color_alerta = "warning"
                icono = "🔍"
            
            # Tarjeta de diagnóstico
            st.markdown(f"""
            <div class="diagnostic-card">
                <h3>{icono} Diagnóstico: {diag['plaga']}</h3>
                <p><strong>Nivel de Certeza:</strong> {int(diag['certeza'] * 100)}%</p>
                <p><strong>Umbral de daño económico:</strong> {diag['umbral']}</p>
            </div>
            """, unsafe_allow_html=True)

            # GRÁFICO DE CERTEZA
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=diag['certeza'] * 100,
                title={'text': "Nivel de Confianza del Diagnóstico"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#4caf50" if diag['certeza'] >= 0.8 else "#ff9800"},
                    'steps': [
                        {'range': [0, 50], 'color': "#ffcdd2"},
                        {'range': [50, 80], 'color': "#fff9c4"},
                        {'range': [80, 100], 'color': "#c8e6c9"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

            # RECOMENDACIONES DE MANEJO
            st.subheader("🌾 Recomendaciones de Manejo Integrado")
            for i, rec in enumerate(diag['recomendaciones'], 1):
                st.markdown(f"**{i}.** {rec}")

        # EXPLICABILIDAD - REQUISITO ACADÉMICO CRÍTICO
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
                        if regla:  # Filtrar None
                            st.code(regla, language="python")
                else:
                    st.info("Ninguna regla específica activada")
            
            # Explicación del proceso
            st.markdown("---")
            st.markdown("**Proceso de inferencia:**")
            st.info(f"""
            1. **Entrada**: Se declararon {len(seleccion)} síntomas como hechos
            2. **Motor de inferencia**: Encadenamiento hacia adelante (forward chaining)
            3. **Evaluación**: Se activaron {len([r for r in resultado["reglas_activadas"] if r])} regla(s)
            4. **Resultado**: Diagnóstico con certeza del {int(diag['certeza']*100)}%
            5. **Base de conocimiento**: CENICAFE, SENASA, INIA (2020-2023)
            """)

        # DIAGNÓSTICOS ALTERNATIVOS
        if len(diagnosticos) > 1:
            with st.expander("📋 Diagnósticos alternativos (diagnóstico diferencial)", expanded=False):
                st.caption("Otras posibles plagas según los síntomas observados")
                for d in diagnosticos[1:]:
                    if d['certeza'] > 0.0:
                        st.markdown(f"""
                        - **{d['plaga']}**  
                          Certeza: {int(d['certeza']*100)}% | Regla: `{d.get('regla_activada', 'N/A')}`
                        """)

        # LIMITACIONES DEL SISTEMA
        with st.expander("⚠️ Limitaciones y Supuestos del Sistema", expanded=False):
            st.markdown("""
            ### Limitaciones conocidas:
            - **Síntomas ambiguos**: Amarillamiento puede ser por cochinillas, deficiencias nutricionales o estrés hídrico
            - **Periodo de observación**: No considera fenología del cultivo ni historial de la parcela
            - **Interacciones complejas**: No detecta infecciones simultáneas de múltiples patógenos
            - **Variabilidad genética**: Asume variedades comerciales comunes (Typica, Caturra, Bourbon)
            
            ### Supuestos del sistema:
            - ✓ Cafetal en condiciones de manejo convencional
            - ✓ Clima tropical/subtropical (temperatura 18-24°C, precipitación 1500-2000mm)
            - ✓ Síntomas observados en plantas adultas en producción
            - ✓ No considera plagas secundarias o regionales específicas
            
            ### Casos donde el sistema puede fallar:
            - Síntomas muy tempranos (periodo de incubación)
            - Daños por factores abióticos (heladas, sequía, toxicidad)
            - Plagas emergentes no documentadas en la base de conocimiento
            """)

        # FUENTES Y VALIDACIÓN
        with st.expander("📚 Fuentes Técnicas y Validación", expanded=False):
            st.markdown("""
            ### Fuentes consultadas:
            **Instituciones de investigación:**
            - **CENICAFE** (Centro Nacional de Investigaciones del Café, Colombia)
            - **SENASA Perú** (Servicio Nacional de Sanidad Agraria)
            - **INIA Perú** (Instituto Nacional de Innovación Agraria) - MIP 2022
            - **Café de Colombia** (Federación Nacional de Cafeteros)
            
            ### Validación:
            ⚠️ **Este sistema NO ha sido validado por expertos en campo**
            - Desarrollado con fines académicos
            - Base de conocimiento extraída de literatura técnica oficial
            - Requiere validación por agrónomos especializados en café
            
            ### Responsable de decisión final:
            👨‍🌾 **Ingeniero agrónomo o técnico agrícola certificado**
            """)

        # NOTA FINAL
        st.markdown("---")
        st.caption("""
        💡 **Nota de Transparencia**: Este sistema experto utiliza reglas determinísticas basadas en 
        literatura técnica oficial. La certeza refleja la completitud de síntomas observados, no probabilidades 
        estadísticas. Siempre consulte con un profesional antes de aplicar tratamientos químicos.
        """)

if __name__ == "__main__":
    from ui.layout import CULTIVOS
    mostrar_diagnostico_cafe(CULTIVOS)
