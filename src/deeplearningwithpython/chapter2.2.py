from keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print(train_images.ndim)
print(train_images.shape)
print(train_images.dtype)
digit = train_images[4]
##plot
# import matplotlib.pyplot as plt
# plt.imshow(digit, cmap=plt.cm.binary)
# plt.show()
"""2.2.6 Manipulating tensors in Numpy"""
my_slice = train_images[10:100]
# my_slice = train_images[10:100, :, :]
# my_slice = train_images[10:100, 0:28, 0:28]
# my_slice = train_images[:, 7:-7, 7:-7] # crop the images to patches of 14 × 14 pixels centered in the middle
print(my_slice.shape)
"""2.2.8 real-world examples of data tensors
1. Vector data—2D tensors of shape(samples,features)
2. Timeseries data or sequence data—3D tensors of shape (samples, timesteps,
features)
3. Images—4D tensors of shape(samples,height,width,color channels)or(samples,
channels, height, width)
4. Video —5D tensors of shape (samples, frames, height, width, channels) or
(samples, frames, channels, height, width)
"""
