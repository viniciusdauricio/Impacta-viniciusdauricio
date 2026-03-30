import streamlit as st
import pandas as pd
import sqlite3
import utils as utils
import logging
from core import config

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Dashboard - Random Users")

# -----------------------
# BOTÃO PARA EXECUTAR PIPELINE
# -----------------------
if st.button("🔄 Rodar Pipeline"):
    try:
        df = utils.ingestion(config)
        utils.preparation(df, config)
        st.success("Pipeline executado com sucesso!")
    except Exception as e:
        st.error(f"Erro no pipeline: {e}")

# -----------------------
# CARREGAR DADOS DO SQLITE
# -----------------------
try:
    conn = sqlite3.connect("assets/database.db")
    df = pd.read_sql("SELECT * FROM random_users", conn)
    conn.close()

    

except Exception as e:
    st.warning("⚠️ Execute o pipeline primeiro!")
    st.stop()
print(df.columns) 
# -----------------------
# MOSTRAR DADOS
# -----------------------
st.subheader("📋 Dados")
st.dataframe(df)

# -----------------------
# GRÁFICOS
# -----------------------
st.subheader("📊 Gráficos")

col1, col2 = st.columns(2)

# Gênero
if "gender" in df.columns:
    col1.bar_chart(df["gender"].value_counts())

# País
if "location_country" in df.columns:
    col2.bar_chart(df["location_country"].value_counts().head(10))

# Idade
if "dob_age" in df.columns:
    st.subheader("📈 Idade")
    st.line_chart(df["dob_age"])

# -----------------------
# FILTRO
# -----------------------
st.sidebar.header("Filtros")

if "gender" in df.columns:
    gender = st.sidebar.selectbox("Gênero", ["Todos"] + list(df["gender"].unique()))

    if gender != "Todos":
        df = df[df["gender"] == gender]

st.subheader("📌 Dados filtrados")
st.dataframe(df)
st.write(df.columns)