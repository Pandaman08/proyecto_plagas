import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas
import os

# Mapeo de plagas a nombres de archivos de imágenes
IMAGENES_PLAGAS = {
    "Broca del café (Hypothenemus hampei)": "broca.jpg",
    "Broca del café (Hypothenemus hampei) – sospecha": "broca.jpg",
    "Roya amarilla del café (Hemileia vastatrix)": "roya.jpg",
    "Roya amarilla del café (Hemileia vastatrix) – etapa inicial": "roya.jpg",
    "Cochinillas de raíces del café (Puto barberi, Dysmicoccus spp)": "cochinilla.jpg",
    "Cochinillas de raíces – indicio por hormigas": "cochinilla.jpg",
    "Minador de hojas del café (Leucoptera coffeella)": "minador.jpg",
    "Arañita roja del café (Oligonychus yothersi)": "arañita.jpg",
    "Arañita roja del café (Oligonychus yothersi) – focos iniciales": "arañita.jpg",
    "Mancha de hierro (Cercospora coffeicola)": "mancha.jpg"
}

def mostrar_diagnostico_cafe(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Café"]["sintomas"]
    
    # DESCARGO DE RESPONSABILIDAD - REQUISITO ACADÉMICO
    st.warning("""
    ⚠️ **AVISO IMPORTANTE**: Este sistema es una herramienta de asistencia para diagnóstico preliminar.
    **La decisión final debe ser tomada por un ingeniero agrónomo, fitopatólogo o técnico agrícola calificado.**
    """)
    
    with st.expander("📖 Guía rápida de síntomas observables (Campo)", expanded=False):
        st.markdown("""
        **Frutos perforados**
        - Perforación circular en el disco del fruto (parte central del grano)

        **Granos dañados internamente**
        - Polvo café fino en el interior del grano

        **Manchas amarillas en hojas**
        - Manchas cloróticas visibles en el envés

        **Polvo naranja**
        - Polvo fino de color naranja o amarillo en la cara inferior de la hoja

        **Hojas con galerías internas**
        - Líneas serpenteadas dentro del tejido foliar

        **Hojas bronceadas**
        - Coloración bronceada o amarillenta en periodos secos

        **Manchas necróticas circulares**
        - Lesiones marrones con borde marcado

        **Plantas débiles o marchitas**
        - Pérdida de vigor, crecimiento lento

        **Presencia de hormigas en el cuello del tallo**
        - Indica posible asociación con cochinillas
        """)

    st.markdown("### Seleccione los síntomas observados en sus plantas")
    st.markdown("---")

    SINTOMAS_DESCRIPCION = {
        "frutos_perforados": "Frutos perforados",
        "granos_dañados": "Daño interno en el grano",
        "cerezas_caidas": "Caída prematura de frutos",
        "manchas_amarillas_envés": "Manchas amarillas en hojas",
        "caida_hojas": "Caída progresiva de hojas",
        "polvo_naranja": "Polvo anaranjado en el envés",
        "amarillamiento_hojas": "Hojas amarillentas generales",
        "marchitez_plantas": "Marchitez persistente",
        "muerte_plantas": "Plantas muy debilitadas",
        "hormigas_cuello_tallo": "Hormigas en el cuello de la planta",
        "minas_serpentinas_hojas": "Trayectorias blanquecinas en hojas",
        "defoliacion": "Pérdida de hojas",
        "hojas_necroticas": "Hojas con partes secas",
        "hojas_bronceadas": "Hojas bronceadas o rojizas",
        "telaraña_envés": "Telarañas finas en el envés",
        "epoca_seca": "Síntomas en época seca",
        "manchas_necroticas_hojas": "Manchas circulares necrosadas",
        "plantulas_debiles": "Plántulas débiles en vivero"
    }

    seleccion = []

    columnas = st.columns(3)
    i = 0
    for sintoma in SINTOMAS_DESCRIPCION:
        if sintoma in sintomas_disponibles:
            if columnas[i % 3].checkbox(SINTOMAS_DESCRIPCION[sintoma], key=sintoma):
                seleccion.append(sintoma)
            i += 1

    if st.button("Diagnosticar"):
        if not seleccion:
            st.warning("Seleccione al menos un síntoma.")
            return

        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("café", seleccion)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        # Verificar que hay diagnósticos
        if not resultado.get("diagnosticos") or len(resultado["diagnosticos"]) == 0:
            st.error("❌ **Sin diagnóstico identificado**: Los síntomas no coinciden con las plagas principales del café.")
            st.info("📋 **Recomendación**: Consulte con un técnico agrícola para análisis adicional.")
            return

        diagnosticos = resultado["diagnosticos"]
        diag = diagnosticos[0]
        
        # Alerta si no hay diagnóstico
        if diag['certeza'] == 0.0:
            st.error("❌ **Sin diagnóstico identificado**: Los síntomas no coinciden con las plagas principales del café.")
            st.info("📋 **Recomendación**: Consulte con un técnico agrícola para análisis adicional.")
            return
        
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

        # Layout con columnas para gráfico y recomendaciones
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # RECOMENDACIONES DE MANEJO
            st.subheader("🌾 Recomendaciones de Manejo Integrado")
            for i, rec in enumerate(diag['recomendaciones'], 1):
                st.markdown(f"**{i}.** {rec}")

        with col2:
            # GRÁFICO DE CERTEZA
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=diag['certeza'] * 100,
                title={'text': "Confianza"},
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
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

        # MOSTRAR IMAGEN DE LA PLAGA
        plaga_nombre = diag['plaga']
        
        if plaga_nombre in IMAGENES_PLAGAS:
            nombre_imagen = IMAGENES_PLAGAS[plaga_nombre]
            ruta_imagen = f"images/cafe/{nombre_imagen}"
            
            if os.path.exists(ruta_imagen):
                try:
                    st.image(ruta_imagen, caption=f"{plaga_nombre}", use_container_width=True)
                except Exception as e:
                    st.warning(f"⚠️ No se pudo cargar la imagen: {str(e)}")
            else:
                st.warning(f"⚠️ Imagen no encontrada: {ruta_imagen}")

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
                if resultado.get("reglas_activadas"):
                    for regla in resultado["reglas_activadas"]:
                        if regla:  # Filtrar None
                            st.code(regla, language="python")
                else:
                    st.info("Ninguna regla específica activada")
            
            # Explicación del proceso
            st.markdown("---")
            st.markdown("**Proceso de inferencia:**")
            reglas_activas = len([r for r in resultado.get("reglas_activadas", []) if r])
            st.info(f"""
            1. **Entrada**: Se declararon {len(seleccion)} síntomas como hechos
            2. **Motor de inferencia**: Encadenamiento hacia adelante (forward chaining)
            3. **Evaluación**: Se activaron {reglas_activas} regla(s)
            4. **Resultado**: Diagnóstico con certeza del {int(diag['certeza']*100)}%
            5. **Base de conocimiento**: CENICAFE, SENASA, INIA (2020-2023)
            """)

        # DIAGNÓSTICOS ALTERNATIVOS
        if len(diagnosticos) > 1:
            with st.expander("📋 Diagnósticos alternativos (diagnóstico diferencial)", expanded=False):
                st.caption("Otras posibles plagas según los síntomas observados")
                for d in diagnosticos[1:]:
                    if d['certeza'] > 0.0:
                        regla_txt = d.get('regla_activada', 'N/A')
                        st.markdown(f"""
                        - **{d['plaga']}**  
                          Certeza: {int(d['certeza']*100)}% | Regla: `{regla_txt}`
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
