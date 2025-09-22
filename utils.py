# utils.py
import streamlit as st
import pandas as pd

CSV_PATH = "new_tracer_alumni_elektro_unsika.csv"

@st.cache_data
def load_data(path: str = CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Basic cleaning safety (ensure expected columns exist)
    # Normalize column names (strip)
    df.columns = [c.strip() for c in df.columns]

    # Optional: rename common variants to expected names
    rename_map = {
        # examples of possible variants → standardized target
        "tahun_angkatan": "Tahun Angkatan",
        "tahun": "Tahun Angkatan",
        "prodi": "Program Studi",
        "program_studi": "Program Studi",
        "konsentrasi_keahlian": "Konsentrasi",
        "lokasi": "Lokasi Geografis",
        "provinsi": "Lokasi Geografis",
        "salary": "Gaji",
        "gaji_bulanan": "Gaji",
        "masa_tunggu": "Masa Tunggu Kerja",
        "masa_tunggu_kerja_bulan": "Masa Tunggu Kerja",
        "relevansi": "Relevansi Kurikulum",
        "bidang": "Bidang Industri",
    }
    intersecting_keys = [k for k in rename_map.keys() if k in df.columns]
    if intersecting_keys:
        df = df.rename(columns={k: rename_map[k] for k in intersecting_keys})

    # Normalize common text columns
    for col in [
        "Program Studi",
        "Konsentrasi",
        "Lokasi Geografis",
        "Bidang Industri",
    ]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )
            # Title-case for location to aid matching with geojson mapping
            if col == "Lokasi Geografis":
                df[col] = df[col].str.title()

    # Standardize province names used by the choropleth in app.py
    if "Lokasi Geografis" in df.columns:
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
            "Papua pegunungan": "Papua Pegunungan",
        }
        df["Lokasi Geografis"] = df["Lokasi Geografis"].replace(mapping_prov)

    # Convert numeric columns safely
    for col in [
        "Gaji",
        "IPK",
        "Masa Tunggu Kerja",
        "Relevansi Kurikulum",
        "Tahun Angkatan",
    ]:
        if col in df.columns:
            # Remove common thousand separators/locale issues
            if df[col].dtype == object:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(".", "", regex=False)
                    .str.replace(",", ".", regex=False)
                )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def init_filters(df: pd.DataFrame):
    """Render global sidebar filters and store selections in session_state."""
    if "filters_initialized" not in st.session_state:
        st.session_state.filters_initialized = True

        # Unique sorted lists (safeguard missing columns)
        years = sorted(df["Tahun Angkatan"].dropna().unique().tolist()) if "Tahun Angkatan" in df.columns else []
        kons = sorted(df["Konsentrasi"].dropna().unique().tolist()) if "Konsentrasi" in df.columns else []
        lokasi = sorted(df["Lokasi Geografis"].dropna().unique().tolist()) if "Lokasi Geografis" in df.columns else []
        prog = sorted(df["Program Studi"].dropna().unique().tolist()) if "Program Studi" in df.columns else []

        # Defaults: all selected
        st.session_state.filter_tahun = years.copy()
        st.session_state.filter_konsentrasi = kons.copy()
        st.session_state.filter_lokasi = lokasi.copy()
        st.session_state.filter_program = prog.copy()

    # Render widgets (always show, values read/write session_state)
    st.sidebar.header("🔎 Filter Global")
    # Tahun
    years_options = sorted(df["Tahun Angkatan"].dropna().unique().tolist()) if "Tahun Angkatan" in df.columns else []
    st.session_state.filter_tahun = st.sidebar.multiselect("Tahun Angkatan", years_options,
                                                            default=st.session_state.get("filter_tahun", years_options))
    # Program Studi
    prog_options = sorted(df["Program Studi"].dropna().unique().tolist()) if "Program Studi" in df.columns else []
    st.session_state.filter_program = st.sidebar.multiselect("Program Studi", prog_options,
                                                             default=st.session_state.get("filter_program", prog_options))
    # Konsentrasi
    kons_options = sorted(df["Konsentrasi"].dropna().unique().tolist()) if "Konsentrasi" in df.columns else []
    st.session_state.filter_konsentrasi = st.sidebar.multiselect("Konsentrasi", kons_options,
                                                                 default=st.session_state.get("filter_konsentrasi", kons_options))
    # Lokasi
    lok_options = sorted(df["Lokasi Geografis"].dropna().unique().tolist()) if "Lokasi Geografis" in df.columns else []
    st.session_state.filter_lokasi = st.sidebar.multiselect("Lokasi Geografis", lok_options,
                                                            default=st.session_state.get("filter_lokasi", lok_options))

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Return dataframe after applying global filters from session_state"""
    df2 = df.copy()
    # Apply filters if selections exist; if empty selection treat as 'no filter' (show all)
    ft = st.session_state.get("filter_tahun", None)
    if ft:
        if "Tahun Angkatan" in df2.columns:
            df2 = df2[df2["Tahun Angkatan"].isin(ft)]

    fp = st.session_state.get("filter_program", None)
    if fp:
        if "Program Studi" in df2.columns:
            df2 = df2[df2["Program Studi"].isin(fp)]

    fk = st.session_state.get("filter_konsentrasi", None)
    if fk:
        if "Konsentrasi" in df2.columns:
            df2 = df2[df2["Konsentrasi"].isin(fk)]

    fl = st.session_state.get("filter_lokasi", None)
    if fl:
        if "Lokasi Geografis" in df2.columns:
            df2 = df2[df2["Lokasi Geografis"].isin(fl)]

    return df2
