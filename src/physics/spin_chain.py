import torch
import numpy as np

class QuantumSpinChain:
    """
    1D Transverse-Field Ising Model (TFIM) with Longitudinal Field & Open Dissipation.
    H = - J * sum(Z_i Z_{i+1}) - h_x * sum(X_i) - h_z * sum(Z_i)
    """
    def __init__(self, num_spins=4, J=1.0, h_x=-1.05, h_z=0.5, dissipation_gamma=0.05, device="cpu"):
        self.num_spins = num_spins
        self.dim = 2 ** num_spins
        self.J = J
        self.h_x = h_x
        self.h_z = h_z
        self.gamma = dissipation_gamma
        self.device = device
        
        # Fundamental Pauli Matrices
        self.I2 = torch.eye(2, dtype=torch.complex128, device=device)
        self.sx = torch.tensor([[0.0, 1.0], [1.0, 0.0]], dtype=torch.complex128, device=device)
        self.sy = torch.tensor([[0.0, -1.0j], [1.0j, 0.0]], dtype=torch.complex128, device=device)
        self.sz = torch.tensor([[1.0, 0.0], [0.0, -1.0]], dtype=torch.complex128, device=device)
        self.sm = torch.tensor([[0.0, 0.0], [1.0, 0.0]], dtype=torch.complex128, device=device)  # sigma minus (lowering)

    def _embed_operator(self, op, site):
        """Embeds single-site operator at given site into 2^L dimensional Hilbert space."""
        res = torch.tensor([[1.0]], dtype=torch.complex128, device=self.device)
        for i in range(self.num_spins):
            if i == site:
                res = torch.kron(res, op)
            else:
                res = torch.kron(res, self.I2)
        return res

    def build_hamiltonian(self, chaotic=True):
        """Constructs the N-spin Hamiltonian."""
        h_z_eff = self.h_z if chaotic else 0.0  # h_z=0 -> Integrable, h_z>0 -> Chaotic
        H = torch.zeros((self.dim, self.dim), dtype=torch.complex128, device=self.device)
        
        # Nearest-neighbor interaction: -J * Z_i * Z_{i+1}
        for i in range(self.num_spins - 1):
            Z_i = self._embed_operator(self.sz, i)
            Z_ip1 = self._embed_operator(self.sz, i + 1)
            H = H - self.J * torch.matmul(Z_i, Z_ip1)
            
        # Transverse magnetic field: -h_x * X_i
        for i in range(self.num_spins):
            X_i = self._embed_operator(self.sx, i)
            H = H - self.h_x * X_i
            
        # Longitudinal magnetic field: -h_z * Z_i
        if abs(h_z_eff) > 1e-9:
            for i in range(self.num_spins):
                Z_i = self._embed_operator(self.sz, i)
                H = H - h_z_eff * Z_i
                
        return H

    def build_local_probe_operator(self, site=0):
        """Returns initial probe operator O_0 = Z_0 normalized under Frobenius norm."""
        O0 = self._embed_operator(self.sz, site)
        norm = torch.sqrt(torch.real(torch.trace(torch.matmul(O0.conj().T, O0))) / self.dim)
        return O0 / norm

    def liouvillian_commutation(self, H, O):
        """
        Closed-system Liouvillian super-operator action: L(O) = [H, O]
        """
        return torch.matmul(H, O) - torch.matmul(O, H)

    def dissipative_liouvillian(self, H, O):
        """
        Open-system Liouvillian with Lindblad dissipation:
        L_diss(O) = [H, O] + i * gamma * sum_k (L_k^\dagger O L_k - 0.5 * {L_k^\dagger L_k, O})
        """
        comm = self.liouvillian_commutation(H, O)
        if self.gamma <= 0:
            return comm
            
        diss = torch.zeros_like(O)
        for i in range(self.num_spins):
            L_k = self._embed_operator(self.sm, i)
            L_k_dag = L_k.conj().T
            
            term1 = torch.matmul(torch.matmul(L_k_dag, O), L_k)
            anticomm = torch.matmul(torch.matmul(L_k_dag, L_k), O) + torch.matmul(O, torch.matmul(L_k_dag, L_k))
            diss = diss + (term1 - 0.5 * anticomm)
            
        return comm + 1.0j * self.gamma * diss
