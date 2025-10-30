import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

def mostrar_diagnostico_limon(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Limon"]["sintomas"]

    # Inicializar el estado de la página si no existe
    if 'pagina_actual' not in st.session_state:
        st.session_state.pagina_actual = 0

    # Mostramos imágenes y descripciones de síntomas en carrusel
    with st.expander("🔍 Guía de síntomas observables", expanded=True):
        sintomas_info = {
            # Daños en hojas
            "hojas_enrolladas": "Hojas retorcidas o encrespadas, típicamente por pulgones o ácaros.",
            "hojas_plateadas": "Apariencia plateada o blanquecina en el haz, causada por ácaro del tostado.",
            "hojas_amarillentas": "Clorosis general, puede indicar queresas o moscas blancas.",
            "hojas_deformadas": "Hojas distorsionadas, arrugadas o con crecimiento anormal.",
            "hojas_con_minas_serpentinas": "Túneles serpenteantes plateados, daño de minador de hojas.",
            "hojas_con_puntos_amarillos": "Pequeños puntos amarillos dispersos por alimentación de ácaros.",
            "hojas_con_manchas_negras": "Manchas oscuras o negras, posible fumagina asociada a insectos chupadores.",
            
            # Presencia de insectos/ácaros
            "escamas_blancas_hojas": "Costras blancas en hojas, piojos blancos o queresas.",
            "escamas_marrones_hojas": "Escamas marrones circulares o alargadas, queresas diaspididas.",
            "insectos_algodonosos": "Masas blancas algodonosas, cochinilla harinosa o acanalada.",
            "moscas_blancas_envés": "Pequeños insectos blancos voladores en envés de hojas.",
            "pulgones_brotes": "Colonias de pulgones verdes, negros o marrones en brotes tiernos.",
            
            # Secreciones
            "mielada": "Sustancia pegajosa brillante en hojas/ramas, producida por insectos chupadores.",
            "fumagina": "Hongo negro hollín sobre mielada, reduce fotosíntesis.",
            
            # Daños en frutos
            "frutos_decolorados": "Frutos con manchas amarillas, grises o marrones.",
            "frutos_con_manchas_oscuras": "Manchas negras o marrones en cáscara, por queresas o ácaros.",
            "frutos_plateados": "Área plateada o bronceada en frutos por ácaro del tostado.",
            "frutos_deformados": "Frutos con forma irregular o desarrollo asimétrico.",
            "frutos_pequeños": "Frutos más pequeños de lo normal, por estrés de plagas.",
            "cáscara_agrietada": "Grietas superficiales en cáscara por daño temprano de ácaros.",
            
            # Daños en ramas/tronco
            "escamas_tronco": "Costras marrones o blancas en tronco y ramas principales.",
            "debilitamiento_planta": "Pérdida de vigor general, amarillamiento progresivo.",
            "muerte_brotes": "Brotes secos o muertos, por queresas o moscas blancas severas."
        }

        # Configuración del carrusel
        items_por_pagina = 3
        total_sintomas = len(sintomas_disponibles)
        total_paginas = (total_sintomas + items_por_pagina - 1) // items_por_pagina
        
        # Calcular índices para la página actual
        inicio = st.session_state.pagina_actual * items_por_pagina
        fin = min(inicio + items_por_pagina, total_sintomas)
        sintomas_pagina = sintomas_disponibles[inicio:fin]

        # Mostrar imágenes de la página actual con altura reducida
        cols = st.columns(3)
        for i, sintoma in enumerate(sintomas_pagina):
            with cols[i]:
                ruta_imagen = f"images/limon/sintomas/{sintoma}.jpg"
                try:
                    st.image(ruta_imagen, use_container_width=True)
                    st.markdown(f"""
                        <div style='margin-top: -10px; margin-bottom: 5px;'>
                            <p style='font-size: 0.9em; font-weight: 600; margin-bottom: 3px;'>
                                🟢 {sintoma.replace('_',' ').capitalize()}
                            </p>
                            <p style='font-size: 0.75em; color: #666; line-height: 1.3; margin: 0;'>
                                {sintomas_info.get(sintoma, "Descripción no disponible.")}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception:
                    st.warning(f"⚠️ {sintoma.replace('_',' ').capitalize()}")

        # Controles de navegación del carrusel - MÁS COMPACTOS
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if st.button("⬅️", disabled=(st.session_state.pagina_actual == 0), use_container_width=True, key="prev_btn"):
                st.session_state.pagina_actual -= 1
                st.rerun()
        
        with col_info:
            st.markdown(f"""
                <div style='text-align: center; padding: 2px; font-size: 0.85em; color: #555;'>
                    Página {st.session_state.pagina_actual + 1} de {total_paginas}
                </div>
            """, unsafe_allow_html=True)
        
        with col_next:
            if st.button("➡️", disabled=(st.session_state.pagina_actual >= total_paginas - 1), use_container_width=True, key="next_btn"):
                st.session_state.pagina_actual += 1
                st.rerun()

    # Selector de síntomas
    seleccion = st.multiselect(
        "Seleccione los síntomas observados en el campo:",
        options=sintomas_disponibles,
        default=[]
    )

    # Botón de diagnóstico
    if st.button("🔍 Diagnosticar Plaga"):
        if not seleccion:
            st.warning("⚠️ Por favor, seleccione al menos un síntoma.")
            return

        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("limon", seleccion)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        diagnosticos = resultado["diagnosticos"]
        if not diagnosticos:
            st.warning("❌ No se encontró un diagnóstico compatible con los síntomas ingresados.")
            return

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