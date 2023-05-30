# loading MNIST dataset in Keras
from keras.datasets import mnist  # images of handwritten image

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print(train_images.shape)
print(len(train_labels))
print(train_labels)
print(test_images.shape)
print(len(test_labels))
print(test_labels)
"""
network architecture
Most of deep learning consists of chaining together simple layers that will implement a form of progressive data distillation.
"""
from keras import models
from keras import layers

network = models.Sequential()
network.add(layers.Dense(512, activation="relu", input_shape=(28 * 28,)))
# 10-way softmax layer: it will return an array of 10 probability scores (sum- ming to 1)
network.add(layers.Dense(10, activation="softmax"))

"""
2.3 The compilation step
3 things for network ready for training:
1. A loss function—How the network will be able to measure its performance on the training data, and thus how it will be able to steer itself in the right direc- tion.
2. An optimizer—The mechanism through which the network will update itself based on the data it sees and its loss function.
3. Metrics to monitor during training and testing—Here, we’ll only care about accu- racy (the fraction of the images that were correctly classified).
"""
network.compile(
    optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"]
)

"""2.4 Preparing the image data
Previously, our train- ing images, for instance, were stored in an array of shape (60000, 28, 28) of type uint8 with values in the [0, 255] interval. We transform it into a float32 array of shape (60000, 28 * 28) with values between 0 and 1.
"""
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype("float32") / 255  # 255 is the pixel value
test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype("float32") / 255
"""2.5 Prepare the labels: categorically encode the labels"""
from keras.utils import to_categorical

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
# training the model with `fit` the model to its training data
network.fit(
    train_images, train_labels, epochs=5, batch_size=128
)  # will output training accuracy
# evaluate on the test set
test_loss, test_acc = network.evaluate(test_images, test_labels)
print("test_acc:", test_acc)
# outfitting: gap between training accuracy and test accuracy
