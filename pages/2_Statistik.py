# pages/2_Statistik.py
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, init_filters, apply_filters
from scipy.stats import chi2_contingency, f_oneway

st.set_page_config(layout="wide")
df = load_data()
init_filters(df)
df_filtered = apply_filters(df)

st.title("📊 Analisis Statistik")

if df_filtered.empty:
    st.warning("Tidak ada data setelah filter.")
else:
    # Regression-like scatter
    if {"IPK","Masa Tunggu Kerja"}.issubset(df_filtered.columns):
        st.subheader("IPK vs Masa Tunggu Kerja (scatter + trendline)")
        fig = px.scatter(df_filtered, x="IPK", y="Masa Tunggu Kerja", trendline="ols",
                         hover_data=["Tahun Angkatan","Bidang Industri","Konsentrasi"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kolom 'IPK' atau 'Masa Tunggu Kerja' tidak ditemukan.")

    # Chi-square: Konsentrasi vs Bidang Industri
    if {"Konsentrasi","Bidang Industri"}.issubset(df_filtered.columns):
        st.subheader("Chi-Square: Konsentrasi vs Bidang Industri")
        ct = pd.crosstab(df_filtered["Konsentrasi"], df_filtered["Bidang Industri"])
        st.dataframe(ct)
        try:
            chi2, p, dof, expected = chi2_contingency(ct)
            st.write(f"- Chi2 = {chi2:.3f}, p-value = {p:.5f}, dof = {dof}")
            if p < 0.05:
                st.success("Terdapat hubungan yang signifikan antara Konsentrasi dan Bidang Industri (p < 0.05).")
            else:
                st.info("Tidak ditemukan bukti hubungan signifikan (p >= 0.05).")
        except Exception as e:
            st.error("Gagal melakukan uji Chi-Square: " + str(e))
    else:
        st.info("Kolom yang diperlukan untuk Chi-Square tidak lengkap.")

    # ANOVA gaji per lokasi (jika >2 grup)
    if {"Lokasi Geografis","Gaji"}.issubset(df_filtered.columns):
        st.subheader("Uji ANOVA: Perbedaan Rata-rata Gaji antar Lokasi")
        groups = [grp["Gaji"].values for name, grp in df_filtered.groupby("Lokasi Geografis")]
        if len(groups) >= 2:
            try:
                stat, pval = f_oneway(*groups)
                st.write(f"F-statistic = {stat:.3f}, p-value = {pval:.5f}")
                if pval < 0.05:
                    st.success("Terdapat perbedaan gaji yang signifikan antar lokasi (p < 0.05).")
                else:
                    st.info("Tidak ada bukti perbedaan signifikan antar lokasi (p >= 0.05).")
            except Exception as e:
                st.error("Gagal melakukan ANOVA: " + str(e))
        else:
            st.info("Perlu minimal 2 lokasi untuk melakukan ANOVA.")
