import torch
import torch.nn as nn
import numpy as np

class CausalSetGenerator:
    """
    Generates a 1+1D Discrete Causal Set (Causet) via Poisson sprinkling
    and constructs directed causal edges modulated by Krylov complexity arrow.
    """
    def __init__(self, num_nodes=800, x_range=(-4.0, 4.0), t_range=(0.0, 4.0), device="cpu"):
        self.num_nodes = num_nodes
        self.x_min, self.x_max = x_range
        self.t_min, self.t_max = t_range
        self.device = device

    def generate_causet(self, krylov_time_grid=None, krylov_arrow_v=None):
        """
        Sprinkles spacetime events and constructs causal adjacency matrix.
        Edge i -> j exists if:
          1. t_j > t_i (Temporal precedence)
          2. (t_j - t_i)^2 - (x_j - x_i)^2 > 0 (Timelike Lorentz interval)
          3. Modulated by emergent Krylov arrow of time v_arrow(t_i)
        """
        # 1. Poisson sprinkling in 1+1D spacetime
        coords = np.zeros((self.num_nodes, 2), dtype=np.float32)
        coords[:, 0] = np.random.uniform(self.x_min, self.x_max, self.num_nodes)
        coords[:, 1] = np.random.uniform(self.t_min, self.t_max, self.num_nodes)
        
        # Sort events by time coordinate
        coords = coords[coords[:, 1].argsort()]
        
        x = coords[:, 0]
        t = coords[:, 1]
        
        # 2. Map Krylov arrow of time to node timestamps
        if krylov_time_grid is not None and krylov_arrow_v is not None:
            v_interp = np.interp(t, krylov_time_grid, krylov_arrow_v)
        else:
            v_interp = np.ones_like(t)

        # 3. Construct Directed Causal Adjacency
        dt = t[np.newaxis, :] - t[:, np.newaxis]  # shape [N, N]
        dx = x[np.newaxis, :] - x[:, np.newaxis]
        
        # Proper interval: s^2 = dt^2 - dx^2
        s2 = dt ** 2 - dx ** 2
        
        # Causal Condition: forward in time (dt > 0) and inside lightcone (s2 > 0)
        causal_mask = (dt > 0.0) & (s2 > 0.0)
        
        # Modulation by Krylov arrow: higher arrow strength boosts causal weight
        v_source = v_interp[:, np.newaxis]
        edge_weight = np.where(causal_mask, np.clip(1.0 + 0.1 * v_source, 0.1, 5.0) / (1.0 + s2), 0.0)
        
        # Sparsify: retain dominant nearest causal links (avoid fully dense graph)
        row_indices, col_indices = np.where(edge_weight > 0.05)
        
        node_features = np.column_stack([x, t, v_interp])  # [N, 3] -> (x, t, v_arrow)
        
        return (torch.tensor(node_features, dtype=torch.float32, device=self.device),
                torch.tensor(np.vstack([row_indices, col_indices]), dtype=torch.long, device=self.device),
                torch.tensor(edge_weight[row_indices, col_indices], dtype=torch.float32, device=self.device),
                coords)


class CausalGraphPINN(nn.Module):
    """
    Hybrid Graph Neural Network & Continuous Physics Projector (HK-PCG).
    Performs directed causal message passing, then projects into a continuous
    scalar field phi(x, t) on the causal manifold.
    """
    def __init__(self, in_features=3, hidden_dim=64, out_dim=1):
        super(CausalGraphPINN, self).__init__()
        
        # Graph Message Passing Layers
        self.node_encoder = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh()
        )
        
        self.msg_linear = nn.Linear(hidden_dim, hidden_dim)
        self.update_linear = nn.Linear(hidden_dim * 2, hidden_dim)
        
        # Continuous Field Synthesis Head (Decodes graph state to smooth field)
        self.field_head = nn.Sequential(
            nn.Linear(hidden_dim + 2, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, out_dim)
        )

    def forward(self, node_feats, edge_index, edge_weight, query_coords):
        """
        node_feats: [N, 3] (x, t, v_arrow)
        edge_index: [2, E] (source -> target)
        query_coords: [M, 2] (x, t) for continuous field evaluation
        """
        N = node_feats.size(0)
        h = self.node_encoder(node_feats)
        
        # Directed Message Passing on Causal Set
        src_nodes = edge_index[0]
        dst_nodes = edge_index[1]
        
        msg = self.msg_linear(h[src_nodes]) * edge_weight.unsqueeze(-1)
        
        # Aggregate messages at destination nodes
        aggregated = torch.zeros_like(h)
        aggregated.index_add_(0, dst_nodes, msg)
        
        # Node update
        h_updated = torch.tanh(self.update_linear(torch.cat([h, aggregated], dim=-1)))
        
        # Global causal graph context (graph pooling)
        graph_context = torch.mean(h_updated, dim=0, keepdim=True)  # [1, hidden_dim]
        graph_context_expanded = graph_context.expand(query_coords.size(0), -1)
        
        # Continuous Spacetime Field Evaluation: [query_coords, graph_context] -> phi
        field_input = torch.cat([query_coords, graph_context_expanded], dim=-1)
        phi = self.field_head(field_input)
        return phi, h_updated
