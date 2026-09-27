import os
import torch

class Config:
    # -----------------------------
    # 1. Device Configuration
    # -----------------------------
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    GPU_NAME = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    NUM_WORKERS = 4
    
    # -----------------------------
    # 2. Spacetime Domain (1+1D)
    # -----------------------------
    # Spatial domain: x in [-L, L]
    X_MIN = -5.0
    X_MAX = 5.0
    
    # Temporal domain: t in [0, T]
    T_MIN = 0.0
    T_MAX = 2.0
    
    # Physical Constants
    HBAR = 1.0  # Reduced Planck constant (natural units)
    MASS = 1.0  # Mass of quantum particle
    
    # -----------------------------
    # 3. Collocation Points (Sampling)
    # -----------------------------
    N_DOMAIN = 10000   # Interior points to enforce PDE residual
    N_INITIAL = 1000   # Initial state points (t = 0)
    N_BOUNDARY = 1000  # Boundary points (x = -L, x = L)
    
    # -----------------------------
    # 4. PINN Architecture
    # -----------------------------
    LAYERS = [2, 128, 128, 128, 128, 2]  # Input: (x, t) -> Hidden -> Output: (u, v) [Re(psi), Im(psi)]
    ACTIVATION = "tanh"  # Standard smooth activation for second derivatives
    
    # -----------------------------
    # 5. Training Hyperparameters
    # -----------------------------
    EPOCHS = 3000
    LEARNING_RATE = 1e-3
    WEIGHT_DECAY = 1e-5
    
    # Loss Weights
    W_PDE = 1.0
    W_INIT = 10.0
    W_BOUND = 5.0
    
    # -----------------------------
    # 6. Checkpoint & Logging Policy
    # -----------------------------
    CHECKPOINT_DIR = "checkpoints"
    BEST_MODEL_PATH = os.path.join(CHECKPOINT_DIR, "best_model.pt")
    LAST_MODEL_PATH = os.path.join(CHECKPOINT_DIR, "last_checkpoint.pt")
    METRICS_PATH = os.path.join(CHECKPOINT_DIR, "training_metrics.json")
    
    PRINT_INTERVAL = 100
    USE_WANDB = False  # Set to True if wandb is configured

    @classmethod
    def display(cls):
        print("=" * 60)
        print(" [HK-PCG] Holographic Krylov-PINN Synthesis - Configuration")
        print("=" * 60)
        print(f" Device          : {cls.DEVICE} ({cls.GPU_NAME})")
        if torch.cuda.is_available():
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f" VRAM Available  : {vram_gb:.2f} GB")
        print(f" Spacetime Grid  : x in [{cls.X_MIN}, {cls.X_MAX}], t in [{cls.T_MIN}, {cls.T_MAX}]")
        print(f" Collocation     : Domain={cls.N_DOMAIN}, Init={cls.N_INITIAL}, Bound={cls.N_BOUNDARY}")
        print(f" Architecture    : {cls.LAYERS} ({cls.ACTIVATION})")
        print(f" Epochs / LR     : {cls.EPOCHS} / {cls.LEARNING_RATE}")
        print(f" Checkpoint Dir  : {cls.CHECKPOINT_DIR} (Auto-Overwrite Enabled)")
        print("=" * 60)
