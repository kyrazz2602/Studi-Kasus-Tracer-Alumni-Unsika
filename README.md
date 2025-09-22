### 🚀 Tracer Alumni UNSIKA — Streamlit Dashboard

Dashboard interaktif untuk menganalisis hasil tracer study alumni (UNSIKA) berbasis Streamlit. Menyediakan KPI, statistik, sentimen, klasterisasi K-Means, korelasi, dan EDA, lengkap dengan filter global yang konsisten di semua halaman.

---

## ✨ Fitur Utama

- **🧭 Filter Global (Sidebar)**: Tahun Angkatan, Program Studi, Konsentrasi, Lokasi Geografis — berlaku di semua halaman.
- **📊 Overview**: KPI (jumlah alumni, rata-rata gaji, IPK, masa tunggu), pie konsentrasi, peta provinsi (choropleth), insight otomatis, ringkasan EDA & korelasi.
- **📈 Statistik**: Scatter + trendline, uji Chi-Square, ANOVA (sesuai ketersediaan kolom).
- **💬 Sentimen**: Distribusi sentimen (rule-based sederhana bila kolom belum ada) dan sampel umpan balik.
- **🧩 Klaster (K-Means)**: Pilih variabel numerik dan jumlah klaster, ringkasan per klaster, visualisasi sebaran.
- **🔗 Korelasi**: Eksplorasi korelasi variabel (di halaman terkait).
- **🧪 EDA**: Eksplorasi data (di halaman terkait).

---

## 🧱 Struktur Proyek

```
Tracer_Dashboard/
├─ app.py                        # Halaman Overview (entry point)
├─ utils.py                      # Loader CSV & manajemen filter global
├─ new_tracer_alumni_elektro_unsika.csv  # Dataset contoh (opsional)
├─ pages/
│  ├─ 1_Karir_Gaji.py           # Karir & Gaji
│  ├─ 2_Statistik.py            # Analisis Statistik
│  ├─ 3_Sentimen.py             # Umpan Balik & Sentimen
│  ├─ 4_Klaster.py              # Klasterisasi K-Means
│  ├─ 5_Korelasi.py             # Korelasi (jika digunakan)
│  └─ 6_EDA.py                  # EDA (jika digunakan)
├─ requirements.txt             # Dependensi Python
└─ .gitignore                   # File/dir yang diabaikan Git
```

---

## 🧰 Prasyarat

- Python 3.9+ (disarankan)
- Pip atau conda

---

## ⚙️ Instalasi

1) Buat dan aktifkan virtual environment (opsional tapi disarankan):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2) Instal dependensi:

```bash
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Aplikasi

Pastikan file data `new_tracer_alumni_elektro_unsika.csv` ada di root proyek (atau sesuaikan `CSV_PATH` di `utils.py`). Lalu jalankan:

```bash
streamlit run app.py
```

Aplikasi akan muncul di `http://localhost:8501`.

---

## 🗂️ Konfigurasi Data

- Path default CSV disetel di `utils.py` melalui konstanta `CSV_PATH`.
- Kolom yang digunakan (contoh, sesuaikan dengan dataset Anda):
  - "Tahun Angkatan", "Program Studi", "Konsentrasi", "Lokasi Geografis"
  - "Gaji", "IPK", "Masa Tunggu Kerja", "Bidang Industri"
  - "Relevansi Kurikulum" (untuk klaster)
- Bila nama kolom berbeda, samakan dengan yang dirujuk di kode atau sesuaikan peta `rename_map` pada `utils.py`.

---

## 🧩 Tentang Halaman Klaster (K-Means)

- Pilih jumlah klaster (k) dan variabel numerik: "Gaji", "Tahun Angkatan", "Relevansi Kurikulum", "IPK", "Masa Tunggu Kerja".
- Data diskalakan dengan `StandardScaler`, lalu dikelompokkan `KMeans`.
- Tersedia ringkasan rata-rata per klaster dan visualisasi (mis. IPK vs Gaji).

---

## ☁️ Deploy ke Streamlit Community Cloud

1) Push repo ke GitHub.
2) Buat app di Streamlit Community Cloud dan arahkan ke repo ini.
3) Set main file `app.py` (Python version mengikuti `requirements.txt`).
4) Sertakan data di repo atau gunakan storage eksternal dan sesuaikan loader.

---

## 🤝 Kontribusi

Kontribusi sangat terbuka. Silakan buat issue untuk bug/ide, atau ajukan pull request.

---

## 📄 Lisensi

Belum ditentukan. Jika ingin menggunakan, sertakan atribusi ke repo ini.

