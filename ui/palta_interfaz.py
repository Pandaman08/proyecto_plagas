import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

def mostrar_diagnostico_palta(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Palta"]["sintomas"]
    
    with st.expander("🔍 Guía de síntomas observables", expanded=False):
        st.markdown("""
        - **raspado_frutos**: raspado visible en frutos recién cuajados
        - **rugosidad_frutos**: textura rugosa y áspera en la epidermis
        - **bronceado_frutos**: coloración bronceada en superficie del fruto
        - **deformacion_frutos**: frutos con formas irregulares
        - **tostado_hojas**: hojas con apariencia tostada o quemada
        - **hojas_rojizas**: coloración rojiza en hojas maduras
        - **perdida_clorofila**: pérdida del color verde en las hojas
        - **defoliacion_prematura**: caída temprana de hojas
        - **perforacion_brotes**: perforaciones en hojas jóvenes y brotes
        - **fumagina**: presencia de hongo negro (hollín) en hojas
        - **debilitamiento_planta**: planta con poco vigor y crecimiento lento
        - **hojas_pegajosas**: hojas con sustancia pegajosa (melaza)
        - **hojas_amarillas**: coloración amarillenta general en follaje
        - **defoliacion**: caída excesiva de hojas
        - **raices_necrosadas**: raíces podridas o con tejido muerto
        - **frutos_pequenos**: frutos más pequeños de lo normal
        - **muerte_regresiva**: muerte progresiva desde las puntas de ramas
        - **cancros_tronco**: heridas o lesiones en tronco y ramas
        - **exudados_blancos**: secreciones blanquecinas y grumosas
        - **muerte_ramas**: ramas completamente muertas con follaje seco
        - **pudricion_frutos_pedunculo**: pudrición del fruto en unión con el tallo
        - **manchas_amarillas_fruto**: lesiones amarillo pálido en forma de vagina en frutos
        - **variegado_hojas**: hojas con manchas de diferentes colores
        - **moteado_hojas**: puntos blancos o rosados en hojas
        - **crecimiento_horizontal**: árbol crece más horizontal que vertical
        - **corteza_facil_desprender**: corteza se desprende fácilmente con líneas amarillentas
        """)

    seleccion = st.multiselect(
        "Seleccione los síntomas observados en el campo:",
        options=sintomas_disponibles,
        default=[]
    )
    
    if st.button("🔍 Diagnosticar Plaga/Enfermedad"):
        if not seleccion:
            st.warning("⚠️ Por favor, seleccione al menos un síntoma.")
            return
        
        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("palta", seleccion)
        
        if "error" in resultado:
            st.error(resultado["error"])
            return
        
        diagnosticos = resultado["diagnosticos"]
        if not diagnosticos:
            st.warning("❌ No se encontró un diagnóstico compatible con los síntomas ingresados.")
            return
        
        # Mostrar diagnóstico principal
        diag = diagnosticos[0]
        
        # Determinar color según certeza
        if diag['certeza'] >= 0.8:
            color_borde = "#4caf50"  # Verde
            icono = "✅"
        elif diag['certeza'] >= 0.6:
            color_borde = "#ff9800"  # Naranja
            icono = "⚠️"
        else:
            color_borde = "#f44336"  # Rojo
            icono = "❓"
        
        st.markdown(f"""
        <div class="diagnostic-card" style="border-left: 4px solid {color_borde};">
            <h3>{icono} Diagnóstico: {diag['plaga']}</h3>
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
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Diagnósticos secundarios (si existen)
        if len(diagnosticos) > 1:
            with st.expander("📋 Diagnósticos alternativos", expanded=False):
                for d in diagnosticos[1:]:
                    if d['certeza'] > 0.5:
                        st.write(f"- **{d['plaga']}** (certeza: {int(d['certeza']*100)}%)")
        
        # Información adicional según el diagnóstico
        if "Tristeza" in diag['plaga']:
            st.info("💡 **Nota importante**: La Tristeza del palto prospera en suelos arcillosos con mal drenaje. Considere mejorar el sistema de drenaje.")
        elif "Brazo negro" in diag['plaga']:
            st.warning("⚠️ **Prevención crítica**: Desinfecte TODAS las herramientas de poda e injerto con lejía entre planta y planta para evitar propagación.")
        elif "Sunblotch" in diag['plaga']:
            st.error("🚨 **ALERTA**: Los viroides NO tienen cura. Las plantas infectadas deben ser eliminadas completamente y quemadas para evitar contagio.")
        
        # Trazabilidad
        with st.expander("🔍 Trazabilidad de la inferencia", expanded=False):
            st.write("**Reglas activadas:**")
            for r in resultado["reglas_activadas"]:
                if r:  # Solo mostrar si hay regla
                    st.code(r, language="python")
            
            st.write("**Síntomas ingresados:**")
            st.write(", ".join(seleccion))
            
            st.write("**Fuente de información:**")
            st.caption("Basado en: Guía fotográfica de síntomas de deficiencias de nutrientes, enfermedades y plagas en paltos - www.caritas.org.pe / PortalFruticola.com (2023)")