import os
import sys
import time
import json
import argparse
import torch
import torch.nn as nn

# Ensure local imports work regardless of execution directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from src.models.pinn_model import ComplexPINN1D
from src.physics.quantum_system import QuantumPhysicsEngine

def parse_args():
    parser = argparse.ArgumentParser(description="HK-PCG Phase 2: Quantum PINN 1+1D Solver")
    parser.add_argument("--epochs", type=int, default=Config.EPOCHS, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=Config.LEARNING_RATE, help="Learning rate")
    parser.add_argument("--resume", type=str, default="", help="Path to checkpoint to resume training")
    return parser.parse_args()

def train():
    args = parse_args()
    Config.display()
    
    # 1. Ensure checkpoint directory exists
    os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)
    
    # 2. Instantiate Model & Physics Engine
    model = ComplexPINN1D(Config.LAYERS, Config.ACTIVATION).to(Config.DEVICE)
    physics = QuantumPhysicsEngine(Config)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=Config.WEIGHT_DECAY)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-5)
    mse_criterion = nn.MSELoss()
    
    start_epoch = 0
    best_loss = float("inf")
    metrics_history = []
    
    # 3. Resume from Checkpoint if requested
    if args.resume and os.path.exists(args.resume):
        print(f"\n[INFO] Loading checkpoint from {args.resume}...")
        checkpoint = torch.load(args.resume, map_location=Config.DEVICE)
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        start_epoch = checkpoint["epoch"] + 1
        best_loss = checkpoint.get("loss", float("inf"))
        print(f"[INFO] Resumed at epoch {start_epoch} (Previous Best Loss: {best_loss:.6e})")
        
    print(f"\n[START] Beginning training for {args.epochs} epochs on {Config.DEVICE}...\n")
    start_time = time.time()
    
    try:
        for epoch in range(start_epoch, args.epochs):
            model.train()
            optimizer.zero_grad()
            
            # --- Sample Spacetime Collocation Points ---
            x_f, t_f = physics.sample_domain_points(Config.N_DOMAIN)
            x_0, t_0, u_0_true, v_0_true = physics.sample_initial_points(Config.N_INITIAL)
            x_b, t_b, u_b_true, v_b_true = physics.sample_boundary_points(Config.N_BOUNDARY)
            
            # --- Loss 1: Interior PDE Physics Residual ---
            loss_pde = physics.compute_pde_residual(model, x_f, t_f)
            
            # --- Loss 2: Initial Condition (t = 0) ---
            u_0_pred, v_0_pred = model(x_0, t_0)
            loss_init = mse_criterion(u_0_pred, u_0_true) + mse_criterion(v_0_pred, v_0_true)
            
            # --- Loss 3: Boundary Condition (x = -L, +L) ---
            u_b_pred, v_b_pred = model(x_b, t_b)
            loss_bound = mse_criterion(u_b_pred, u_b_true) + mse_criterion(v_b_pred, v_b_true)
            
            # --- Total Physics-Informed Objective ---
            total_loss = (Config.W_PDE * loss_pde + 
                          Config.W_INIT * loss_init + 
                          Config.W_BOUND * loss_bound)
            
            total_loss.backward()
            optimizer.step()
            scheduler.step()
            
            current_loss = total_loss.item()
            
            # --- Periodic Checkpointing (Auto-Overwrite Policy) ---
            is_best = current_loss < best_loss
            if is_best:
                best_loss = current_loss
                torch.save({
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": best_loss,
                    "pde_loss": loss_pde.item(),
                    "init_loss": loss_init.item()
                }, Config.BEST_MODEL_PATH)
                
            if (epoch + 1) % Config.PRINT_INTERVAL == 0 or epoch == args.epochs - 1:
                # Save last checkpoint
                torch.save({
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": current_loss
                }, Config.LAST_MODEL_PATH)
                
                elapsed = time.time() - start_time
                lr_curr = optimizer.param_groups[0]["lr"]
                status_star = "*" if is_best else " "
                print(f"[{status_star}] Epoch {epoch+1:5d}/{args.epochs} | "
                      f"Loss: {current_loss:.6e} | "
                      f"PDE: {loss_pde.item():.6e} | "
                      f"Init: {loss_init.item():.6e} | "
                      f"Bound: {loss_bound.item():.6e} | "
                      f"LR: {lr_curr:.2e} | "
                      f"Elapsed: {elapsed:.1f}s")
                
                metrics_history.append({
                    "epoch": epoch + 1,
                    "total_loss": current_loss,
                    "pde_loss": loss_pde.item(),
                    "init_loss": loss_init.item(),
                    "bound_loss": loss_bound.item(),
                    "lr": lr_curr,
                    "elapsed_sec": round(elapsed, 2)
                })

        total_runtime = time.time() - start_time
        print("\n" + "=" * 60)
        print(f"[SUCCESS] Training completed in {total_runtime:.2f} seconds ({total_runtime/60:.2f} minutes).")
        print(f"[SUCCESS] Optimal Physics Loss achieved : {best_loss:.6e}")
        print(f"[SUCCESS] Best Model Saved to           : {Config.BEST_MODEL_PATH}")
        print("=" * 60)
        
        # Save metrics JSON for plotting and Scopus manuscript tables
        with open(Config.METRICS_PATH, "w") as f:
            json.dump({
                "gpu": Config.GPU_NAME,
                "epochs": args.epochs,
                "best_loss": best_loss,
                "total_time_seconds": total_runtime,
                "history": metrics_history
            }, f, indent=2)
            
    except KeyboardInterrupt:
        print("\n[WARNING] Training interrupted by user. Saving emergency checkpoint...")
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": current_loss
        }, Config.LAST_MODEL_PATH)
        print(f"[INFO] Emergency state saved to {Config.LAST_MODEL_PATH}")

if __name__ == "__main__":
    train()
