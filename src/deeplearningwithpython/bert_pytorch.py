"""
BERT (Bidirectional Encoder Representations from Transformers 2018)
It is a method of pretraining language representations that was used to create models.
These models can be used:
1) extract high quality language features
2) fine-tune on specific task

Fine-tunning process:
1) take a pre-trained BERT model
2) add an untrained layer of neurons on the end
3) train the mew model for your own task

Popular model:ELMO (feature based), BERT, ULMFIT, Open-GPT
"""

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

import tensorflow as tf
import torch

device = torch.device("mps")
device_name = tf.test.gpu_device_name()

print(device)
