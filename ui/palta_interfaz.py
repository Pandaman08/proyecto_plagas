import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

def mostrar_diagnostico_palta(CULTIVOS):  # ← Recibe CULTIVOS como parámetro
    sintomas_disponibles = CULTIVOS["Palta"]["sintomas"]
    
    with st.expander("🔍 Guía de síntomas observables", expanded=False):
        st.markdown("""
        - **manchas_folares**: manchas en las hojas.
        - **caida_prematura**: caída temprana de hojas/frutos.
        - **frutos_manchados**: manchas en los frutos.
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
        
        st.info("El módulo de diagnóstico para Palta estará disponible próximamente.")