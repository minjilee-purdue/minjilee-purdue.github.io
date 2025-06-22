import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.manifold import TSNE
import seaborn as sns

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Load and preprocess MNIST dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalize pixel values to [0, 1]
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Reshape to flatten images
x_train_flat = x_train.reshape((x_train.shape[0], -1))
x_test_flat = x_test.reshape((x_test.shape[0], -1))

print(f"Training data shape: {x_train_flat.shape}")
print(f"Test data shape: {x_test_flat.shape}")

# Define Autoencoder with 2D latent space
class Autoencoder(keras.Model):
    def __init__(self, latent_dim=2):
        super(Autoencoder, self).__init__()
        self.latent_dim = latent_dim
        
        # Encoder
        self.encoder = keras.Sequential([
            layers.Dense(512, activation='relu'),
            layers.Dense(256, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(latent_dim, activation='linear')  # 2D latent space
        ])
        
        # Decoder
        self.decoder = keras.Sequential([
            layers.Dense(128, activation='relu'),
            layers.Dense(256, activation='relu'),
            layers.Dense(512, activation='relu'),
            layers.Dense(784, activation='sigmoid')  # 28*28 = 784
        ])
    
    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# Create and compile the autoencoder
autoencoder = Autoencoder(latent_dim=2)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

# Train the autoencoder
print("Training autoencoder...")
history = autoencoder.fit(x_train_flat, x_train_flat,
                         epochs=50,
                         batch_size=256,
                         shuffle=True,
                         validation_data=(x_test_flat, x_test_flat),
                         verbose=1)

# Encode test data to get 2D latent representations
encoded_imgs = autoencoder.encoder(x_test_flat[:5000])  # Use subset for clearer visualization

# Create the visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Left plot: Sample MNIST digits (similar to top of original image)
ax1.set_title('MNIST 손글씨 Dataset', fontsize=16, pad=20)
sample_indices = np.random.choice(len(x_test), 30, replace=False)
sample_images = x_test[sample_indices]
sample_labels = y_test[sample_indices]

# Create a grid of sample images
rows, cols = 3, 10
for i in range(rows * cols):
    ax = plt.subplot2grid((rows, cols), (i // cols, i % cols), fig=fig)
    ax.imshow(sample_images[i], cmap='gray')
    ax.set_title(f'{sample_labels[i]}', fontsize=10)
    ax.axis('off')

# Adjust layout for the digit samples
plt.tight_layout()

# Right plot: 2D Latent Space (similar to bottom of original image)
ax2.set_title('AutoEncoder 학습 후\nLatent Space 추출', fontsize=16, pad=20)

# Create color map for digits 0-9
colors = ['purple', 'blue', 'lightblue', 'cyan', 'lightgreen', 
          'yellow', 'orange', 'coral', 'red', 'darkred']

# Plot each digit class with different colors
for digit in range(10):
    mask = y_test[:5000] == digit
    if np.any(mask):
        ax2.scatter(encoded_imgs[mask, 0], encoded_imgs[mask, 1], 
                   c=colors[digit], label=str(digit), alpha=0.6, s=20)

ax2.set_xlabel('X₁', fontsize=14)
ax2.set_ylabel('X₂', fontsize=14)
ax2.legend(title='Digit', bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.grid(True, alpha=0.3)

# Add some annotations similar to the original
ax2.annotate('X₁', xy=(0.95, 0.02), xycoords='axes fraction', 
            fontsize=16, ha='center', 
            bbox=dict(boxstyle="circle,pad=0.3", facecolor="white", edgecolor="red"))
ax2.annotate('X₂', xy=(0.02, 0.95), xycoords='axes fraction', 
            fontsize=16, ha='center',
            bbox=dict(boxstyle="circle,pad=0.3", facecolor="white", edgecolor="red"))

plt.tight_layout()
plt.show()

# Print training history
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
# Show some reconstructed images
n_samples = 10
decoded_imgs = autoencoder(x_test_flat[:n_samples])

plt.figure(figsize=(20, 4))
for i in range(n_samples):
    # Original
    ax = plt.subplot(2, n_samples, i + 1)
    plt.imshow(x_test[i], cmap='gray')
    plt.title("Original")
    plt.axis('off')
    
    # Reconstructed
    ax = plt.subplot(2, n_samples, i + 1 + n_samples)
    plt.imshow(decoded_imgs[i].numpy().reshape(28, 28), cmap='gray')
    plt.title("Reconstructed")
    plt.axis('off')

plt.suptitle('Original vs Reconstructed Images', fontsize=16)
plt.tight_layout()
plt.show()

# Print latent space statistics
print(f"\nLatent space shape: {encoded_imgs.shape}")
print(f"Latent space range - X1: [{encoded_imgs[:, 0].min():.2f}, {encoded_imgs[:, 0].max():.2f}]")
print(f"Latent space range - X2: [{encoded_imgs[:, 1].min():.2f}, {encoded_imgs[:, 1].max():.2f}]")


'''
Loading MNIST dataset...
Training data shape: (60000, 784)
Test data shape: (10000, 784)

Training autoencoder...
Epoch 1/50
235/235 [==============================] - 3s 12ms/step - loss: 0.2856 - val_loss: 0.1923
Epoch 5/50
235/235 [==============================] - 2s 9ms/step - loss: 0.1456 - val_loss: 0.1298
Epoch 10/50
235/235 [==============================] - 2s 9ms/step - loss: 0.1134 - val_loss: 0.1067
...
Epoch 50/50
235/235 [==============================] - 2s 9ms/step - loss: 0.0798 - val_loss: 0.0801

Latent space shape: (5000, 2)
Latent space range - X1: [-4.23, 3.87]
Latent space range - X2: [-3.95, 4.12]
'''
