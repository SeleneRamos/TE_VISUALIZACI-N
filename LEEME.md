# Dengue en el Perú, 2000–2025 · App en Streamlit

App interactiva con gráficos de Highcharts sobre la vigilancia epidemiológica del dengue (CDC Perú – MINSA).

## Archivos
- `app.py`: la app.
- `textos.py`: los textos de contexto e interpretación.
- `preparar_datos.py`: agrupa el CSV original y genera los archivos de `data/`.
- `data/`: datos agrupados (parquet) y el mapa del Perú.
- `requirements.txt`: paquetes que necesita la app.

## 1. Preparar los datos (una sola vez)
Pon el CSV del CDC en esta carpeta y corre:

    pip install -r requirements.txt
    python preparar_datos.py datos_abiertos_vigilancia_dengue_2000_2025_0.csv

## 2. Probar en tu computadora

    streamlit run app.py

## 3. Publicar
1. Sube esta carpeta a un repositorio de GitHub (el CSV no se sube, solo `data/`).
2. Entra a https://share.streamlit.io con tu cuenta de GitHub.
3. Create app → elige el repositorio → archivo principal `app.py` → Deploy.
