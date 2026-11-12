# Analisis Penyewaan Sepeda (Bike Sharing)

Proyek ini menganalisis data penyewaan sepeda harian pada 2011–2012 dan menyajikan hasilnya dalam dashboard interaktif Streamlit. Analisis utama dilakukan di `notebook.ipynb`; dashboard membaca data hasil olahan dari `dashboard/main_data.csv`.

## Pertanyaan Bisnis

1. Bagaimana rata-rata penyewaan harian berbeda menurut musim dan kondisi cuaca?
2. Bagaimana perbandingan pengguna casual dan registered pada hari kerja dibanding hari nonkerja (akhir pekan atau hari libur)?
3. Bagaimana pertumbuhan total penyewaan tiap bulan pada 2012 dibanding bulan yang sama pada 2011?

## Temuan Utama

- Rata-rata penyewaan tertinggi terjadi pada musim Fall (5.644 sewa per hari), sedangkan terendah pada Spring (2.604); selisih relatifnya 116,7%.
- Cuaca Cerah memiliki rata-rata tertinggi (4.877 per hari), sedangkan Hujan/Salju Ringan terendah (1.803); selisih relatifnya 170,4%.
- Pengguna casual rata-rata menyewa lebih banyak pada hari nonkerja daripada hari kerja (1.371 dibanding 607). Porsi casual naik dari 13,2% menjadi 31,7%; pengguna registered tetap menjadi mayoritas pada kedua jenis hari.
- Total penyewaan meningkat 64,9%, dari 1.243.103 pada 2011 menjadi 2.049.576 pada 2012. Pertumbuhan bulanan tertinggi terjadi pada Maret (157,4%) dan terendah pada Juni (41,3%).
- Pada analisis suhu, proporsi hari dengan permintaan tinggi terbesar terjadi pada rentang 20 hingga kurang dari 30 C (43,0%). Temuan ini bersifat deskriptif dan tidak membuktikan hubungan sebab-akibat.

## Fitur Dashboard

- Filter rentang tanggal, musim, dan kondisi cuaca.
- Ringkasan total penyewaan, rata-rata penyewaan harian, serta porsi pengguna casual dan registered.
- Grafik penyewaan menurut musim dan cuaca.
- Perbandingan jenis pengguna pada hari kerja dan hari nonkerja.
- Tren penyewaan bulanan 2011 dan 2012.
- Perbandingan kategori suhu dengan tingkat permintaan.

## Struktur Proyek

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Data

- `data/day.csv`: data penyewaan harian yang digunakan untuk menjawab pertanyaan bisnis.
- `data/hour.csv`: data penyewaan per jam; disertakan sebagai bagian dari dataset, tetapi tidak digunakan dalam analisis harian ini.
- `dashboard/main_data.csv`: data bersih dan fitur turunan yang dibaca oleh dashboard. Berkas ini dihasilkan oleh sel ekspor di notebook.

Notebook mengubah tanggal dan label kategori, menangani satu nilai kelembapan bernilai nol, serta mengonversi beberapa kolom cuaca ke satuan yang lebih mudah dibaca. Nilai ekstrem tidak dihapus karena belum terbukti sebagai kesalahan pencatatan.

## Persiapan Environment

Pastikan Python dan pip sudah terpasang. Jalankan perintah dari folder utama proyek.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS atau Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Dependensi dashboard yang dipasang tercantum di `requirements.txt`: pandas, numpy, matplotlib, seaborn, dan streamlit.

## Menjalankan Dashboard

Dari folder utama proyek dan setelah environment diaktifkan:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan tersedia di [http://localhost:8501](http://localhost:8501).

## Menjalankan Notebook

Buka `notebook.ipynb` di VS Code dengan ekstensi Jupyter, pilih interpreter dari environment proyek, lalu jalankan semua sel dari atas ke bawah. Jalankan dari folder utama proyek agar path `data/day.csv` dan ekspor `dashboard/main_data.csv` ditemukan dengan benar. Jika kernel belum tersedia, pasang `ipykernel` pada environment tersebut.