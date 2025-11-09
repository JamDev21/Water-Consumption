import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from functools import reduce
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import json

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Análisis de Consumo Hídrico",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    </style>
""", unsafe_allow_html=True)

def load_lottiefile(filepath: str):
    """Carga una animación Lottie desde un archivo JSON local"""
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def typewriter_title(text, speed=50, repeat_delay=4000):
    """Crea el efecto de máquina de escribir para el título que se repite"""
    html_code = f"""
    <style>
    
    .typewriter-container {{
        min-height: 80px;
        display: flex;
        align-items: center;
    }}
    
    .typewriter-title {{
        font-size: 2.5rem;
        font-weight: 700;
        color: #055ee4;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        white-space: normal;
        word-wrap: break-word;
        display: inline;
        line-height: 1.3;
        text-shadow: 0 2px 4px rgba(5, 94, 228, 0.2);
    }}
    
    .cursor {{
        display: inline-block;
        width: 3px;
        background-color: #055ee4;
        margin-left: 2px;
        animation: blink 0.75s step-end infinite;
    }}
    
    @keyframes blink {{
        from, to {{ opacity: 1; }}
        50% {{ opacity: 0; }}
    }}
    </style>
    
    <div class="header-wrapper">
        <div class="typewriter-container">
            <span id="typewriter-title" class="typewriter-title"></span>
            <span id="cursor" class="cursor">|</span>
        </div>
    </div>
    
    <script>
    const text = "{text}";
    const speed = {speed};
    const repeatDelay = {repeat_delay};
    let i = 0;
    let isDeleting = false;
    
    function typeWriter() {{
        const element = document.getElementById("typewriter-title");
        
        if (!isDeleting && i < text.length) {{
            element.innerHTML = text.substring(0, i + 1);
            i++;
            setTimeout(typeWriter, speed);
        }} else if (!isDeleting && i === text.length) {{
            setTimeout(() => {{
                isDeleting = true;
                typeWriter();
            }}, repeatDelay);
        }} else if (isDeleting && i > 0) {{
            element.innerHTML = text.substring(0, i - 1);
            i--;
            setTimeout(typeWriter, speed / 2);
        }} else if (isDeleting && i === 0) {{
            isDeleting = false;
            setTimeout(typeWriter, 500);
        }}
    }}
    
    setTimeout(typeWriter, 300);
    </script>
    """
    components.html(html_code, height=130)

def create_stat_card(icon, title, value, color="#0066cc"):
    """Crea una tarjeta estadística con efecto glassmorphism"""
    return f"""
    <div style="
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        transition: all 0.3s ease;
    "
    onmouseover="this.style.transform='translateY(-8px) scale(1.02)'; this.style.boxShadow='0 12px 40px 0 rgba(31, 38, 135, 0.25)';"
    onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px 0 rgba(31, 38, 135, 0.15)';"
    >
        <div style="display: flex; align-items: center; gap: 15px; flex-wrap: wrap;">
            <div style="font-size: 2.8rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">{icon}</div>
            <div style="flex: 1; min-width: 120px;">
                <div style="color: ##03b1f9; font-size: 0.95rem; font-weight: 600; margin-bottom: 5px; text-shadow: 0 1px 2px rgba(255,255,255,0.8);">{title}</div>
                <div style="color: {color}; font-size: 1.9rem; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">{value}</div>
            </div>
        </div>
    </div>
    """

# --- INTERFAZ DE LA APLICACIÓN ---
# Header con Lottie y Título animado
col1, col2 = st.columns([1, 6])

with col1:
    lottie_water = load_lottiefile('riA9NvUSJs.json')
    if lottie_water:
        st_lottie(lottie_water, height=120, key="water_animation")
    else:
        st.markdown("### 💧")

with col2:
    typewriter_title("Analizador de Consumo Hídrico en México", speed=70, repeat_delay=4000)


# --- CARGAR DATOS DESDE CSV ---
@st.cache_data
def cargar_datos_desde_csv(ruta_archivo):
    """Carga los datos de los estados de México desde un archivo CSV"""
    try:
        df = pd.read_csv(ruta_archivo)
        return df
    except FileNotFoundError:
        st.error(f"❌ Error: No se encontró el archivo '{ruta_archivo}'. Asegúrate de que esté en la misma carpeta que tu script.")
        return None

def procesar_datos(df):
    """Aplica conceptos de programación funcional para enriquecer los datos"""
    lista_de_datos = df.to_dict('records')

    def enriquecer_area(area):
        area_nueva = area.copy()
        
        if area_nueva['poblacion'] > 0:
            consumo_per_capita = (area_nueva['consumo_anual_m3'] * 1000) / (area_nueva['poblacion'] * 365)
        else:
            consumo_per_capita = 0
            
        area_nueva['consumo_per_capita_l_dia'] = round(consumo_per_capita)

        if consumo_per_capita > 200:
            area_nueva['nivel_consumo'] = 'Alto'
            area_nueva['color'] = [255, 48, 48]
        elif 100 <= consumo_per_capita <= 200:
            area_nueva['nivel_consumo'] = 'Moderado'
            area_nueva['color'] = [255, 165, 0]
        else:
            area_nueva['nivel_consumo'] = 'Bueno'
            area_nueva['color'] = [34, 139, 34]
            
        return area_nueva

    datos_enriquecidos = list(map(enriquecer_area, lista_de_datos))
    return pd.DataFrame(datos_enriquecidos)

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

# 1. Cargar y procesar datos
df_original = cargar_datos_desde_csv('Consumo_Agua_Estados_rm.csv')

if df_original is not None:
    df_procesado = procesar_datos(df_original)

    # 2. Sidebar mejorado
    with st.sidebar:
        st.markdown("###  Panel de Control")
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
    st.markdown("###  Recomendaciones Personalizadas")

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