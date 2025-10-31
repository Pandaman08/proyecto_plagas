import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas
import os

# Mapeo de plagas a nombres de archivos de imágenes
IMAGENES_PLAGAS = {
    "Moniliasis del cacao (Moniliophthora roreri)": "moniliasis.jpg",
    "Moniliasis del cacao (Moniliophthora roreri) – etapa inicial": "moniliasis.jpg",
    "Riesgo de Moniliasis – condiciones ambientales favorables": "moniliasis.jpg",
    "Escoba de bruja (Moniliophthora perniciosa)": "escoba_bruja.jpg",
    "Escoba de bruja (Moniliophthora perniciosa) – sospecha": "escoba_bruja.jpg",
    "Mazorquero del cacao (Carmenta spp)": "mazorquero.jpg",
    "Mazorquero del cacao (Carmenta spp) – daño inicial": "mazorquero.jpg",
    "Pudrición negra de mazorca (Phytophthora palmivora)": "pudricion_negra.jpg",
    "Pudrición negra de mazorca (Phytophthora spp) – etapa inicial": "pudricion_negra.jpg",
    "Sin plaga identificada": None
}

def mostrar_diagnostico_cacao(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Cacao"]["sintomas"]
    
    # DESCARGO DE RESPONSABILIDAD - REQUISITO ACADÉMICO
    st.warning("""
    AVISO IMPORTANTE: Este sistema es una herramienta de asistencia para diagnóstico preliminar.
    La decisión final debe ser tomada por un ingeniero agrónomo, fitopatólogo o técnico agrícola calificado.
    """)
    
    with st.expander("Guía rápida de síntomas observables (Campo)", expanded=False):
        st.markdown("""
        **Manchas oscuras en mazorca**
        - Pequeñas manchas oscuras en superficie de mazorca
        
        **Polvo blanco**
        - Polvo blanco característico (millones de conidias)
        
        **Pudrición de fruto**
        - Pudrición interna del fruto, mazorca momificada
        
        **Alta humedad ambiente**
        - Humedad relativa mayor al 80%
        
        **Temperatura óptima**
        - Temperatura 21-27°C favorable
        
        **Brotes anormales**
        - Brotes hinchados, deformados (fase verde)
        
        **Hipertrofia de cojines**
        - Cojines florales hinchados anormalmente
        
        **Escobas secas**
        - Brotes secos necróticos (fase seca - fuente de esporas)
        
        **Mazorcas perforadas**
        - Perforaciones pequeñas en cáscara
        
        **Galerías internas**
        - Galerías en pulpa y semillas
        
        **Adulto volador presente**
        - Observación de polillas adultas
        
        **Manchas negras en mazorca**
        - Manchas negras con borde difuso
        
        **Pudrición rápida**
        - Pudrición acelerada en 3-5 días
        
        **Lluvia reciente**
        - Síntomas evidentes después de lluvias
        """)

    st.markdown("### Seleccione los síntomas observados en sus plantas")
    st.markdown("---")

    SINTOMAS_DESCRIPCION = {
        "manchas_oscuras_mazorca": "Manchas oscuras en mazorca",
        "polvo_blanco": "Polvo blanco",
        "pudricion_fruto": "Pudrición de fruto",
        "alta_humedad_ambiente": "Alta humedad ambiente",
        "temperatura_optima": "Temperatura óptima (21-27°C)",
        "brotes_anormales": "Brotes anormales",
        "hipertrofia_cojines": "Hipertrofia de cojines florales",
        "escobas_secas": "Escobas secas",
        "mazorcas_perforadas": "Mazorcas perforadas",
        "galerias_internas": "Galerías internas",
        "adulto_volador_presente": "Adulto volador presente",
        "manchas_negras_mazorca": "Manchas negras en mazorca",
        "pudricion_rapida": "Pudrición rápida",
        "lluvia_reciente": "Lluvia reciente"
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
        resultado = motor.diagnosticar("cacao", seleccion)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        # Verificar que hay diagnósticos
        if not resultado.get("diagnosticos") or len(resultado["diagnosticos"]) == 0:
            st.error("Sin diagnóstico identificado: Los síntomas no coinciden con las plagas principales del cacao.")
            st.info("Recomendación: Consulte con un técnico agrícola para análisis adicional.")
            return

        diagnosticos = resultado["diagnosticos"]
        diag = diagnosticos[0]
        
        # Alerta si no hay diagnóstico
        if diag['certeza'] == 0.0:
            st.error("Sin diagnóstico identificado: Los síntomas no coinciden con las plagas principales del cacao.")
            st.info("Recomendación: Consulte con un técnico agrícola para análisis adicional.")
            return
        
        # Alerta para enfermedades devastadoras
        if "Moniliasis" in diag['plaga'] or "Escoba de bruja" in diag['plaga']:
            st.error(f"""
            ALERTA: {diag['plaga'].split('(')[0]} es una enfermedad devastadora.
            Puede causar pérdidas del 40-90% de la producción. 
            Acción inmediata requerida.
            """)
        
        # Color según certeza
        if diag['certeza'] >= 0.9:
            color_alerta = "success"
        elif diag['certeza'] >= 0.7:
            color_alerta = "info"
        else:
            color_alerta = "warning"
        
        # Tarjeta de diagnóstico
        st.markdown(f"""
        <div class="diagnostic-card">
            <h3>Diagnóstico: {diag['plaga']}</h3>
            <p><strong>Nivel de Certeza:</strong> {int(diag['certeza'] * 100)}%</p>
            <p><strong>Umbral de daño económico:</strong> {diag['umbral']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Layout con columnas para gráfico y recomendaciones
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # RECOMENDACIONES DE MANEJO
            st.subheader("Recomendaciones de Manejo Integrado")
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
        
        if plaga_nombre in IMAGENES_PLAGAS and IMAGENES_PLAGAS[plaga_nombre] is not None:
            nombre_imagen = IMAGENES_PLAGAS[plaga_nombre]
            ruta_imagen = f"images/cacao/{nombre_imagen}"
            
            if os.path.exists(ruta_imagen):
                try:
                    st.image(ruta_imagen, caption=f"{plaga_nombre}", use_container_width=True)
                except Exception as e:
                    st.warning(f"No se pudo cargar la imagen: {str(e)}")
            else:
                st.info(f"Imagen no disponible para esta plaga. Ruta esperada: {ruta_imagen}")

        # EXPLICABILIDAD - REQUISITO ACADÉMICO CRÍTICO
        with st.expander("Explicación del Razonamiento (Trazabilidad)", expanded=True):
            st.markdown("### Cómo el sistema llegó a esta conclusión")
            
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
            1. Entrada: Se declararon {len(seleccion)} síntomas como hechos
            2. Motor de inferencia: Encadenamiento hacia adelante (forward chaining)
            3. Evaluación: Se activaron {reglas_activas} regla(s)
            4. Resultado: Diagnóstico con certeza del {int(diag['certeza']*100)}%
            5. Base de conocimiento: INIAP Ecuador, AGROSAVIA Colombia (2014-2022)
            """)

        # DIAGNÓSTICOS ALTERNATIVOS
        if len(diagnosticos) > 1:
            with st.expander("Diagnósticos alternativos (diagnóstico diferencial)", expanded=False):
                st.caption("Otras posibles plagas según los síntomas observados")
                for d in diagnosticos[1:]:
                    if d['certeza'] > 0.0:
                        regla_txt = d.get('regla_activada', 'N/A')
                        st.markdown(f"""
                        - **{d['plaga']}**  
                          Certeza: {int(d['certeza']*100)}% | Regla: `{regla_txt}`
                        """)

        # LIMITACIONES DEL SISTEMA
        with st.expander("Limitaciones y Supuestos del Sistema", expanded=False):
            st.markdown("""
            ### Limitaciones conocidas:
            - **Periodo de latencia**: Moniliasis puede tardar 40-80 días sin síntomas visibles
            - **Síntomas ambiguos**: Manchas oscuras pueden ser por múltiples patógenos
            - **Periodo de observación**: No considera fenología del cultivo ni historial de la parcela
            - **Interacciones complejas**: No detecta infecciones simultáneas de múltiples patógenos
            - **Variabilidad genética**: Asume variedades comerciales comunes (CCN-51, ICS, Trinitarios)
            
            ### Supuestos del sistema:
            - Plantación de cacao en condiciones de manejo convencional
            - Clima tropical/subtropical (temperatura 21-27°C, humedad relativa alta)
            - Síntomas observados en plantas adultas en producción
            - No considera plagas secundarias o regionales específicas
            
            ### Casos donde el sistema puede fallar:
            - Síntomas muy tempranos (periodo de incubación)
            - Daños por factores abióticos (sequía, toxicidad, vientos)
            - Plagas emergentes no documentadas en la base de conocimiento
            - Diferenciación entre Moniliasis y Phytophthora en etapas tempranas
            """)

        # FUENTES Y VALIDACIÓN
        with st.expander("Fuentes Técnicas y Validación", expanded=False):
            st.markdown("""
            ### Fuentes consultadas:
            **Instituciones de investigación:**
            - **INIAP Ecuador** (Instituto Nacional de Investigaciones Agropecuarias)
            - **AGROSAVIA Colombia** (Corporación Colombiana de Investigación Agropecuaria)
            - **SENASA Perú** (Servicio Nacional de Sanidad Agraria)
            - **CATIE** (Centro Agronómico Tropical de Investigación y Enseñanza)
            
            ### Validación:
            Este sistema NO ha sido validado por expertos en campo
            - Desarrollado con fines académicos
            - Base de conocimiento extraída de literatura técnica oficial
            - Requiere validación por agrónomos especializados en cacao
            
            ### Responsable de decisión final:
            Ingeniero agrónomo o técnico agrícola certificado
            """)

        # NOTA FINAL
        st.markdown("---")
        st.caption("""
        Nota de Transparencia: Este sistema experto utiliza reglas determinísticas basadas en 
        literatura técnica oficial. La certeza refleja la completitud de síntomas observados, no probabilidades 
        estadísticas. Siempre consulte con un profesional antes de aplicar tratamientos químicos.
        """)


if __name__ == "__main__":
    from ui.layout import CULTIVOS
    mostrar_diagnostico_cacao(CULTIVOS)
