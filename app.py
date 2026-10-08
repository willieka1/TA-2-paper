from flask import Flask, jsonify, render_template, request, Response
import os

# Initialize Flask app, supporting both templates/ directory and current directory
app = Flask(__name__, template_folder="templates")

F, P, N = "full", "part", "none"

DATA = {
    "papers": [
        {
            "id": "A",
            "short": "Apruzzese et al. (2023)",
            "title": "5G and Companion Technologies as a Boost in New Business Models for Logistics and Supply Chain",
            "venue": "Sustainability 15(15):11846, 2023",
            "type": "Survei kuesioner daring + analisis klaster (n=44 responden)",
            "verdict": "NOT RELEVANT (Secara Teknis Algoritmik)",
            "kpi": "Persentase adopsi teknologi & persepsi stakeholder (%)",
            "takeaway": "Konteks use-case logistik pelabuhan (Living Lab Athena, Hamburg, Koper di 5G-LOGINNOV) & gerbang referensi primer. Tidak memuat mekanisme alokasi dinamis, network slicing aktif, SLA teknis, MEC edge compute, maupun kontrol closed-loop.",
            "method": "Metodologi lean GUEST, survei kuesioner 44 responden dari ekosistem pelabuhan, k-means clustering menjadi 3 kelompok aktor.",
            "limitations": "Sampel kecil (n=44), tidak ada formulasi matematis, tidak ada arsitektur teknis atau evaluasi kinerja jaringan/edge, data sharing antar tenant dinilai rendah (85.7% data terisolasi).",
            "color": "#f43f5e",
        },
        {
            "id": "B",
            "short": "Zhang et al. (2017)",
            "title": "Network Slicing Based 5G and Future Mobile Networks: Mobility, Resource Management, and Challenges",
            "venue": "IEEE Communications Magazine, Agustus 2017",
            "type": "Arsitektur logis + formulasi alokasi radio 2-tier (dievaluasi via simulasi komputer)",
            "verdict": "POTENTIALLY RELEVANT",
            "kpi": "Kapasitas uplink per slice (b/s/Hz) & ketahanan terhadap interferensi small cell",
            "takeaway": "Kerangka arsitektur MANO/VIM/VNFM/SDN dan formulasi alokasi daya transmit serta 50 subchannel antar slice eMBB/uRLLC/IoT. Namun evaluasi statis (tanpa sumbu waktu), tidak ada SLA formal, edge compute tidak dimodelkan, open-loop tanpa feedback, dan stabilitas sesi saat realokasi tidak diukur.",
            "method": "Arsitektur NFV/SDN 2-tier; optimasi alokasi subchannel & daya diselesaikan dengan relaksasi kontinu variabel biner + Lagrangian Dual Decomposition + KKT + Subgradient.",
            "limitations": "Simulasi statis snapshot tanpa fluktuasi waktu, hanya alokasi spektrum radio (compute/storage MEC diabaikan), open-loop (tanpa feedback monitoring), tanpa jaminan SLA per slice selain uRLLC, gangguan sesi aktif saat rekonfigurasi tidak diukur.",
            "color": "#38bdf8",
        },
        {
            "id": "TA",
            "short": "Proposed TA Innovation",
            "title": "Closed-Loop SLA-Aware Dynamic Network Slicing & Edge Orchestration with Minimal Session Disruption",
            "venue": "Topik Tugas Akhir (Open5GS + UERANSIM + Edge MEC)",
            "type": "Closed-Loop O-RAN/MANO Controller + Testbed Nyata",
            "verdict": "PROPOSED SOLUTION (TA TARGET)",
            "kpi": "Zero Session Drops (0%), Latency uRLLC < 5ms, Throughput SLA Guarantee, Edge CPU Efficiency",
            "takeaway": "Menjembatani keterbatasan Zhang (2017) dan kebutuhan pelabuhan Apruzzese (2023) melalui kontrol Closed-Loop otomatis (Monitor-Decide-Allocate-Measure) yang mengoordinasikan Radio PRB + Edge vCPU secara adaptif terhadap waktu tanpa memutuskan koneksi aktif pengguna.",
            "method": "Real-time Telemetry Collector + SLA-Aware Decision Engine + Graceful Soft-Reconfiguration (buffer & packet queuing) + Testbed Open5GS & UERANSIM.",
            "limitations": "Fokus TA: memvalidasi performa transisi rekonfigurasi dinamis dan isolasi SLA multi-tenant pada infrastruktur virtual 5G.",
            "color": "#10b981",
        }
    ],
    "matrix": [
        ["Arsitektur 5G End-to-End", P, F, "Konteks persepsi stakeholder pelabuhan terhadap 5G (Fig 5)", "Arsitektur lengkap Core, Edge, RAN, MANO, NFV/SDN (Fig 1-2)"],
        ["Network Slicing (eMBB/uRLLC/mMTC)", P, F, "Hanya definisi konseptual satu kalimat (p.2)", "Model slice eMBB, uRLLC, IoT dengan isolasi subchannel (Fig 1, p.140)"],
        ["Dynamic Allocation (Sumbu Waktu)", N, P, "Tidak dibahas sama sekali", "Hanya simulasi statis snapshot variasi jumlah small cell (10-40), tanpa dinamika waktu (Fig 4-6)"],
        ["Edge Computing / MEC", N, P, "Hanya disebut sekilas sebagai teknologi komplementer", "MEC dan Edge Cloud digambarkan pada arsitektur (Fig 1, p.139-140)"],
        ["Alokasi Resource Edge (vCPU/RAM)", N, N, "Tidak dibahas", "Komputasi dan storage disebut di Fig 2, tetapi formulasi optimasi HANYA alokasi daya radio dan subchannel"],
        ["Koordinasi Joint Radio + Edge", N, P, "Tidak ada", "SDN memetakan VM ke edge cloud secara konseptual, tanpa formulasi matematis bersama"],
        ["SLA Formal per Slice", N, P, "Tidak dibahas", "Hanya constraint minimum rate uRLLC dan ambang interferensi; IoT terdegradasi tanpa proteksi SLA"],
        ["Monitoring Telemetri Real-Time", P, P, "Tujuan survei ('continuous monitoring') tanpa metrik teknis", "VIM memantau utilisasi resource & UE kirim measurement report, tanpa spesifikasi metrik/periode"],
        ["Decision Engine Adaptif", N, P, "Tidak ada", "MANO/SDN controller konseptual + solver Lagrangian statis"],
        ["Orchestration & Enforcement", N, P, "Tidak ada", "VNFM/VIM memetakan fungsi ke VM (konseptual, tanpa detail protokol antarmuka)"],
        ["Rekonfigurasi Transisi Slice", N, P, "Tidak ada", "Siklus hidup slice (create/activate/deactivate) secara konseptual tanpa analisis transisi"],
        ["Session Stability / Zero Drop", N, P, "Tidak ada", "Handover UE konseptual (buffering & end-marker, Fig 3); gangguan sesi saat alokasi TIDAK diukur"],
        ["Closed-Loop Control (Feedback)", N, N, "Tidak ada (alur linier survei bisnis)", "Open-Loop: solver menghitung alokasi tanpa loop umpan balik terotomatisasi"],
        ["Validasi Testbed Nyata", P, N, "Survei di 3 living lab pelabuhan, tanpa data uji teknis", "Hanya simulasi numerik komputer (tool simulator tidak dijelaskan)"],
        ["Implementasi Open5GS / UERANSIM", N, N, "Tidak disebut", "Tidak disebut (karena terbit 2017)"]
    ],
    "loop": [
        {
            "step": "1. Monitor",
            "name": "Pemantauan Telemetri",
            "desc": "Ukur beban traffic real-time, PRB radio utilization, antrean paket, serta penggunaan vCPU/RAM pada MEC node.",
            "A": "Hanya tujuan survei stakeholder pelabuhan ('continuous tracking'). Tidak ada sensor atau arsitektur monitoring teknis.",
            "B": "VIM memantau utilisasi resource; UE mengirimkan measurement report sinyal. Namun tanpa periode sampling, metrik latensi, atau antarmuka spesifik.",
            "TA": "Collector telemetri real-time terintegrasi Open5GS (UPF/gNB metrics) dan Node Exporter MEC untuk memantau throughput, latency, dan buffer queue."
        },
        {
            "step": "2. Decide",
            "name": "Pengambilan Keputusan SLA",
            "desc": "Kalkulasi alokasi kapasitas radio dan komputasi edge menggunakan kebijakan SLA-aware dan prioritas slice.",
            "A": "Tidak ada decision engine teknis. Hanya analisis klaster preferensi bisnis.",
            "B": "Solver Lagrangian dual decomposition menghitung daya transmit dan subchannel untuk small cell. Bekerja secara statis per snapshot.",
            "TA": "SLA-Aware Orchestration Engine yang menghitung kebutuhan joint radio PRB + edge vCPU secara dinamis, mengutamakan uRLLC dan mencegah starvation slice IoT."
        },
        {
            "step": "3. Allocate",
            "name": "Enforcement & Rekonfigurasi",
            "desc": "Menerapkan pembaruan jatah ke RAN dan edge container secara mulus (graceful) tanpa merusak sesi pengguna aktif.",
            "A": "Tidak ada mekanisme enforcement.",
            "B": "VNFM/VIM memetakan virtual function ke VM. Mekanisme penerapan fisik daya dan subchannel tidak dijelaskan secara konkret.",
            "TA": "Graceful Reconfiguration: migrasi kuota traffic dengan buffering aktif, zero connection reset, dan auto-scaling microservices MEC di edge."
        },
        {
            "step": "4. Measure Again",
            "name": "Verifikasi Umpan Balik (Closed-Loop)",
            "desc": "Cek apakah KPI latensi dan throughput sudah kembali memenuhi SLA; ulangi penyesuaian bila ada deviasi.",
            "A": "Hanya usulan kuesioner berkala, bukan kontrol otomatis.",
            "B": "Tidak ada umpan balik tertutup (Open Loop). Jika traffic berubah, sistem tidak memiliki mekanisme koreksi mandiri.",
            "TA": "Closed-Loop feedback berkesinambungan: mendeteksi lonjakan berikutnya secara adaptif, menjaga stabilitas sesi secara otomatis."
        }
    ],
    "gaps": [
        {
            "id": 1,
            "title": "Alokasi Dinamis Saat Trafik Berfluktuasi Terhadap Waktu",
            "paper_proof": "Fig 4-6 pada Zhang et al. (2017) hanya menyapu (sweep) variasi jumlah small cell (10-40) dalam kondisi statis, tanpa kurva dinamika waktu.",
            "ta_solution": "TA memodelkan traffic time-series dengan pola fluktuatif (bursty eMBB & sporadic IoT) dan mengevaluasi adaptasi alokasi dari detik ke detik.",
            "tag": "Dynamic Time-Series"
        },
        {
            "id": 2,
            "title": "Jaminan SLA Multi-Slice dan Perlindungan Slice Rendah",
            "paper_proof": "Zhang et al. hanya membatasi rate minimum uRLLC; akibatnya kapasitas IoT turun tajam (dari 134 ke 76 b/s/Hz) tanpa adanya ambang SLA minimum.",
            "ta_solution": "TA menerapkan multi-tier SLA constraint yang menjamin batas minimum untuk semua slice aktif dan mengisolasi interferensi antar tenant.",
            "tag": "SLA-Guaranteed"
        },
        {
            "id": 3,
            "title": "Alokasi Bersama (Joint) Radio RAN + Resource Edge Compute",
            "paper_proof": "Gambar 2 Zhang et al. menyebut compute/storage di edge cloud, namun formulasi matematisnya hanya mengalokasikan RF transmit power dan subchannel.",
            "ta_solution": "TA mengintegrasikan alokasi 5G PRB dengan alokasi vCPU/RAM container MEC di edge, mengatasi bottleneck pemrosesan komputasi.",
            "tag": "Joint Radio & Edge"
        },
        {
            "id": 4,
            "title": "Mekanisme Enforcement & Protokol Antarmuka Konkret",
            "paper_proof": "Peran MANO/VIM/SDN pada paper Zhang dkk. bersifat deskriptif tanpa spesifikasi protokol kontrol (misal O-RAN E2, Nnssf, atau Kubernetes CNI).",
            "ta_solution": "TA mengimplementasikan controller konkret yang mengirim perintah rekonfigurasi langsung ke 5G Core dan orchestrator edge container.",
            "tag": "Concrete Enforcement"
        },
        {
            "id": 5,
            "title": "Stabilitas & Kontinuitas Sesi Pengguna Saat Rekonfigurasi",
            "paper_proof": "Zhang et al. hanya mengulas mobilitas handover UE (Fig 3), tanpa mengukur apakah realokasi slice menyebabkan pemutusan TCP/UDP atau lonjakan packet drop.",
            "ta_solution": "TA membandingkan Hard Restart vs Graceful Reconfiguration untuk membuktikan eliminasi session drops dan minimasi jitter paket.",
            "tag": "Session Continuity"
        },
        {
            "id": 6,
            "title": "Siklus Kontrol Tertutup (Closed-Loop Automation)",
            "paper_proof": "Apruzzese et al. adalah studi survei tanpa kontrol; Zhang et al. adalah optimasi statis satu arah (Open Loop).",
            "ta_solution": "TA membangun arsitektur loop otonom Monitor ➔ Decide ➔ Allocate ➔ Measure again untuk adaptasi mandiri tanpa intervensi manual.",
            "tag": "Closed-Loop O-RAN"
        },
        {
            "id": 7,
            "title": "Validasi Menggunakan Testbed 5G Nyata",
            "paper_proof": "Paper Apruzzese menggunakan kuesioner kualitatif; Paper Zhang hanya menggunakan simulasi numerik tanpa validasi protokol.",
            "ta_solution": "TA memvalidasi solusi di atas platform open-source industri Open5GS dan UERANSIM dengan simulasi paket data jaringan aktual.",
            "tag": "Open5GS & UERANSIM"
        }
    ],
    "primary_references": [
        {"name": "5G-MoNArch", "focus": "Mobile Network Architecture for 5G, konsep network slicing pada smart port (Hamburg port testbed)."},
        {"name": "5G-EVE", "focus": "European 5G end-to-end validation platform, multi-site slicing dan MEC facility."},
        {"name": "VITAL-5G", "focus": "Vertical Innovations in Transport and Logistics over 5G testbeds and NetApps."},
        {"name": "Open5GS & UERANSIM", "focus": "Platform 3GPP Release 16 5G Core and gNodeB/UE simulator untuk validasi eksperimental."}
    ]
}


base_dir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(base_dir, "templates")

def get_index_html():
    # Try templates/index.html first, then root index.html
    for p in [os.path.join(templates_dir, "index.html"), os.path.join(base_dir, "index.html")]:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>5G Slicing Simulator</h1>"

@app.route("/")
@app.route("/index.html")
@app.route("/index")
@app.route("/app.py")
@app.route("/app")
def index():
    return Response(get_index_html(), mimetype="text/html")

@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Endpoint not found"}), 404
    return Response(get_index_html(), mimetype="text/html")

@app.route("/api/data")
def data():
    return jsonify(DATA)



@app.route("/api/simulate", methods=["POST"])
def simulate():
    req = request.get_json() or {}
    demand_a = float(req.get("demand_a", 35))  # eMBB
    demand_b = float(req.get("demand_b", 25))  # uRLLC
    demand_c = float(req.get("demand_c", 20))  # mMTC
    mode = req.get("mode", "graceful")         # "hard" or "graceful"
    interference = float(req.get("interference", 0.3)) # 0..1 scale
    
    total_demand = demand_a + demand_b + demand_c
    total_radio_capacity = 100.0
    total_edge_capacity = 100.0
    
    # SLA thresholds
    sla_b_min = 25.0 # uRLLC requires strict min
    sla_c_min = 20.0 # mMTC minimum telemetry
    
    # Calculation of allocated radio
    if mode == "graceful":
        # SLA-aware prioritized allocation
        alloc_b = max(sla_b_min, demand_b)
        rem_radio = max(0.0, total_radio_capacity - alloc_b)
        
        # Next allocate eMBB up to demand, protecting mMTC base
        alloc_c = min(demand_c, sla_c_min + (rem_radio * 0.2))
        alloc_a = min(demand_a, total_radio_capacity - alloc_b - alloc_c)
        
        # Disruption & performance
        session_drops = 0.0
        packet_loss = round(max(0.05, (total_demand - 100.0) * 0.15 + (interference * 1.5)) if total_demand > 100 else interference * 0.5, 2)
        latency_urllc = round(2.5 + (alloc_b / 50.0) * 1.2 + (interference * 0.8), 1)
        latency_embb = round(12.0 + (demand_a / alloc_a if alloc_a > 0 else 5.0) * 4.0, 1)
        sla_compliance = 100.0 if (alloc_b >= sla_b_min and (alloc_c >= sla_c_min or demand_c < sla_c_min)) else 85.0
    else:
        # Hard restart / Open-loop (Zhang 2017 baseline behavior)
        # Slices suffer service disconnection during reconfiguration
        alloc_a = min(demand_a, 55.0)
        alloc_b = sla_b_min
        alloc_c = max(10.0, 100.0 - alloc_a - alloc_b)
        
        session_drops = round(18.5 + (total_demand * 0.12), 1)
        packet_loss = round(8.5 + (interference * 5.0), 2)
        latency_urllc = round(18.0 + (interference * 8.0), 1)  # spikes during reset
        latency_embb = round(45.0 + (interference * 12.0), 1)
        sla_compliance = 62.0
    
    # Edge compute allocation (vCPU/RAM)
    edge_a = round(min(alloc_a * 1.1, total_edge_capacity * 0.6), 1)
    edge_b = round(min(alloc_b * 0.8, total_edge_capacity * 0.3), 1)
    edge_c = round(max(5.0, total_edge_capacity - edge_a - edge_b), 1)
    
    return jsonify({
        "status": "success",
        "radio": {
            "a": round(alloc_a, 1),
            "b": round(alloc_b, 1),
            "c": round(alloc_c, 1),
            "remaining": round(max(0.0, total_radio_capacity - (alloc_a + alloc_b + alloc_c)), 1)
        },
        "edge": {
            "a": edge_a,
            "b": edge_b,
            "c": edge_c,
            "remaining": round(max(0.0, total_edge_capacity - (edge_a + edge_b + edge_c)), 1)
        },
        "kpi": {
            "session_drops_pct": session_drops,
            "packet_loss_pct": packet_loss,
            "latency_urllc_ms": latency_urllc,
            "latency_embb_ms": latency_embb,
            "sla_compliance_pct": sla_compliance
        }
    })


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "5G-Slicing-Edge-Simulator"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
