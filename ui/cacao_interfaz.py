import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

def mostrar_diagnostico_cacao(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Cacao"]["sintomas"]
    
    with st.expander("🔍 Guía de síntomas observables", expanded=False):
        st.markdown("""
        ### Plagas del Cacao (Theobroma cacao)
        
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
        default=[]
    )

    if st.button("🔍 Diagnosticar Plaga"):
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

        # Mostrar diagnóstico principal
        diag = diagnosticos[0]
        
        # Color del borde según severidad
        color_borde = "#d32f2f" if diag['certeza'] >= 0.9 else "#4caf50"
        
        st.markdown(f"""
        <div class="diagnostic-card" style="border-left: 4px solid {color_borde}">
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

        # Alerta especial para enfermedades devastadoras
        if "Moniliasis" in diag['plaga'] or "Escoba de bruja" in diag['plaga']:
            st.error(f"""
            ⚠️ **ALERTA**: {diag['plaga'].split('(')[0]} es una enfermedad devastadora.
            Puede causar pérdidas del 40-90% de la producción. 
            **Acción inmediata requerida.**
            """)

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
            - INIAP Ecuador (Instituto Nacional de Investigaciones Agropecuarias)
            - AGROSAVIA Colombia (Corporación Colombiana de Investigación Agropecuaria)
            - SENASA Perú (Servicio Nacional de Sanidad Agraria)
            - CATIE (Centro Agronómico Tropical de Investigación y Enseñanza)
            - CropLife Latin America - Ficha técnica Moniliasis
            
            **Referencias clave:**
            - "Estado de la moniliasis del cacao causada por Moniliophthora roreri en Colombia" (Acta Agronómica, 2014)
            - "Manejo integrado de problemas fitosanitarios del cacao en Amazonía Ecuatoriana" (INIAP, 2011)
            - "Guía del manejo integrado de enfermedades del cultivo de cacao" (INIAP, 2020)
            - Phillips-Mora et al. (2007) - Diversidad genética de M. roreri
            
            **Datos importantes:**
            - Colombia: origen probable de Moniliasis (mayor diversidad genética)
            - Pérdidas anuales en Santander (Colombia): 40% = 33 millones USD
            - Amazonia ecuatoriana: >40% pérdidas por Moniliasis
            """)