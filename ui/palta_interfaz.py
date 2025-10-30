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
        - **bronceado_hojas**: bronceado en hojas por alta densidad de ácaros
        - **defoliacion_prematura**: caída temprana de hojas
        - **perforacion_brotes**: perforaciones en hojas jóvenes y brotes
        - **fumagina**: presencia de hongo negro (hollín) en hojas
        - **debilitamiento_planta**: planta con poco vigor y crecimiento lento
        - **hojas_pegajosas**: hojas con sustancia pegajosa (melaza)
        - **escamas_marron_frutos**: escamas alargadas marrón amarillento en frutos
        - **escamas_marron_hojas**: escamas alargadas con pliegue central en hojas
        - **secamiento_hojas**: hojas que se secan progresivamente
        - **escamas_blancas_pedunculo**: escamas blanco-rosadas en zona del pedúnculo
        - **escamas_circulares_frutos**: escamas circulares u ovaladas en frutos
        - **espirales_cera_hojas**: grandes espirales de secreciones céreas en envés
        - **huevos_desordenados_enves**: huevos alargados dispuestos desordenadamente
        - **cobertura_cera_hojas**: cobertura blanca de cera muy acentuada
        - **cestos_colgantes_hojas**: estructuras en forma de cesto colgando de hojas
        - **raspado_epidermis_hojas**: raspado superficial en epidermis de hojas
        - **larvas_con_refugio**: larvas protegidas dentro de cestos de follaje
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
        
        # Información adicional según el diagnóstico
        if "Tristeza" in diag['plaga']:
            st.info("💡 **Nota importante**: La Tristeza del palto prospera en suelos arcillosos con mal drenaje. Considere mejorar el sistema de drenaje.")
        elif "Brazo negro" in diag['plaga']:
            st.warning("⚠️ **Prevención crítica**: Desinfecte TODAS las herramientas de poda e injerto con lejía entre planta y planta para evitar propagación.")
        elif "Sunblotch" in diag['plaga']:
            st.error("🚨 **ALERTA**: Los viroides NO tienen cura. Las plantas infectadas deben ser eliminadas completamente y quemadas para evitar contagio.")
        elif "Queresas" in diag['plaga']:
            st.info("💡 **Importante para exportación**: Las queresas afectan la calidad cosmética del fruto y son frecuentemente interceptadas en cuarentena. Requiere tratamientos pre-cosecha y certificación fitosanitaria.")
        elif "Arañita" in diag['plaga']:
            st.info("💡 **Dato importante**: Esta especie de ácaro se encuentra en la cara SUPERIOR de las hojas (diferente a otros ácaros). Densidades de 300 ácaros/hoja o 70 hembras/hoja en sequía causan daño económico.")
        elif "Bicho del cesto" in diag['plaga']:
            st.success("✅ **Control facilitado**: Los cestos son muy visibles y pueden recolectarse manualmente. El control es más efectivo en estadios tempranos antes de que completen el cesto protector.")
        
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