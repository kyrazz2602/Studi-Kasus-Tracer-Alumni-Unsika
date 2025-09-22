# app.py
import streamlit as st
import plotly.express as px
from utils import load_data, init_filters, apply_filters

# -------------------------------------------------
# Helper functions (presentation only)
# -------------------------------------------------
def _fmt_currency(value: float) -> str:
    if value is None:
        return "-"
    try:
        return f"Rp {value:,.0f}"
    except Exception:
        return "-"

st.set_page_config(page_title="Tracer Alumni UNSIKA - Overview", layout="wide")
df = load_data()

# Global filters (render once and stored in session_state)
init_filters(df)
df_filtered = apply_filters(df)

st.title("📊 Dashboard Tracer Alumni UNSIKA — Overview")
st.markdown("Gunakan filter di sidebar untuk menyaring data secara global (berlaku untuk semua halaman).")

# KPI cards
col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,1.2])
with col1:
    st.metric("Jumlah Alumni (filter)", value=f"{len(df_filtered):,}")
with col2:
    if "Gaji" in df_filtered.columns and not df_filtered.empty:
        st.metric("Rata-rata Gaji", value=_fmt_currency(float(df_filtered['Gaji'].mean())))
    else:
        st.metric("Rata-rata Gaji", value="-")
with col3:
    if "IPK" in df_filtered.columns and not df_filtered.empty:
        st.metric("Rata-rata IPK", value=f"{df_filtered['IPK'].mean():.2f}")
    else:
        st.metric("Rata-rata IPK", value="-")
with col4:
    if "Masa Tunggu Kerja" in df_filtered.columns and not df_filtered.empty:
        st.metric("Rata-rata Masa Tunggu (bln)", value=f"{df_filtered['Masa Tunggu Kerja'].mean():.1f}")
    else:
        st.metric("Rata-rata Masa Tunggu (bln)", value="-")

# Top area charts
st.subheader("Distribusi Konsentrasi (filter aktif)")
if not df_filtered.empty and "Konsentrasi" in df_filtered.columns:
    fig_pie = px.pie(df_filtered, names="Konsentrasi", title="Proporsi Alumni per Konsentrasi")
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("Tidak ada data konsentrasi yang tersedia untuk filter ini.")

# Peta Choropleth sederhana per Provinsi (butuh nama provinsi sesuai geojson)
st.subheader("Sebaran Alumni per Provinsi")
if not df_filtered.empty and "Lokasi Geografis" in df_filtered.columns:
    prov_df = df_filtered["Lokasi Geografis"].value_counts().reset_index()
    prov_df.columns = ["Provinsi", "Jumlah"]

    # Normalisasi teks (hapus spasi, kapitalisasi awal tiap kata)
    prov_df["Provinsi"] = prov_df["Provinsi"].str.strip().str.title()

    # Mapping manual untuk selisih nama
    mapping_prov = {
        "Dki Jakarta": "DKI Jakarta",
        "Jakarta": "DKI Jakarta",
        "Jawa barat": "Jawa Barat",
        "Jawa timur": "Jawa Timur",
        "Jawa tengah": "Jawa Tengah",
        "Yogyakarta": "DI Yogyakarta",
        "Daerah Istimewa Yogyakarta": "DI Yogyakarta",
        "Aceh darussalam": "Aceh",
        "Kepulauan riau": "Kepulauan Riau",
        "Bangka belitung": "Kep. Bangka Belitung",
        "Kepulauan Bangka Belitung": "Kep. Bangka Belitung",
        "Papua barat": "Papua Barat",
        "Papua selatan": "Papua Selatan",
        "Papua tengah": "Papua Tengah",
        "Papua pegunungan": "Papua Pegunungan"
    }
    prov_df["Provinsi"] = prov_df["Provinsi"].replace(mapping_prov)

    geojson_url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province.json"
    try:
        fig_map = px.choropleth(
            prov_df,
            geojson=geojson_url,
            locations="Provinsi",
            featureidkey="properties.Propinsi",
            color="Jumlah",
            color_continuous_scale="Viridis",
            title="Sebaran Alumni per Provinsi"
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map, use_container_width=True)
    except Exception as e:
        st.error("Gagal menampilkan peta. Periksa mapping provinsi.")
        st.write(str(e))
else:
    st.info("Tidak ada data lokasi untuk filter ini.")


# Insight otomatis sederhana
st.subheader("📌 Insight Otomatis (ringkas)")
if not df_filtered.empty:
    lines = []
    # avg salary
    if "Gaji" in df_filtered.columns:
        avg_sal = df_filtered["Gaji"].mean()
        overall_avg = df["Gaji"].mean() if "Gaji" in df.columns else None
        delta = f"{(avg_sal/overall_avg -1)*100:.1f}%" if overall_avg else ""
        lines.append(f"- Rata-rata gaji pada filter: **Rp {avg_sal:,.0f}** ({delta} vs keseluruhan).")
    # top industry
    if "Bidang Industri" in df_filtered.columns:
        top_ind = df_filtered["Bidang Industri"].value_counts().idxmax()
        lines.append(f"- Bidang industri dominan: **{top_ind}**.")
    # top provinsi
    if "Lokasi Geografis" in df_filtered.columns:
        top_prov = df_filtered["Lokasi Geografis"].value_counts().idxmax()
        lines.append(f"- Provinsi terbanyak: **{top_prov}** ({df_filtered['Lokasi Geografis'].value_counts().max()} alumni).")
    st.markdown("\n".join(lines))
else:
    st.warning("Filter menghasilkan dataset kosong — tidak ada insight yang dapat ditampilkan.")

# ===================================================
# 📌 Ringkasan EDA & Korelasi (Auto Insight)
# ===================================================
st.subheader("📊 Ringkasan EDA & Korelasi")

# Variabel numerik
num_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
cat_cols = df_filtered.select_dtypes(exclude=['number']).columns.tolist()

# Insight distribusi numerik
if num_cols:
    st.markdown("**Insight Numerik:**")
    for col in num_cols:
        if col.lower() == "ipk":  # khusus IPK pakai float 2 desimal
            mean_val = round(df_filtered[col].mean(), 2)
            median_val = round(df_filtered[col].median(), 2)
            min_val = round(df_filtered[col].min(), 2)
            max_val = round(df_filtered[col].max(), 2)
        else:  # default integer
            mean_val = int(round(df_filtered[col].mean()))
            median_val = int(round(df_filtered[col].median()))
            min_val = int(round(df_filtered[col].min()))
            max_val = int(round(df_filtered[col].max()))

        if median_val != 0 and abs(mean_val - median_val) / (median_val+1e-9) > 0.2:
            skew_info = "→ Distribusi miring (mean ≠ median)."
        else:
            skew_info = "→ Distribusi relatif simetris."

        st.write(f"- {col}: mean = {mean_val}, median = {median_val}, range = [{min_val}, {max_val}] {skew_info}")


# Insight kategorikal
if cat_cols:
    st.markdown("**Insight Kategorikal:**")
    for col in cat_cols[:3]:  # batasi agar ringkas
        freq = df_filtered[col].value_counts()
        if not freq.empty:
            top_cat, top_val = freq.index[0], freq.iloc[0]
            ratio = top_val / freq.sum()
            if ratio > 0.6:
                warn = "⚠️ kategori ini sangat dominan (>60%)."
            else:
                warn = ""
            st.write(f"- {col}: kategori terbanyak = **{top_cat}** ({top_val} data). {warn}")

# Insight korelasi
if len(num_cols) >= 2:
    corr = df_filtered[num_cols].corr()
    strong_corr = []
    for i in corr.columns:
        for j in corr.columns:
            if i != j and abs(corr.loc[i, j]) >= 0.5:
                strong_corr.append((i, j, corr.loc[i, j]))
    if strong_corr:
        st.markdown("**Insight Korelasi (|r| ≥ 0.5):**")
        seen = set()
        for (a, b, r) in strong_corr:
            if (b, a) not in seen:
                arah = "positif" if r > 0 else "negatif"
                st.write(f"- {a} & {b}: r = {r:.2f} ({arah})")
            seen.add((a, b))
    else:
        st.info("Tidak ada korelasi kuat antar variabel numerik (|r| ≥ 0.5).")
