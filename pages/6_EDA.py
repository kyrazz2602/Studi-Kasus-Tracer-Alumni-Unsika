# pages/6_EDA.py
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

st.title("🔍 Exploratory Data Analysis (EDA)")

if df_filtered.empty:
    st.warning("Tidak ada data setelah filter.")
else:
    st.subheader("Ringkasan Statistik Deskriptif")
    st.dataframe(df_filtered.describe(include="all").T)

    st.subheader("Distribusi Variabel Numerik")
    num_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        chosen_num = st.selectbox("Pilih variabel numerik:", num_cols)
        fig, ax = plt.subplots()
        sns.histplot(df_filtered[chosen_num], kde=True, bins=20, ax=ax)
        ax.set_title(f"Distribusi {chosen_num}")
        st.pyplot(fig)
    else:
        st.info("Tidak ada variabel numerik.")

    st.subheader("Distribusi Variabel Kategorikal")
    cat_cols = df_filtered.select_dtypes(exclude=[np.number]).columns.tolist()
    if cat_cols:
        chosen_cat = st.selectbox("Pilih variabel kategorikal:", cat_cols)
        freq = df_filtered[chosen_cat].value_counts().reset_index()
        freq.columns = [chosen_cat, "Jumlah"]
        fig2 = px.bar(freq, x=chosen_cat, y="Jumlah", title=f"Distribusi {chosen_cat}")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Tidak ada variabel kategorikal.")

    st.subheader("Boxplot Outlier Detection")
    if num_cols:
        chosen_box = st.selectbox("Pilih variabel numerik untuk boxplot:", num_cols, index=0)
        fig3, ax3 = plt.subplots()
        sns.boxplot(x=df_filtered[chosen_box], ax=ax3)
        ax3.set_title(f"Boxplot {chosen_box}")
        st.pyplot(fig3)

    st.subheader("Pairplot Variabel Terpilih")
    if len(num_cols) >= 2:
        selected_pair = st.multiselect("Pilih variabel numerik untuk pairplot (max 4):", num_cols, default=num_cols[:2])
        if len(selected_pair) >= 2:
            fig4 = sns.pairplot(df_filtered[selected_pair], diag_kind="kde")
            st.pyplot(fig4)

    st.subheader("Tabulasi Silang Dua Variabel Kategorikal")
    if len(cat_cols) >= 2:
        var1 = st.selectbox("Pilih variabel kategorikal 1:", cat_cols, index=0)
        var2 = st.selectbox("Pilih variabel kategorikal 2:", cat_cols, index=1)
        ct = pd.crosstab(df_filtered[var1], df_filtered[var2])
        st.dataframe(ct)

# Tambahan insight otomatis

# Setelah statistik deskriptif
st.subheader("📌 Insight Statistik Deskriptif")
if not df_filtered.empty:
    if num_cols:
        avg_vals = df_filtered[num_cols].mean().round(2)
        max_vals = df_filtered[num_cols].max().round(2)
        min_vals = df_filtered[num_cols].min().round(2)
        st.markdown("- Rata-rata variabel numerik:")
        for c in num_cols:
            st.write(f"  • {c}: {avg_vals[c]} (min: {min_vals[c]}, max: {max_vals[c]})")

# Setelah distribusi numerik
st.subheader("📌 Insight Distribusi Numerik")
if chosen_num:
    mean_val = df_filtered[chosen_num].mean()
    median_val = df_filtered[chosen_num].median()
    if abs(mean_val - median_val) / median_val > 0.2:
        st.warning(f"- Distribusi **{chosen_num}** tampak miring (mean {mean_val:.2f} ≠ median {median_val:.2f}).")
    else:
        st.success(f"- Distribusi **{chosen_num}** relatif simetris (mean ≈ median).")

# Setelah distribusi kategorikal
st.subheader("📌 Insight Distribusi Kategorikal")
if chosen_cat:
    top_cat = freq.iloc[0]
    st.write(f"- Kategori paling dominan di **{chosen_cat}**: **{top_cat[chosen_cat]}** ({top_cat['Jumlah']} data).")
    if len(freq) > 5 and (top_cat['Jumlah'] / freq['Jumlah'].sum()) > 0.6:
        st.warning(f"- Ada dominasi kategori di {chosen_cat}, sebaiknya hati-hati dalam analisis.")

# Setelah boxplot
st.subheader("📌 Insight Outlier")
if chosen_box:
    q1 = df_filtered[chosen_box].quantile(0.25)
    q3 = df_filtered[chosen_box].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr
    outliers = df_filtered[(df_filtered[chosen_box] < lower) | (df_filtered[chosen_box] > upper)]
    st.write(f"- Ditemukan **{len(outliers)} outlier** pada {chosen_box}.")
    if len(outliers) > 0:
        st.dataframe(outliers[[chosen_box]].head())

# Setelah pairplot
if len(selected_pair) >= 2:
    st.subheader("📌 Insight Pairplot")
    corr = df_filtered[selected_pair].corr()
    strong_corr = [(a, b, corr.loc[a, b]) for a in corr.columns for b in corr.columns if a != b and abs(corr.loc[a, b]) > 0.5]
    if strong_corr:
        st.markdown("Hubungan korelasi kuat terdeteksi:")
        for a, b, r in strong_corr:
            arah = "positif" if r > 0 else "negatif"
            st.write(f"- {a} & {b}: r = {r:.2f} ({arah})")
