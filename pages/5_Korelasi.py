# pages/5_Korelasi.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from utils import load_data, init_filters, apply_filters

st.set_page_config(layout="wide")
df = load_data()
init_filters(df)
df_filtered = apply_filters(df)

st.title("🔗 Analisis Korelasi Variabel")

if df_filtered.empty:
    st.warning("Tidak ada data setelah filter.")
else:
    # Ambil hanya kolom numerik
    num_df = df_filtered.select_dtypes(include=[np.number])

    if num_df.shape[1] < 2:
        st.info("Tidak cukup kolom numerik untuk analisis korelasi.")
    else:
        st.subheader("Matriks Korelasi (Heatmap)")
        corr = num_df.corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, cbar=True)
        st.pyplot(fig)

        # ==========================
        # INSIGHT OTOMATIS
        # ==========================
        st.subheader("📌 Insight Otomatis Korelasi")
        high_corr = []
        for i in corr.columns:
            for j in corr.columns:
                if i != j and abs(corr.loc[i, j]) >= 0.5:
                    high_corr.append((i, j, corr.loc[i, j]))

        if high_corr:
            st.markdown("Hubungan korelasi kuat yang ditemukan (|r| ≥ 0.5):")
            seen = set()
            for (a, b, r) in high_corr:
                if (b, a) not in seen:  # hindari duplikasi
                    arah = "positif" if r > 0 else "negatif"
                    st.write(f"- **{a}** & **{b}**: r = {r:.2f} ({arah})")
                seen.add((a, b))
        else:
            st.info("Tidak ditemukan korelasi kuat antar variabel (|r| ≥ 0.5).")

        # ==========================
        # Scatter eksplorasi
        # ==========================
        st.subheader("Scatter Plot Antar Variabel")
        var_x = st.selectbox("Pilih variabel X:", num_df.columns, index=0)
        var_y = st.selectbox("Pilih variabel Y:", num_df.columns, index=1 if len(num_df.columns) > 1 else 0)

        if var_x and var_y and var_x != var_y:
            fig2, ax2 = plt.subplots()
            sns.scatterplot(x=num_df[var_x], y=num_df[var_y], ax=ax2)
            ax2.set_title(f"{var_x} vs {var_y}")
            st.pyplot(fig2)

            # Insight scatter
            r_val = corr.loc[var_x, var_y]
            arah = "positif" if r_val > 0 else "negatif"
            st.markdown(f"📌 Hubungan {var_x} & {var_y}: **r = {r_val:.2f} ({arah})**")

        # ==========================
        # Distribusi variabel
        # ==========================
        st.subheader("Distribusi Variabel Numerik")
        chosen_num = st.selectbox("Pilih variabel untuk histogram:", num_df.columns)
        if chosen_num:
            fig3, ax3 = plt.subplots()
            sns.histplot(num_df[chosen_num], kde=True, bins=20, ax=ax3)
            ax3.set_title(f"Distribusi {chosen_num}")
            st.pyplot(fig3)

            mean_val = num_df[chosen_num].mean()
            median_val = num_df[chosen_num].median()
            if abs(mean_val - median_val) / (median_val+1e-9) > 0.2:
                st.warning(f"- Distribusi **{chosen_num}** tampak miring (mean {mean_val:.2f} ≠ median {median_val:.2f}).")
            else:
                st.success(f"- Distribusi **{chosen_num}** relatif simetris (mean ≈ median).")
