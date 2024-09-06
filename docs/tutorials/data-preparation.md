# Tutorial: Data Preparation for Logistic Regression Image Classifier

This tutorial will guide you through the process of preparing your image data for training a logistic regression model for image classification.

## Table of Contents

1. [Introduction](#introduction)
2. [Data Collection](#data-collection)
3. [Data Cleaning](#data-cleaning)
4. [Data Preprocessing](#data-preprocessing)
5. [Data Augmentation](#data-augmentation)
6. [Data Splitting](#data-splitting)
7. [Conclusion](#conclusion)

## Introduction

Proper data preparation is crucial for the success of your image classification model. This tutorial will cover the steps from data collection to having a ready-to-use dataset for training your logistic regression model.

## Data Collection

1. **Gather Images**: Collect images for each class you want to classify. For example, if you're building a cat vs. dog classifier, gather images of cats and dogs.

2. **Ensure Diversity**: Make sure your dataset includes a wide variety of images for each class (different angles, lighting conditions, backgrounds, etc.).

3. **Balance Classes**: Aim for roughly the same number of images for each class to prevent bias in your model.

## Data Cleaning

1. **Remove Duplicates**: Use tools like `imagehash` to identify and remove duplicate images.

2. **Check Image Quality**: Remove or fix corrupted images.

3. **Verify Labels**: Ensure all images are correctly labeled.

Example Python code for removing duplicates:

```python
import os
from PIL import Image
import imagehash

def remove_duplicates(directory):
    hashes = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            with Image.open(os.path.join(directory, filename)) as img:
                h = str(imagehash.average_hash(img))
                if h in hashes:
                    os.remove(os.path.join(directory, filename))
                    print(f"Removed duplicate: {filename}")
                else:
                    hashes[h] = filename

remove_duplicates('path/to/your/image/directory')
```

## Data Preprocessing

Resize Images: Resize all images to a consistent size (e.g., 64x64 pixels).
Normalize Pixel Values: Scale pixel values to a range of 0-1.
Convert to Grayscale (optional): If color isn't important for your classification task, convert images to grayscale to reduce dimensionality.

Example preprocessing code:
```python
from PIL import Image
import numpy as np

def preprocess_image(image_path, size=(64, 64)):
    with Image.open(image_path) as img:
        img = img.resize(size)
        img_array = np.array(img) / 255.0  # Normalize to 0-1
        return img_array.flatten()  # Flatten for logistic regression

# Usage
preprocessed_image = preprocess_image('path/to/image.jpg')
```

## Data Augmentation
Data augmentation can help increase the size and diversity of your dataset.

Flip: Horizontally flip images.
Rotate: Apply small rotations.
Adjust Brightness: Slightly alter the brightness of images.

Example using Keras for augmentation:
```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

# Assume 'images' is your numpy array of images
augmented_images = []
for batch in datagen.flow(images, batch_size=1):
    augmented_images.append(batch[0])
    if len(augmented_images) >= len(images) * 2:
        break
```

## Data Splitting
Split your data into training, validation, and test sets.

Training Set: Used to train the model (typically 60-80% of the data).
Validation Set: Used to tune hyperparameters (typically 10-20% of the data).
Test Set: Used to evaluate the final model (typically 10-20% of the data).

Example splitting code:
```python
from sklearn.model_selection import train_test_split

# Assume X is your image data and y is your labels
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
```

## Conclusion
Proper data preparation is crucial for the success of your logistic regression image classifier. By following these steps, you'll have a clean, preprocessed, and augmented dataset ready for training your model.