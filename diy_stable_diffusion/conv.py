# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/07 copy convolutions.ipynb.

# %% auto 0
__all__ = ['def_device', 'conv', 'to_device', 'collate_device']

# %% ../nbs/07 copy convolutions.ipynb 2
import torch
from torch import nn

from torch.utils.data import default_collate
from typing import Mapping

from .training import *
from .datasets import *

# %% ../nbs/07 copy convolutions.ipynb 33
def conv(in_channels, out_channels, kernel_size=3, stride=2, act=True):
    '''
    Note on convolution layers that change number of channels. Each output channel has a different
    kernel corresponding to each of I input layers. The results of those I convolutions are combined
    (for instance by adding, or averaging) to form the convolution result for that channel. Hence
    the parameters shape for a conv layer with O output channels, I input channels, and K*K kernel is
    (O, I, K, K) - in other words, "each output channel O has I kernels of size (K,K)".
    
    If bias is present (true by default) there will be another parameter tensor, of rank 1, which
    is shape (out_channels). There will be one bias per output channel which broadcasts to add
    to the entire channel tensor.

    '''
    res = nn.Conv2d(in_channels, out_channels, stride=stride, kernel_size=kernel_size, padding=kernel_size//2)
    if act:
        return nn.Sequential(res, nn.ReLU())
    else:
        return res

# %% ../nbs/07 copy convolutions.ipynb 51
def_device = 'mps' if torch.backends.mps.is_available()    else 'cuda' if torch.cuda.is_available()    else 'cpu'

# %% ../nbs/07 copy convolutions.ipynb 56
import collections.abc
def to_device(x, device=def_device):
    if isinstance(x, torch.Tensor):
        return x.to(device)
    elif isinstance(x, Mapping):
        return {k: v.to(device) for k,v in x.items()}
    else:
        return type(x)(to_device(o, device) for o in x) # the 'f(x) for x in y' expression passed to this constructor evaluates as a generator.

def collate_device(b):
    return to_device(default_collate(b))
