# CRITICAL PAPER REVIEW UNTUK TUGAS AKHIR (TA)
**Paper:** *5G network slices resource orchestration using Machine Learning techniques*  
**Penulis:** Nazih Salhab, Rami Langar, Rana Rahim  
**Publikasi:** *Computer Networks*, Vol. 188, Elsevier (2021), 107829  
**DOI:** [10.1016/j.comnet.2021.107829](https://doi.org/10.1016/j.comnet.2021.107829)  
**Topik TA Pengguna:** *"Bagaimana mengelola kapasitas network slicing 5G dan edge computing secara dinamis, otomatis, dan dengan gangguan minimum terhadap layanan/session pengguna saat trafik berubah-ubah."*

---

## 1. IDENTITAS PAPER
| Item | Isi |
| :--- | :--- |
| **Title** | 5G network slices resource orchestration using Machine Learning techniques |
| **Keywords** | Network slicing, Machine-Learning, Resource orchestration, 5G and beyond, OpenAirInterface OAI |
| **Author** | Nazih Salhab (a,b), Rami Langar (a), Rana Rahim (b,c) |
| **Afiliasi** | (a) LIGM, CNRS-UMR 8049, University Gustave Eiffel, France; (b) DSST, Lebanese University; (c) Faculty of Science, Lebanese University |
| **Tahun** | 2021 (Received: 14 Aug 2020; Accepted: 7 Jan 2021; Available online: 13 Jan 2021) |
| **Journal/Conference** | Computer Networks (Elsevier), Vol. 188, 107829 |
| **DOI** | 10.1016/j.comnet.2021.107829 |
| **Jenis Paper** | **System Implementation + Experimental + Algorithm/Optimization** |

**Ringkasan Inti Paper (1–2 kalimat):**  
Paper ini mengusulkan framework orkestrasi resource 5G end-to-end yang mengintegrasikan klasifikasi demand (Gatekeeper), prediksi rasio slicing PRB berbasis Regression Trees, kontrol admisi dan penjadwalan berbasis Knapsack (D-MCKP), serta manajemen resource adaptif berbasis Deep Reinforcement Learning (DRL) yang divalidasi pada testbed nyata OpenAirInterface (OAI) dan Docker.

---

## 2. RELEVANSI TERHADAP TA
**Klasifikasi:** **HIGHLY RELEVANT**

**Alasan Berdasarkan Isi Paper:**  
Paper ini sangat relevan karena secara langsung mengatasi masalah alokasi resource dinamis pada *network slicing 5G*, mengimplementasikan siklus *closed-loop orchestration* (monitoring via TICK stack, prediksi beban, kontrol admisi, dan penyesuaian adaptif), memodelkan kapasitas radio (PRBs) dan komputasi/memori (vCPU dan RAM), serta menguji arsitekturnya di *testbed* 5G nyata berbasis OpenAirInterface (OAI) dan microservices Docker yang menjamin koneksi sesi aktif tidak terputus (*zero session interruption*).

### Tabel Pemetaan 15 Aspek TA
| Aspek TA | Status | Bukti dari Paper |
| :--- | :---: | :--- |
| **5G** | ✓ | Menggunakan 5G NSA (Option 3) dengan split fungsional CU/DU dan FlexRAN SDN controller (Section 4.1, Fig. 3). |
| **Network slicing** | ✓ | Mengimplementasikan 3 slice standar: eMBB, uRLLC, dan mMTC (Section 1, Table 1, Section 4.2). |
| **Dynamic resource allocation** | ✓ | Memprediksi rasio alokasi PRB dinamis berdasarkan profil trafik historis dan kondisi cuaca (Section 3.2, Algorithm 1). |
| **Edge computing** | △ | Diterapkan secara konseptual melalui penempatan CU/DU dan microservice container; referensi MEC broker dibahas (Section 2.1, 4.1). |
| **Edge resource allocation** | ✓ | Memodelkan kapasitas vCPU ($C^{(1)}=2$) dan RAM ($C^{(2)}=1$ GB) dalam Knapsack optimization (Section 3.3.1, Table 2). |
| **SLA** | ✓ | Berbasis QCI standar 3GPP (delay budget 10–300 ms, loss rate $10^{-2} - 10^{-6}$, priority level) (Table 1). |
| **Network + Edge coordination** | △ | Mengoordinasikan alokasi PRBs di RAN dengan scaling container vCPU/RAM, namun belum formulasi optimasi gabungan satu atap. |
| **Monitoring** | ✓ | Menggunakan TICK Stack (Telegraf, InfluxDB, Chronograf, Kapacitor) untuk pengumpulan telemetri real-time (Section 4.1). |
| **Decision engine** | ✓ | Forecast-Aware Slicer (Regression Trees) + Admission Controller (D-MCKP heuristic) (Section 3.2, 3.3). |
| **Orchestration** | ✓ | Mengembangkan framework 4 blok pembangun (Gatekeeper, Decision Maker, Slice Scheduler, Resource Manager) (Fig. 1). |
| **Reconfiguration** | ✓ | Rekonfigurasi rasio PRB dan auto-scaling container saat beban trafik berfluktuasi (Section 3.5, Fig. 6). |
| **Session stability** | ✓ | Menggunakan container Docker untuk auto-scaling yang menjamin sesi aplikasi tidak terinterupsi (Section 3.5, sitasi [46]). |
| **Closed-loop** | ✓ | Loop tertutup diimplementasikan: Slice Scheduler memberikan feedback ke Decision Maker dan Resource Manager terlatih via DRL (Section 3, Fig. 1). |
| **Real testbed** | ✓ | Prototype eksperimental 5G menggunakan USRP B210, laptop Ubuntu, smartphone COTS, dan OAI (Section 4.1). |
| **Open5GS/UERANSIM** | △ | Menggunakan platform sejenis yakni OpenAirInterface (OAI) + FlexRAN, bukan Open5GS/UERANSIM. |

*Keterangan: ✓ = substantif; △ = konseptual/sebagian; ✗ = tidak ada.*

---

## 3. PROBLEM → OBJECTIVE → METHOD → EXPERIMENT → RESULT

### 3.1 Problem [FACT, p.1-2]
- Operator 5G harus melayani permintaan heterogen (eMBB, uRLLC, mMTC) dengan keterbatasan sumber daya eksternal (spektrum frekuensi dan daya pancar) dan infrastruktur (komputasi, memori, storage).
- Solusi statis (*static slicing*) dan acak (*random slicing*) menyebabkan pemborosan Physical Resource Blocks (PRBs) atau pelanggaran SLA karena ketidakmampuan beradaptasi dengan dinamika trafik.
- Banyak penelitian terdahulu hanya fokus pada satu aspek QoS tanpa arsitektur terintegrasi, atau hanya berbasis simulasi matematis tanpa validasi di *testbed* 5G nyata.

### 3.2 Objective [FACT, p.1-2]
1. Merancang framework orkestrasi resource 5G end-to-end yang terdiri dari 4 blok pembangun: klasifikasi permintaan, prediksi rasio slicing, kontrol admisi & penjadwalan, serta manajemen resource adaptif.
2. Memprediksi rasio alokasi PRB optimal menggunakan Regression Trees (RTs).
3. Memodelkan kontrol admisi dan penjadwalan sebagai masalah optimasi Knapsack berdimensi-D (D-MCKP) dan menyelesaikannya dalam waktu polinomial.
4. Mengembangkan adaptive flow control berbasis Deep Reinforcement Learning (DDPG/DQL) untuk auto-scaling container tanpa memutus sesi.
5. Memvalidasi performa di atas prototype 5G nyata berbasis OpenAirInterface (OAI).

### 3.3 Method
- **Gatekeeper:** Klasifikasi demand berdasarkan QCI standar 3GPP menggunakan dot product bobot fitur (Eq. 1).
- **Forecast Aware Slicer:** Model regresi pohon keputusan (Regression Trees) meminimalkan sumbu kuadrat galat ($S^*$, Eq. 3) menggunakan prediktor timestamp, hari, agenda terjadwal, dan kondisi cuaca/awan.
- **Admission Controller:** D-dimensional Multiple Choice Knapsack Problem (D-MCKP, Eq. 4) dengan batasan vCPU dan RAM, diselesaikan dengan algoritma heuristik berbasis sorting efisiensi $v_j / C_i^{(d^*)}$ via Quicksort (Algorithm 2).
- **Slice Scheduler:** Knapsack scheduling problem (Eq. 5) dengan *time window* $\tau = 100$ ms.
- **Adaptive Resource Manager:** Kontrol aliran adaptif analogi *vehicle cruise control* (Eq. 6–8) dengan agen DRL (DDPG Actor-Critic & DQL) untuk optimasi kecepatan aliran $f_{\text{set}}$ dan auto-scaling Docker container tanpa *session interruption*.

### 3.4 Experiment / Evaluation [FACT, p.8-12]
- **Testbed:** 5G NSA prototype (Option 3) dengan functional split CU dan DU sebagai Docker container, FlexRAN SDN controller, USRP B210 (10 MHz / 50 PRB dan 20 MHz / 100 PRB), smartphone COTS, dan TICK Stack (Telegraf, InfluxDB, Chronograf, Kapacitor).
- **Dataset:** Data telemetri aktual selama 24 jam via background script FlexRAN (slicing ratio, priority, QCI, power measurements, PRB usage, BSR).
- **Baseline:** Static Slicing (rasio tetap 50:50) dan Uninformed Random Slicing.
- **KPI:** Akurasi prediksi (FA, RMSE, $R^2$, MAE), kecepatan inferensi (obs/s), Number of Uplink PRBs, Buffer Status Report (BSR) 0..63, System CPU utilization, dan Network throughput.

### 3.5 Result
- **Measured Result:**
  - Simple Regression Tree mencapai akurasi klasifikasi 95.3% dengan kecepatan 9200 obs/s (tertinggi dibanding SVM dan KNN) (Table 3, Table 4).
  - Prediksi rasio slicing RTs hanya berjarak gap 5% dari alokasi teoritis optimal (Fig. 6).
  - Jumlah event BSR tidak nol (indikator buffer menumpuk/tersendat) turun dari **>400 kali** (tanpa decision maker) menjadi **0 kali** pada rasio alokasi tinggi ketika modul diaktifkan (Table 6, Fig. 8b).
  - Penggunaan PRB terdistribusi lebih mulus (*smoothed*) tanpa lonjakan pemborosan (Fig. 8a).
  - Throughput eMBB terjaga konsisten stabil bahkan ketika beban video upload baru ditambahkan pada menit ke-50 (Fig. 9a, 9b).
- **Author's Claim:** Kombinasi RTs untuk prediksi rasio PRB dan DRL untuk manajemen resource adaptif mengungguli solusi statis dan random dalam akurasi, efisiensi spektrum, dan pemanfaatan sistem.
- **Our Interpretation:** Paper ini membuktikan bahwa pendekatan hibrida (prediksi supervised + knapsack heuristic + DRL actuation) sangat efektif di testbed OAI nyata; elastisitas container Docker mencegah putusnya sesi aktif pengguna.

---

## 4. EXISTING SYSTEM
- **Sistem Existing:** Alokasi resource statis (*static slicing*, rasio fixed 50% eMBB / 50% mMTC) atau alokasi acak tanpa informasi (*uninformed random*).
- **Pengelola Resource:** Administrator jaringan secara manual atau rule statis.
- **Resource yang Dikelola:** PRB di RAN dan alokasi VM dasar.
- **Cara Alokasi:** Statis / manual per konfigurasi awal.
- **Kelemahan:** Terjadi *buffer bloat* (>400 event non-zero BSR), pemborosan PRB saat trafik rendah, dan degradasi throughput saat terjadi lonjakan trafik tiba-tiba.

---

## 5. MASALAH DAN TRIGGER
1. **Trigger:** Lonjakan trafik upload video eMBB (misal YouTube video upload) atau peningkatan densitas perangkat IoT.
2. **Kondisi Sistem:** Kapasitas PRB radio (50/100 PRB) dan komputasi (2 vCPU, 1 GB RAM) terbatas dan dibagi bersama antar-slice.
3. **Masalah:** Buffer antrean UE membengkak (BSR index tinggi), paket tertunda, dan potensi pelanggaran batas delay budget QCI (10 ms untuk uRLLC).
4. **Threshold:** Delay budget 10 ms (QCI 65), time window $\tau = 100$ ms, batas variasi aliran $\gamma_{\text{min}} = -1$, $\gamma_{\text{max}} = 1$.
5. **Angka:** Nilai BSR index 0..63; kapasitas PRB 50 (10 MHz) dan 100 (20 MHz).

---

## 6. DAMPAK (KPI)
- **BSR (Buffer Status Report):** Tanpa kontroler terdapat >400 kejadian non-zero BSR $\rightarrow$ Dengan proposed system menjadi 0 kejadian pada rasio tinggi (perbaikan total).
- **PRB Usage:** Alokasi bergeser ke bin PRB rendah yang efisien (1–10 PRB) $\rightarrow$ penggunaan spektrum menjadi halus tanpa lonjakan liar.
- **Throughput:** Throughput normalized eMBB tetap tinggi dan stabil mendekati 0.8–0.9 meskipun beban baru diinjeksi.
- **CPU Utilization:** Meningkat proporsional dari 30% ke ~60–80% saat beban naik, menunjukkan elastisitas autoscaling sistem.

---

## 7. MENGAPA MASALAH BELUM SELESAI?
- **[FACT]:** Kompleksitas komputasional pencarian solusi optimal bersifat NP-hard; prediksi time series konvensional (SARIMA/Holt-Winters) gagal menangkap lonjakan abnormal non-musiman; trade-off antara waktu training ML dan kecepatan inferensi online.
- **[INFERENCE]:** Koordinasi antara radio (PRB) dan komputasi edge pada paper ini masih diselesaikan secara terpisah (RTs untuk PRB, Knapsack/DRL untuk container), belum menjadi satu formulasi matematis *joint optimization* tertutup penuh.

---

## 8. EXISTING RESEARCH (KOMPARASI)
| Research | Problem | Method | Resource | Testbed | KPI | Result | Limitation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Le et al. [7]** | Klasifikasi & slicing SON | ML + SDN/NFV | eMBB slice | Simulasi | Accuracy | Klasifikasi berhasil | Tanpa admission control & scheduling |
| **Xiong et al. [9]** | Dynamic slicing 5G | DRL | Radio | Simulasi numerik | Utility | DRL > Q-learning | Tidak ada implementasi testbed |
| **Zanzi et al. [10]** | Multi-tenant MEC broker | Heuristic broker | MEC CPU/RAM | Simulasi | SLA violation | Menghindari SLA violation | Mengabaikan elastisitas cloud |
| **Zanzi et al. [23] (OVNES)** | Overbooking slicing | ML + admission | Slice capacity | Testbed | Network efficiency | Prediksi trafik baik | Detail modul tidak dijelaskan |
| **Salhab et al. (Paper ini)** | End-to-end orchestration | RTs + Knapsack + DRL | PRB, vCPU, RAM | OAI + Docker + USRP B210 | PRBs, BSR, Throughput, CPU | BSR 0, gap 5% ke optimum | Belum multi-cell handover |

---

## 9. PROPOSED METHOD / ARCHITECTURE
```
INPUT: Permintaan Tenant r_h(l)(t), Profil Trafik Historis, Kondisi Cuaca/Awan
  ↓
GATEKEEPER (MONITOR): Klasifikasi demand ke QCI via dot product utility (Eq. 1)
  ↓
DECISION MAKER:
  - Forecast Aware Slicer: Prediksi rasio PRB via Regression Trees (Algorithm 1)
  - Admission Controller: Seleksi permintaan via D-MCKP Knapsack (Algorithm 2)
  ↓
SLICE SCHEDULER: Penjadwalan permintaan diterima pada time window tau = 100 ms (Eq. 5)
  ↓
RESOURCE MANAGER (ENFORCEMENT):
  - DRL (DDPG/DQL) Adaptive Flow Control (Eq. 6-16)
  - Auto-scaling Docker microservice container (Scale-in / Scale-out)
  ↓
SYSTEM: 5G NSA gNB (CU/DU) OAI + FlexRAN SDN Controller + USRP B210 + TICK Stack
  ↓
OUTPUT: Zero Buffer Backlog (BSR=0), Throughput Stabil, Zero Session Interruption
```

---

## 10. CLOSED-LOOP ANALYSIS
| Tahap | Status | Bukti dari Paper |
| :--- | :---: | :--- |
| **Monitor** | ✓ | TICK Stack (Telegraf, InfluxDB) mengumpulkan telemetri dari FlexRAN secara real-time. |
| **Decide** | ✓ | Forecast Aware Slicer (RTs) memprediksi rasio; Admission Controller menyeleksi via Knapsack. |
| **Allocate** | ✓ | FlexRAN menerapkan PRB ke RAN; Resource Manager men-scale container Docker. |
| **Measure Again** | ✓ | Slice Scheduler mengirimkan umpan balik ke Decision Maker; denied request dilatih ke DRL agent. |

**Klasifikasi:** **Implemented closed loop** (Diuji langsung pada prototype 5G OAI).

---

## 11. EXPERIMENT / EVALUATION
| Item | Isi |
| :--- | :--- |
| **Testbed** | 5G NSA Experimental Prototype (Option 3) |
| **Hardware** | 2 Laptop Ubuntu 16.04 (Quad Core i7, 16 GB RAM), USRP B210 USB3, COTS Smartphone |
| **Software** | OpenAirInterface (OAI), FlexRAN Controller, Docker, TICK Stack (InfluxDB, Telegraf), MATLAB |
| **Network** | RAN FDD Band 7 (2.6 GHz), Bandwidth 10 MHz (50 PRBs) & 20 MHz (100 PRBs), Gigabit Backhaul |
| **Dataset** | 24 jam capture log FlexRAN (JSON format, 23.586 records pengukuran PRB) |
| **Users** | 3 UEs (2 untuk eMBB, 1 sebagai IoT Gateway untuk mMTC) |
| **Traffic** | Video upload YouTube terus-menerus + agregasi sensor IoT |
| **Resource** | 50/100 PRBs, 2 vCPUs, 1 GB RAM |
| **Algorithm** | Simple Regression Tree, D-MCKP Quicksort, DDPG Actor-Critic, DQL |
| **Baseline** | Static Slicing (50:50) dan Uninformed Random Slicing |
| **KPI** | Akurasi (FA %), Kecepatan (obs/s), RMSE, PRB Distribution, BSR Index, Throughput, CPU |
| **Duration** | Pengujian eksperimen streaming selama 2 jam (120 menit) |
| **Scenario** | Video upload normal (0–50 menit) diikuti injeksi video upload baru (50–120 menit) |

---

## 12. RESULT
- **Apa yang dibuktikan:** Regression Trees memprediksi rasio alokasi dengan error terkecil (gap 5% ke optimum) dan eksekusi tercepat (9200 obs/s). Modul scheduler dan DRL berhasil mengeliminasi antrean buffer (BSR nol).
- **Dibandingkan dengan siapa:** Static Slicing, Random Slicing, Linear Regression, SVM, KNN, GPR.
- **KPI & Hasil Konkret:**
  - Non-zero BSR events: **400+ (Baseline) $\rightarrow$ 0 (Proposed)** pada rasio 90–100%.
  - Gap ke optimum: Hanya **5%**.
  - RMSE: Turun 6x lipat dibanding regresi linear.
  - Kecepatan inferensi: 9200 obs/s (Simple Tree).

---

## 13. LIMITATION
### Explicit Limitation (Penulis):
- Validasi dilakukan pada skenario *single-base station* (1 USRP), tidak mengevaluasi mobilitas *handover* antar multi-sel.
- Jumlah perangkat uji dibatasi pada 3 smartphone COTS.
- Training time Regression Trees lebih lama dibanding regresi linear sederhana.

### Inferred Limitation (Analisis Kritis):
- Alokasi radio (PRBs) dan alokasi komputasi (vCPU/RAM) dimodelkan pada modul berbeda tanpa formulasi optimasi *joint* langsung.
- Pengujian belum mengevaluasi protokol 5G Standalone (SA) modern seperti Open5GS Release 16 SBI.

---

## 14. CANDIDATE GAP
### A. Gap yang Dinyatakan Paper:
- Evaluasi mobilitas dan handover pada multi-cell base station (Section 4.1).
- Penambahan metrik Quality of Experience (QoE) end-user secara langsung.

### B. Candidate Gap Hasil Review (Untuk TA Kita):
1. **Validasi pada 5G SA (Open5GS + UERANSIM):** Salhab dkk. menggunakan 4G/5G NSA OAI. TA kita dapat mengimplementasikan arsitektur ini pada 5G Core Standalone murni (Open5GS SBI berbasis HTTP/2).
2. **Joint Mathematical Optimization Radio + Edge:** Menggabungkan alokasi PRB RAN dan MEC container dalam satu formulasi objektif terintegrasi.
3. **Analisis Latensi Transisi Rekonfigurasi:** Mengukur delay sinyalisasi kontrol plane saat realokasi kuota slice dilakukan.

---

## 15. CLAIM TO VERIFY
| No | Claim | Status | Bukti Paper | Yang Belum Terbukti | Perlu Cari Apa? |
| :-: | :--- | :---: | :--- | :--- | :--- |
| 1 | **Dynamic PRB allocation** | [FACT] | Algoritma RTs menyesuaikan rasio PRB tiap interval (Fig. 5, 6). | Kinerja saat pergantian channel mendadak. | Trace kanal real-time. |
| 2 | **Zero session interruption** | [FACT] | Docker elasticity menjaga sesi tetap aktif (Section 3.5, Fig. 9a). | Dampak jitter paket selama proses scale-out. | Analisis packet delay variation. |
| 3 | **Near-optimal slicing** | [FACT] | Gap hanya 5% terhadap estimasi agregasi optimal (Fig. 6). | Apakah gap tetap 5% pada 10+ slice heterogen. | Uji skalabilitas slice. |
| 4 | **Closed-loop control** | [FACT] | Loop telemetri TICK stack $\rightarrow$ RTs $\rightarrow$ DRL $\rightarrow$ FlexRAN terbukti berjalan. | Stabilitas kontrol jika ada packet delay pada NBI. | Latensi loop kontrol O-RAN. |

---

## 16. TA MAPPING MATRIX (15 KOMPONEN TA)
| Komponen TA | Status | Keterangan |
| :--- | :---: | :--- |
| **5G Background** | ✓ | Mengadopsi arsitektur 3GPP NSA Option 3 & SDN RAN. |
| **Network Slicing** | ✓ | Mengisolasi slice eMBB, uRLLC, dan mMTC. |
| **Dynamic Allocation** | ✓ | Prediksi rasio PRB berbasis Regression Trees adaptif terhadap waktu. |
| **Edge Computing** | △ | Diterapkan via arsitektur microservices container pada node komputasi. |
| **Edge Allocation** | ✓ | Optimasi vCPU dan RAM via Knapsack problem. |
| **Network-Edge Coordination** | △ | Koordinasi dilakukan bertahap antara PRB radio dan scaling container. |
| **SLA** | ✓ | Jaminan delay budget 10ms (uRLLC) dan kuota GBR berbasis QCI. |
| **Monitoring** | ✓ | Pengumpulan telemetri real-time menggunakan TICK Stack. |
| **Decision** | ✓ | Dual decision maker: Forecast Aware Slicer + Admission Controller. |
| **Allocation** | ✓ | Penerapan kuota ke RAN melalui FlexRAN NBI/SBI. |
| **Measure Again** | ✓ | Evaluasi feedback loop terus-menerus ke DRL resource manager. |
| **Reconfiguration** | ✓ | Rekonfigurasi rasio slice dinamis tanpa mematikan layanan. |
| **Session Stability** | ✓ | Pemanfaatan container Docker memastikan zero session drops. |
| **Testbed** | ✓ | Implementasi nyata dengan USRP B210 dan laptop Linux. |
| **Open5GS/UERANSIM** | △ | Menggunakan OAI + FlexRAN (menjadi basis analogi kuat untuk Open5GS). |

---

## 17. HUBUNGAN LANGSUNG DENGAN TA
1. **Apa yang bisa diambil:** Desain modular 4-blok (Gatekeeper, Decision Maker, Scheduler, Adaptive Resource Manager), penggunaan Knapsack untuk admisi vCPU/RAM, serta bukti empiris bahwa Regression Trees sangat cepat dan akurat untuk alokasi PRB.
2. **Apa yang TIDAK boleh diklaim:** Jangan mengklaim Salhab dkk. menggunakan Open5GS/UERANSIM (mereka menggunakan OAI), dan jangan mengklaim mereka telah menguji skenario multi-cell mobility/handover.
3. **Bagian TA yang didukung:** Desain *closed-loop dynamic slicing* dan pencegahan gangguan sesi aktif (*session continuity*).
4. **Bagian TA yang belum dijawab:** Orkestrasi pada arsitektur 5G Standalone (Open5GS Rel-16) dan koordinasi joint radio-edge dalam satu fungsi objektif terpadu.
5. **Topik berikutnya yang harus dicari:** Implementasi O-RAN Near-RT RIC (xApps) yang mengintegrasikan Open5GS dengan modul kontroler Python.
6. **Kesimpulan arah:** Paper ini **sangat mendukung arah TA** dan memberikan cetak biru arsitektur teknis yang konkret.

---

## 18. REKOMENDASI PEMBACAAN DALAM KELOMPOK
- **Primary Reader: Person 2 (Network Slicing / Resource Allocation)** & **Person 4 (Open5GS / Testbed / Implementation)**
- **Secondary Reader: Person 3 (MEC / Edge Computing)**
- **Alasan:** Person 2 dan 4 wajib mempelajari Section 3 (Formulasi matematika RTs, Knapsack D-MCKP, DRL) dan Section 4 (Setup OAI, FlexRAN, TICK Stack). Person 3 dapat mempelajari Section 3.3 terkait batasan vCPU dan RAM.

---

## 19. FINAL SUMMARY — SATU PARAGRAF
> Paper karya Salhab et al. (2021) berjudul *"5G network slices resource orchestration using Machine Learning techniques"* memecahkan masalah kelangkaan sumber daya spektrum dan komputasi pada 5G network slicing heterogen melalui framework orkestrasi 4 tahap: klasifikasi permintaan (Gatekeeper), prediksi rasio alokasi PRB berbasis Regression Trees, kontrol admisi dan penjadwalan berbasis Knapsack (D-MCKP), serta manajemen adaptif berbasis DRL. Menggunakan prototype 5G nyata berbasis OpenAirInterface (OAI), Docker, dan USRP B210, paper ini membuktikan bahwa Regression Trees mencapai akurasi 95.3% dengan selisih hanya 5% dari alokasi optimum teoritis, sementara DRL dan autoscaling container berhasil mengeliminasi penumpukan buffer (BSR nol) dan menjaga kelangsungan throughput video tanpa memutus sesi pengguna aktif. Keterbatasan paper ini terletak pada pengujian yang masih berskala single-cell NSA dan pemodelan radio-edge yang belum dioptimasi secara bersamaan (*joint*). Paper ini **HIGHLY RELEVANT** dan menjadi rujukan arsitektural utama bagi Tugas Akhir kami.

---

## 20. FINAL EXCEL ROW
| No | Judul | Tahun | Journal/Conference | Author | Domain | Problem | Objective | Method | Hasil Kunci | Limitation | Relevansi |
| :-: | :--- | :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | 5G network slices resource orchestration using Machine Learning techniques | 2021 | Computer Networks (Elsevier) | Nazih Salhab, Rami Langar, Rana Rahim | 5G Network Slicing & Resource Orchestration | Alokasi resource statis menyebabkan pemborosan PRB dan pelanggaran SLA pada beban heterogen | Merancang framework closed-loop adaptif untuk orkestrasi PRB dan komputasi | Regression Trees + Knapsack D-MCKP + DRL + OAI/Docker Testbed | Gap 5% ke optimum, BSR backlog turun ke 0, throughput stabil tanpa putus sesi | Single base station, belum multi-cell handover, radio & edge belum joint optimization | **HIGHLY RELEVANT** |
