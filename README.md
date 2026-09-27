# Holographic Krylov-PINN (HK-PCG) Synthesis
> **Deconstructing the Illusion of Time and Quantum Gravity through Physics-Informed AI**

Repository riset komputasi untuk implementasi model **HK-PCG (Fase 1 & Fase 2)** berbasis PyTorch dan akselerasi GPU NVIDIA L40S di [UNISMUH ComputeHub](https://computehub.lab.if.unismuh.ac.id/).

---

## 🚀 Panduan Eksekusi di UNISMUH ComputeHub

### 1. Kloning / Unduh Repositori
Di Terminal UNISMUH ComputeHub:
```bash
git clone <URL_REPO_ANDA>
cd ke8
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
