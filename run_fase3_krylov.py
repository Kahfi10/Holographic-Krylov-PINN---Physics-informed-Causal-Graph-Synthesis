import os
import sys
import time
import json
import argparse
import numpy as np
import torch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from src.physics.spin_chain import QuantumSpinChain
from src.physics.krylov_solver import KrylovComplexitySolver

def parse_args():
    parser = argparse.ArgumentParser(description="HK-PCG Phase 3: Krylov Complexity & Emergent Arrow of Time")
    parser.add_argument("--spins", type=int, default=5, help="Number of spins in chain (e.g. 4, 5, 6, 8)")
    parser.add_argument("--max_k", type=int, default=35, help="Maximum Krylov subspace dimension")
    parser.add_argument("--t_max", type=float, default=8.0, help="Simulation time horizon")
    parser.add_argument("--t_points", type=int, default=300, help="Number of time evaluation steps")
    return parser.parse_args()

def run_fase3():
    args = parse_args()
    os.makedirs(Config.CHECKPOINT_DIR, exist_ok=True)
    
    device = Config.DEVICE
    print("=" * 65)
    print(" [HK-PCG Phase 3] Quantum Operator Growth & Krylov Complexity")
    print("=" * 65)
    print(f" Hardware Device : {device} ({Config.GPU_NAME})")
    print(f" Spin Chain Size : {args.spins} Qubits (Hilbert Dim = {2**args.spins})")
    print(f" Krylov Horizon  : Max Dim = {args.max_k}, Time = [0, {args.t_max}] ({args.t_points} steps)")
    print("=" * 65)

    time_grid = np.linspace(0.0, args.t_max, args.t_points)
    results = {}
    
    regimes = [
        ("Integrable (Closed)", {"chaotic": False, "dissipative": False, "gamma": 0.0}),
        ("Quantum Chaotic (Closed)", {"chaotic": True, "dissipative": False, "gamma": 0.0}),
        ("Open Dissipative (Arrow of Time)", {"chaotic": True, "dissipative": True, "gamma": 0.08})
    ]

    total_start = time.time()

    for name, params in regimes:
        print(f"\n---> Simulating Regime: {name}...")
        t0 = time.time()

        chain = QuantumSpinChain(
            num_spins=args.spins,
            J=1.0,
            h_x=-1.05,
            h_z=0.5,
            dissipation_gamma=params["gamma"],
            device=device
        )
        
        solver = KrylovComplexitySolver(chain, max_krylov_dim=args.max_k)
        
        # 1. Build Hamiltonian & Liouvillian
        H = chain.build_hamiltonian(chaotic=params["chaotic"])
        
        # 2. Lanczos Iteration
        a_coeffs, b_coeffs, basis = solver.compute_lanczos_coefficients(
            H, is_dissipative=params["dissipative"]
        )
        
        # 3. Simulate Krylov Operator Dynamics
        K_t, S_t, v_arrow = solver.simulate_krylov_dynamics(a_coeffs, b_coeffs, time_grid)
        
        elapsed = time.time() - t0
        print(f"     [Done in {elapsed:.3f}s] Lanczos Dim: {len(a_coeffs)} | Peak K(t): {np.max(K_t):.3f} | Max Arrow v(t): {np.max(v_arrow):.3f}")

        results[name] = {
            "a_coeffs": a_coeffs.tolist(),
            "b_coeffs": b_coeffs.tolist(),
            "complexity": K_t.tolist(),
            "entropy": S_t.tolist(),
            "arrow_of_time": v_arrow.tolist()
        }

    total_elapsed = time.time() - total_start
    output_json = os.path.join(Config.CHECKPOINT_DIR, "krylov_metrics.json")
    
    payload = {
        "metadata": {
            "spins": args.spins,
            "device": str(device),
            "gpu_name": Config.GPU_NAME,
            "total_time_sec": round(total_elapsed, 3),
            "time_grid": time_grid.tolist()
        },
        "regimes": results
    }

    with open(output_json, "w") as f:
        json.dump(payload, f, indent=2)

    print("\n" + "=" * 65)
    print(f"[SUCCESS] Phase 3 Completed in {total_elapsed:.2f} seconds!")
    print(f"[SUCCESS] Metrics Saved to: {output_json}")
    print("=" * 65)

if __name__ == "__main__":
    run_fase3()
