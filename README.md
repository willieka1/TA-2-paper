# 5G Network Slices Resource Orchestration — Critical Review & Interactive Simulation

Platform web interaktif untuk tinjauan kritis paper (**20 panduan review**) dan simulasi orkestrasi resource 5G network slicing & edge computing berdasarkan paper:

> **"5G network slices resource orchestration using Machine Learning techniques"**  
> *Nazih Salhab, Rami Langar, Rana Rahim*  
> Published in: **Elsevier Computer Networks**, Vol. 188 (2021), 107829  
> DOI: [10.1016/j.comnet.2021.107829](https://doi.org/10.1016/j.comnet.2021.107829)

Repository: [https://github.com/willieka1/TA-2-paper](https://github.com/willieka1/TA-2-paper)

---

## 🎯 Relevansi Terhadap Topik Tugas Akhir (TA)
**Topik TA:**
> *"Bagaimana mengelola kapasitas network slicing 5G dan edge computing secara dinamis, otomatis, dan dengan gangguan minimum terhadap layanan/session pengguna saat trafik berubah-ubah."*

**Status Paper:** **HIGHLY RELEVANT**
- ✅ **Dynamic Resource Allocation:** Memprediksi rasio alokasi Physical Resource Blocks (PRBs) di RAN secara adaptif via *Regression Trees* (selisih hanya 5% terhadap optimum teoritis).
- ✅ **Edge Computing & Admission Control:** Mengontrol admisi vCPU (2 vCPUs) dan RAM (1 GB) berbasis optimasi Knapsack berdimensi-D (D-MCKP).
- ✅ **Zero Session Interruption:** Menggunakan elastisitas *Docker microservices* dan kontrol aliran adaptif Deep Reinforcement Learning (DRL) untuk menjamin koneksi aktif pengguna tidak terputus.
- ✅ **Validasi Testbed Nyata:** Diuji pada prototype 5G NSA (Option 3) menggunakan OpenAirInterface (OAI), FlexRAN SDN controller, USRP B210 (10 MHz/50 PRB & 20 MHz/100 PRB), dan COTS smartphones.
- ✅ **Eliminasi Buffer Backlog:** Menurunkan kejadian non-zero Buffer Status Report (BSR) dari >400 kejadian menjadi 0 kejadian.

---

## 🚀 Fitur Utama Web

1. **🎮 Simulasi Interaktif 5G Orchestrator:**
   - Pemilihan bandwidth: 10 MHz (50 PRBs) atau 20 MHz (100 PRBs).
   - Pembanding 4 algoritma: **Regression Trees (Paper)**, **Optimum**, **Static (50:50)**, dan **Random**.
   - Kendali beban 3 slice: eMBB (YouTube video), uRLLC (misi kritis delay 10ms), mMTC (sensor gateway).
   - Saklar perbandingan: **With Decision Maker & Scheduler** vs **Without Decision Maker** (membuktikan eliminasi BSR backlog dan zero session drop).
   - Grafik animasi live throughput dan utilisasi CPU over time (mereproduksi Fig. 9a & 9b paper).
2. **📑 20 Bagian Critical Review Lengkap:**
   - Tersusun terstruktur sesuai template panduan review PDF (Identitas, Problem-Objective-Method-Experiment-Result, Existing System, Masalah & Trigger, Dampak KPI, Analisis Closed-Loop, Limitasi Eksplisit/Inferensi, Candidate Gaps, Claim to Verify, Rekomendasi Bacaan, hingga Final Summary).
3. **📊 Komparasi 3 Paper Utama:**
   - Menjajarkan *Salhab et al. (2021)* dengan *Zhang et al. (2017)* dan *Apruzzese et al. (2023)*.
4. **📋 Matriks 15 Aspek TA:**
   - Pemetaan 15 komponen tugas akhir beserta kutipan bukti halaman paper.
5. **📄 Ringkasan 1-Menit & Format Excel (TSV):**
   - Dilengkapi tombol 1-klik untuk menyalin ringkasan dan baris tabel Excel ke clipboard.

---

## ⚡ Deployment ke Vercel

Web ini dirancang tanpa dependensi eksternal (*zero-dependency* vanilla web) sehingga dapat langsung di-deploy ke **Vercel** secara otomatis:

1. Import repository `willieka1/TA-2-paper` di dashboard [Vercel](https://vercel.com).
2. Framework Preset: pilih **Other** (karena menggunakan file `index.html` murni di root).
3. Klik **Deploy** — web langsung aktif secara global dalam hitungan detik!

File konfigurasi `vercel.json` sudah tersedia di root proyek:
```json
{
  "version": 2,
  "cleanUrls": true
}
```

---

## 💻 Menjalankan Secara Lokal

### Opsi A: Langsung Buka di Browser (Paling Cepat)
Cukup buka file `index.html` dengan peramban web apapun (Google Chrome, Microsoft Edge, Mozilla Firefox).

### Opsi B: Menggunakan Python Flask
```bash
# Install dependensi
pip install -r requirements.txt

# Jalankan server
python app.py
```
Akses di browser: `http://127.0.0.1:5000`
