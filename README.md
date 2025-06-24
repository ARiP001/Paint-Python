# Web Paint Sederhana 🎨

[🌐 Coba versi online di Streamlit Cloud](https://paint-grafika-python.streamlit.app/)

Aplikasi web sederhana untuk menggambar (paint) berbasis [Streamlit](https://streamlit.io/). Cocok untuk kreativitas digital, interaksi visual ringan, dan demonstrasi fitur drawing di web.

## Fitur Utama
- Pilihan mode gambar: Free Draw, Line, Rectangle, Circle, Polygon, Transform
- Pengaturan warna stroke, warna fill, transparansi, dan background
- Undo/Redo aksi gambar
- Upload gambar sebagai background
- Download hasil gambar sebagai PNG
- Tabel data objek gambar (untuk analisis/inspeksi)

## Demo
![Demo Web Paint Sederhana](https://user-images.githubusercontent.com/your-demo-image.png)

## Instalasi
1. **Clone repository ini:**
   ```bash
   git clone https://github.com/yourusername/web-paint-sederhana.git
   cd web-paint-sederhana
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Aplikasi
Jalankan perintah berikut di terminal:
```bash
streamlit run app.py
```
Akses aplikasi di browser pada alamat yang tertera (biasanya http://localhost:8501).

## Penggunaan
- Pilih mode gambar dan pengaturan di sidebar.
- Gambar di kanvas utama.
- Gunakan tombol Undo/Redo untuk mengelola aksi.
- Klik "Download PNG" untuk mengunduh hasil gambar.
- Data objek gambar ditampilkan dalam bentuk tabel di bawah kanvas.

## Dependencies
- streamlit
- streamlit-drawable-canvas
- pillow
- pandas
- streamlit-option-menu

Semua dependencies dapat diinstall melalui `requirements.txt`.

## Lisensi
MIT License

---

> Dibuat untuk pembelajaran dan demonstrasi fitur interaktif Streamlit. 