"""
App de Streamlit: vigilancia epidemiológica del dengue en el Perú (2000–2025)
Gráficos interactivos con Highcharts. Autora: Selene Ramos Orue
"""
import html
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from sklearn.metrics import silhouette_score

import textos as tx

DATA = Path(__file__).parent / "data"
HC_VERSION = "11.4.8"

st.set_page_config(page_title="Dengue en el Perú", page_icon="🦟", layout="wide")

# ---------------------------------------------------------------------------
# Estilo de la página
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stMarkdown, p, li, label { font-family: 'Poppins', sans-serif; }
.stApp { background: radial-gradient(circle at 100% 0%, #ece9ff 0%, rgba(236,233,255,0) 35%),
                     radial-gradient(circle at 0% 60%, #e3f6ef 0%, rgba(227,246,239,0) 30%), #f7f8fb; }
.block-container { padding-top: 2.2rem; max-width: 1250px; }
.stMarkdown p, .stMarkdown li { font-size: 0.97rem; line-height: 1.7; color: #374151; }

/* Encabezado */
.hero { position: relative; overflow: hidden; border-radius: 24px; padding: 34px 38px 30px;
        background: linear-gradient(120deg, #1e1b4b 0%, #4c3fc4 45%, #2a78d6 78%, #1baf7a 100%);
        box-shadow: 0 18px 40px rgba(76, 63, 196, 0.28); margin-bottom: 22px; }
.hero::before, .hero::after { content: ""; position: absolute; border-radius: 50%; background: rgba(255,255,255,0.08); }
.hero::before { width: 320px; height: 320px; right: -80px; top: -140px; }
.hero::after { width: 200px; height: 200px; right: 160px; bottom: -120px; }
.hero-tag { display: inline-block; font-size: 0.75rem; letter-spacing: .08em; text-transform: uppercase;
            color: #c7d2fe; font-weight: 600; margin-bottom: 6px; }
.hero h1 { color: #ffffff !important; font-size: 2.5rem !important; font-weight: 700 !important;
           margin: 0 0 6px 0 !important; padding: 0 !important; line-height: 1.15 !important; }
.hero p { color: #e0e7ff !important; font-size: 1.02rem !important; margin: 0 0 16px 0 !important; max-width: 720px; }
.chip { display: inline-block; background: rgba(255,255,255,0.14); color: #ffffff; border: 1px solid rgba(255,255,255,0.25);
        padding: 5px 13px; border-radius: 999px; font-size: 0.8rem; margin: 0 6px 6px 0; backdrop-filter: blur(4px); }

/* Indicadores */
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 26px; }
@media (max-width: 900px) { .kpis { grid-template-columns: repeat(2, 1fr); } }
.kpi { position: relative; background: #ffffff; border-radius: 18px; padding: 18px 20px 16px;
       box-shadow: 0 8px 24px rgba(31, 41, 55, 0.07); overflow: hidden; }
.kpi::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 4px;
              background: linear-gradient(90deg, var(--c), var(--c2)); }
.kpi-top { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.kpi-ico { width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
           font-size: 1.15rem; background: var(--bg); }
.kpi-lbl { font-size: 0.82rem; color: #6b7280; font-weight: 500; line-height: 1.25; }
.kpi-val { font-size: 1.95rem; font-weight: 700; color: #1f2937; line-height: 1.1; }
.kpi-sub { font-size: 0.78rem; color: #9ca3af; margin-top: 2px; }

/* Pestañas tipo botón */
[data-baseweb="tab-list"] { gap: 8px; flex-wrap: wrap; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none; }
button[data-baseweb="tab"], [data-testid="stTab"] { background: #ffffff; border-radius: 999px; padding: 8px 18px !important;
       box-shadow: 0 3px 10px rgba(31,41,55,0.06); border: 1px solid #eceef3; height: auto; }
button[data-baseweb="tab"] p, [data-testid="stTab"] p { font-weight: 500; font-size: 0.92rem; }
button[data-baseweb="tab"][aria-selected="true"], [data-testid="stTab"][aria-selected="true"] { background: linear-gradient(90deg, #6250d6, #2a78d6); border-color: transparent; }
button[data-baseweb="tab"][aria-selected="true"] p, [data-testid="stTab"][aria-selected="true"] p { color: #ffffff; }

/* Títulos de sección */
.sec { display: flex; align-items: center; gap: 14px; margin: 34px 0 10px; }
.sec-n { min-width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center;
         color: #ffffff; font-weight: 700; font-size: 0.95rem;
         background: linear-gradient(135deg, #6250d6, #2a78d6); box-shadow: 0 6px 14px rgba(98,80,214,0.3); }
.sec-t { font-size: 1.45rem; font-weight: 700; color: #1f2937; line-height: 1.2; }

/* Gráficos */
iframe { border-radius: 18px; box-shadow: 0 8px 26px rgba(31, 41, 55, 0.08); background: #ffffff; }

/* Recuadros de interpretación */
[class*="st-key-interp"] { background: #ffffff; border-radius: 16px; padding: 18px 22px 6px;
       border-left: 5px solid #1baf7a; box-shadow: 0 6px 20px rgba(31, 41, 55, 0.06); margin: 6px 0 12px; }
[class*="st-key-interp"]::before { content: "Interpretación"; display: inline-block; font-size: 0.72rem; font-weight: 600;
       letter-spacing: .07em; text-transform: uppercase; color: #138a60; background: #e3f6ef;
       padding: 3px 10px; border-radius: 999px; margin-bottom: 4px; }

/* Tarjetas de inicio */
.card { background: #ffffff; border-radius: 18px; padding: 20px 22px; height: 100%;
        box-shadow: 0 8px 24px rgba(31, 41, 55, 0.07); border-top: 4px solid var(--c); }
.card-ico { font-size: 1.6rem; margin-bottom: 6px; }
.card-t { font-weight: 600; color: #1f2937; margin-bottom: 4px; }
.card-d { font-size: 0.88rem; color: #6b7280; line-height: 1.55; }

/* Glosario */
.glos { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 8px; }
@media (max-width: 1000px) { .glos { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .glos { grid-template-columns: 1fr; } }
.term { background: #ffffff; border-radius: 16px; padding: 16px 18px 14px; position: relative;
        box-shadow: 0 6px 20px rgba(31, 41, 55, 0.06); border: 1px solid #eef0f4; transition: transform .15s, box-shadow .15s; }
.term:hover { transform: translateY(-3px); box-shadow: 0 12px 28px rgba(31, 41, 55, 0.10); }
.term-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px; }
.term-t { font-weight: 700; color: #1f2937; font-size: 1.02rem; }
.term-cat { font-size: 0.68rem; font-weight: 600; letter-spacing: .05em; text-transform: uppercase;
            padding: 3px 9px; border-radius: 999px; color: var(--c); background: var(--bg); white-space: nowrap; }
.term-d { font-size: 0.88rem; color: #4b5563; line-height: 1.6; }
.term-u { font-size: 0.78rem; color: #6b7280; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #e5e7eb; }
.term-u b { color: var(--c); font-weight: 600; }
.glos-count { font-size: 0.85rem; color: #6b7280; margin: 4px 0 2px; }

/* Pestaña Datos */
.ficha { background: #ffffff; border-radius: 18px; padding: 18px 20px; box-shadow: 0 8px 24px rgba(31,41,55,0.07);
         border-top: 4px solid #0ea5a4; }
.ficha-t { font-weight: 700; color: #1f2937; margin-bottom: 8px; }
.ficha-r { display: flex; justify-content: space-between; gap: 12px; padding: 7px 0; border-bottom: 1px dashed #e5e7eb;
           font-size: 0.86rem; }
.ficha-r:last-child { border-bottom: none; }
.ficha-r span { color: #6b7280; } .ficha-r b { color: #1f2937; font-weight: 600; text-align: right; }
.dtable-wrap { background: #ffffff; border-radius: 18px; box-shadow: 0 8px 24px rgba(31,41,55,0.07);
               overflow-x: auto; margin: 6px 0 10px; }
.dtable { width: 100%; border-collapse: collapse; font-size: 0.86rem; }
.dtable th { text-align: left; background: linear-gradient(90deg, #1e1b4b, #4c3fc4); color: #ffffff;
             padding: 12px 14px; font-weight: 600; }
.dtable td { padding: 10px 14px; border-bottom: 1px solid #f0f1f5; color: #374151; vertical-align: top; }
.dtable tr:nth-child(even) td { background: #fafafe; }
.dtable tr:hover td { background: #f1efff; }
.dtable code { background: #efedfc; color: #4c3fc4; padding: 2px 7px; border-radius: 6px; font-size: 0.82rem; }
.dtable tr.fila-nouso td { color: #9ca3af; }
.origen { font-size: 0.72rem; font-weight: 600; padding: 3px 9px; border-radius: 999px; white-space: nowrap; }
.o-orig { background: #e6f0fc; color: #1d5fae; } .o-creada { background: #e3f6ef; color: #138a60; }
.o-nouso { background: #f3f4f6; color: #9ca3af; }
.cat-card { background: #ffffff; border-radius: 16px; padding: 16px 16px 10px; box-shadow: 0 6px 20px rgba(31,41,55,0.06);
            height: 100%; }
.cat-t { font-weight: 700; color: #1f2937; font-size: 0.95rem; margin-bottom: 8px; }
.cat-card { margin-bottom: 16px; }
.ctable, .ctable tr, .ctable td { border: none !important; }
.ctable { width: 100%; border-collapse: collapse; font-size: 0.86rem; display: table; }
.ctable td { padding: 7px 4px; border-bottom: 1px solid #f0f1f5 !important; color: #374151; }
.ctable td:first-child { width: 45%; }
.ctable td.num { text-align: right; white-space: nowrap; }
.barra { display: inline-block; width: 120px; height: 6px; background: #eef0f3; border-radius: 999px; margin-right: 6px;
         vertical-align: middle; overflow: hidden; }
.barra span { display: block; height: 100%; background: linear-gradient(90deg, #6250d6, #2a78d6); border-radius: 999px; }

/* Barra lateral */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1e1b4b 0%, #312e81 60%, #3b3399 100%); }
[data-testid="stSidebar"] * { color: #e0e7ff; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #e0e7ff !important; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #1f2937; }
[data-testid="stSidebar"] [data-baseweb="tag"] { background: #6250d6 !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] * { color: #ffffff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
.side-t { font-size: 1.25rem; font-weight: 700; color: #ffffff !important; margin-bottom: 2px; }
.side-s { font-size: 0.82rem; color: #c7d2fe !important; margin-bottom: 14px; }
.side-box { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px;
            padding: 12px 14px; font-size: 0.8rem; line-height: 1.5; color: #c7d2fe !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Paleta y tema de Highcharts (el mismo del Rmd)
# ---------------------------------------------------------------------------
PAL = {"azul": "#2a78d6", "naranja": "#eb6834", "aqua": "#1baf7a", "violeta": "#6250d6"}
FUENTE = "Fuente: CDC Perú – MINSA"


def grad(c1, c2):
    """Degradado de arriba hacia abajo (en barras horizontales va a lo largo de la barra)."""
    return {"linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1}, "stops": [[0, c1], [1, c2]]}


TEMA = {
    "colors": list(PAL.values()),
    "chart": {"backgroundColor": "#ffffff", "style": {"fontFamily": "Poppins, sans-serif"}},
    "title": {"align": "left", "style": {"color": "#1f2937", "fontWeight": "600", "fontSize": "17px"}},
    "subtitle": {"align": "left", "style": {"color": "#6b7280", "fontSize": "12px"}},
    "xAxis": {"lineColor": "#e5e7eb", "tickColor": "#e5e7eb",
              "labels": {"style": {"color": "#6b7280"}}, "title": {"style": {"color": "#6b7280"}}},
    "yAxis": {"gridLineColor": "#eef0f3", "gridLineDashStyle": "Dash",
              "labels": {"style": {"color": "#6b7280"}}, "title": {"style": {"color": "#6b7280"}}},
    "legend": {"itemStyle": {"color": "#374151", "fontWeight": "500"}},
    "tooltip": {"backgroundColor": "rgba(255,255,255,0.97)", "borderWidth": 0, "borderRadius": 10,
                "shadow": True, "style": {"color": "#1f2937", "fontSize": "12px"}},
    "plotOptions": {"series": {"animation": {"duration": 1000}},
                    "column": {"borderRadius": 5, "borderWidth": 0},
                    "bar": {"borderRadius": 5, "borderWidth": 0},
                    "pie": {"borderWidth": 3, "borderColor": "#ffffff"}},
    "credits": {"enabled": True, "text": FUENTE, "href": "",
                "style": {"color": "#9ca3af"}},
    "lang": {"thousandsSep": ",", "decimalPoint": ".", "drillUpText": "◁ Volver a {series.name}",
             "rangeSelectorZoom": "Ver", "resetZoom": "Quitar zoom",
             "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                        "Septiembre", "Octubre", "Noviembre", "Diciembre"],
             "shortMonths": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct",
                             "Nov", "Dic"],
             "weekdays": ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
             "contextButtonTitle": "Menú", "downloadPNG": "Descargar PNG",
             "downloadJPEG": "Descargar JPEG", "downloadSVG": "Descargar SVG",
             "downloadPDF": "Descargar PDF", "viewFullscreen": "Pantalla completa",
             "exitFullscreen": "Salir de pantalla completa", "printChart": "Imprimir"},
    "exporting": {"buttons": {"contextButton": {
        "menuItems": ["viewFullscreen", "downloadPNG", "downloadSVG"]}}},
}


class JS(str):
    """Marca un texto como código JavaScript (por ejemplo, un formatter)."""


def _a_json(obj, funciones):
    if isinstance(obj, JS):
        funciones.append(str(obj))
        return f"__JSFUNC{len(funciones) - 1}__"
    if isinstance(obj, dict):
        return {k: _a_json(v, funciones) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_a_json(v, funciones) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return None if np.isnan(obj) else float(obj)
    return obj


def hc(opciones, tipo="chart", alto=440):
    """Dibuja un gráfico de Highcharts dentro de la app."""
    funciones = []
    texto = json.dumps(_a_json(opciones, funciones), ensure_ascii=False)
    for i, f in enumerate(funciones):
        texto = texto.replace(f'"__JSFUNC{i}__"', f)
    base = f"https://cdn.jsdelivr.net/npm/highcharts@{HC_VERSION}"
    modulos = ["modules/stock.js", "modules/map.js", "modules/heatmap.js",
               "modules/drilldown.js", "modules/exporting.js"]
    scripts = f'<script src="{base}/highcharts.js"></script>' + "".join(
        f'<script src="{base}/{m}"></script>' for m in modulos)
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
{scripts}
<style>html,body{{margin:0;padding:0;background:#ffffff;font-family:Poppins,sans-serif}}
#c{{height:{alto - 20}px;padding:8px 6px}}</style></head>
<body><div id="c"></div><script>
Highcharts.setOptions({json.dumps(TEMA, ensure_ascii=False)});
Highcharts.{tipo}('c', {texto});
</script></body></html>"""
    components.html(html, height=alto, scrolling=False)


# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------
@st.cache_data
def cargar():
    agg = pd.read_parquet(DATA / "casos_agregados.parquet")
    prov = pd.read_parquet(DATA / "casos_provincia.parquet")
    for c in ["departamento", "enfermedad", "tipo_dx", "sexo", "grupo_edad"]:
        agg[c] = agg[c].astype(str)
    mapa = json.loads((DATA / "pe-all.geo.json").read_text(encoding="utf-8"))
    return agg, prov, mapa


agg_total, prov_total, MAPA_PE = cargar()

CODIGOS = {
    "AMAZONAS": "pe-am", "ANCASH": "pe-an", "APURIMAC": "pe-ap", "AREQUIPA": "pe-ar",
    "AYACUCHO": "pe-ay", "CAJAMARCA": "pe-cj", "CALLAO": "pe-cl", "CUSCO": "pe-cs",
    "HUANCAVELICA": "pe-hv", "HUANUCO": "pe-hc", "ICA": "pe-ic", "JUNIN": "pe-ju",
    "LA LIBERTAD": "pe-ll", "LAMBAYEQUE": "pe-lb", "LORETO": "pe-lo", "MADRE DE DIOS": "pe-md",
    "MOQUEGUA": "pe-mq", "PASCO": "pe-pa", "PIURA": "pe-pi", "PUNO": "pe-pu",
    "SAN MARTIN": "pe-sm", "TACNA": "pe-ta", "TUMBES": "pe-tu", "UCAYALI": "pe-uc",
}
SIN_ALARMA = "Dengue sin signos de alarma"
GRAVEDADES = [SIN_ALARMA, "Dengue con signos de alarma", "Dengue grave"]
EDADES = ["0-4", "5-11", "12-17", "18-29", "30-59", "60+"]


def fmt(n):
    return f"{int(round(n)):,}"


_contador = {"sec": 0, "interp": 0}


def seccion(titulo):
    """Título de sección con número."""
    _contador["sec"] += 1
    st.markdown(f'<div class="sec"><div class="sec-n">{_contador["sec"]:02d}</div>'
                f'<div class="sec-t">{titulo}</div></div>', unsafe_allow_html=True)


def interp(texto):
    """Recuadro con la interpretación del gráfico."""
    _contador["interp"] += 1
    with st.container(key=f"interp_{_contador['interp']}"):
        st.markdown(texto)


# ---------------------------------------------------------------------------
# Barra lateral: filtros
# ---------------------------------------------------------------------------
anio_min, anio_max_total = int(agg_total["ano"].min()), int(agg_total["ano"].max())
with st.sidebar:
    st.markdown('<div class="side-t">🦟 Filtros</div><div class="side-s">Elige el periodo y los departamentos</div>',
                unsafe_allow_html=True)
    rango = st.slider("Años", anio_min, anio_max_total, (anio_min, anio_max_total))
    deptos_todos = sorted(agg_total["departamento"].unique())
    deptos = st.multiselect("Departamentos", deptos_todos, placeholder="Todos los departamentos")
    st.markdown(f'<div class="side-box">{tx.AVISO_FILTROS.strip()}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="side-box"><b>Autora:</b> Selene Ramos Orue<br><b>Datos:</b> CDC Perú – MINSA<br>'
                '<b>Gráficos:</b> Highcharts</div>', unsafe_allow_html=True)

agg = agg_total[(agg_total["ano"] >= rango[0]) & (agg_total["ano"] <= rango[1])]
prov = prov_total[(prov_total["ano"] >= rango[0]) & (prov_total["ano"] <= rango[1])]
if deptos:
    agg = agg[agg["departamento"].isin(deptos)]
    prov = prov[prov["departamento"].isin(deptos)]

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
  <div class="hero-tag">Vigilancia epidemiológica · CDC Perú – MINSA</div>
  <h1>Dengue en el Perú, {anio_min}–{anio_max_total}</h1>
  <p>Cuándo, dónde y a quiénes afecta el dengue, contado con gráficos interactivos en Highcharts.</p>
  <span class="chip">📅 {rango[0]}–{rango[1]}</span>
  <span class="chip">📍 {"Todo el Perú" if not deptos else f"{len(deptos)} departamento(s)"}</span>
  <span class="chip">📊 Más de 1 millón de registros</span>
</div>""", unsafe_allow_html=True)

if agg.empty:
    st.warning("No hay casos con los filtros elegidos. Prueba con otro rango de años o departamentos.")
    st.stop()

por_anio = agg.groupby("ano")["casos"].sum()
desde_2011 = agg[agg["ano"] >= 2011]
pct_alarma = 100 * desde_2011.loc[desde_2011["enfermedad"] != SIN_ALARMA, "casos"].sum() / \
    max(desde_2011["casos"].sum(), 1)
sexo_ok = agg[agg["sexo"].isin(["Masculino", "Femenino"])]
pct_muj = 100 * sexo_ok.loc[sexo_ok["sexo"] == "Femenino", "casos"].sum() / max(sexo_ok["casos"].sum(), 1)

def kpi(ico, etiqueta, valor, sub, c, c2, bg):
    return (f'<div class="kpi" style="--c:{c};--c2:{c2};--bg:{bg}"><div class="kpi-top">'
            f'<div class="kpi-ico">{ico}</div><div class="kpi-lbl">{etiqueta}</div></div>'
            f'<div class="kpi-val">{valor}</div><div class="kpi-sub">{sub}</div></div>')


st.markdown('<div class="kpis">'
            + kpi("🦟", "Casos notificados", fmt(agg["casos"].sum()), f"{rango[0]}–{rango[1]}",
                  "#2a78d6", "#6250d6", "#e6f0fc")
            + kpi("📈", "Año con más casos", f"{por_anio.idxmax()}", f"{fmt(por_anio.max())} casos",
                  "#eb6834", "#f59e6b", "#fdeee6")
            + kpi("⚠️", "Con signos de alarma o graves", f"{pct_alarma:.1f} %", "casos desde 2011",
                  "#6250d6", "#8a7cf0", "#efedfc")
            + kpi("👩", "Casos en mujeres", f"{pct_muj:.1f} %", "del total con sexo registrado",
                  "#1baf7a", "#2fd096", "#e3f6ef")
            + '</div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 Inicio", "📋 Datos", "📈 Tiempo", "🗺️ Territorio", "👥 Población", "🧩 Clustering",
                "📖 Glosario", "✅ Conclusiones"])

# ---------------------------------------------------------------------------
# Inicio
# ---------------------------------------------------------------------------
with tabs[0]:
    _contador["sec"] = 0
    tarjetas = [("📋", "Datos", "Origen de la base, diccionario de variables y casos por categoría.", "#0ea5a4"),
                ("📈", "Tiempo", "Casos por año, serie semanal con zoom y estacionalidad.", "#2a78d6"),
                ("🗺️", "Territorio", "Mapa del Perú y drilldown de departamento a provincia.", "#1baf7a"),
                ("👥", "Población", "Gravedad, edad, sexo y tipo de diagnóstico.", "#eb6834"),
                ("🧩", "Clustering", "Grupos de departamentos con perfiles parecidos.", "#6250d6"),
                ("📖", "Glosario", f"{len(tx.GLOSARIO)} términos explicados en palabras sencillas.", "#e87ba4")]
    cols = st.columns(len(tarjetas), gap="small")
    for col, (ico, t, d, c) in zip(cols, tarjetas):
        col.markdown(f'<div class="card" style="--c:{c}"><div class="card-ico">{ico}</div>'
                     f'<div class="card-t">{t}</div><div class="card-d">{d}</div></div>', unsafe_allow_html=True)
    st.write("")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        seccion("Sobre la app")
        st.markdown(tx.INTRO)
    with c2:
        seccion("Cómo usar la app")
        st.markdown(tx.COMO_USAR)

# ---------------------------------------------------------------------------
# Datos: descripción de la base
# ---------------------------------------------------------------------------
with tabs[1]:
    _contador["sec"] = 0
    seccion("Descripción de los datos")
    st.markdown(tx.DATOS_INTRO)
    total_casos = agg_total["casos"].sum()
    n_dep = agg_total["departamento"].nunique()
    n_prov = prov_total[["departamento", "provincia"]].drop_duplicates().shape[0]
    sin_edad = agg_total.loc[agg_total["grupo_edad"] == "Sin dato", "casos"].sum()
    st.markdown('<div class="kpis">'
                + kpi("🧾", "Registros (casos)", fmt(total_casos), "una fila = un caso notificado",
                      "#2a78d6", "#6250d6", "#e6f0fc")
                + kpi("📅", "Periodo", f"{anio_min}–{anio_max_total}",
                      f"{anio_max_total - anio_min + 1} años, por semana epidemiológica", "#eb6834", "#f59e6b", "#fdeee6")
                + kpi("📍", "Departamentos", f"{n_dep}", f"{n_prov} provincias con casos",
                      "#1baf7a", "#2fd096", "#e3f6ef")
                + kpi("🔢", "Variables", "15 + 4", "originales + creadas en la limpieza",
                      "#6250d6", "#8a7cf0", "#efedfc")
                + '</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2], gap="large")
    with c1:
        st.markdown(tx.DATOS)
    with c2:
        st.markdown(f"""<div class="ficha">
<div class="ficha-t">Ficha de la base</div>
<div class="ficha-r"><span>Nombre</span><b>Vigilancia Epidemiológica de dengue</b></div>
<div class="ficha-r"><span>Fuente</span><b>CDC Perú – MINSA</b></div>
<div class="ficha-r"><span>Publicada en</span><b>Plataforma Nacional de Datos Abiertos</b></div>
<div class="ficha-r"><span>Formato original</span><b>CSV, más de 100 MB</b></div>
<div class="ficha-r"><span>Unidad de análisis</span><b>Caso notificado</b></div>
<div class="ficha-r"><span>Nivel geográfico</span><b>Lugar probable de infección</b></div>
<div class="ficha-r"><span>Casos sin edad</span><b>{fmt(sin_edad)} ({100 * sin_edad / total_casos:.2f} %)</b></div>
<div class="ficha-r"><span>Estado</span><b>Datos provisionales</b></div>
</div>""", unsafe_allow_html=True)

    seccion("Diccionario de variables")
    st.markdown(tx.DATOS_TABLA)
    valores_din = {"n_dep": n_dep, "n_prov": n_prov, "anio_min": anio_min, "anio_max": anio_max_total}
    filas = []
    for var, tipo, origen, desc, valores in tx.DICCIONARIO:
        clase = "o-creada" if origen == "Creada" else ("o-nouso" if "no se usa" in origen else "o-orig")
        filas.append(f'<tr class="{"fila-nouso" if clase == "o-nouso" else ""}"><td><code>{var}</code></td>'
                     f'<td>{tipo}</td><td><span class="origen {clase}">{origen}</span></td>'
                     f'<td>{html.escape(desc)}</td><td>{html.escape(valores.format(**valores_din))}</td></tr>')
    st.markdown('<div class="dtable-wrap"><table class="dtable"><thead><tr><th>Variable</th><th>Tipo</th>'
                '<th>Origen</th><th>Descripción</th><th>Valores</th></tr></thead><tbody>'
                + "".join(filas) + '</tbody></table></div>', unsafe_allow_html=True)

    seccion("Casos por categoría")
    st.markdown(tx.DATOS_CATEGORIAS)
    orden_cat = {"enfermedad": GRAVEDADES, "grupo_edad": EDADES,
                 "sexo": ["Femenino", "Masculino"], "tipo_dx": ["Confirmado", "Probable", "Sospechoso"]}
    nombres = {"enfermedad": "Gravedad (enfermedad)", "tipo_dx": "Tipo de diagnóstico",
               "sexo": "Sexo", "grupo_edad": "Grupo de edad"}
    cols = st.columns(2, gap="medium") + st.columns(2, gap="medium")
    for col, var in zip(cols, ["enfermedad", "grupo_edad", "tipo_dx", "sexo"]):
        cnt = agg_total.groupby(var)["casos"].sum()
        orden = [c for c in orden_cat[var] if c in cnt.index] + [c for c in cnt.index if c not in orden_cat[var]]
        cnt = cnt.reindex(orden)
        filas = "".join(
            f'<tr><td>{html.escape(str(c).replace("Dengue ", "").capitalize())}</td><td class="num">{fmt(v)}</td>'
            f'<td class="num"><div class="barra"><span style="width:{100 * v / total_casos:.1f}%"></span></div>'
            f'{100 * v / total_casos:.1f} %</td></tr>' for c, v in cnt.items())
        col.markdown(f'<div class="cat-card"><div class="cat-t">{nombres[var]}</div>'
                     f'<table class="ctable"><tbody>{filas}</tbody></table></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Tiempo
# ---------------------------------------------------------------------------
with tabs[2]:
    _contador["sec"] = 0
    # Casos por año
    seccion("Casos por año")
    st.markdown(tx.ANIO_ANTES)
    pico = por_anio.idxmax()
    puntos = [{"x": int(a), "y": int(v),
               **({"color": grad("#f59e6b", PAL["naranja"])} if a == pico else {})}
              for a, v in por_anio.items()]
    hc({
        "chart": {"type": "column"},
        "title": {"text": f"Casos de dengue notificados por año, {rango[0]}–{rango[1]}"},
        "subtitle": {"text": f"En naranja el año con más casos ({pico})"},
        "xAxis": {"title": {"text": "Año"}, "allowDecimals": False},
        "yAxis": {"title": {"text": "Número de casos"}},
        "legend": {"enabled": False},
        "tooltip": {"pointFormat": "<b>{point.y:,.0f}</b> casos", "headerFormat": "Año {point.x}<br>"},
        "series": [{"name": "Casos", "data": puntos, "color": grad(PAL["azul"], PAL["violeta"])}],
    })
    pa = agg_total.groupby("ano")["casos"].sum()
    interp(tx.ANIO_DESPUES.format(
        anio_max=pa.idxmax(), casos_max=fmt(pa.max()),
        casos_2324=fmt(pa[pa.index.isin([2023, 2024])].sum()),
        casos_hasta22=fmt(pa[pa.index <= 2022].sum())))

    # Serie semanal
    seccion("Serie semanal con selector de rango")
    st.markdown(tx.SEMANAL_ANTES)
    sem = agg.groupby(["ano", "semana"])["casos"].sum().reset_index()
    fechas = pd.to_datetime(sem["ano"].astype(str) + "-01-01") + pd.to_timedelta((sem["semana"] - 1) * 7, unit="D")
    sem["ms"] = (fechas - pd.Timestamp("1970-01-01")) // pd.Timedelta(milliseconds=1)
    sem = sem.sort_values("ms")
    hc({
        "title": {"text": "Casos semanales de dengue"},
        "subtitle": {"text": "Usa los botones o la barra inferior para elegir el periodo"},
        "rangeSelector": {
            "selected": 4, "inputEnabled": False,
            "buttonTheme": {"r": 8, "width": 50, "fill": "#f1f2f6", "style": {"color": "#374151"},
                            "states": {"select": {"fill": PAL["violeta"], "style": {"color": "#ffffff"}}}},
            "buttons": [{"type": "year", "count": 1, "text": "1a"}, {"type": "year", "count": 3, "text": "3a"},
                        {"type": "year", "count": 5, "text": "5a"}, {"type": "year", "count": 10, "text": "10a"},
                        {"type": "all", "text": "Todo"}]},
        "navigator": {"maskFill": "rgba(98,80,214,0.12)",
                      "series": {"color": PAL["violeta"], "fillOpacity": 0.2}},
        "scrollbar": {"enabled": False},
        "tooltip": {"pointFormat": "<b>{point.y:,.0f}</b> casos", "xDateFormat": "Semana del %d %b %Y"},
        "series": [{"type": "areaspline", "name": "Casos", "color": PAL["violeta"], "lineWidth": 2,
                    "data": sem[["ms", "casos"]].values.tolist(),
                    "fillColor": grad("rgba(98,80,214,0.45)", "rgba(42,120,214,0.02)")}],
    }, tipo="stockChart", alto=460)
    interp(tx.SEMANAL_DESPUES)

    # Mapa de calor
    seccion("Estacionalidad: año × semana")
    st.markdown(tx.CALOR_ANTES)
    cal = agg[agg["semana"] <= 52].groupby(["ano", "semana"])["casos"].sum()
    idx = pd.MultiIndex.from_product([sorted(agg["ano"].unique()), range(1, 53)], names=["ano", "semana"])
    cal = cal.reindex(idx, fill_value=0).reset_index()
    cal["pct"] = 100 * cal["casos"] / cal.groupby("ano")["casos"].transform("sum").replace(0, np.nan)
    cal["pct"] = cal["pct"].fillna(0).round(2)
    hc({
        "chart": {"type": "heatmap"},
        "title": {"text": "¿En qué semanas se concentran los casos de cada año?"},
        "subtitle": {"text": "Porcentaje de los casos del año notificados en cada semana"},
        "xAxis": {"title": {"text": "Semana epidemiológica"}, "gridLineWidth": 0},
        "yAxis": {"title": {"text": "Año"}, "reversed": True, "gridLineWidth": 0},
        "colorAxis": {"min": 0, "labels": {"format": "{value}%"},
                      "stops": [[0, "#f4f8fe"], [0.2, "#cde2fb"], [0.4, "#86b6ef"],
                                [0.6, "#3987e5"], [0.8, "#1c5cab"], [1, "#0d366b"]]},
        "legend": {"layout": "horizontal", "align": "right", "symbolWidth": 260},
        "tooltip": {"formatter": JS("function(){ return 'Año ' + this.point.y + ', semana ' + this.point.x"
                                    " + '<br><b>' + Highcharts.numberFormat(this.point.casos, 0) + '</b> casos ('"
                                    " + this.point.value.toFixed(1) + '% del año)'; }")},
        "series": [{"name": "% del año", "borderColor": "#ffffff", "borderWidth": 1, "turboThreshold": 0,
                    "data": [{"x": int(r.semana), "y": int(r.ano), "value": float(r.pct), "casos": int(r.casos)}
                             for r in cal.itertuples()]}],
    }, alto=max(360, 120 + 18 * cal["ano"].nunique()))
    interp(tx.CALOR_DESPUES)

# ---------------------------------------------------------------------------
# Territorio
# ---------------------------------------------------------------------------
with tabs[3]:
    _contador["sec"] = 0
    seccion("Casos por departamento")
    st.markdown(tx.MAPA_ANTES)
    pd_dep = prov.groupby(["departamento", "provincia"])["casos"].sum().reset_index()
    pd_dep["codigo"] = np.where(
        pd_dep["departamento"] == "LIMA",
        np.where(pd_dep["provincia"] == "LIMA", "pe-lp", "pe-lr"),
        pd_dep["departamento"].map(CODIGOS))
    por_cod = pd_dep.dropna(subset=["codigo"]).groupby("codigo")["casos"].sum()
    hc({
        "chart": {"map": MAPA_PE},
        "title": {"text": "Casos acumulados de dengue por departamento"},
        "subtitle": {"text": "En gris: departamentos sin casos registrados. Pasa el mouse para ver el total"},
        "mapNavigation": {"enabled": True, "buttonOptions": {"verticalAlign": "bottom"}},
        "colorAxis": {"type": "logarithmic", "stops": [[0, "#e3f4ee"], [0.25, "#a8dcc9"], [0.5, "#5cbf9f"],
                                                       [0.75, "#1b8f6a"], [1, "#0b5a43"]]},
        "legend": {"title": {"text": "Casos (escala log)"}, "symbolWidth": 260},
        "series": [{
            "name": "Casos", "joinBy": "hc-key", "nullColor": "#eef0f3", "borderColor": "#ffffff",
            "data": [{"hc-key": k, "value": int(v)} for k, v in por_cod.items()],
            "states": {"hover": {"color": PAL["naranja"]}},
            "tooltip": {"pointFormat": "{point.name}: <b>{point.value:,.0f}</b> casos"},
            "dataLabels": {"enabled": True, "format": "{point.name}",
                           "style": {"fontSize": "9px", "fontWeight": "500", "color": "#1f2937",
                                     "textOutline": "1px #ffffff"}}}],
    }, tipo="mapChart", alto=620)
    interp(tx.MAPA_DESPUES)

    seccion("Departamentos y provincias (drilldown)")
    st.markdown(tx.DRILL_ANTES)
    top = prov.groupby("departamento")["casos"].sum().sort_values(ascending=False).head(15)
    series_prov = []
    for d in top.index:
        p = prov[prov["departamento"] == d].groupby("provincia")["casos"].sum() \
            .sort_values(ascending=False).head(10)
        series_prov.append({"id": d, "name": d, "type": "bar", "color": grad(PAL["violeta"], "#f59e6b"),
                            "data": [[str(n), int(v)] for n, v in p.items()]})
    hc({
        "chart": {"type": "bar"},
        "title": {"text": "Departamentos con más casos"},
        "subtitle": {"text": "Haz clic en una barra para ver sus provincias"},
        "xAxis": {"type": "category", "title": {"text": None}},
        "yAxis": {"title": {"text": "Número de casos"}},
        "legend": {"enabled": False},
        "tooltip": {"pointFormat": "<b>{point.y:,.0f}</b> casos"},
        "series": [{"name": "Casos", "color": grad(PAL["aqua"], PAL["azul"]),
                    "data": [{"name": d, "y": int(v), "drilldown": d} for d, v in top.items()]}],
        "drilldown": {"series": series_prov,
                      "activeAxisLabelStyle": {"color": "#1f2937", "textDecoration": "none"},
                      "breadcrumbs": {"buttonTheme": {"r": 8, "fill": "#f1f2f6", "stroke": "none"}}},
    }, alto=max(380, 110 + 30 * len(top)))
    total_pais = agg_total["casos"].sum()
    piura = agg_total.loc[agg_total["departamento"] == "PIURA", "casos"].sum()
    interp(tx.DRILL_DESPUES.format(pct_piura=f"{100 * piura / total_pais:.1f}"))

# ---------------------------------------------------------------------------
# Población
# ---------------------------------------------------------------------------
with tabs[4]:
    _contador["sec"] = 0
    seccion("Gravedad de los casos por año")
    st.markdown(tx.GRAVEDAD_ANTES)
    grav = desde_2011.groupby(["ano", "enfermedad"])["casos"].sum().unstack(fill_value=0)
    anios_g = [int(a) for a in grav.index]
    colores_g = {"Dengue sin signos de alarma": "#9ec5f4", "Dengue con signos de alarma": PAL["violeta"],
                 "Dengue grave": PAL["naranja"]}
    if grav.empty:
        st.info("El rango de años elegido no incluye datos desde 2011.")
    else:
        hc({
            "chart": {"type": "column"},
            "title": {"text": "Distribución de casos según gravedad"},
            "xAxis": {"categories": anios_g, "title": {"text": "Año"}},
            "yAxis": {"title": {"text": "% de casos"}, "labels": {"format": "{value}%"}, "max": 100},
            "plotOptions": {"column": {"stacking": "percent", "borderRadius": 0, "borderWidth": 1,
                                       "borderColor": "#ffffff"}},
            "legend": {"itemDistance": 40},
            "tooltip": {"shared": True, "pointFormat": "<span style='color:{series.color}'>●</span> "
                        "{series.name}: <b>{point.y:,.0f}</b> ({point.percentage:.1f}%)<br/>"},
            "series": [{"name": g, "color": colores_g[g],
                        "data": [int(v) for v in grav.get(g, pd.Series(0, index=grav.index))]}
                       for g in GRAVEDADES],
        })
    interp(tx.GRAVEDAD_DESPUES)

    c1, c2 = st.columns([3, 2], gap="medium")
    with c1:
        seccion("Pirámide por edad y sexo")
        st.markdown(tx.PIRAMIDE_ANTES)
        pir = agg[agg["grupo_edad"].isin(EDADES) & agg["sexo"].isin(["Masculino", "Femenino"])] \
            .groupby(["grupo_edad", "sexo"])["casos"].sum().unstack(fill_value=0).reindex(EDADES, fill_value=0)
        hc({
            "chart": {"type": "bar"},
            "title": {"text": "Casos por grupo de edad y sexo"},
            "xAxis": [{"categories": EDADES, "reversed": False},
                      {"categories": EDADES, "opposite": True, "reversed": False, "linkedTo": 0}],
            "yAxis": {"title": {"text": "Número de casos"},
                      "labels": {"formatter": JS("function(){ return Highcharts.numberFormat(Math.abs(this.value), 0); }")}},
            "plotOptions": {"series": {"stacking": "normal", "pointPadding": 0.05}},
            "tooltip": {"formatter": JS("function(){ return '<b>' + this.series.name + ', ' + this.point.category"
                                        " + ' años</b><br/>Casos: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0); }")},
            "series": [
                {"name": "Masculino", "color": grad("#86b6ef", PAL["azul"]),
                 "data": [-int(v) for v in pir.get("Masculino", pd.Series(0, index=EDADES))]},
                {"name": "Femenino", "color": grad("#f59e6b", PAL["naranja"]),
                 "data": [int(v) for v in pir.get("Femenino", pd.Series(0, index=EDADES))]}],
        }, alto=430)
    with c2:
        seccion("Tipo de diagnóstico")
        st.markdown(tx.DX_ANTES)
        dx = agg.groupby("tipo_dx")["casos"].sum().sort_values(ascending=False)
        colores_dx = {"Confirmado": grad("#4f95e6", PAL["azul"]), "Probable": grad("#2fd096", PAL["aqua"]),
                      "Sospechoso": grad("#8a7cf0", PAL["violeta"]), "Sin dato": "#d1d5db"}
        hc({
            "chart": {"type": "pie"},
            "title": {"text": "Casos según tipo de diagnóstico"},
            "subtitle": {"text": f"<span style='font-size:20px;font-weight:600'>{fmt(dx.sum())}</span><br>casos",
                         "align": "center", "verticalAlign": "middle", "floating": True, "y": 20,
                         "useHTML": True},
            "plotOptions": {"pie": {"innerSize": "62%", "dataLabels": {
                "enabled": True, "distance": 14, "format": "<b>{point.name}</b><br>{point.percentage:.1f}%",
                "style": {"fontWeight": "400", "textOutline": "none"}}}},
            "tooltip": {"pointFormat": "<b>{point.y:,.0f}</b> casos ({point.percentage:.1f}%)"},
            "series": [{"name": "Casos", "data": [{"name": n, "y": int(v), "color": colores_dx.get(n, "#d1d5db")}
                                                  for n, v in dx.items()]}],
        }, alto=430)

    s_ok = agg_total[agg_total["sexo"].isin(["Masculino", "Femenino"])]
    dx_t = agg_total.groupby("tipo_dx")["casos"].sum()
    interp(tx.PIRAMIDE_DESPUES.format(
        pct_mujeres=f"{100 * s_ok.loc[s_ok['sexo'] == 'Femenino', 'casos'].sum() / s_ok['casos'].sum():.1f}"))
    interp(tx.DX_DESPUES.format(pct_conf=f"{100 * dx_t.get('Confirmado', 0) / dx_t.sum():.1f}",
                                     pct_prob=f"{100 * dx_t.get('Probable', 0) / dx_t.sum():.1f}"))

# ---------------------------------------------------------------------------
# Clustering (siempre con los datos completos)
# ---------------------------------------------------------------------------
def mediana_ponderada(valores, pesos):
    """Mediana igual a la de R (si el total es par, promedia los dos valores centrales)."""
    orden = np.argsort(valores)
    v, w = np.asarray(valores)[orden], np.asarray(pesos)[orden]
    acum, n = np.cumsum(w), w.sum()
    pos = lambda p: v[np.searchsorted(acum, p)]
    return float(pos((n + 1) / 2 - 1)) if n % 2 else (pos(n / 2 - 1) + pos(n / 2)) / 2


@st.cache_data
def perfil_departamentos(agg_completo):
    n_anios = agg_completo["ano"].max() - agg_completo["ano"].min() + 1
    filas = []
    for d, g in agg_completo.groupby("departamento"):
        casos = g["casos"].sum()
        g11 = g[g["ano"] >= 2011]
        con_edad = g[g["grupo_edad"].isin(EDADES)]
        con_sexo = g[g["sexo"].isin(["Masculino", "Femenino"])]
        sem = g.groupby("semana")["casos"].sum()
        filas.append({
            "departamento": d, "casos": int(casos), "log_casos": np.log10(casos),
            "persistencia": 100 * g["ano"].nunique() / n_anios,
            "pct_alarma": 100 * g11.loc[g11["enfermedad"] != SIN_ALARMA, "casos"].sum() / g11["casos"].sum()
            if g11["casos"].sum() else 0.0,
            "semana_med": mediana_ponderada(sem.index.values, sem.values),
            "pct_menores": 100 * con_edad.loc[con_edad["grupo_edad"].isin(["0-4", "5-11", "12-17"]), "casos"].sum()
            / max(con_edad["casos"].sum(), 1),
            "pct_mujeres": 100 * con_sexo.loc[con_sexo["sexo"] == "Femenino", "casos"].sum()
            / max(con_sexo["casos"].sum(), 1),
        })
    return pd.DataFrame(filas).query("casos >= 30").reset_index(drop=True)


with tabs[5]:
    _contador["sec"] = 0
    seccion("Clustering de departamentos")
    st.markdown(tx.CLUSTER_ANTES)
    perfil = perfil_departamentos(agg_total)
    VARS = ["log_casos", "persistencia", "pct_alarma", "semana_med", "pct_menores", "pct_mujeres"]
    X = perfil[VARS].values
    desv = X.std(axis=0, ddof=1)
    X = (X[:, desv > 0] - X.mean(axis=0)[desv > 0]) / desv[desv > 0]   # se omite una variable si no varía
    Z = linkage(X, method="ward")

    k = st.slider("Número de grupos", 2, 5, 3,
                  help="El análisis del texto corresponde a 3 grupos. Cambia el valor para explorar otros cortes.")
    grupos = fcluster(Z, t=k, criterion="maxclust")
    # El Grupo 1 es el de más casos (promedio de log_casos), como en el Rmd
    orden = pd.Series(perfil["log_casos"].values).groupby(grupos).mean().sort_values(ascending=False)
    renombrar = {g: i + 1 for i, g in enumerate(orden.index)}
    perfil["grupo"] = [renombrar[g] for g in grupos]
    sil = silhouette_score(X, perfil["grupo"])
    COL_GRUPOS = [PAL["naranja"], PAL["violeta"], PAL["aqua"], PAL["azul"], "#e87ba4"]

    # Dendrograma con Highcharts
    dn = dendrogram(Z, labels=perfil["departamento"].tolist(), no_plot=True)
    lineas = []
    for xs, ys in zip(dn["icoord"], dn["dcoord"]):
        lineas += [[x, y] for x, y in zip(xs, ys)] + [None]
    etiquetas = {5 + 10 * i: n for i, n in enumerate(dn["ivl"])}
    corte = (Z[-k, 2] + Z[-k + 1, 2]) / 2
    hc({
        "chart": {"type": "line"},
        "title": {"text": "Dendrograma de departamentos (Ward)"},
        "subtitle": {"text": f"La línea punteada marca el corte en {k} grupos"},
        "xAxis": {"tickPositions": list(etiquetas.keys()), "lineWidth": 0, "tickLength": 0,
                  "labels": {"rotation": -60, "style": {"fontSize": "10px"},
                             "formatter": JS("function(){ return " + json.dumps(etiquetas) + "[this.value] || ''; }")}},
        "yAxis": {"title": {"text": "Altura"}, "min": 0,
                  "plotLines": [{"value": float(corte), "color": PAL["naranja"], "dashStyle": "Dash", "width": 2,
                                 "label": {"text": f"Corte en {k} grupos", "style": {"color": PAL["naranja"]}}}]},
        "legend": {"enabled": False},
        "tooltip": {"enabled": False},
        "plotOptions": {"series": {"marker": {"enabled": False}, "states": {"hover": {"enabled": False}}}},
        "series": [{"name": "Uniones", "data": lineas, "color": "#6b7280", "lineWidth": 1.5}],
    }, alto=440)
    if k == 3:
        interp(tx.DENDRO_DESPUES)

    st.markdown(f"**Silueta promedio con {k} grupos: {sil:.2f}**")
    tabla = perfil.groupby("grupo").agg(
        departamentos=("departamento", "count"), casos_prom=("casos", "mean"),
        persistencia=("persistencia", "mean"), pct_alarma=("pct_alarma", "mean"),
        semana_med=("semana_med", "mean"), pct_menores=("pct_menores", "mean"),
        pct_mujeres=("pct_mujeres", "mean")).round(1)
    tabla["casos_prom"] = tabla["casos_prom"].round(0).astype(int)
    tabla.index = [f"Grupo {g}" for g in tabla.index]
    st.dataframe(tabla.rename(columns={
        "departamentos": "Departamentos", "casos_prom": "Casos promedio", "persistencia": "% años con casos",
        "pct_alarma": "% con signos de alarma", "semana_med": "Semana mediana", "pct_menores": "% menores de 18",
        "pct_mujeres": "% mujeres"}), use_container_width=True)
    with st.expander("Ver qué departamentos hay en cada grupo"):
        for g in sorted(perfil["grupo"].unique()):
            st.markdown(f"**Grupo {g}:** " + ", ".join(sorted(perfil.loc[perfil['grupo'] == g, 'departamento'].str.title())))
    if k == 3:
        interp(tx.PERFIL_DESPUES)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        datos_mapa = []
        for r in perfil.itertuples():
            cods = ["pe-lp", "pe-lr"] if r.departamento == "LIMA" else [CODIGOS.get(r.departamento)]
            datos_mapa += [{"hc-key": c, "value": int(r.grupo), "casos": int(r.casos)} for c in cods if c]
        hc({
            "chart": {"map": MAPA_PE},
            "title": {"text": "Grupos de departamentos"},
            "subtitle": {"text": "En gris: sin casos o con muy pocos"},
            "mapNavigation": {"enabled": True, "buttonOptions": {"verticalAlign": "bottom"}},
            "colorAxis": {"dataClasses": [{"from": i, "to": i, "color": COL_GRUPOS[i - 1], "name": f"Grupo {i}"}
                                          for i in range(1, k + 1)]},
            "series": [{"name": "Grupo", "joinBy": "hc-key", "data": datos_mapa, "nullColor": "#eef0f3",
                        "borderColor": "#ffffff",
                        "tooltip": {"pointFormat": "{point.name}: <b>Grupo {point.value}</b><br>{point.casos:,.0f} casos"},
                        "dataLabels": {"enabled": True, "format": "{point.name}",
                                       "style": {"fontSize": "9px", "fontWeight": "500", "color": "#1f2937",
                                                 "textOutline": "1px #ffffff"}}}],
        }, tipo="mapChart", alto=560)
    with c2:
        hc({
            "chart": {"type": "scatter"},
            "title": {"text": "Casos acumulados y persistencia"},
            "subtitle": {"text": "Cada punto es un departamento, coloreado por su grupo"},
            "xAxis": {"type": "logarithmic", "title": {"text": "Casos (escala log)"}},
            "yAxis": {"title": {"text": "% de años con casos"}, "max": 100},
            "tooltip": {"headerFormat": "", "pointFormat": "<b>{point.name}</b><br>{point.x:,.0f} casos"
                                                         "<br>Casos en {point.y:.0f}% de los años"},
            "plotOptions": {"scatter": {"marker": {"symbol": "circle", "radius": 7, "lineWidth": 2, "lineColor": "#ffffff"}}},
            "series": [{"name": f"Grupo {g}", "color": COL_GRUPOS[g - 1],
                        "data": [{"x": int(r.casos), "y": round(float(r.persistencia), 1),
                                  "name": r.departamento.title()}
                                 for r in perfil[perfil["grupo"] == g].itertuples()]}
                       for g in sorted(perfil["grupo"].unique())],
        }, alto=560)
    if k == 3:
        interp(tx.MAPA_GRUPOS_DESPUES)
        interp(tx.DISPERSION_DESPUES)
    else:
        st.info("Las interpretaciones de esta pestaña corresponden a 3 grupos. Vuelve a 3 para leerlas.")

# ---------------------------------------------------------------------------
# Glosario
# ---------------------------------------------------------------------------
COLORES_TEMA = {"Enfermedad": ("#c2410c", "#fdeee6"), "Vigilancia": ("#2a78d6", "#e6f0fc"),
                "Datos": ("#138a60", "#e3f6ef"), "Visualización": ("#6250d6", "#efedfc"),
                "Estadística": ("#be185d", "#fce7f1")}

with tabs[6]:
    _contador["sec"] = 0
    seccion("Glosario del dengue y de la app")
    st.markdown(tx.GLOSARIO_INTRO)
    c1, c2 = st.columns([1, 2], gap="medium")
    buscar = c1.text_input("Buscar un término", placeholder="Ej.: brote, silueta, Aedes…",
                           label_visibility="collapsed")
    temas = list(COLORES_TEMA)
    tema = c2.segmented_control("Tema", ["Todos"] + temas, default="Todos", label_visibility="collapsed")
    q = buscar.strip().lower()
    terminos = [t for t in tx.GLOSARIO
                if (tema in (None, "Todos") or t[1] == tema)
                and (not q or q in t[0].lower() or q in t[2].lower())]
    terminos.sort(key=lambda t: t[0].lower())
    st.markdown(f'<div class="glos-count">{len(terminos)} de {len(tx.GLOSARIO)} términos</div>',
                unsafe_allow_html=True)
    if not terminos:
        st.info("No se encontró ningún término. Prueba con otra palabra.")
    else:
        tarjetas_g = []
        for nombre, cat, definicion, uso in terminos:
            c, bg = COLORES_TEMA[cat]
            tarjetas_g.append(
                f'<div class="term" style="--c:{c};--bg:{bg}"><div class="term-top">'
                f'<div class="term-t">{html.escape(nombre)}</div><div class="term-cat">{cat}</div></div>'
                f'<div class="term-d">{html.escape(definicion)}</div>'
                f'<div class="term-u"><b>En la app:</b> {html.escape(uso)}</div></div>')
        st.markdown('<div class="glos">' + "".join(tarjetas_g) + '</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Conclusiones
# ---------------------------------------------------------------------------
with tabs[7]:
    _contador["sec"] = 0
    top3 = agg_total.groupby("departamento")["casos"].sum().nlargest(3)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        seccion("Sobre el dengue en el Perú")
        st.markdown(tx.CONCLUSIONES_DENGUE.format(
            total=fmt(agg_total["casos"].sum()), pct_top3=f"{100 * top3.sum() / agg_total['casos'].sum():.1f}"))
    with c2:
        seccion("Sobre la herramienta")
        st.markdown(tx.CONCLUSIONES_HERRAMIENTA)
    seccion("Referencias")
    st.markdown(tx.REFERENCIAS)
