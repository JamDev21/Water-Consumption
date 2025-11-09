import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from functools import reduce
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import json
import firebase_admin 
from firebase_admin import credentials, db
import base64


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

@st.cache_data
def get_video_as_base64(file_path):
    """Lee un archivo de video y lo codifica en Base64."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo de video '{file_path}'")
        return None

def hero_section_video(video_src_data, title_text):
    """
    Crea una sección de héroe con un video de fondo, título animado y subtítulo.
    """
    st.markdown(f"""
        <style>
        /* Contenedor principal del hero */
        .hero-container {{
            position: relative;
            width: 100%;
            height: 400px; /* Ajusta la altura según necesites */
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            margin-bottom: 30px;
            border-radius: 15px; /* Bordes redondeados */
            box-shadow: 0 10px 30px rgba(0,0,0,0.2); /* Sombra sutil */
        }}
        
        /* Video de fondo */
        .hero-video {{
            position: absolute;
            top: 50%;
            left: 50%;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            z-index: -1;
            transform: translateX(-50%) translateY(-50%);
            background-size: cover;
            filter: brightness(60%) contrast(110%); /* Oscurece y da contraste al video */
        }}
        
        /* Contenido sobre el video */
        .hero-content {{
            position: relative;
            z-index: 1;
            padding: 20px;
            max-width: 800px;
        }}

        /* Título animado con efecto de máquina de escribir */
        .typewriter-title-hero {{
            font-size: 3.5rem; /* Más grande */
            font-weight: 800;
            color: white;
            text-shadow: 0 4px 10px rgba(0, 0, 0, 0.6), 0 0 15px rgba(5, 94, 228, 0.8); /* Doble sombra para impacto */
            font-family: 'Montserrat', sans-serif; 
            line-height: 1.2;
            margin-bottom: 15px;
        }}

        /* Subtítulo */
        .hero-subtitle {{
            font-size: 1.3rem;
            font-weight: 400;
            color: rgba(255, 255, 255, 0.9);
            text-shadow: 0 2px 5px rgba(0,0,0,0.5);
        }}

        /* Cursor para el typewriter */
        .cursor-hero {{
            display: inline-block;
            width: 5px; /* Más ancho */
            background-color: white;
            margin-left: 5px;
            animation: blink-hero 0.75s step-end infinite;
        }}
        @keyframes blink-hero {{
            from, to {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}
        </style>
        
        <div class="hero-container">
            <video autoplay muted loop class="hero-video">
                <source src="data:video/mp4;base64,{video_src_data}" type="video/mp4">
                Tu navegador no soporta el tag de video.
            </video>
            <div class="hero-content">
                <div class="typewriter-container-hero">
                    <span id="typewriter-title-hero" class="typewriter-title-hero"></span>
                    <span id="cursor-hero" class="cursor-hero">|</span>
                </div>
                <p class="hero-subtitle">
                    Análisis inteligente y estratégico para la gestión del agua en México.
                </p>
            </div>
        </div>

        <script>
        // Script para el efecto de máquina de escribir en el hero
        const textHero = "{title_text}";
        const speedHero = 70;
        const repeatDelayHero = 4000;
        let iHero = 0;
        let isDeletingHero = false;
        
        function typeWriterHero() {{
            const element = document.getElementById("typewriter-title-hero");
            if (!element) return; // Salir si el elemento no existe

            if (!isDeletingHero && iHero < textHero.length) {{
                element.innerHTML = textHero.substring(0, iHero + 1);
                iHero++;
                setTimeout(typeWriterHero, speedHero);
            }} else if (!isDeletingHero && iHero === textHero.length) {{
                setTimeout(() => {{
                    isDeletingHero = true;
                    typeWriterHero();
                }}, repeatDelayHero);
            }} else if (isDeletingHero && iHero > 0) {{
                element.innerHTML = textHero.substring(0, iHero - 1);
                iHero--;
                setTimeout(typeWriterHero, speedHero / 2);
            }} else if (isDeletingHero && iHero === 0) {{
                isDeletingHero = false;
                setTimeout(typeWriterHero, 500);
            }}
        }}
        
        setTimeout(typeWriterHero, 300);
        </script>
    """, unsafe_allow_html=True)

# ----- INICIO DE LA SECCIÓN HERO -----
# 1. Define el nombre de tu archivo de video
video_file_name = "Visualización_Futurista_de_Datos_Hídricos_Mexicanos.mp4"  # <--- !!! REEMPLAZA ESTO POR TU NOMBRE DE ARCHIVO !!!

# 2. Codifica el video
video_base64 = get_video_as_base64(video_file_name)

# 3. Muestra la sección
if video_base64:
    hero_section_video(video_base64, "Analizador Inteligente de Consumo Hídrico")
else:
    # Si el video falla, muestra un título normal como respaldo
    st.title("Analizador Inteligente de Consumo Hídrico")
    st.error(f"No se pudo cargar el video: '{video_file_name}'. Asegúrate de que el nombre sea correcto y esté en la misma carpeta.")

# ----- FIN DE LA SECCIÓN HERO -----

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
    
# --- SISTEMA DE PRODUCCIÓN BASADO EN REGLAS ---

def regla_calcular_consumo_per_capita(hecho):
    """
    Regla de Negocio 1: Calcula el consumo per cápita.
    Un "hecho" (municipio) entra, y un "hecho inferido" (con el nuevo dato) sale.
    """
    hecho_inferido = hecho.copy()
    if hecho_inferido['poblacion'] > 0:
        consumo = (hecho_inferido['consumo_anual_m3'] * 1000) / (hecho_inferido['poblacion'] * 365)
    else:
        consumo = 0
    hecho_inferido['consumo_per_capita_l_dia'] = round(consumo)
    return hecho_inferido

def regla_asignar_nivel_y_color(hecho_calculado):
    """
    Regla de Negocio 2: Asigna el nivel de consumo y el color.
    Aplica lógica para inferir el estado de un municipio basado en su consumo.
    """
    hecho_inferido = hecho_calculado.copy()
    consumo = hecho_inferido['consumo_per_capita_l_dia']
    
    if consumo > 350:  # Umbral Alto (Ajustado)
        hecho_inferido['nivel_consumo'] = 'Alto'
        hecho_inferido['color'] = [255, 48, 48]
    elif 150 <= consumo <= 350: # Umbral Moderado (Ajustado)
        hecho_inferido['nivel_consumo'] = 'Moderado'
        hecho_inferido['color'] = [255, 165, 0]
    else: # Nivel Bueno
        hecho_inferido['nivel_consumo'] = 'Bueno'
        hecho_inferido['color'] = [34, 139, 34]
        
    return hecho_inferido

def motor_de_inferencia(hechos_originales):
    """
    Motor de Inferencia: Aplica la cadena de reglas a la lista de hechos.
    Esto simula la arquitectura de un sistema de producción.
    """
    # 1. Aplicar la primera regla a todos los hechos
    hechos_calculados = list(map(regla_calcular_consumo_per_capita, hechos_originales))
    
    # 2. Aplicar la segunda regla a los resultados de la primera
    nuevos_hechos_inferidos = list(map(regla_asignar_nivel_y_color, hechos_calculados))
    
    return nuevos_hechos_inferidos

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

# 1. Cargar "Hechos" y ejecutar "Inferencia"
hechos_originales = cargar_hechos_firebase()


if hechos_originales:
    # Ejecuta el motor de inferencia para obtener los datos procesados
    lista_datos_inferidos = motor_de_inferencia(hechos_originales)
    df_procesado = pd.DataFrame(lista_datos_inferidos)
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
else:
    st.error("No se pudieron cargar los datos de la base de conocimiento de Firebase.")