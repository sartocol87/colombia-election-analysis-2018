from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Elecciones Colombia 2018",
    page_icon="🗳️",
    layout="wide",
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "2018_presidencia_primera_vuelta.dta.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["candidato"] = (
        df["primer_apellido"].fillna("") + " "
        + df["segundo_apellido"].fillna("") + " "
        + df["nombres"].fillna("")
    ).str.replace(r"\s+", " ", regex=True).str.strip()

    special = {
        "VOTOS EN BLANCO",
        "PROMOTORES VOTO EN BLANCO",
        "VOTOS NULOS",
        "TARJETAS NO MARCADAS",
    }
    df["tipo_registro"] = df["candidato"].apply(
        lambda x: "Categoría electoral" if x in special else "Candidato"
    )
    return df

df = load_data()

st.title("🗳️ Elecciones presidenciales de Colombia — 2018")
st.caption("Primera vuelta · Análisis exploratorio")

departments = ["Todos"] + sorted(df["departamento"].dropna().unique().tolist())
selected_department = st.sidebar.selectbox("Departamento", departments)

filtered = df.copy()
if selected_department != "Todos":
    filtered = filtered[filtered["departamento"] == selected_department]

candidate_df = filtered[filtered["tipo_registro"] == "Candidato"]

results = (
    candidate_df.groupby("candidato", as_index=False)["votos"]
    .sum()
    .sort_values("votos", ascending=False)
)

total_votes = int(filtered["votos"].sum())
candidate_votes = int(candidate_df["votos"].sum())
winner = results.iloc[0]["candidato"] if not results.empty else "Sin datos"

col1, col2, col3 = st.columns(3)
col1.metric("Votos registrados", f"{total_votes:,}")
col2.metric("Votos a candidatos", f"{candidate_votes:,}")
col3.metric("Candidato líder", winner)

fig = px.bar(
    results,
    x="votos",
    y="candidato",
    orientation="h",
    title="Votos por candidato",
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

municipalities = (
    filtered.groupby("municipio", as_index=False)["votos"]
    .sum()
    .sort_values("votos", ascending=False)
    .head(15)
)

fig2 = px.bar(
    municipalities,
    x="municipio",
    y="votos",
    title="Municipios con mayor cantidad de votos",
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Explorar un municipio")
city = st.selectbox(
    "Municipio",
    sorted(filtered["municipio"].dropna().unique().tolist()),
)

city_results = (
    candidate_df[candidate_df["municipio"] == city]
    .groupby("candidato", as_index=False)["votos"]
    .sum()
    .sort_values("votos", ascending=False)
)

fig3 = px.bar(
    city_results,
    x="candidato",
    y="votos",
    title=f"Resultados en {city}",
)
st.plotly_chart(fig3, use_container_width=True)

st.dataframe(city_results, use_container_width=True)
