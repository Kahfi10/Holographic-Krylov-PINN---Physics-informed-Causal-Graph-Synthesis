# Holographic Krylov-PINN (HK-PCG) Synthesis
> **Deconstructing the Illusion of Time and Quantum Gravity through Physics-Informed AI**

Repository riset komputasi untuk implementasi model **HK-PCG (Fase 1 & Fase 2)** berbasis PyTorch dan akselerasi GPU NVIDIA L40S di [UNISMUH ComputeHub](https://computehub.lab.if.unismuh.ac.id/).

---

## 🚀 Panduan Eksekusi di UNISMUH ComputeHub

### 1. Kloning / Unduh Repositori
Di Terminal UNISMUH ComputeHub:
```bash
git clone https://github.com/Kahfi10/Holographic-Krylov-PINN---Physics-informed-Causal-Graph-Synthesis.git
cd Holographic-Krylov-PINN---Physics-informed-Causal-Graph-Synthesis
```

### 2. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Training di Latar Belakang (Pilih Salah Satu)

#### Opsi A: Menggunakan `nohup` (Anti-Putus saat Logout)
```bash
nohup python train_poc.py --epochs 3000 > training.log 2>&1 &
```
* Pantau progres kapan saja:
  ```bash
  tail -f training.log
  ```

#### Opsi B: Menggunakan `tmux`
```bash
tmux new -s training
python train_poc.py --epochs 3000
# Tekan Ctrl+B lalu D untuk detach/keluar
```
* Untuk kembali melihat layar:
  ```bash
  tmux attach -t training
  ```

---

## 📊 File Luaran & Checkpoint (Auto-Overwrite)

Seluruh luaran tersimpan otomatis di direktori `checkpoints/`:
* `checkpoints/best_model.pt` : Bobot model dengan nilai residual fisika terbaik.
* `checkpoints/last_checkpoint.pt` : Checkpoint terakhir untuk pemulihan (*resume*).
* `checkpoints/training_metrics.json` : Riwayat log loss untuk pembuatan grafik publikasi.

### Menghasilkan Grafik Publikasi Standar Scopus (600 DPI)
```bash
python plot_results.py
```
Akan menghasilkan file `figure_convergence.png` siap pakai untuk naskah jurnal internasional.

---

## 🌀 Fase 3: Simulasi Kompleksitas Krylov & Panah Waktu Emergen

Untuk menjalankan simulasi dinamika operator kuantum rantai spin ($L=6$ spin) dan ekstraksi koefisien Lanczos $b_n$:

```bash
# Jalankan simulasi 3 rezim (Integrable, Chaotic, Open Dissipative)
python run_fase3_krylov.py --spins 6

# Hasilkan figur 3-panel 600 DPI (Lanczos, Complexity K(t), Arrow of Time)
python plot_krylov_results.py
```
File metrik akan tersimpan di `checkpoints/krylov_metrics.json` dan gambar di `figure_krylov_dynamics.png`.

---

## 🌐 Fase 4: Integrasi GNN-PINN (Mini HK-PCG)

Untuk menjalankan sintesis ruang-waktu kausal diskrit ke kontinu (800 node causet + regularisasi Klein-Gordon):

```bash
# Jalankan pelatihan integrasi GNN-PINN Mini HK-PCG
python train_fase4_hk_pcg.py --nodes 800 --epochs 2500

# Hasilkan figur 3-panel 600 DPI (Causal Set, Continuous Field, Equilibrium Convergence)
python plot_fase4_results.py
```
File metrik akan tersimpan di `checkpoints/fase4_metrics.json`, bobot model di `checkpoints/hk_pcg_best.pt`, dan gambar di `figure_fase4_hk_pcg.png`.


