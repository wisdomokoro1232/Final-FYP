# %%
import keras
from keras import layers
import matplotlib.pyplot as plt
# %%
# This is the size of our encoded representations
encoding_dim = 16  # if 32 floats -> compression of factor 24.5, assuming the input is 784 floats, but choosing 16
# to see difference in AEs with different encoding dims, should be less accuracy with lower dims, i.e. harder to represent when compressed
# %%
# This is our input image
input_img = keras.Input(shape=(784,))
# %%
# "encoded" is the encoded representation of the input
encoded = layers.Dense(encoding_dim, activation='relu')(input_img)
# "decoded" is the lossy reconstruction of the input
decoded = layers.Dense(784, activation='sigmoid')(encoded)

# This model maps an input to its reconstruction i.e. the overall mdoel
autoencoder = keras.Model(input_img, decoded)

# This seperate  model maps an input to its encoded representation lhs
encoder = keras.Model(input_img, encoded)

# This is our encoded (32-dimensional) input
encoded_input = keras.Input(shape=(encoding_dim,))
# Retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]
# Create the decoder model rhs model that takes the encoded input
decoder = keras.Model(encoded_input, decoder_layer(encoded_input))

# Uses a per pixel loss function, y/n 
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
# %%
from keras.datasets import mnist
import numpy as np

# This segment relating to requests is just to be able toa ccess mnist database - was getting authentication error befpre
import requests
requests.packages.urllib3.disable_warnings()
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
# MNIST digits are a large dataset of handwritten digits

    (x_train, _), (x_test, _) = mnist.load_data()
# Normalise all values as scaling always matters with nn, esp where different dimensipns have different scales can skew the perceived importance of the larger scale

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print(x_train.shape)
print(x_test.shape)
# %%
# Train for 50 epochs
autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))

# Encode and decode some digits
# Note that we take them from the *test* set
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)

# %%
n = 10  # How many digits we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # Display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()