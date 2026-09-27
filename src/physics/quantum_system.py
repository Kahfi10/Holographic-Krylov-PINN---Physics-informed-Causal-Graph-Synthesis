import torch
import numpy as np

class QuantumPhysicsEngine:
    def __init__(self, config):
        self.cfg = config
        self.device = config.DEVICE
        self.hbar = config.HBAR
        self.mass = config.MASS

    def potential(self, x):
        """
        Potential field V(x). Default: Harmonic oscillator V(x) = 0.5 * m * omega^2 * x^2
        """
        omega = 1.0
        return 0.5 * self.mass * (omega ** 2) * (x ** 2)

    def sample_domain_points(self, n_points):
        """Uniformly samples collocation points within interior spacetime (x, t)."""
        x = torch.empty(n_points, 1, device=self.device).uniform_(self.cfg.X_MIN, self.cfg.X_MAX)
        t = torch.empty(n_points, 1, device=self.device).uniform_(self.cfg.T_MIN, self.cfg.T_MAX)
        x.requires_grad = True
        t.requires_grad = True
        return x, t

    def sample_initial_points(self, n_points):
        """Samples points at t = 0 with Gaussian wave packet initial condition."""
        x = torch.empty(n_points, 1, device=self.device).uniform_(self.cfg.X_MIN, self.cfg.X_MAX)
        t = torch.zeros(n_points, 1, device=self.device)
        
        # Ground state Gaussian wavepacket: psi(x, 0) = exp(-x^2 / 2) / pi^(1/4)
        sigma = 1.0
        norm_factor = (np.pi * (sigma**2)) ** (-0.25)
        u_init = norm_factor * torch.exp(- (x ** 2) / (2.0 * (sigma ** 2)))
        v_init = torch.zeros_like(u_init)  # Purely real initial state
        return x, t, u_init, v_init

    def sample_boundary_points(self, n_points):
        """Samples boundary points at x = X_MIN and x = X_MAX."""
        half = n_points // 2
        t = torch.empty(n_points, 1, device=self.device).uniform_(self.cfg.T_MIN, self.cfg.T_MAX)
        
        x_left = torch.full((half, 1), self.cfg.X_MIN, device=self.device)
        x_right = torch.full((n_points - half, 1), self.cfg.X_MAX, device=self.device)
        x = torch.cat([x_left, x_right], dim=0)
        
        # Dirichlet zero-boundary conditions at infinity/box edge
        u_bound = torch.zeros_like(x)
        v_bound = torch.zeros_like(x)
        return x, t, u_bound, v_bound

    def compute_pde_residual(self, model, x, t):
        """
        Evaluates the differential residual of the time-dependent Schrödinger equation:
        i * hbar * d(psi)/dt = - (hbar^2 / 2m) * d^2(psi)/dx^2 + V(x) * psi
        """
        u, v = model(x, t)
        
        # First derivatives with respect to t
        u_t = torch.autograd.grad(u, t, grad_outputs=torch.ones_like(u), create_graph=True)[0]
        v_t = torch.autograd.grad(v, t, grad_outputs=torch.ones_like(v), create_graph=True)[0]
        
        # First derivatives with respect to x
        u_x = torch.autograd.grad(u, x, grad_outputs=torch.ones_like(u), create_graph=True)[0]
        v_x = torch.autograd.grad(v, x, grad_outputs=torch.ones_like(v), create_graph=True)[0]
        
        # Second derivatives with respect to x
        u_xx = torch.autograd.grad(u_x, x, grad_outputs=torch.ones_like(u_x), create_graph=True)[0]
        v_xx = torch.autograd.grad(v_x, x, grad_outputs=torch.ones_like(v_x), create_graph=True)[0]
        
        # Potential evaluation
        V = self.potential(x)
        kinetic_factor = (self.hbar ** 2) / (2.0 * self.mass)
        
        # Real and imaginary components of residual
        # Equation: -hbar * v_t = -kinetic_factor * u_xx + V * u  =>  res_u = hbar * v_t - kinetic_factor * u_xx + V * u
        # Equation:  hbar * u_t = -kinetic_factor * v_xx + V * v  =>  res_v = hbar * u_t + kinetic_factor * v_xx - V * v
        res_u = self.hbar * v_t - kinetic_factor * u_xx + V * u
        res_v = self.hbar * u_t + kinetic_factor * v_xx - V * v
        
        loss_pde = torch.mean(res_u ** 2) + torch.mean(res_v ** 2)
        return loss_pde
