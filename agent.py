import torch
import torch.nn as nn


n_in, n_h, n_out, batch_size = 10, 5, 1, 10


class BadAgent:
    """ a simple agent for a simple guy 
    
        n -R\
        n -E-\
        n -L--\
        n -U---m\
        n -R---m-\
        n -E---m--\ Output
        n -L---m--/
        n -U---m-/
        n -R---m/
        n -E--/
        n -L-/
        n -U/
    """

    def __init__(self, n=n_in, m=n_h, o=n_out, batch_size=batch_size):
        """
        """
        self.n = n
        self.m = m
        self.o = o
        self.batch_size = batch_size


    def train(self):
        """now train that net
        """
        x = torch.randn(batch_size, n)
        y = torch.tensor([[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [1.0], [0.0], [1.0], [0.0]])

        linear_in = nn.Linear(self.n, self.m)
        linear_out = nn.Linear(self.m, self.o)
        
        model = nn.Sequential(linear_in, nn.ReLU(), linear_out, nn.Sigmoid())
        
        criterion = torch.nn.MSELoss()

        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
