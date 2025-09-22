# pages/4_Klaster.py
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, init_filters, apply_filters
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")
df = load_data()
init_filters(df)
df_filtered = apply_filters(df)

st.title("🧩 Klasterisasi Alumni (K-Means)")

if df_filtered.empty:
    st.warning("Tidak ada data setelah filter.")
else:
    # Pilih kolom numerik
    candidate_cols = [
        c for c in ["Gaji", "Tahun Angkatan", "Relevansi Kurikulum", "IPK", "Masa Tunggu Kerja"]
        if c in df_filtered.columns
    ]

    if not candidate_cols:
        st.info("Tidak ada kolom numerik yang cukup untuk clustering.")
    else:
        st.sidebar.subheader("Pengaturan Klaster")
        k = st.sidebar.slider("Jumlah klaster (k)", 2, 8, 4)
        cols_to_use = st.sidebar.multiselect(
            "Variabel untuk clustering", candidate_cols, default=candidate_cols
        )

        df_cluster = df_filtered.dropna(subset=cols_to_use).copy()
        if len(df_cluster) < k:
            st.warning("Data kurang untuk jumlah klaster yang dipilih setelah dropna.")
        else:
            # K-Means
            scaler = StandardScaler()
            X = scaler.fit_transform(df_cluster[cols_to_use])
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X)
            df_cluster["Cluster"] = labels.astype(int)

            # Ringkasan per klaster
            st.subheader("Ringkasan per Klaster")
            summary = df_cluster.groupby("Cluster")[cols_to_use].mean().round(2)
            
            # ubah format Tahun Angkatan & Masa Tunggu Kerja jadi integer
            if "Tahun Angkatan" in summary.columns:
                summary["Tahun Angkatan"] = summary["Tahun Angkatan"].round().astype(int).astype(str)

            if "Masa Tunggu Kerja" in summary.columns:
                summary["Masa Tunggu Kerja"] = summary["Masa Tunggu Kerja"].round().astype(int)


            st.dataframe(summary)

            # Insight otomatis
            st.subheader("📌 Insight Otomatis Klaster")
            for c in summary.index:
                gaji_mean = float(summary.loc[c, "Gaji"]) if "Gaji" in summary.columns else None
                ipk_mean = float(summary.loc[c, "IPK"]) if "IPK" in summary.columns else None
                tunggu_mean = float(summary.loc[c, "Masa Tunggu Kerja"]) if "Masa Tunggu Kerja" in summary.columns else None
                tahun_mean = summary.loc[c, "Tahun Angkatan"] if "Tahun Angkatan" in summary.columns else None
                relevansi_mean = float(summary.loc[c, "Relevansi Kurikulum"]) if "Relevansi Kurikulum" in summary.columns else None

                st.markdown(f"**Klaster {c}:**")
                if gaji_mean is not None:
                    st.write(f"- Rata-rata gaji: Rp {gaji_mean:,.0f}")
                if ipk_mean is not None:
                    st.write(f"- Rata-rata IPK: {ipk_mean:.2f}")
                if tunggu_mean is not None:
                    st.write(f"- Rata-rata masa tunggu kerja: {int(round(tunggu_mean))} bulan")
                if tahun_mean is not None:
                    st.write(f"- Rata-rata tahun angkatan: {tahun_mean}")
                if relevansi_mean is not None:
                    st.write(f"- Rata-rata relevansi kurikulum: {relevansi_mean:.2f}")

                # Highlight khusus
                notes = []
                if (gaji_mean is not None) and (gaji_mean == float(summary["Gaji"].max())):
                    notes.append("💰 Klaster dengan gaji tertinggi")
                if (gaji_mean is not None) and (gaji_mean == float(summary["Gaji"].min())):
                    notes.append("💸 Klaster dengan gaji terendah")
                if (ipk_mean is not None) and (ipk_mean == float(summary["IPK"].max())):
                    notes.append("🎓 Klaster dengan IPK tertinggi")
                if (tunggu_mean is not None) and (tunggu_mean == float(summary["Masa Tunggu Kerja"].min())):
                    notes.append("⚡ Klaster dengan masa tunggu kerja tercepat")
                if notes:
                    st.markdown("➡️ " + "; ".join(notes))

            # Visualisasi klaster
            st.subheader("Visualisasi Klaster")
            if {"IPK", "Gaji"}.issubset(df_cluster.columns):
                fig = px.scatter(
                    df_cluster, x="IPK", y="Gaji", color="Cluster",
                    hover_data=["Tahun Angkatan", "Bidang Industri", "Konsentrasi"],
                    title="IPK vs Gaji (Cluster)"
                )
                st.plotly_chart(fig, use_container_width=True)
            elif len(cols_to_use) >= 2:
                xcol, ycol = cols_to_use[0], cols_to_use[1]
                fig = px.scatter(
                    df_cluster, x=xcol, y=ycol, color="Cluster",
                    hover_data=["Tahun Angkatan", "Bidang Industri", "Konsentrasi"],
                    title=f"{xcol} vs {ycol} (Cluster)"
                )
                st.plotly_chart(fig, use_container_width=True)
