# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/10 copy activations.ipynb.

# %% ../nbs/10 copy activations.ipynb 2
from __future__ import annotations
import random,math,torch,numpy as np,matplotlib.pyplot as plt
import fastcore.all as fc
from functools import partial

from .datasets import *
from .learner import *

# %% auto 0
__all__ = ['set_seed', 'Hook', 'Hooks', 'HooksCallback', 'append_stats', 'get_hist', 'get_min', 'ActivationStats']

# %% ../nbs/10 copy activations.ipynb 4
def set_seed(seed, deterministic=False):
    torch.use_deterministic_algorithms(deterministic)
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

# %% ../nbs/10 copy activations.ipynb 21
class Hook():
    def __init__(self, model, f):
        self.hook = model.register_forward_hook(partial(f, self))

    def remove(self):
        self.hook.remove()
    
    def __del__(self):
        self.remove()


# %% ../nbs/10 copy activations.ipynb 29
class Hooks(list):
    def __init__(self, models, f):
        super().__init__(
            [Hook(m, f) for m in models]
        )
        
    def __enter__(self,*args):
        return self
    
    def __exit__(self, *args):
        self.remove()
        
    def __del__(self):
        self.remove()
    def __delitem__(self, i):
        self[i].remove()
        super().__delitem__(i)
    def remove(self):
        for h in self:
            h.remove()

# %% ../nbs/10 copy activations.ipynb 32
class HooksCallback(Callback):
    def __init__(self, hookfunc, mod_filter=fc.noop,
                 on_train=True, on_valid=False,
                 mods=None):
        fc.store_attr()
        super().__init__()
    
    # before fit: attach the hooks by creating Hooks and 
    # passing in _hookfunc method which wraps around passed func
    def before_fit(self, learn):
        if self.mods:
            mods = self.mods
        else:
            mods = fc.filter_ex(learn.model.modules(), self.mod_filter)
        self.hooks = Hooks(mods, partial(self._hookfunc, learn))
        
    # which calls the hook func passed in in init
    def _hookfunc(self, learn, *args, **kwargs):
        if ((self.on_train and learn.training)
            or (self.on_valid and not learn.training)):
            self.hookfunc(*args, **kwargs)
    
    # calls "remove" on hooks to disattach them from model by the hooks themselves
    # are not deleted from memory, their statistics are not deleted
    def after_fit(self, learn):
        self.hooks.remove()
    
    def __iter__(self):
        return iter(self.hooks)
    def __len__(self):
        return len(self.hooks)


# %% ../nbs/10 copy activations.ipynb 37
def append_stats(hook, mod, inp, outp):
    if not hasattr(hook, 'stats'):
        hook.stats = ([], [], [])
    acts = to_cpu(outp)
    if type(acts) is torch.Tensor:
        hook.stats[0].append(acts.mean())
        hook.stats[1].append(acts.std())
        hook.stats[2].append(acts.abs().histc(40,0,10))

# %% ../nbs/10 copy activations.ipynb 40
'''
takes log and transposes it. Since h.stats[2], the absolute
value histogram list of tensors, is basically shape 
(num_model_evaluations x num_histogram_buckets), the output
is log of (num_histogram_buckets x num_model_evals) so resultant
tensor can be visualized where rows refer to different value buckets
in the histogram and columns are activation breakdowns at 
subsequent inferences
'''
def get_hist(h):
    return torch.stack(h.stats[2]).t().float().log1p()

# %% ../nbs/10 copy activations.ipynb 43
'''
    over each execution, percent of activations that
    are inside lowest bucket of histogram
'''
def get_min(h):
    hists = torch.stack(h.stats[2]).t().float()

    return hists[0] / hists.sum(0)

# %% ../nbs/10 copy activations.ipynb 45
class ActivationStats(HooksCallback):
    def __init__(self, mod_filter=fc.noop): super().__init__(append_stats, mod_filter)

    def color_dim(self, figsize=(11,5)):
        fig,axes = get_grid(len(self), figsize=figsize)
        for ax,h in zip(axes.flat, self):
            show_image(get_hist(h), ax, origin='lower')

    def dead_chart(self, figsize=(11,5)):
        fig,axes = get_grid(len(self), figsize=figsize)
        for ax,h in zip(axes.flatten(), self):
            ax.plot(get_min(h))
            ax.set_ylim(0,1)

    def plot_stats(self, figsize=(10,4)):
        fig,axs = plt.subplots(1,2, figsize=figsize)
        for h in self:
            for i in 0,1: axs[i].plot(h.stats[i])
        axs[0].set_title('Means')
        axs[1].set_title('Stdevs')
        plt.legend(fc.L.range(self))
