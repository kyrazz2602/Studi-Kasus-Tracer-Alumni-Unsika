# pages/3_Sentimen.py
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, init_filters, apply_filters
from collections import Counter
import re

st.set_page_config(layout="wide")
df = load_data()
init_filters(df)
df_filtered = apply_filters(df)

st.title("💬 Analisis Umpan Balik & Sentimen")

if df_filtered.empty:
    st.warning("Tidak ada data setelah filter.")
else:
    # Ensure Sentiment column exists (if not, create simple rule-based)
    if "Sentiment" not in df_filtered.columns:
        def quick_sent(s: str):
            s = str(s).lower()
            if any(w in s for w in ["baik","bagus","membantu","positif","recommend","recommended"]):
                return "Positive"
            # improvement keywords -> neutral
            if any(w in s for w in ["perlu","perbanyak","tingkatkan","kurang","update","perbarui"]):
                return "Neutral"
            return "Neutral"
        feedback_series = df_filtered["Umpan Balik"] if "Umpan Balik" in df_filtered.columns else pd.Series([None]*len(df_filtered))
        df_filtered["Sentiment"] = feedback_series.apply(quick_sent)

    sent_cnt = df_filtered["Sentiment"].value_counts().reset_index()
    sent_cnt.columns = ["Sentiment","Jumlah"]
    fig = px.bar(sent_cnt, x="Sentiment", y="Jumlah", color="Sentiment", title="Distribusi Sentimen")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Contoh Umpan Balik")
    if "Umpan Balik" in df_filtered.columns:
        sample_df = df_filtered[["Umpan Balik","Sentiment"]].dropna()
        if not sample_df.empty:
            st.write(sample_df.sample(min(8, len(sample_df)), random_state=42).reset_index(drop=True))
        else:
            st.info("Tidak ada teks umpan balik non-null untuk ditampilkan.")
    else:
        st.info("Kolom 'Umpan Balik' tidak tersedia.")
