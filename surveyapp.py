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

        st.write("
### Analisis Hubungan Antar Variabel")
        for col1, col2 in combinations(assoc_cols, 2):
            val = corr.loc[col1, col2]
            is_numeric = pd.api.types.is_numeric_dtype(df[col1]) and pd.api.types.is_numeric_dtype(df[col2])

            if is_numeric:
                p1 = stats.shapiro(df[col1])[1]
                p2 = stats.shapiro(df[col2])[1]
                if p1 > 0.05 and p2 > 0.05:
                    test = "Pearson"
                    coef, pval = stats.pearsonr(df[col1], df[col2])
                else:
                    test = "Spearman"
                    coef, pval = stats.spearmanr(df[col1], df[col2])
            else:
                test = "Chi-Square"
                contingency = pd.crosstab(df[col1], df[col2])
                chi2, pval, dof, expected = stats.chi2_contingency(contingency)
                coef = chi2

            conclusion = "Ada hubungan yang signifikan" if pval < 0.05 else "Tidak ada hubungan signifikan"

            st.write(f"**{col1} vs {col2}**")
            st.write(f"Tes yang digunakan: **{test}**")
            st.write(f"Nilai statistik: {coef:.3f}")
            st.write(f"p-value: {pval:.4f}")
            st.write(f"Kesimpulan: **{conclusion}**
")

        st.write("Interpretasi Sederhana:")
        for col1, col2 in combinations(assoc_cols, 2):
            val = corr.loc[col1, col2]
            st.write(f"• Korelasi antara **{col1}** dan **{col2}** = {val:.3f}")
