### Tracer Alumni UNSIKA — Streamlit Dashboard

Dashboard interaktif untuk analisis hasil tracer study alumni (UNSIKA) berbasis Streamlit. Proyek ini memuat berbagai halaman analitik seperti ringkasan KPI, statistik, sentimen, klasterisasi K-Means, korelasi, dan EDA, dengan filter global yang konsisten di seluruh halaman.

---

## Fitur Utama

- **Filter Global (Sidebar)**: Tahun Angkatan, Program Studi, Konsentrasi, Lokasi Geografis — berlaku untuk semua halaman.
- **Overview (Halaman Utama)**:
  - KPI: jumlah alumni, rata-rata gaji, rata-rata IPK, rata-rata masa tunggu kerja.
  - Pie Konsentrasi, peta sebaran provinsi (choropleth), insight otomatis ringkas.
  - Ringkasan EDA & Korelasi otomatis (numerik, kategorikal, korelasi kuat).
- **Statistik** (`pages/2_Statistik.py`): Ringkasan visual statistik (sesuai implementasi file).
- **Sentimen** (`pages/3_Sentimen.py`): Analisis sentimen (sesuai implementasi file).
- **Klaster** (`pages/4_Klaster.py`): Klasterisasi K-Means dengan pemilihan variabel dan jumlah klaster, ringkasan per klaster, serta visualisasi sebaran klaster.
- **Korelasi** (`pages/5_Korelasi.py`): Eksplorasi korelasi variabel (sesuai implementasi file).
- **EDA** (`pages/6_EDA.py`): Eksplorasi data (sesuai implementasi file).

---

## Struktur Proyek

```
Tracer_Dashboard/
├─ app.py                        # Halaman Overview (entry point)
├─ utils.py                      # Loader CSV & manajemen filter global
├─ new_tracer_alumni_elektro_unsika.csv  # Dataset sumber (contoh)
├─ pages/
│  ├─ 1_Karir_Gaji.py           # (opsional) karir & gaji
│  ├─ 2_Statistik.py            # statistik
│  ├─ 3_Sentimen.py             # sentimen
│  ├─ 4_Klaster.py              # klasterisasi K-Means
│  ├─ 5_Korelasi.py             # korelasi
│  └─ 6_EDA.py                  # EDA
```

---

## Prasyarat

- Python 3.9+ (disarankan)
- Pip atau conda

---

## Instalasi

1) Buat dan aktifkan virtual environment (opsional tapi disarankan):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2) Instal dependensi yang diperlukan:

```bash
pip install streamlit pandas plotly scikit-learn
```

---

## Menjalankan Aplikasi

Pastikan file data `new_tracer_alumni_elektro_unsika.csv` tersedia di root proyek (atau atur path pada `utils.py`). Lalu jalankan:

```bash
streamlit run app.py
```

Streamlit akan menampilkan URL lokal, misalnya `http://localhost:8501`.

---

## Konfigurasi Data

- Lokasi default CSV diatur pada `utils.py` melalui konstanta `CSV_PATH`.
- Kolom yang digunakan (contoh, dapat disesuaikan dengan dataset Anda):
  - "Tahun Angkatan", "Program Studi", "Konsentrasi", "Lokasi Geografis"
  - "Gaji", "IPK", "Masa Tunggu Kerja", "Bidang Industri"
  - "Relevansi Kurikulum" (untuk klaster)
- Jika nama kolom Anda berbeda, samakan dengan yang dirujuk di kode atau modifikasi kode sesuai kebutuhan.

---

## Tentang Halaman Klaster (K-Means)

- Pilih jumlah klaster (k) dan variabel numerik yang tersedia: "Gaji", "Tahun Angkatan", "Relevansi Kurikulum", "IPK", "Masa Tunggu Kerja".
- Data diproses dengan StandardScaler lalu dikelompokkan dengan KMeans (`sklearn`).
- Ditampilkan ringkasan rata-rata per klaster serta visualisasi sebaran (mis. IPK vs Gaji).

---

## Deploy ke Streamlit Community Cloud

1) Push repo ini ke GitHub.
2) Di Streamlit Community Cloud, buat aplikasi baru dan arahkan ke repo ini.
3) Atur file utama ke `app.py` dan Python version (jika perlu).
4) Tambahkan file data ke repo atau gunakan storage eksternal (S3/GDrive) dan ubah loader.

Untuk produksi, sebaiknya tambahkan `requirements.txt` berisi:

```
streamlit
pandas
plotly
scikit-learn
```

---

## Kontribusi

Kontribusi sangat terbuka. Silakan buat issue untuk bug/ide, atau ajukan pull request.

---

## Lisensi

Belum ditentukan. Jika ingin menggunakan, sebutkan sumber repo ini.


