import streamlit as st
import pandas as pd
import scipy.stats as stats
from itertools import combinations


# ====================================================
# Fungsi otomatis memilih Pearson, Spearman, Chi-square
# ====================================================
def automatic_test(x, y):

    is_numeric_x = pd.api.types.is_numeric_dtype(x)
    is_numeric_y = pd.api.types.is_numeric_dtype(y)

    # --------------------------------------
    # Jika keduanya numeric → Pearson / Spearman
    # --------------------------------------
    if is_numeric_x and is_numeric_y:

        # Uji normalitas (Shapiro)
        p_x = stats.shapiro(x.dropna())[1]
        p_y = stats.shapiro(y.dropna())[1]

        # Pearson jika keduanya normal
        if p_x > 0.05 and p_y > 0.05:
            test_name = "Pearson"
            coef, pval = stats.pearsonr(x, y)
        else:
            test_name = "Spearman"
            coef, pval = stats.spearmanr(x, y)

    # --------------------------------------
    # Jika salah satu kategorikal → Chi-square
    # --------------------------------------
    else:
        test_name = "Chi-Square"
        contingency = pd.crosstab(x, y)
        chi2, pval, dof, expected = stats.chi2_contingency(contingency)
        coef = chi2

    # Interpretasi kesimpulan
    conclusion = "Ada hubungan yang signifikan." if pval < 0.05 else "Tidak ada hubungan signifikan."

    return test_name, coef, pval, conclusion



# ====================================================
#                  STREAMLIT APP
# ====================================================

st.title("Aplikasi Analisis Data Survei")

uploaded = st.file_uploader("Upload File Excel", type=["xlsx", "xls"])

if uploaded:
    df = pd.read_excel(uploaded)

    st.subheader("Preview Data")
    st.dataframe(df.head())

    # ========================
    # Analisis Deskriptif
    # ========================
    st.subheader("Analisis Deskriptif")

    desc_cols = st.multiselect("Pilih kolom untuk deskriptif", df.columns)

    if desc_cols:
        st.write(df[desc_cols].describe(include="all"))


    # ========================
    # Analisis Asosiasi
    # ========================
    st.subheader("Analisis Asosiasi (Hubungan Variabel)")

    assoc_cols = st.multiselect("Pilih kolom untuk analisis asosiasi", df.columns)

    if len(assoc_cols) >= 2:

        st.markdown("### Matriks Korelasi (untuk variabel numerik saja)")
        corr = df[assoc_cols].corr(numeric_only=True)
        st.dataframe(corr)

        st.markdown("### Hasil Analisis Hubungan Variabel")

        for col1, col2 in combinations(assoc_cols, 2):
            x = df[col1]
            y = df[col2]

            test_name, coef, pval, conclusion = automatic_test(x, y)

            st.write(f"#### {col1} vs {col2}")
            st.write(f"- **Tes yang digunakan:** {test_name}")
            st.write(f"- **Nilai Statistik:** {coef:.4f}")
            st.write(f"- **p-value:** {pval:.4f}")
            st.write(f"- **Kesimpulan:** {conclusion}")
            st.markdown("---")
