from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# Configuración general
# ---------------------------------------------------------

st.set_page_config(
    page_title="Elecciones Colombia 2018",
    page_icon="🗳️",
    layout="wide",
)

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_PROCESADOS = RAIZ_PROYECTO / "data" / "processed"


# ---------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------

@st.cache_data
def cargar_csv(nombre_archivo: str) -> pd.DataFrame:
    """Carga una tabla procesada desde data/processed."""
    ruta = RUTA_PROCESADOS / nombre_archivo

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo procesado: {ruta}"
        )

    return pd.read_csv(ruta)


def cargar_tablas() -> dict[str, pd.DataFrame]:
    """Carga todas las tablas utilizadas por el dashboard."""
    archivos = {
        "resultados_candidatos": "resultados_candidatos.csv",
        "votos_departamento": "votos_por_departamento.csv",
        "margenes_departamentales": "margenes_departamentales.csv",
        "votos_municipio": "votos_por_municipio.csv",
        "margenes_municipales": "margenes_municipales.csv",
        "concentracion_municipal": "concentracion_municipal_extrema.csv",
        "resultados_ciudades": "resultados_ciudades.csv",
        "participacion_departamental": (
            "participacion_departamental_candidato.csv"
        ),
    }

    return {
        nombre: cargar_csv(archivo)
        for nombre, archivo in archivos.items()
    }


try:
    tablas = cargar_tablas()
except FileNotFoundError as error:
    st.error(str(error))
    st.info(
        "Ejecuta primero el notebook completo para generar "
        "los archivos de data/processed."
    )
    st.stop()


# ---------------------------------------------------------
# Encabezado
# ---------------------------------------------------------

st.title("🗳️ Elecciones presidenciales de Colombia de 2018")
st.caption(
    "Análisis exploratorio y territorial de la primera vuelta presidencial."
)

st.sidebar.header("Navegación")
seccion = st.sidebar.radio(
    "Selecciona una sección",
    [
        "Resumen nacional",
        "Departamentos",
        "Municipios",
        "Ciudades principales",
    ],
)


# ---------------------------------------------------------
# Resumen nacional
# ---------------------------------------------------------

if seccion == "Resumen nacional":
    resultados = tablas["resultados_candidatos"].copy()

    if "votos" in resultados.columns:
        resultados = resultados.sort_values(
            "votos",
            ascending=False
        )

    total_votos = (
        int(resultados["votos"].sum())
        if "votos" in resultados.columns
        else 0
    )

    total_candidatos = (
        resultados["candidato"].nunique()
        if "candidato" in resultados.columns
        else len(resultados)
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Votos registrados en la tabla",
        f"{total_votos:,.0f}".replace(",", "."),
    )
    col2.metric(
        "Candidaturas",
        f"{total_candidatos}",
    )

    st.subheader("Resultados por candidato")

    if {"candidato", "votos"}.issubset(resultados.columns):
        grafica = (
            resultados[["candidato", "votos"]]
            .set_index("candidato")
        )
        st.bar_chart(grafica)

    st.dataframe(
        resultados,
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# Departamentos
# ---------------------------------------------------------

elif seccion == "Departamentos":
    votos_departamento = tablas["votos_departamento"].copy()
    margenes = tablas["margenes_departamentales"].copy()
    participacion = tablas["participacion_departamental"].copy()

    st.subheader("Análisis por departamento")

    departamentos_disponibles = []

    for tabla in [votos_departamento, margenes, participacion]:
        if "departamento" in tabla.columns:
            departamentos_disponibles.extend(
                tabla["departamento"].dropna().astype(str).tolist()
            )

    departamentos_disponibles = sorted(
        set(departamentos_disponibles)
    )

    departamento = st.selectbox(
        "Selecciona un departamento",
        ["Todos"] + departamentos_disponibles,
    )

    if departamento != "Todos":
        if "departamento" in votos_departamento.columns:
            votos_departamento = votos_departamento[
                votos_departamento["departamento"] == departamento
            ]

        if "departamento" in margenes.columns:
            margenes = margenes[
                margenes["departamento"] == departamento
            ]

        if "departamento" in participacion.columns:
            participacion = participacion[
                participacion["departamento"] == departamento
            ]

    st.markdown("#### Votos por departamento")

    if {"departamento", "votos"}.issubset(
        votos_departamento.columns
    ):
        grafica_departamentos = (
            votos_departamento
            .sort_values("votos", ascending=False)
            .set_index("departamento")[["votos"]]
        )
        st.bar_chart(grafica_departamentos)

    st.dataframe(
        votos_departamento,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Ganadores y márgenes departamentales")
    st.dataframe(
        margenes,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### Participación de cada departamento "
        "en la votación nacional del candidato"
    )
    st.dataframe(
        participacion,
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# Municipios
# ---------------------------------------------------------

elif seccion == "Municipios":
    votos_municipio = tablas["votos_municipio"].copy()
    margenes = tablas["margenes_municipales"].copy()
    concentracion = tablas["concentracion_municipal"].copy()

    st.subheader("Análisis municipal")

    departamentos = []

    for tabla in [votos_municipio, margenes, concentracion]:
        if "departamento" in tabla.columns:
            departamentos.extend(
                tabla["departamento"].dropna().astype(str).tolist()
            )

    departamentos = sorted(set(departamentos))

    departamento = st.selectbox(
        "Filtrar por departamento",
        ["Todos"] + departamentos,
    )

    if departamento != "Todos":
        if "departamento" in votos_municipio.columns:
            votos_municipio = votos_municipio[
                votos_municipio["departamento"] == departamento
            ]

        if "departamento" in margenes.columns:
            margenes = margenes[
                margenes["departamento"] == departamento
            ]

        if "departamento" in concentracion.columns:
            concentracion = concentracion[
                concentracion["departamento"] == departamento
            ]

    st.markdown("#### Municipios con mayor volumen de votos")

    if "votos" in votos_municipio.columns:
        top_municipios = (
            votos_municipio
            .sort_values("votos", ascending=False)
            .head(20)
        )
    else:
        top_municipios = votos_municipio.head(20)

    if {"municipio", "votos"}.issubset(top_municipios.columns):
        grafica_municipios = (
            top_municipios[["municipio", "votos"]]
            .set_index("municipio")
        )
        st.bar_chart(grafica_municipios)

    st.dataframe(
        top_municipios,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Márgenes municipales")
    st.dataframe(
        margenes,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Concentraciones elevadas del voto")
    st.caption(
        "Estos resultados son descriptivos y no constituyen "
        "evidencia de irregularidad electoral."
    )

    if "porcentaje_ganador" in concentracion.columns:
        concentracion = concentracion.sort_values(
            "porcentaje_ganador",
            ascending=False,
        )

    st.dataframe(
        concentracion,
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# Ciudades principales
# ---------------------------------------------------------

else:
    ciudades = tablas["resultados_ciudades"].copy()

    st.subheader("Resultados en ciudades principales")

    if "ciudad" in ciudades.columns:
        opciones_ciudad = sorted(
            ciudades["ciudad"].dropna().astype(str).unique()
        )
        ciudad = st.selectbox(
            "Selecciona una ciudad",
            ["Todas"] + opciones_ciudad,
        )

        if ciudad != "Todas":
            ciudades = ciudades[
                ciudades["ciudad"] == ciudad
            ]

    elif "municipio" in ciudades.columns:
        opciones_ciudad = sorted(
            ciudades["municipio"].dropna().astype(str).unique()
        )
        ciudad = st.selectbox(
            "Selecciona una ciudad",
            ["Todas"] + opciones_ciudad,
        )

        if ciudad != "Todas":
            ciudades = ciudades[
                ciudades["municipio"] == ciudad
            ]

    if {"candidato", "votos"}.issubset(ciudades.columns):
        grafica_ciudades = (
            ciudades
            .groupby("candidato", as_index=False)["votos"]
            .sum()
            .sort_values("votos", ascending=False)
            .set_index("candidato")
        )
        st.bar_chart(grafica_ciudades)

    st.dataframe(
        ciudades,
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# Pie de página
# ---------------------------------------------------------

st.divider()
st.caption(
    "Fuente: Centro de Estudios en Democracia y Asuntos "
    "Electorales — CEDAE."
)