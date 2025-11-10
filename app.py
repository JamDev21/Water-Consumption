import streamlit as st
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pydeck as pdk
from functools import reduce
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import json  
import firebase_admin 
from firebase_admin import credentials, db
import base64

st.set_page_config(
    page_title="Análisis de Consumo Hídrico",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)
# --- CONEXIÓN A LA BASE DE CONOCIMIENTO (FIREBASE) ---
@st.cache_resource
def init_firebase():
    """Inicializa la conexión con Firebase usando st.secrets."""
    try:
        # Comprueba si la app ya está inicializada
        firebase_admin.get_app()
    except ValueError:
        # Si no, inicialízala
        
        # --- INICIO DE LA CORRECCIÓN ---
        
        # 1. Convertir el objeto "Secrets" de Streamlit a un dict normal de Python
        cred_dict = dict(st.secrets["firebase_credentials"])
        
        # 2. Corregir los saltos de línea en la llave privada
        cred_dict["private_key"] = cred_dict["private_key"].replace('\\n', '\n')
        
        # --- FIN DE LA CORRECCIÓN ---

        # Ahora cred_dict es un diccionario válido que Firebase puede entender
        cred = credentials.Certificate(cred_dict)
        
        firebase_admin.initialize_app(cred, {
            'databaseURL': f"https://{cred_dict['project_id']}-default-rtdb.firebaseio.com/"
        })

init_firebase()

# ---------------------------------------------------------------------
# --- SECCIÓN MODIFICADA 1: La función `hero_section_video` ---
# ---------------------------------------------------------------------

# Esta es la nueva función 'hero_section_video'.
# Acepta una 'lista' de títulos y tiene un nuevo script de JS.
import streamlit.components.v1 as components
def hero_section_video(video_url, titles_list):
    """
    VERSIÓN FINAL CON VIDEO A ANCHO COMPLETO.
    Usa 'position: fixed' para que el video ocupe todo el iframe.
    """
    
    titles_json = json.dumps(titles_list)
    
    html_string = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* Aseguramos que el HTML y BODY del IFRAME ocupen el 100% */
            body, html {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                font-family: 'Montserrat', sans-serif;
                overflow: hidden; /* Evita scrolls dentro del iframe */
            }}
            
            /* El contenedor principal dentro del iframe */
            .hero-container {{
                position: relative;
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                color: white;
            }}
            
            /* --- ¡CAMBIOS CLAVE AQUÍ EN .hero-video-bg ! --- */
            .hero-video-bg {{
                position: fixed; /* Lo saca del flujo normal */
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: cover; /* Cubre TODO, recortando si es necesario */
                z-index: 0;
                filter: brightness(50%) contrast(110%);
            }}
            
            /* Contenido (texto) */
            .hero-content {{
                position: relative;
                z-index: 1; /* Asegura que el texto esté encima del video */
                padding: 20px;
                max-width: 900px;
            }}
            
            /* Estilo del texto animado */
            .hero-text-animator {{
                font-size: 3.8rem; 
                font-weight: 800;
                color: white;
                text-shadow: 0 5px 15px rgba(0, 0, 0, 0.9);
                line-height: 1.2;
                margin-bottom: 15px;
            }}
            
            /* Estilo del cursor parpadeante */
            .hero-cursor {{
                display: inline-block;
                width: 5px;
                background-color: white;
                margin-left: 8px;
                animation: blink-video 0.75s step-end infinite;
            }}
            
            @keyframes blink-video {{
                from, to {{ opacity: 1; }}
                50% {{ opacity: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="hero-container">
            <video autoplay muted loop class="hero-video-bg">
                <source src="{video_url}" type="video/mp4">
                Tu navegador no soporta el tag de video.
            </video>
            <div class="hero-content">
                <div>
                    <span id="hero-text-animator" class="hero-text-animator"></span>
                    <span class="hero-cursor">|</span>
                </div>
            </div>
        </div>

        <script>
        (function() {{
            console.log("SCRIPT EN IFRAME: ¡Iniciando!");
            const titles = {titles_json};
            const elementId = "hero-text-animator";
            console.log("SCRIPT EN IFRAME: Títulos:", titles);
            console.log("SCRIPT EN IFRAME: Buscando ID:", elementId);
            const speedHero = 70;
            const holdTime = 3000;
            const speedDelete = 40;
            let titleIndex = 0;
            let charIndex = 0;
            let isDeleting = false;
            
            function typeWriterHero() {{
                const element = document.getElementById(elementId);
                if (!element) {{
                    console.error("SCRIPT EN IFRAME: No se encontró el elemento.");
                    return;
                }}
                const currentText = titles[titleIndex];
                if (isDeleting) {{
                    element.innerHTML = currentText.substring(0, charIndex - 1);
                    charIndex--;
                    if (charIndex === 0) {{
                        isDeleting = false;
                        titleIndex = (titleIndex + 1) % titles.length;
                        setTimeout(typeWriterHero, 500);
                    }} else {{
                        setTimeout(typeWriterHero, speedDelete);
                    }}
                }} else {{
                    element.innerHTML = currentText.substring(0, charIndex + 1);
                    charIndex++;
                    if (charIndex === currentText.length) {{
                        isDeleting = true;
                        setTimeout(typeWriterHero, holdTime);
                    }} else {{
                        setTimeout(typeWriterHero, speedHero);
                    }}
                }}
            }}
            setTimeout(typeWriterHero, 50); 
        }})();
        </script>
    </body>
    </html>
    """
    
    components.html(html_string, height=500)
# ---------------------------------------------------------------------
# --- SECCIÓN MODIFICADA 2: La llamada a la función ---
# ---------------------------------------------------------------------

# ----- INICIO DE LA SECCIÓN HERO -----

# 1. Pega aquí la URL "Raw" de tu NUEVO video ("video_fondo.mp4")
VIDEO_URL = "https://raw.githubusercontent.com/JamDev21/Water-Consumption/tema3-logica/video_fondo.mp4" 

# 2. Define la lista de títulos para la transición
hero_titles = [
    "Análisis inteligente y estratégico para la gestión del agua en México.",
    "Decisiones basadas en datos reales.",
    "Planeando el futuro hídrico de México.",
    "Optimización y sostenibilidad con IA.",
    "Plataforma de Inteligencia Hídrica."
]

# 3. Muestra la sección (con lógica simplificada)
if not VIDEO_URL:
    st.error("La variable VIDEO_URL está vacía.")
else:
    # Llamamos a la función con la LISTA de títulos
    hero_section_video(VIDEO_URL, hero_titles)

# ----- FIN DE LA SECCIÓN HERO -----


# --- CONFIGURACIÓN DE LA PÁGINA ---


# --- ESTILOS CSS GLOBALES ---
st.markdown("""
    <style>
    /* Fondo con gradiente sutil */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f4f8 100%);
    }
    
    /* Mejorar headers */
    h1, h2, h3 {
        color: #055ee4;
        font-weight: 600;
    }
    
    /* Tarjetas de métricas con glassmorphism */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: bold;
        color: #0066cc;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
        background: rgba(255, 255, 255, 0.35);
    }
    
    /* Sidebar con glassmorphism */
    [data-testid="stSidebar"] {
    background: #0066CC;
background: linear-gradient(210deg,rgba(0, 102, 204, 1) 31%, rgba(28, 96, 255, 1) 72%, rgba(10, 18, 242, 1) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}
    
    /* Slider con glassmorphism */
    [data-testid="stSlider"] {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 500;
    }
    
    /* Mejorar info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #055ee4;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    /* Selectbox y otros inputs con glassmorphism */
    [data-baseweb="select"], [data-baseweb="popover"] {
        background: rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 8px !important;
    }
    
    /* Menú desplegable con blur */
    [role="listbox"] {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(5, 94, 228, 0.2) !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 32px rgba(5, 94, 228, 0.15) !important;
    }
    
    [role="option"] {
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    
    [role="option"]:hover {
        background: rgba(5, 94, 228, 0.1) !important;
    }
    
    /* Animación de entrada para contenido */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stApp > div > div {
        animation: slideUp 0.5s ease-out;
    }
            
    /* Reemplaza los eventos JS por CSS puro para el hover */
    .stat-card-hover-effect:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
    }}
            
    /* Quita los 'paddings' de los lados y de arriba del contenedor principal */
    .block-container {
       padding-top: 0rem !important;
    }

    div[data-st-component="st.iframe"] {
        /* Usa el truco de 100% del ancho de la ventana (viewport width) */
        width: 100vw !important; 
        
        /* Centra el elemento de ancho completo */
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        
        /* Asegura que no haya márgenes extra */
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    </style>
""", unsafe_allow_html=True)

def create_stat_card(icon, title, value, color="#0066cc"):
    """Crea una tarjeta estadística con efecto glassmorphism (VERSIÓN CSS)"""
    # AÑADIMOS la clase 'stat-card-hover-effect'
    # QUITAMOS 'onmouseover' y 'onmouseout'
    return f"""
    <div class="stat-card-hover-effect" style="
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        transition: all 0.3s ease;
    ">
        <div style="display: flex; align-items: center; gap: 15px; flex-wrap: wrap;">
            <div style="font-size: 2.8rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">{icon}</div>
            <div style="flex: 1; min-width: 120px;">
                <div style="color: ##03b1f9; font-size: 0.95rem; font-weight: 600; margin-bottom: 5px; text-shadow: 0 1px 2px rgba(255,255,255,0.8);">{title}</div>
                <div style="color: {color}; font-size: 1.9rem; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">{value}</div>
            </div>
        </div>
    </div>
    """

@st.cache_data
def cargar_hechos_firebase():
    """Carga los "hechos" (municipios) desde la Base de Conocimiento en Firebase."""
    try:
        ref = db.reference('/municipios')
        hechos = ref.get()

        # --- INICIO DE LA CORRECCIÓN ---
        
        # Verificamos si 'hechos' es una lista (lo que Firebase probablemente hizo)
        if isinstance(hechos, list):
            # Si es una lista, la usamos directamente.
            # Filtramos cualquier 'None' que Firebase pueda haber añadido (suele pasar)
            lista_hechos = [item for item in hechos if item is not None]
            return lista_hechos
        
        # Si NO es una lista, significa que es un diccionario (como esperábamos)
        elif isinstance(hechos, dict):
            lista_hechos = [valor for valor in hechos.values()]
            return lista_hechos
        
        # Si no es ninguna de las dos (ej. es None porque la ruta está mal)
        else:
            st.error("❌ Error: Los datos de Firebase no tienen el formato esperado (ni lista ni diccionario).")
            return None
        
        # --- FIN DE LA CORRECCIÓN ---

    except Exception as e:
        st.error(f"❌ Error al conectar con Firebase: {e}")
        return None
    
# --- SISTEMA DE PRODUCCIÓN BASADO EN LÓGICA DIFUSA (MAMDANI) ---

@st.cache_resource
def crear_sistema_inferencia_difuso():
    """
    Crea y configura el Sistema de Inferencia Difuso (FIS) Mamdani.
    Esto cumple con los indicadores 04 y 06 de la rúbrica del manual.
    """
    
    # 1. Definir Variables (Antecedentes y Consecuentes)
    # Universo de discurso para el consumo (0 a 500 L/día)
    consumo = ctrl.Antecedent(np.arange(0, 501, 1), 'consumo')
    # Universo de discurso para el riesgo (0 a 100 puntos)
    riesgo = ctrl.Consequent(np.arange(0, 101, 1), 'riesgo')

    # 2. Definir Funciones de Pertenencia (Fuzzy Sets)
    # "Analiza el diseño de reglas... si-entonces"
    # El consumo puede ser "bueno", "moderado" o "alto"
    consumo['bueno'] = fuzz.trimf(consumo.universe, [0, 0, 150])
    consumo['moderado'] = fuzz.trimf(consumo.universe, [100, 250, 400])
    consumo['alto'] = fuzz.trimf(consumo.universe, [350, 500, 500])
    
    # El riesgo puede ser "bajo", "medio" o "critico"
    riesgo['bajo'] = fuzz.trimf(riesgo.universe, [0, 0, 40])
    riesgo['medio'] = fuzz.trimf(riesgo.universe, [30, 50, 70])
    riesgo['critico'] = fuzz.trimf(riesgo.universe, [60, 100, 100])

    # 3. Definir las Reglas de Negocio (SI-ENTONCES)
    # "Analiza claramente el uso de reglas"
    regla1 = ctrl.Rule(consumo['bueno'], riesgo['bajo'])
    regla2 = ctrl.Rule(consumo['moderado'], riesgo['medio'])
    regla3 = ctrl.Rule(consumo['alto'], riesgo['critico'])
    
    # 4. Construir el Sistema de Control (Mamdani)
    # "descripción de modelos como Mamdani"
    sistema_control = ctrl.ControlSystem([regla1, regla2, regla3])
    sistema_inferencia = ctrl.ControlSystemSimulation(sistema_control)
    
    return sistema_inferencia


def procesar_hechos_con_logica_difusa(hechos_originales, sistema_inferencia):
    """
    Nuevo "Motor de Inferencia" que usa el sistema de Lógica Difusa.
    Toma los hechos de Firebase y aplica el FIS Mamdani.
    """
    hechos_inferidos = []
    
    for hecho in hechos_originales:
        nuevo_hecho = hecho.copy()
        
        # 1. Calcular el consumo per cápita (dato de entrada "nítido")
        if nuevo_hecho['poblacion'] > 0:
            consumo_calculado = (nuevo_hecho['consumo_anual_m3'] * 1000) / (nuevo_hecho['poblacion'] * 365)
        else:
            consumo_calculado = 0
        
        nuevo_hecho['consumo_per_capita_l_dia'] = round(consumo_calculado)

        # 2. Aplicar Inferencia Difusa
        # "Analiza claramente el uso de inferencia"
        try:
            sistema_inferencia.input['consumo'] = consumo_calculado
            sistema_inferencia.compute()
            riesgo_calculado = sistema_inferencia.output['riesgo']
        except:
            # Fallback por si algun dato de entrada es inválido
            riesgo_calculado = 0
            
        nuevo_hecho['riesgo_difuso'] = round(riesgo_calculado, 2)

        # 3. Asignar color basado en el resultado "difuso" (el riesgo)
        if riesgo_calculado > 70:
            nuevo_hecho['nivel_consumo'] = 'Alto'
            nuevo_hecho['color'] = [255, 48, 48]  # Rojo
        elif riesgo_calculado > 40:
            nuevo_hecho['nivel_consumo'] = 'Moderado'
            nuevo_hecho['color'] = [255, 165, 0] # Naranja
        else:
            nuevo_hecho['nivel_consumo'] = 'Bueno'
            nuevo_hecho['color'] = [34, 139, 34]   # Verde
        
        hechos_inferidos.append(nuevo_hecho)
        
    return hechos_inferidos

def generar_recomendaciones(area):
    """Genera recomendaciones dinámicas basadas en las características de un área"""
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #055ee4 0%, #0ea5e9 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 4px 16px rgba(5, 94, 228, 0.3);
        ">
            <h3 style="color: white; margin: 0;">Recomendaciones para: {area['nombre_area']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    recomendaciones = []
    
    if area['tipo_zona'] in ['Residencial', 'Mixta', 'Servicios']:
        recomendaciones.append(("💡", "Implementar campañas de concienciación sobre el uso de regaderas y grifos ahorradores en zonas urbanas."))
        recomendaciones.append(("🌧️", "Promover la recolección de agua de lluvia para riego de parques y limpieza exterior."))
    if area['tipo_zona'] == 'Industrial':
        recomendaciones.append(("🏭", "Incentivar fiscalmente a las industrias para que realicen auditorías hídricas y optimicen sus procesos."))
        recomendaciones.append(("♻️", "Invertir en tecnologías de tratamiento y reutilización de aguas residuales en corredores industriales."))
    if area['tipo_zona'] == 'Agrícola':
        recomendaciones.append(("🌾", "Modernizar los sistemas de riego para pasar de riego por inundación a riego por goteo, que es mucho más eficiente."))
        
    if area['consumo_per_capita_l_dia'] > 250:
         recomendaciones.append(("⚠️", "ALERTA: Establecer un programa de tarifas progresivas para desincentivar el consumo excesivo y subsidiar a los usuarios eficientes."))
    
    for icon, rec in recomendaciones:
        st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.35);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                padding: 18px;
                border-radius: 12px;
                margin-bottom: 12px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            ">
                <p style="margin: 0; color: ###a3ebe9; text-shadow: 0 1px 2px rgba(255,255,255,0.5);">
                    <span style="font-size: 1.4rem; margin-right: 10px;">{icon}</span>
                    {rec}
                </p>
            </div>
        """, unsafe_allow_html=True)

# --- Carga de datos y lógica principal ---
hechos_originales = cargar_hechos_firebase()

# 1. CREA EL SISTEMA DE INFERENCIA (se cargará desde el caché)
sistema_inferencia = crear_sistema_inferencia_difuso()


if hechos_originales and sistema_inferencia:
    # 2. LLAMA AL NUEVO MOTOR DE LÓGICA DIFUSA
    lista_datos_inferidos = procesar_hechos_con_logica_difusa(hechos_originales, sistema_inferencia)
    df_procesado = pd.DataFrame(lista_datos_inferidos)
    # 2. Sidebar mejorado
    with st.sidebar:
        st.markdown("###  Panel de Control")
        st.markdown("---")
        
        umbral_alto_consumo = st.slider(
            ' Umbral de "Alto Consumo"',
            min_value=100,
            max_value=300,
            value=200, 
            step=10,
            help="Define el límite en litros por persona por día"
        )
        
        st.markdown("---")
        
        tipos_zona_filtro = st.multiselect(
            'Vocación Económica',
            options=df_procesado['tipo_zona'].unique(),
            default=df_procesado['tipo_zona'].unique(),
            help="Filtra por tipo de actividad económica"
        )
        
        st.markdown("---")
        st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                padding: 15px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                margin-top: 20px;
            ">
                <p style="color: white; font-size: 0.9rem; margin: 0; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">
                    💡 <strong>Tip:</strong> Ajusta los filtros para explorar diferentes escenarios de consumo
                </p>
            </div>
        """, unsafe_allow_html=True)

    # 3. Aplicar filtros
    df_filtrado = df_procesado[df_procesado['tipo_zona'].isin(tipos_zona_filtro)]
    datos_filtrados_lista = df_filtrado.to_dict('records')

    areas_alto_consumo_lista = list(filter(
        lambda area: area['consumo_per_capita_l_dia'] > umbral_alto_consumo,
        datos_filtrados_lista
    ))
    df_alto_consumo = pd.DataFrame(areas_alto_consumo_lista)

    # 4. Dashboard Principal con tarjetas mejoradas
    st.markdown("### Indicadores Clave")
    
    col1, col2, col3 = st.columns(3)

    if not df_alto_consumo.empty:
        poblacion_afectada = reduce(
            lambda total, area: total + area['poblacion'],
            areas_alto_consumo_lista,
            0
        )
        consumo_total_alto_consumo_m3 = reduce(
            lambda total, area: total + area['consumo_anual_m3'],
            areas_alto_consumo_lista,
            0
        )
    else:
        poblacion_afectada = 0
        consumo_total_alto_consumo_m3 = 0

    with col1:
        st.markdown(create_stat_card("🚨", "Estados con Alto Consumo", len(df_alto_consumo), "#ef4444"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_stat_card("👥", "Población Afectada", f"{poblacion_afectada:,}", "#f59e0b"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_stat_card("💧", "Consumo Anual Total", f"{consumo_total_alto_consumo_m3:,} m³", "#3b82f6"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Sección de mapa
    st.markdown("### Distribución Geográfica")
    
    if df_alto_consumo.empty:
        st.warning("⚠️ No se encontraron estados que superen el umbral de alto consumo seleccionado.")
    else:
        st.info(f"📍 Mostrando **{len(df_alto_consumo)} estados** que superan los **{umbral_alto_consumo} L/persona/día**")
        
        view_state = pdk.ViewState(
            latitude=23.6345,
            longitude=-102.5528,
            zoom=4,
            pitch=45
        )

        layer = pdk.Layer(
            'ScatterplotLayer',
            data=df_filtrado,
            get_position='[lon, lat]',
            get_color='color',
            get_radius=3000,
            pickable=True,
            auto_highlight=True
        )

        tooltip = {
            "html": "<b> Municipio:</b> {nombre_area}, {estado}<br/>"
                    "<b> Población:</b> {poblacion}<br/>"
                    "<b> Nivel de Consumo:</b> {nivel_consumo}<br/>"
                    "<b> Consumo per cápita:</b> {consumo_per_capita_l_dia} L/día",
            "style": {
                "backgroundColor": "white",
                "color": "#1e293b",
                "fontSize": "14px",
                "padding": "10px",
                "borderRadius": "8px"
            }
        }

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip
        )   
        
        st.pydeck_chart(deck, use_container_width=True)

    # 6. Recomendaciones
    st.markdown("###  Recomendaciones Personalizadas")

    if not df_alto_consumo.empty:
        area_seleccionada_nombre = st.selectbox(
            "Selecciona un estado para ver recomendaciones específicas:",
            options=df_alto_consumo['nombre_area'].tolist(),
            help="Elige un estado para obtener estrategias de conservación adaptadas"
        )
        
        area_seleccionada_dict = next(
            (area for area in areas_alto_consumo_lista if area['nombre_area'] == area_seleccionada_nombre), None
        )
        
        if area_seleccionada_dict:
            generar_recomendaciones(area_seleccionada_dict)
    else:
        st.info("✅ No hay estados con alto consumo para generar recomendaciones.")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #6b7280; padding: 20px;">
            <p>💧 Dashboard de Análisis Hídrico | Desarrollado por JamDev21</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("No se pudieron cargar los datos de la base de conocimiento de Firebase.")