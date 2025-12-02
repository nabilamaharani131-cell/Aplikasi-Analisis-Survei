import streamlit as st
import pandas as pd
from itertools import combinations

st.title("Aplikasi Pengolahan Data Survey")

uploaded = st.file_uploader("Upload File Excel", type=["xlsx", "xls"])

if uploaded:
    df = pd.read_excel(uploaded)
    st.subheader("Preview Data")
    st.dataframe(df.head())

    st.subheader("Analisis Deskriptif")
    desc_cols = st.multiselect("Pilih kolom untuk deskriptif", df.columns)

    if desc_cols:
        st.write(df[desc_cols].describe(include='all'))

    st.subheader("Analisis Asosiasi (Korelasi)")
    assoc_cols = st.multiselect("Pilih kolom untuk asosiasi", df.columns)

    if len(assoc_cols) >= 2:
        corr = df[assoc_cols].corr()
        st.write("Matriks Korelasi:")
        st.dataframe(corr)

        st.write("Interpretasi Sederhana:")
        for col1, col2 in combinations(assoc_cols, 2):
            val = corr.loc[col1, col2]
            st.write(f"• Korelasi antara **{col1}** dan **{col2}** = {val:.3f}")
