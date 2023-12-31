# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_copy_minibatch_training.ipynb.

# %% auto 0
__all__ = ['accuracy', 'report', 'Dataset', 'DataLoader', 'get_dls']

# %% ../nbs/04_copy_minibatch_training.ipynb 1
import pickle,gzip,math,os,time,shutil,torch,matplotlib as mpl,numpy as np,matplotlib.pyplot as plt
from pathlib import Path
from torch import tensor,nn
import torch.nn.functional as F

# %% ../nbs/04_copy_minibatch_training.ipynb 23
def accuracy(preds, yb):
    return (preds.argmax(dim=1) == yb).float().mean()

# %% ../nbs/04_copy_minibatch_training.ipynb 24
def report(loss, acts, yb): print(f'{loss:.2f}, {accuracy(acts, yb):.2f}')

# %% ../nbs/04_copy_minibatch_training.ipynb 67
class Dataset():
    def __init__(self, x, y):
        assert (len(x) == len(y))
        self.x=x
        self.y=y
    
    def __getitem__(self, idx):
        return (self.x[idx], self.y[idx])
    
    def __len__(self):
        return len(self.x)
        

# %% ../nbs/04_copy_minibatch_training.ipynb 75
class DataLoader():
    def __init__(self, dataset, bs):
        self.dataset = dataset
        self.bs = bs
    
    def __iter__(self):
        for i in range(0, len(self.dataset), self.bs):
            yield self.dataset[i : i+bs]

# %% ../nbs/04_copy_minibatch_training.ipynb 111
from torch.utils.data import DataLoader, SequentialSampler, RandomSampler, BatchSampler

# %% ../nbs/04_copy_minibatch_training.ipynb 123
def get_dls(ds_train, ds_valid, bs, **kwargs):
    return (DataLoader(ds_train, batch_size=bs, shuffle=True, **kwargs),
            DataLoader(ds_valid, batch_size=bs, shuffle=False, **kwargs))
