import os
import sys
import time
import json
import argparse
import numpy as np
import torch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from src.models.causal_gnn import CausalSetGenerator, CausalGraphPINN
from src.physics.causal_pinn_loss import CausalFieldLossEngine

def parse_args():
    parser = argparse.ArgumentParser(description="HK-PCG Phase 4: GNN-PINN Causal Spacetime Synthesis")
    parser.add_argument("--nodes", type=int, default=800, help="Number of causal set nodes (e.g. 500-1000)")
    parser.add_argument("--epochs", type=int, default=2500, help="Training epochs")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    return parser.parse_args()

def train_fase4():
    args = parse_args()
    device = Config.DEVICE
    os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)
    
    print("=" * 65)
    print(" [HK-PCG Phase 4] Mini HK-PCG: GNN-PINN Causal Spacetime Synthesis")
    print("=" * 65)
    print(f" Hardware Device : {device} ({Config.GPU_NAME})")
    print(f" Causal Topology : {args.nodes} Spacetime Events (Poisson Sprinkled)")
    print(f" Optimization    : {args.epochs} Epochs | LR = {args.lr}")
    print("=" * 65)
    
    # 1. Load Krylov Arrow of Time from Phase 3
    krylov_json = os.path.join(Config.CHECKPOINT_DIR, "krylov_metrics.json")
    t_grid = None
    v_arrow = None
    if os.path.exists(krylov_json):
        print(f"[INFO] Ingesting Phase 3 Krylov Arrow of Time from {krylov_json}...")
        with open(krylov_json, "r") as f:
            kdata = json.load(f)
        t_grid = np.array(kdata["metadata"]["time_grid"])
        # Use Open Dissipative arrow vector
        v_arrow = np.array(kdata["regimes"]["Open Dissipative (Arrow of Time)"]["arrow_of_time"])
        print(f"[INFO] Arrow vector ingested (Peak Arrow Velocity: {np.max(v_arrow):.3f})")
    else:
        print("[WARNING] Krylov metrics not found. Using default causal arrow.")

    # 2. Generate Discrete Causal Set (Causet)
    generator = CausalSetGenerator(num_nodes=args.nodes, x_range=(-4.0, 4.0), t_range=(0.0, 4.0), device=device)
    node_feats, edge_index, edge_weight, raw_coords = generator.generate_causet(t_grid, v_arrow)
    num_edges = edge_index.size(1)
    print(f"[INFO] Causal Set Constructed: {args.nodes} nodes, {num_edges} directed causal links.")

    # 3. Instantiate GNN-PINN & Loss Engine
    model = CausalGraphPINN(in_features=3, hidden_dim=64, out_dim=1).to(device)
    loss_engine = CausalFieldLossEngine(scalar_mass=1.0, device=device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-5)

    # 4. Collocation Points Sampling
    n_domain = 4000
    n_init = 500
    n_bound = 500
    
    # Sample collocation points
    x_d = torch.empty(n_domain, 1, device=device).uniform_(-4.0, 4.0).requires_grad_(True)
    t_d = torch.empty(n_domain, 1, device=device).uniform_(0.0, 4.0).requires_grad_(True)
    
    x_0 = torch.empty(n_init, 1, device=device).uniform_(-4.0, 4.0)
    t_0 = torch.zeros(n_init, 1, device=device)
    phi_0_true = torch.exp(- (x_0 ** 2) / 2.0)  # Initial Gaussian pulse
    
    half_b = n_bound // 2
    x_b = torch.cat([torch.full((half_b, 1), -4.0, device=device),
                     torch.full((n_bound - half_b, 1), 4.0, device=device)], dim=0)
    t_b = torch.empty(n_bound, 1, device=device).uniform_(0.0, 4.0)
    
    best_loss = float("inf")
    metrics_history = []
    start_time = time.time()
    
    print("\n[START] Executing GNN-PINN Spacetime Metric Smoothing...\n")
    
    for epoch in range(args.epochs):
        model.train()
        optimizer.zero_grad()
        
        total_loss, loss_pde, loss_init, loss_bound, loss_arrow = loss_engine.compute_equilibrium_loss(
            model, node_feats, edge_index, edge_weight,
            (x_d, t_d), (x_0, t_0, phi_0_true), (x_b, t_b),
            krylov_arrow_t0=torch.mean(node_feats[:, 2])
        )
        
        total_loss.backward()
        optimizer.step()
        scheduler.step()
        
        cur_loss = total_loss.item()
        is_best = cur_loss < best_loss
        if is_best:
            best_loss = cur_loss
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "node_coords": raw_coords.tolist(),
                "edge_index": edge_index.cpu().numpy().tolist(),
                "loss": best_loss,
                "pde_loss": loss_pde.item()
            }, os.path.join(Config.CHECKPOINT_DIR, "hk_pcg_best.pt"))
            
        if (epoch + 1) % 100 == 0 or epoch == args.epochs - 1:
            elapsed = time.time() - start_time
            star = "*" if is_best else " "
            print(f"[{star}] Epoch {epoch+1:4d}/{args.epochs} | "
                  f"Total Loss: {cur_loss:.6e} | "
                  f"PDE (Box phi): {loss_pde.item():.6e} | "
                  f"Init: {loss_init.item():.6e} | "
                  f"Arrow: {loss_arrow.item():.6e} | "
                  f"Elapsed: {elapsed:.1f}s")
                  
            metrics_history.append({
                "epoch": epoch + 1,
                "total_loss": cur_loss,
                "pde_loss": loss_pde.item(),
                "init_loss": loss_init.item(),
                "bound_loss": loss_bound.item(),
                "arrow_loss": loss_arrow.item(),
                "elapsed_sec": round(elapsed, 2)
            })

    total_time = time.time() - start_time
    output_json = os.path.join(Config.CHECKPOINT_DIR, "fase4_metrics.json")
    
    with open(output_json, "w") as f:
        json.dump({
            "nodes": args.nodes,
            "edges": num_edges,
            "gpu": Config.GPU_NAME,
            "total_time_seconds": total_time,
            "best_loss": best_loss,
            "history": metrics_history,
            "node_coords": raw_coords.tolist()
        }, f, indent=2)

    print("\n" + "=" * 65)
    print(f"[SUCCESS] Phase 4 (Mini HK-PCG) Completed in {total_time:.2f} seconds ({total_time/60:.2f} min)!")
    print(f"[SUCCESS] Spacetime Equilibrium Loss: {best_loss:.6e}")
    print(f"[SUCCESS] Checkpoint: checkpoints/hk_pcg_best.pt")
    print(f"[SUCCESS] Metrics   : {output_json}")
    print("=" * 65)

if __name__ == "__main__":
    train_fase4()
