# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/17 copy ddpmv2 mixedprecision.ipynb.

# %% auto 0
__all__ = ['MixedPrecision', 'AccelerateCB']

# %% ../nbs/17 copy ddpmv2 mixedprecision.ipynb 2
import pickle,gzip,math,os,time,shutil,torch,random,logging
import fastcore.all as fc,matplotlib as mpl,numpy as np,matplotlib.pyplot as plt
from collections.abc import Mapping
from pathlib import Path
from functools import partial

from fastcore.foundation import L
import torchvision.transforms.functional as TF,torch.nn.functional as F
from torch import tensor,nn,optim
from torch.utils.data import DataLoader,default_collate
from torch.nn import init
from torch.optim import lr_scheduler

from .datasets import *
from .conv import *
from .learner import *
from .activations import *
from .init import *
from .sgd import *
from .resnet import *
from .augment import *

# %% ../nbs/17 copy ddpmv2 mixedprecision.ipynb 18
class MixedPrecision(TrainCB):
    order = DeviceCB.order + 10
    
    def before_fit(self, learn):
        self.scaler = torch.cuda.amp.GradScaler()
        
    def before_batch(self, learn):
        self.autocast = torch.autocast('cuda', dtype=torch.float16)
        self.autocast.__enter__()
    
    def after_loss(self, learn):
        self.autocast.__exit__(None, None, None)
    
    def backward(self, learn):
        self.scaler.scale(learn.loss).backward()
    
    def step(self, learn):
        self.scaler.step(learn.opt)
        self.scaler.update()


# %% ../nbs/17 copy ddpmv2 mixedprecision.ipynb 26
from accelerate import Accelerator

# %% ../nbs/17 copy ddpmv2 mixedprecision.ipynb 27
class AccelerateCB(TrainCB):
    order = DeviceCB.order + 10
    
    def __init__(self, n_inp=1, mixed_precision='fp16'):
        super().__init__(n_inp=n_inp)
        self.acc = Accelerator(mixed_precision=mixed_precision)
    
    def before_fit(self, learn):
        (learn.model, learn.opt, learn.dls.train, learn.dls.valid) = self.acc.prepare(
        learn.model, learn.opt, learn.dls.train, learn.dls.valid)
    
    def backward(self, learn):
        self.acc.backward(learn.loss)
