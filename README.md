# Bike Sharing Data Analysis Dashboard 🚲

## Deskripsi
Proyek ini merupakan analisis data pada dataset "Bike Sharing" untuk mengeksplorasi pola penyewaan sepeda berdasarkan berbagai faktor seperti waktu (jam), kondisi cuaca, dan suhu. Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Struktur Direktori
- **dashboard**: Berisi file utama untuk dashboard (`app.py`) dan dataset yang sudah dibersihkan (`main_data.csv`).
- **data**: Berisi dataset mentah dalam format CSV (`day.csv` dan `hour.csv`).
- **notebook.ipynb**: File Jupyter Notebook yang berisi proses analisis data lengkap dari Wrangling hingga Visualisasi.
- **requirements.txt**: Daftar library Python yang dibutuhkan.
- **README.md**: Dokumentasi proyek ini.

## Instalasi
1. Clone repositori ini ke komputer lokal Anda:
    git clone (https://github.com/hafifahoktariwidri-lang/proyek-analisis-data-bike-sharing))
2. Pastikan Anda memiliki Python terinstal (disarankan versi 3.9 ke atas).
3. Instal library yang dibutuhkan menggunakan pip:
```
     pip install -r requirements.txt
```

## Cara Menjalankan Dashboard
1. Buka terminal atau command prompt.
2. Masuk ke direktori proyek (folder dashboard):
  ```
 cd dashboard
```
3. Jalankan aplikasi Streamlit:
 ```
  streamlit run app.py
```
4. Dashboard akan terbuka secara otomatis di browser Anda
   (http://localhost:8501).
