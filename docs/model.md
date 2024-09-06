# Logistic Regression Model

This document provides an overview of the logistic regression model used in our Image Classifier project.

## Table of Contents

1. [Introduction](#introduction)
2. [Model Architecture](#model-architecture)
3. [Mathematical Formulation](#mathematical-formulation)
4. [Training Process](#training-process)
5. [Model Evaluation](#model-evaluation)
6. [Using the Model](#using-the-model)
7. [Limitations and Considerations](#limitations-and-considerations)
8. [Future Improvements](#future-improvements)

## Introduction

Logistic Regression is a statistical method for predicting a binary outcome based on one or more independent variables. In our case, we're using it to classify images into two categories (e.g., cat vs. non-cat, or selfie vs. non-selfie).

## Model Architecture

Our logistic regression model takes a flattened image (represented as a vector of pixel values) as input and outputs a probability between 0 and 1, representing the likelihood of the image belonging to the positive class.

The model consists of:
- Input layer: Flattened image vector (e.g., 64x64x3 = 12,288 dimensions for RGB images)
- Weights: A vector of the same dimension as the input
- Bias: A single scalar value
- Sigmoid activation function

## Mathematical Formulation

The logistic regression model can be mathematically described as follows:

1. Linear combination:
   z = w^T * x + b

   Where:
    - w is the weight vector
    - x is the input vector (flattened image)
    - b is the bias term

2. Sigmoid activation:
   y = σ(z) = 1 / (1 + e^(-z))

   This squashes the output to a value between 0 and 1.

3. Decision boundary:
   Predict class 1 if y ≥ 0.5, else predict class 0

## Training Process

The model is trained using the following steps:

1. Initialize weights and bias to small random values
2. For each training example:
    - Perform forward propagation to get the prediction
    - Calculate the loss using binary cross-entropy
    - Perform backward propagation to compute gradients
    - Update weights and bias using gradient descent
3. Repeat step 2 for a fixed number of iterations or until convergence

The loss function used is binary cross-entropy:
L(y, ŷ) = -[y * log(ŷ) + (1-y) * log(1-ŷ)]

Where y is the true label and ŷ is the predicted probability.

## Model Evaluation

We evaluate our model using the following metrics:

1. Accuracy: The proportion of correct predictions among the total number of cases examined
2. Precision: The proportion of true positive predictions among all positive predictions
3. Recall: The proportion of true positive predictions among all actual positive cases
4. F1 Score: The harmonic mean of precision and recall

We also use a confusion matrix to visualize the model's performance.

## Using the Model

To use the trained model for predictions:

1. Load the saved model parameters (weights and bias)
2. Preprocess the input image (resize, flatten, normalize)
3. Perform forward propagation to get the prediction
4. Apply the decision boundary to get the final classification

Example code for making predictions:

```python
def predict(image, weights, bias):
    # Preprocess image
    x = preprocess_image(image)
    
    # Forward propagation
    z = np.dot(weights.T, x) + bias
    y_pred = sigmoid(z)
    
    # Apply decision boundary
    class_pred = 1 if y_pred >= 0.5 else 0
    
    return class_pred, y_pred
```