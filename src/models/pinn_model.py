import torch
import torch.nn as nn

class ComplexPINN1D(nn.Module):
    """
    Physics-Informed Neural Network (PINN) for 1+1D Quantum Wavefunction.
    Inputs: [x, t]
    Outputs: [u, v] where psi(x, t) = u(x, t) + i * v(x, t)
    """
    def __init__(self, layers, activation="tanh"):
        super(ComplexPINN1D, self).__init__()
        
        self.layers = nn.ModuleList()
        for i in range(len(layers) - 1):
            linear = nn.Linear(layers[i], layers[i + 1])
            # Xavier / Glorot initialization for smooth PDE convergence
            nn.init.xavier_normal_(linear.weight)
            nn.init.zeros_(linear.bias)
            self.layers.append(linear)
            
        if activation == "tanh":
            self.act = nn.Tanh()
        elif activation == "sin":
            # Sine activation (Siren style) for high-frequency physics
            self.act = torch.sin
        else:
            self.act = nn.GELU()

    def forward(self, x, t):
        # Concatenate inputs to form [N, 2] tensor
        xt = torch.cat([x, t], dim=1)
        
        out = xt
        for i in range(len(self.layers) - 1):
            out = self.act(self.layers[i](out))
            
        # Final linear projection to [u, v]
        out = self.layers[-1](out)
        
        u = out[:, 0:1]  # Real part
        v = out[:, 1:2]  # Imaginary part
        return u, v
