import streamlit as st
import pandas as pd
import scipy.stats as stats
from itertools import combinations

st.title("Aplikasi Analisis Survey")

# Upload file
uploaded = st.file_uploader("Upload file Excel", type=["xlsx", "xls"])

if uploaded:
    df = pd.read_excel(uploaded)

    st.subheader("Preview Data")
    st.dataframe(df.head())

    # ============================
    # ANALISIS DESKRIPTIF
    # ============================
    st.subheader("Analisis Deskriptif")

    desc_cols = st.multiselect("Pilih kolom untuk deskriptif", df.columns)

    if desc_cols:
        st.write(df[desc_cols].describe(include="all"))


    # ============================
    # ANALISIS ASOSIASI
    # ============================
    st.subheader("Analisis Asosiasi (Korelasi/Hubungan)")

    assoc_cols = st.multiselect("Pilih kolom untuk asosiasi", df.columns)

    if len(assoc_cols) >= 2:

        st.markdown("### Matriks Korelasi (untuk numeric)")
        corr = df[assoc_cols].corr(numeric_only=True)
        st.dataframe(corr)

        st.markdown("### Analisis Hubungan Antar Variabel")

        for col1, col2 in combinations(assoc_cols, 2):

            # Deteksi tipe data
            is_numeric = (
                pd.api.types.is_numeric_dtype(df[col1]) and
                pd.api.types.is_numeric_dtype(df[col2])
            )

            # ============================
            # Numeric vs Numeric
            # ============================
            if is_numeric:
                # Uji normalitas Shapiro
                p1 = stats.shapiro(df[col1])[1]
                p2 = stats.shapiro(df[col2])[1]

                if p1 > 0.05 and p2 > 0.05:
                    test = "Pearson"
                    coef, pval = stats.pearsonr(df[col1], df[col2])
                else:
                    test = "Spearman"
                    coef, pval = stats.spearmanr(df[col1], df[col2])

            # ============================
            # Jika kategorikal -> Chi-square
            # ============================
            else:
                test = "Chi-Square"
                contingency = pd.crosstab(df[col1], df[col2])
                chi2, pval, dof, expected = stats.chi2_contingency(contingency)
                coef = chi2

            # ============================
            # Kesimpulan
            # ============================
            if pval < 0.05:
                conclusion = "Ada hubungan yang signifikan."
            else:
                conclusion = "Tidak ada hubungan signifikan."

            # ============================
            # OUTPUT
            # ============================
            st.write(f"**{col1} vs {col2}**")
            st.write(f"Tes digunakan : **{test}**")
            st.write(f"Nilai statistik : `{coef:.4f}`")
            st.write(f"p-value : `{pval:.4f}`")
            st.write(f"Kesimpulan : **{conclusion}**")
            st.markdown("---")
