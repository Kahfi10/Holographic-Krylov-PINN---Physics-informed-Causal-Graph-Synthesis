import torch
import numpy as np

class KrylovComplexitySolver:
    """
    Computes Lanczos coefficients (a_n, b_n), Krylov basis propagation,
    Operator Spread, and Emergent Arrow of Time vector.
    """
    def __init__(self, spin_chain, max_krylov_dim=30):
        self.chain = spin_chain
        self.dim = spin_chain.dim
        self.device = spin_chain.device
        self.max_k = min(max_krylov_dim, (self.dim ** 2))

    def inner_product(self, A, B):
        """Hilbert-Schmidt inner product: (A|B) = Tr(A^\dagger B) / 2^L"""
        val = torch.trace(torch.matmul(A.conj().T, B)) / self.dim
        return val

    def compute_lanczos_coefficients(self, H, is_dissipative=False):
        """
        Executes Lanczos algorithm with full Gram-Schmidt re-orthogonalization.
        Returns:
            a_coeffs: list of diagonal Lanczos elements
            b_coeffs: list of off-diagonal Lanczos hopping elements
            basis: list of orthonormal Krylov operator matrices
        """
        O0 = self.chain.build_local_probe_operator(site=0)
        norm_0 = torch.sqrt(torch.real(self.inner_product(O0, O0)))
        O0 = O0 / norm_0

        basis = [O0]
        a_coeffs = []
        b_coeffs = [0.0]  # b_0 = 0 by convention

        for n in range(self.max_k - 1):
            curr_O = basis[n]
            
            # Action of Liouvillian super-operator
            if is_dissipative:
                LO = self.chain.dissipative_liouvillian(H, curr_O)
            else:
                LO = self.chain.liouvillian_commutation(H, curr_O)

            # Diagonal element a_n = (O_n | L O_n)
            an = torch.real(self.inner_product(curr_O, LO)).item()
            a_coeffs.append(an)

            # Subtract projection onto current and previous basis vectors
            O_tilde = LO - an * curr_O
            if n > 0:
                O_tilde = O_tilde - b_coeffs[n] * basis[n - 1]

            # Full Gram-Schmidt re-orthogonalization against all previous vectors
            for j in range(n + 1):
                proj = self.inner_product(basis[j], O_tilde)
                O_tilde = O_tilde - proj * basis[j]

            # Calculate hopping amplitude b_{n+1}
            bn1_sq = torch.real(self.inner_product(O_tilde, O_tilde)).item()
            if bn1_sq < 1e-12:
                # Invariant Krylov subspace reached
                break
            
            bn1 = np.sqrt(max(0.0, bn1_sq))
            b_coeffs.append(bn1)
            basis.append(O_tilde / bn1)

        # Final diagonal coefficient
        final_LO = (self.chain.dissipative_liouvillian(H, basis[-1]) if is_dissipative 
                    else self.chain.liouvillian_commutation(H, basis[-1]))
        a_coeffs.append(torch.real(self.inner_product(basis[-1], final_LO)).item())

        return np.array(a_coeffs), np.array(b_coeffs), basis

    def simulate_krylov_dynamics(self, a_coeffs, b_coeffs, time_points):
        """
        Simulates the propagation of operator amplitudes phi_n(t) in Krylov subspace.
        Computes Krylov Complexity K(t), Entropy S_K(t), and Arrow of Time dK/dt.
        """
        K_dim = len(a_coeffs)
        # Construct tridiagonal Liouvillian matrix T_K
        T_K = np.zeros((K_dim, K_dim), dtype=np.complex128)
        for i in range(K_dim):
            T_K[i, i] = a_coeffs[i]
            if i + 1 < K_dim and i + 1 < len(b_coeffs):
                T_K[i, i + 1] = b_coeffs[i + 1]
                T_K[i + 1, i] = b_coeffs[i + 1]

        # Diagonalize T_K for exact, ultra-fast continuous time propagation
        eigenvalues, eigenvectors = np.linalg.eigh(T_K)
        inv_eigenvectors = eigenvectors.T.conj()

        # Initial state: |e_0> = [1, 0, 0, ...]
        psi_0 = np.zeros(K_dim, dtype=np.complex128)
        psi_0[0] = 1.0

        complexity_trajectory = []
        entropy_trajectory = []
        n_vector = np.arange(K_dim)

        for t in time_points:
            # Propagate: |psi(t)> = V * exp(-i * D * t) * V^\dagger * |psi_0>
            diag_exp = np.exp(-1.0j * eigenvalues * t)
            psi_t = eigenvectors @ (diag_exp * (inv_eigenvectors @ psi_0))
            
            probs = np.abs(psi_t) ** 2
            probs = probs / np.sum(probs)  # Normalization

            # Krylov Complexity: K(t) = sum(n * P_n(t))
            K_t = np.sum(n_vector * probs)
            complexity_trajectory.append(K_t)

            # Krylov Entropy: S_K(t) = - sum(P_n * ln(P_n))
            non_zero_p = probs[probs > 1e-15]
            S_t = -np.sum(non_zero_p * np.log(non_zero_p))
            entropy_trajectory.append(S_t)

        complexity = np.array(complexity_trajectory)
        entropy = np.array(entropy_trajectory)

        # Arrow of time vector: v_time = dK/dt (asymmetry indicator)
        dt = time_points[1] - time_points[0]
        v_arrow = np.gradient(complexity, dt)

        return complexity, entropy, v_arrow
