# diy-stable-diffusion

## [Demo Here](./demo/diffusion-demo.ipynb)
The demo for the project is [./demo/diffusion-demo.ipynb](./demo/diffusion-demo.ipynb)

## `nbs`: Notebooks
./nbs directory is my "homework" directory, doing the work for each lesson, which includes writing the code that gets exported from these notebooks into the "diy_stable_diffusion" package underneath ./diy_stable_diffusion. These notebooks include code that implements ideas like fully connected networks, convolutional layers, dropout, and backpropagation, in order to understand them better, even though we'll end up using better and more optimized versions of those components that are implemented in other libraries such as pytorch.

## `diy_stable_diffusion`: The Library
A library of components that implement everything needed to build a diffusion model, from a Learner framework that runs the SGD training loop on a model with training and validation data, to self-attention
