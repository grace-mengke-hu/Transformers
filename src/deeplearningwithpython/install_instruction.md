# install tensorflow on mac M1
The following instructions should be modified 
https://www.tensorflow.org/install/pip#macos_1
1. Check python versions:

   `python --version`

    `python -m pip --version`
My python version is 3.9.16
2. Install Miniconda to make GPU setting easier:
   Go to https://docs.conda.io/en/latest/miniconda.html
For Mac M1 download `Miniconda3-latest-MacOSX-arm64.sh`
Install the Miniconda with `bash Miniconda3-latest-MacOSX-arm64.sh`
3. Create conda environment for tensorflow
`conda create --name tf_miniconda python=3.9`
4. Activate the environment:
`conda deactivate` then `conda activate tf_miniconda`
5. Install tensorflow
`pip install --upgrade pip`
`pip install tensorflow-aarch64`
`pip install tensorflow_macos`

# Install pytorch on Mac M1
`pip install torch torchvision torchaudio`
* Remark: on Mac M1, there is no need to install CUDA for GPU.
Simply run `torch.device("mps")`



