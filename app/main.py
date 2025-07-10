# app/main.py

import streamlit as st
import pandas as pd
from utils import detect_column_types, plot_chart

st.set_page_config(page_title="Visualiseur de Données", layout="wide")

st.title("📊 Visualiseur de Données CSV")

st.markdown("Téléversez un fichier CSV pour explorer et visualiser vos données facilement.")

# Upload de fichier
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Fichier chargé avec succès !")
        st.subheader("Aperçu des données")
        st.dataframe(df.head())

        # Détection des types de colonnes
        numeric_cols, cat_cols, date_cols = detect_column_types(df)

        st.sidebar.header("Paramètres de visualisation")

        # Choix du type de graphique
        chart_type = st.sidebar.selectbox(
            "Quel type de graphique souhaitez-vous créer ?",
            ["Histogramme", "Camembert", "Scatter Plot", "Box Plot", "Courbe temporelle"]
        )

        # Afficher les bons sélecteurs selon le type choisi
        if chart_type == "Histogramme":
            col = st.sidebar.selectbox("Colonne numérique", numeric_cols)
            if col:
                plot_chart(df, chart_type, x=col)

        elif chart_type == "Camembert":
            col = st.sidebar.selectbox("Colonne catégorielle", cat_cols)
            if col:
                plot_chart(df, chart_type, x=col)

        elif chart_type == "Scatter Plot":
            x_col = st.sidebar.selectbox("Axe X (numérique)", numeric_cols)
            y_col = st.sidebar.selectbox("Axe Y (numérique)", [col for col in numeric_cols if col != x_col])
            if x_col and y_col:
                plot_chart(df, chart_type, x=x_col, y=y_col)

        elif chart_type == "Box Plot":
            num_col = st.sidebar.selectbox("Variable numérique", numeric_cols)
            cat_col = st.sidebar.selectbox("Variable catégorielle", cat_cols)
            if num_col and cat_col:
                plot_chart(df, chart_type, x=cat_col, y=num_col)

        elif chart_type == "Courbe temporelle":
            date_col = st.sidebar.selectbox("Colonne date", date_cols)
            y_col = st.sidebar.selectbox("Valeur numérique", numeric_cols)
            if date_col and y_col:
                plot_chart(df, chart_type, x=date_col, y=y_col)

    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
else:
    st.info("🗂️ Veuillez téléverser un fichier CSV pour commencer.")
