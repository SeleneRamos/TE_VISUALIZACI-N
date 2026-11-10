"""
Prepara la data para la app.

Lee el CSV original del CDC Perú (más de 100 MB), lo limpia igual que en el Rmd
y guarda dos archivos pequeños con los casos ya agrupados en la carpeta data/.
Solo hay que correrlo una vez:

    python preparar_datos.py datos_abiertos_vigilancia_dengue_2000_2025_0.csv
"""
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ruta = sys.argv[1] if len(sys.argv) > 1 else "datos_abiertos_vigilancia_dengue_2000_2025_0.csv"
salida = Path(__file__).parent / "data"
salida.mkdir(exist_ok=True)

columnas = ["departamento", "provincia", "enfermedad", "ano", "semana",
            "tipo_dx", "edad", "tipo_edad", "sexo"]
try:
    df = pd.read_csv(ruta, dtype=str, usecols=columnas, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(ruta, dtype=str, usecols=columnas, encoding="latin-1")
print(f"Filas leídas: {len(df):,}")


def sin_tildes(texto):
    if pd.isna(texto):
        return texto
    texto = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in texto if not unicodedata.combining(c)).upper().strip()


# Limpieza (la misma que en el Rmd)
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
df["semana"] = pd.to_numeric(df["semana"], errors="coerce")
df = df.dropna(subset=["ano", "semana"])
df["ano"] = df["ano"].astype(int)
df["semana"] = df["semana"].astype(int)

edad = pd.to_numeric(df["edad"], errors="coerce")
divisor = df["tipo_edad"].map({"A": 1, "M": 12, "D": 365})
edad_anios = edad / divisor
df["grupo_edad"] = pd.cut(edad_anios, bins=[-np.inf, 4, 11, 17, 29, 59, np.inf],
                          labels=["0-4", "5-11", "12-17", "18-29", "30-59", "60+"]).astype(str)
df.loc[edad_anios.isna(), "grupo_edad"] = "Sin dato"

df["sexo"] = df["sexo"].map({"M": "Masculino", "F": "Femenino"}).fillna("Sin dato")
df["tipo_dx"] = df["tipo_dx"].map({"C": "Confirmado", "P": "Probable",
                                   "S": "Sospechoso"}).fillna("Sin dato")
enf = df["enfermedad"].fillna("").str.strip()
df["enfermedad"] = enf.str[:1].str.upper() + enf.str[1:].str.lower()
df["departamento"] = df["departamento"].map(sin_tildes)
df["provincia"] = df["provincia"].map(sin_tildes)

# Tabla 1: casos por año, semana, departamento, gravedad, diagnóstico, sexo y edad
claves = ["ano", "semana", "departamento", "enfermedad", "tipo_dx", "sexo", "grupo_edad"]
agregado = df.groupby(claves, dropna=False).size().reset_index(name="casos")
for c in ["departamento", "enfermedad", "tipo_dx", "sexo", "grupo_edad"]:
    agregado[c] = agregado[c].astype("category")
agregado["ano"] = agregado["ano"].astype("int16")
agregado["semana"] = agregado["semana"].astype("int8")
agregado["casos"] = agregado["casos"].astype("int32")
agregado.to_parquet(salida / "casos_agregados.parquet", index=False)

# Tabla 2: casos por año, departamento y provincia (para el drilldown y Lima en el mapa)
provincia = df.groupby(["ano", "departamento", "provincia"], dropna=False).size() \
              .reset_index(name="casos")
provincia.to_parquet(salida / "casos_provincia.parquet", index=False)

print(f"Casos totales: {agregado['casos'].sum():,}")
for f in salida.glob("*.parquet"):
    print(f"{f.name}: {f.stat().st_size / 1e6:.1f} MB")
