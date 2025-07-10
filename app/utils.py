# app/utils.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def detect_column_types(df):
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    # Détection des colonnes de date
    date_cols = []
    for col in df.columns:
        try:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                date_cols.append(col)
            elif pd.to_datetime(df[col], errors='coerce').notnull().sum() > len(df) * 0.7:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                date_cols.append(col)
        except:
            continue

    return numeric_cols, cat_cols, date_cols

def plot_chart(df, chart_type, x=None, y=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.xticks(rotation=45)

    if chart_type == "Histogramme":
        sns.histplot(df[x].dropna(), kde=True, ax=ax)
        ax.set_title(f"Histogramme de {x}")

    elif chart_type == "Camembert":
        value_counts = df[x].value_counts().head(10)
        ax.pie(value_counts, labels=value_counts.index, autopct="%1.1f%%")
        ax.set_title(f"Répartition de {x}")

    elif chart_type == "Scatter Plot":
        sns.scatterplot(data=df, x=x, y=y, ax=ax)
        ax.set_title(f"{y} en fonction de {x}")

    elif chart_type == "Box Plot":
        sns.boxplot(data=df, x=x, y=y, ax=ax)
        ax.set_title(f"Box Plot de {y} selon {x}")

    elif chart_type == "Courbe temporelle":
        df_sorted = df.sort_values(by=x)
        sns.lineplot(data=df_sorted, x=x, y=y, ax=ax)
        ax.set_title(f"Évolution de {y} dans le temps ({x})")

    st.pyplot(fig)
