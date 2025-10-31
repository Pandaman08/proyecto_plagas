import streamlit as st
import plotly.graph_objects as go
from engine import SistemaExpertoPlagas

# Mapeo de síntomas técnicos a lenguaje común
SINTOMAS_LEGIBLES = {
    "verrugas_hojas": "Bolitas o verrugas en las hojas",
    "nudosidades_raices": "Pelotitas en las raíces",
    "hojas_gris_plomizo": "Hojas de color gris",
    "tejido_araña": "Telarañas en las hojas",
    "brotacion_lenta": "Tarda en brotar",
    "hojas_abarquilladas": "Hojas enrolladas hacia adentro",
    "picaduras_racimos": "Marcas o picaduras en las uvas",
    "aves_presentes": "Palomas o pájaros rondando",
    "bayas_vacias": "Uvas vacías, solo cáscara",
    "avispa_presencia": "Avispas alrededor de los racimos",
    "racimos_consumidos": "Racimos comidos",
    "madrigueras": "Hoyos en el suelo cerca de las plantas",
    "hojas_consumidas": "Hojas comidas o con huecos",
    "gusano_grande": "Gusano verde grande con cuerno",
    "plantas_debiles": "Planta débil o raquítica",
    "nódulos_redondeados_raíz": "Bultos redondos en raíces",
    "polvillo_blanco": "Polvo blanco en las hojas",
    "aborto_flores": "Flores se caen antes de dar fruto",
    "moho_gris": "Pelusa gris en los racimos",
    "racimos_podridos": "Racimos podridos",
    "agallas_tallo": "Bultos o pelotas en el tronco",
    "plantas_pequeñas": "Planta más chica de lo normal",
    "clorosis_hojas": "Hojas amarillas",
    "crecimiento_lento": "Crece muy lento",
    "hojas_marchitas": "Hojas caídas o sin fuerza",
    "suelo_seco": "Tierra muy seca",
    "hojas_amarrillentas": "Hojas amarillentas",
    "raíces_dañadas": "Raíces rotas o negras",
    "flores_no_cuajan": "No salen uvas después de la flor",
    "temperatura_alta": "Mucho calor últimamente",
    "racimos_desiguales": "Racimos desparejos",
    "poda_inadecuada": "Se podó mal o no se podó"
}

EXPLICACION_REGLAS = {
    "filoxera_completa": {
        "titulo": "¿Por qué identificamos Filóxera?",
        "explicacion": "Detectamos esta plaga porque encontraste **dos señales clave**: verrugas en las hojas y pelotitas en las raíces. Cuando aparecen juntas, es casi seguro que se trata de filóxera.",
    },
    "filoxera_parcial": {
        "titulo": "¿Por qué sospechamos de Filóxera?",
        "explicacion": "Vimos **solo una de las dos señales** típicas de filóxera (verrugas en hojas O pelotitas en raíces). Por eso lo marcamos como sospecha. Te recomendamos revisar bien las raíces.",
    },
    "aranita_roja_completa": {
        "titulo": "¿Por qué identificamos Arañita Roja?",
        "explicacion": "Las **hojas grises** junto con **telarañas** son el síntoma clásico de arañita roja. Estos bichitos se alimentan de las hojas y les quitan el color.",
    },
    "aranita_roja_parcial": {
        "titulo": "¿Por qué sospechamos de Arañita Roja?",
        "explicacion": "Las hojas grises pueden ser arañita roja, pero necesitamos confirmar. Voltea las hojas y busca con cuidado unos bichitos rojos muy pequeños.",
    },
    "acaro_hialino_completa": {
        "titulo": "¿Por qué identificamos Ácaro Hialino?",
        "explicacion": "Cuando la planta **tarda en brotar** y las **hojas se enrollan**, es señal de ácaro hialino. Estos ácaros atacan los brotes nuevos.",
    },
    "acaro_hialino_parcial": {
        "titulo": "¿Por qué sospechamos de Ácaro Hialino?",
        "explicacion": "Vimos hojas enrolladas pero no confirmamos brotación lenta. Puede ser ácaro hialino en etapa temprana. Observa los brotes en los próximos días.",
        "referencia": "Manual Uva - Página 13: 'Síntomas tempranos en follaje.'"
    },
    "aves_completa": {
        "titulo": "¿Por qué identificamos daño por Aves?",
        "explicacion": "Si ves **picaduras en las uvas** y hay **pájaros rondando**, está claro que son ellos los culpables. Las aves picotean las uvas maduras.",
    },
    "picaduras_generales": {
        "titulo": "¿Por qué hay daño en racimos sin identificar la causa?",
        "explicacion": "Detectamos **picaduras en las uvas** pero no viste pájaros ni avispas. Podría ser cualquiera de los dos. Observa el campo en diferentes horas.",
    },
    "avispas_abejas_completa": {
        "titulo": "¿Por qué identificamos Avispas y Abejas?",
        "explicacion": "Las **uvas vacías** (solo cáscara) con **avispas volando** es típico. Las avispas entran y se comen todo el jugo de la uva.",
    },
    "bayas_vacias_parcial": {
        "titulo": "¿Por qué sospechamos de Avispas?",
        "explicacion": "Las **uvas vacías** son típicas de avispas, pero no confirmaste su presencia. Revisa los racimos en las mañanas cuando están más activas.",
    },
    "ratas_raton_completa": {
        "titulo": "¿Por qué identificamos Ratas y Ratones?",
        "explicacion": "Los **racimos comidos** junto con **hoyos en el suelo** delatan a las ratas. Ellas comen los racimos completos y hacen madrigueras.",
    },
    "ratas_raton_parcial": {
        "titulo": "¿Por qué sospechamos de Roedores?",
        "explicacion": "Encontraste **racimos comidos O madrigueras** (pero no ambos). Es probable que haya ratas, pero necesitamos más evidencia como heces o rastros.",
    },
    "gusano_cornudo_completa": {
        "titulo": "¿Por qué identificamos Gusano Cornudo?",
        "explicacion": "Si hay **hojas comidas** y ves un **gusano grande con cuerno**, es el gusano cornudo de la vid. Es grande y fácil de ver.",
    },
    "hojas_consumidas_parcial": {
        "titulo": "¿Por qué hay daño en hojas sin identificar el insecto?",
        "explicacion": "Las **hojas comidas** indican un insecto defoliador, pero sin ver el gusano grande no podemos confirmar que sea gusano cornudo. Busca larvas grandes.",
    },
    "nematodos_completa": {
        "titulo": "¿Por qué identificamos Nematodos?",
        "explicacion": "Las **plantas débiles** con **bultos redondos en las raíces** indican nematodos. Son como anguilitas que atacan las raíces."
    },
    "nematodos_parcial": {
        "titulo": "¿Por qué sospechamos de Nematodos?",
        "explicacion": "Detectamos **bultos en las raíces** que son típicos de nematodos, aunque la planta no se ve débil aún. Es importante actuar antes que empeore."
    },
    "oidium_completa": {
        "titulo": "¿Por qué identificamos Oidio?",
        "explicacion": "El **polvo blanco** en las hojas junto con **flores que se caen** es oidio (caracha). Es una de las enfermedades más comunes en uva.",
    },
    "oidium_parcial": {
        "titulo": "¿Por qué sospechamos de Oidio?",
        "explicacion": "El polvo blanco solo puede ser oidio, pero como no viste otros síntomas, lo marcamos como sospecha. Revisa bien los racimos.",
    },
    "podredumbre_gris_completa": {
        "titulo": "¿Por qué identificamos Podredumbre Gris?",
        "explicacion": "La **pelusa gris** en **racimos podridos** es podredumbre gris (botrytis). Aparece sobre todo cuando hay mucha humedad.",
    },
    "podredumbre_gris_parcial": {
        "titulo": "¿Por qué sospechamos de Podredumbre Gris?",
        "explicacion": "La pelusa gris es el primer síntoma. Si no ves racimos podridos aún, estás a tiempo de controlarlo."
    },
    "racimos_podridos_general": {
        "titulo": "¿Por qué hay pudrición sin identificar la causa?",
        "explicacion": "Los **racimos podridos** sin pelusa gris visible pueden ser por exceso de humedad, daño por insectos o mala ventilación. No es necesariamente botrytis.",
    },
    "agalla_corona_completa": {
        "titulo": "¿Por qué identificamos Agalla de la Corona?",
        "explicacion": "Los **bultos en el tronco** junto con **plantas chicas** indican agalla de la corona. Es una bacteria que forma tumores."
    },
    "agalla_corona_parcial": {
        "titulo": "¿Por qué sospechamos de Agalla de la Corona?",
        "explicacion": "Vimos **bultos en el tronco** pero la planta no está pequeña todavía. Puede ser agalla en etapa inicial. Importante desinfectar herramientas."
    },
    "deficiencia_nutricional": {
        "titulo": "¿Por qué pensamos en Deficiencia Nutricional?",
        "explicacion": "Las **hojas amarillas** con **crecimiento lento** sin otros síntomas sugieren que le faltan nutrientes a la planta (nitrógeno o potasio).",
    },
    "estrés_hidrico": {
        "titulo": "¿Por qué pensamos en Falta de Agua?",
        "explicacion": "Las **hojas caídas** con **tierra seca** es señal clara: tu planta tiene sed. Necesita más riego.",
    },
    "problema_raices": {
        "titulo": "¿Por qué pensamos en Problemas de Raíces?",
        "explicacion": "Las **hojas amarillentas** con **raíces dañadas** indican problemas en el suelo: puede ser mal drenaje o pH inadecuado.",
    },
    "estrés_ambiental": {
        "titulo": "¿Por qué pensamos en Estrés por Calor?",
        "explicacion": "Cuando **no salen uvas después de la flor** y ha hecho **mucho calor**, el problema es el clima. El calor extremo afecta la formación de frutos.",
    },
    "manejo_cultivo": {
        "titulo": "¿Por qué pensamos en Mal Manejo del Cultivo?",
        "explicacion": "Los **racimos desparejos** con **mala poda** indican errores de manejo. No es una plaga, sino cómo se está cuidando la planta."
    },
    "sin_diagnostico": {
        "titulo": "¿Por qué no encontramos una plaga específica?",
        "explicacion": "Los síntomas que marcaste no coinciden con ninguna plaga o enfermedad conocida de la uva. Puede ser un problema diferente.",
    }
}

COMBINACIONES_SINTOMAS = {
    "picaduras_sin_agente": ["picaduras_racimos"],
    "bayas_vacias_sin_avispa": ["bayas_vacias"],
    "racimos_podridos_sin_moho": ["racimos_podridos"],
    "hojas_comidas_sin_gusano": ["hojas_consumidas"],
    "madrigueras_o_racimos": ["madrigueras", "racimos_consumidos"],
    "nodulos_sin_debilidad": ["nódulos_redondeados_raíz"],
    "agallas_sin_enanismo": ["agallas_tallo"]
}

def mostrar_diagnostico_uva(CULTIVOS):
    sintomas_disponibles = CULTIVOS["Uva"]["sintomas"]
    
    st.markdown("### ¿Qué está pasando con tus uvas?")
    st.markdown("Marca lo que ves en tus plantas:")
    
    categorias = {
        "🍃 Hojas": [
            "verrugas_hojas", "hojas_gris_plomizo", "tejido_araña", 
            "hojas_abarquilladas", "hojas_consumidas", "polvillo_blanco",
            "clorosis_hojas", "hojas_marchitas", "hojas_amarrillentas"
        ],
        "🍇 Racimos y frutos": [
            "picaduras_racimos", "bayas_vacias", "racimos_consumidos",
            "moho_gris", "racimos_podridos", "racimos_desiguales"
        ],
        "🌱 Planta completa": [
            "brotacion_lenta", "plantas_debiles", "plantas_pequeñas",
            "crecimiento_lento", "agallas_tallo"
        ],
        "🌿 Raíces": [
            "nudosidades_raices", "nódulos_redondeados_raíz", "raíces_dañadas"
        ],
        "🌸 Flores": [
            "aborto_flores", "flores_no_cuajan"
        ],
        "🐦 Animales presentes": [
            "aves_presentes", "avispa_presencia", "gusano_grande", "madrigueras"
        ],
        "🌡️ Condiciones ambientales": [
            "suelo_seco", "temperatura_alta", "poda_inadecuada"
        ]
    }
    
    sintomas_seleccionados = []
    
    for categoria, sintomas_cat in categorias.items():
        with st.expander(categoria):
            cols = st.columns(2)
            for idx, sintoma_clave in enumerate(sintomas_cat):
                if sintoma_clave and sintoma_clave in sintomas_disponibles:
                    col = cols[idx % 2]
                    texto_mostrar = SINTOMAS_LEGIBLES.get(sintoma_clave, sintoma_clave.replace("_", " "))
                    if col.checkbox(texto_mostrar, key=sintoma_clave):
                        sintomas_seleccionados.append(sintoma_clave)

    st.markdown("---")
    
    if st.button("🔍 Ver qué puede ser", type="primary", use_container_width=True):
        if not sintomas_seleccionados:
            st.warning("⚠️ Marca al menos una cosa que veas en tus plantas")
            return

        motor = SistemaExpertoPlagas()
        resultado = motor.diagnosticar("uva", sintomas_seleccionados)

        if "error" in resultado:
            st.error(resultado["error"])
            return

        diagnosticos = resultado["diagnosticos"]
        if not diagnosticos:
            st.info("🤔 Con estos síntomas no logro identificar el problema. Intenta marcar más detalles o consulta a un técnico agrónomo.")
            return

        diag = diagnosticos[0]
        certeza_pct = int(diag['certeza'] * 100)
        
        st.success(f"### 🎯 Problema identificado: **{diag['plaga']}**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Nivel de seguridad:** {certeza_pct}%")
            st.markdown(f"**Cuándo actuar:** {diag['umbral']}")
            
            st.markdown("#### 💡 Qué hacer:")
            for rec in diag['recomendaciones']:
                st.markdown(f"- {rec}")
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=certeza_pct,
                title={'text': "Confianza"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2e7d32"},
                    'steps': [
                        {'range': [0, 60], 'color': "#ffebee"},
                        {'range': [60, 85], 'color': "#c8e6c9"},
                        {'range': [85, 100], 'color': "#81c784"}
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

        if diag.get("imagen"):
            try:
                st.image(f"images/{diag['imagen']}", caption=f"{diag['plaga']}", use_column_width=True)
            except Exception:
                pass

        if len(diagnosticos) > 1:
            with st.expander("🔄 También podría ser..."):
                for d in diagnosticos[1:]:
                    st.markdown(f"**{d['plaga']}** — Probabilidad: {int(d['certeza']*100)}%")

        # Explicación interactiva de la regla
        regla_usada = diag.get('regla_activada')
        if regla_usada and regla_usada in EXPLICACION_REGLAS:
            with st.expander("🧠 ¿Cómo llegamos a este diagnóstico?", expanded=False):
                info_regla = EXPLICACION_REGLAS[regla_usada]
                
                st.markdown(f"#### {info_regla['titulo']}")
                st.markdown(info_regla['explicacion'])
                
                st.markdown("**📌 Lo que marcaste:**")
                sintomas_texto = [SINTOMAS_LEGIBLES.get(s, s) for s in sintomas_seleccionados]
                for s in sintomas_texto:
                    st.markdown(f"- ✓ {s}")
                
                st.info(f"📖 **Referencia técnica:** {info_regla['referencia']}")
                
                # Sugerencias adicionales basadas en la regla
                if "parcial" in regla_usada or "sospecha" in diag['plaga'].lower():
                    st.warning("⚠️ **Este es un diagnóstico preliminar.** Te sugerimos observar más síntomas o consultar a un especialista para confirmar.")
                    
                    # Sugerencias de qué buscar según la regla
                    sugerencias_busqueda = {
                        "filoxera_parcial": "Revisa las raíces buscando nudosidades o pelotitas.",
                        "aranita_roja_parcial": "Busca telarañas finas en la parte inferior de las hojas.",
                        "acaro_hialino_parcial": "Observa si los brotes tardan en salir en los próximos días.",
                        "picaduras_generales": "Visita tu campo al amanecer y al atardecer para ver si hay aves o avispas.",
                        "bayas_vacias_parcial": "Busca avispas activas en las mañanas cerca de los racimos.",
                        "ratas_raton_parcial": "Busca heces de roedor (negras, ovaladas) o más madrigueras.",
                        "hojas_consumidas_parcial": "Revisa las plantas de noche con una linterna para encontrar larvas grandes.",
                        "nematodos_parcial": "Observa si la planta se debilita en las próximas semanas.",
                        "oidium_parcial": "Revisa los racimos buscando el polvo blanco o flores que se caen.",
                        "podredumbre_gris_parcial": "Verifica si aparecen racimos podridos, especialmente en climas húmedos.",
                        "agalla_corona_parcial": "Monitorea el crecimiento de la planta comparándola con plantas sanas.",
                        "racimos_podridos_general": "Busca moho gris (botrytis) o verifica el riego y ventilación."
                    }
                    
                    if regla_usada in sugerencias_busqueda:
                        st.markdown(f"**🔍 Qué buscar para confirmar:** {sugerencias_busqueda[regla_usada]}")
        else:
            # Si no hay explicación de la regla, mostrar información general
            with st.expander("🧠 ¿Cómo llegamos a este diagnóstico?", expanded=False):
                st.markdown("**📌 Lo que marcaste:**")
                sintomas_texto = [SINTOMAS_LEGIBLES.get(s, s) for s in sintomas_seleccionados]
                for s in sintomas_texto:
                    st.markdown(f"- ✓ {s}")
                
                st.info("Este diagnóstico se basa en la combinación de síntomas que seleccionaste según las reglas del sistema experto.")

        # Información técnica detallada
        with st.expander("⚙️ Información técnica (para especialistas)"):
            st.caption("**Reglas del sistema experto aplicadas:**")
            for r in resultado["reglas_activadas"]:
                st.code(r, language="python")
            
            st.caption("**Síntomas técnicos procesados:**")
            st.json(sintomas_seleccionados)