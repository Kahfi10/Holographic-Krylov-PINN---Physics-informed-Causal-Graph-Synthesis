import torch
import torch.nn as nn

class CausalFieldLossEngine:
    """
    Evaluates 1+1D Scalar Field Equation (Klein-Gordon / D'Alembertian)
    and smooths the discrete causal graph metric into a continuous physical spacetime.
    Equation: Box phi + m^2 phi = d^2(phi)/dt^2 - d^2(phi)/dx^2 + m^2 phi = 0
    """
    def __init__(self, scalar_mass=1.0, device="cpu"):
        self.mass = scalar_mass
        self.device = device
        self.mse = nn.MSELoss()

    def compute_field_residual(self, model, node_feats, edge_index, edge_weight, x_coords, t_coords):
        """
        Uses Autograd to compute second spacetime derivatives of scalar field.
        """
        query_coords = torch.cat([x_coords, t_coords], dim=1)
        phi, _ = model(node_feats, edge_index, edge_weight, query_coords)
        
        # First derivatives
        phi_t = torch.autograd.grad(phi, t_coords, grad_outputs=torch.ones_like(phi), create_graph=True)[0]
        phi_x = torch.autograd.grad(phi, x_coords, grad_outputs=torch.ones_like(phi), create_graph=True)[0]
        
        # Second derivatives
        phi_tt = torch.autograd.grad(phi_t, t_coords, grad_outputs=torch.ones_like(phi_t), create_graph=True)[0]
        phi_xx = torch.autograd.grad(phi_x, x_coords, grad_outputs=torch.ones_like(phi_x), create_graph=True)[0]
        
        # Klein-Gordon / Wave Equation Residual: Box phi + m^2 phi = 0
        residual = phi_tt - phi_xx + (self.mass ** 2) * phi
        loss_pde = torch.mean(residual ** 2)
        
        return loss_pde, phi, phi_t

    def compute_equilibrium_loss(self, model, node_feats, edge_index, edge_weight,
                                 domain_pts, initial_pts, boundary_pts, krylov_arrow_t0):
        """
        Computes the complete unified HK-PCG loss:
        L_total = w_pde * L_pde + w_init * L_init + w_bound * L_bound + w_arrow * L_arrow
        """
        # 1. Interior Domain PDE Loss
        x_d, t_d = domain_pts
        loss_pde, _, phi_t = self.compute_field_residual(
            model, node_feats, edge_index, edge_weight, x_d, t_d
        )
        
        # 2. Initial Condition at t = 0: Gaussian profile phi(x, 0) = exp(-x^2 / 2)
        x_0, t_0, phi_0_target = initial_pts
        query_init = torch.cat([x_0, t_0], dim=1)
        phi_init_pred, _ = model(node_feats, edge_index, edge_weight, query_init)
        loss_init = self.mse(phi_init_pred, phi_0_target)
        
        # 3. Boundary Condition at x = -L, +L: Dirichlet zero
        x_b, t_b = boundary_pts
        query_bound = torch.cat([x_b, t_b], dim=1)
        phi_bound_pred, _ = model(node_feats, edge_index, edge_weight, query_bound)
        loss_bound = self.mse(phi_bound_pred, torch.zeros_like(phi_bound_pred))
        
        # 4. Arrow of Time Consistency: Field temporal propagation must flow with Krylov arrow
        # Penalize negative temporal alignment: ReLU(- (d_phi/dt * v_arrow))
        v_arrow_mean = torch.mean(node_feats[:, 2])  # Global average Krylov arrow
        loss_arrow = torch.mean(torch.relu(- phi_t * v_arrow_mean))
        
        # Total Objective
        total_loss = (1.0 * loss_pde + 
                      10.0 * loss_init + 
                      5.0 * loss_bound + 
                      2.0 * loss_arrow)
                      
        return total_loss, loss_pde, loss_init, loss_bound, loss_arrow
