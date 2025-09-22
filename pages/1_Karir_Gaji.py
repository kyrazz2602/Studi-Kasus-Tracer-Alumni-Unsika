# pages/1_Karir_Gaji.py
import streamlit as st
import plotly.express as px
from utils import load_data, init_filters, apply_filters

st.set_page_config(layout="wide")
df = load_data()
init_filters(df)
df_filtered = apply_filters(df)

st.title("💼 Karir & Gaji")

if df_filtered.empty:
    st.warning("Tidak ada data setelah filter.")
else:

    # ========================
    # Boxplot per Industri
    # ========================
    st.subheader("Distribusi Gaji per Bidang Industri (Boxplot)")
    if {"Bidang Industri","Gaji"}.issubset(df_filtered.columns):
        fig1 = px.box(df_filtered, x="Bidang Industri", y="Gaji", points="all", title="Gaji per Industri")
        st.plotly_chart(fig1, use_container_width=True)

    # ========================
    # Bar plot rata-rata gaji per Industri
    # ========================
    st.subheader("Rata-rata Gaji per Bidang Industri (Bar Plot)")
    if {"Bidang Industri","Gaji"}.issubset(df_filtered.columns):
        avg_industri = df_filtered.groupby("Bidang Industri")["Gaji"].mean().reset_index()
        fig_bar_ind = px.bar(avg_industri, x="Bidang Industri", y="Gaji",
                             title="Rata-rata Gaji per Industri", text_auto=".2s")
        st.plotly_chart(fig_bar_ind, use_container_width=True)

    # ========================
    # Boxplot per Lokasi
    # ========================
    st.subheader("Distribusi Gaji per Lokasi Geografis (Boxplot)")
    if {"Lokasi Geografis","Gaji"}.issubset(df_filtered.columns):
        fig2 = px.box(df_filtered, x="Lokasi Geografis", y="Gaji", points="all", title="Gaji per Lokasi")
        st.plotly_chart(fig2, use_container_width=True)

    # ========================
    # Bar plot rata-rata gaji per Lokasi
    # ========================
    st.subheader("Rata-rata Gaji per Lokasi Geografis (Bar Plot)")
    if {"Lokasi Geografis","Gaji"}.issubset(df_filtered.columns):
        avg_lokasi = df_filtered.groupby("Lokasi Geografis")["Gaji"].mean().reset_index()
        fig_bar_loc = px.bar(avg_lokasi, x="Lokasi Geografis", y="Gaji",
                             title="Rata-rata Gaji per Lokasi", text_auto=".2s")
        st.plotly_chart(fig_bar_loc, use_container_width=True)

    # ========================
    # Top 10 Perusahaan
    # ========================
    st.subheader("Top 10 Perusahaan (filter)")
    if "Perusahaan" in df_filtered.columns:
        st.table(
            df_filtered["Perusahaan"].value_counts()
            .head(10)
            .rename_axis("Perusahaan")
            .reset_index(name="Jumlah")
        )

    # ========================
    # Top 10 Posisi/Jabatan
    # ========================
    st.subheader("Top 10 Posisi/Jabatan (filter)")
    if "Posisi/Jabatan" in df_filtered.columns:
        st.table(
            df_filtered["Posisi/Jabatan"].value_counts()
            .head(10)
            .rename_axis("Posisi/Jabatan")
            .reset_index(name="Jumlah")
        )
