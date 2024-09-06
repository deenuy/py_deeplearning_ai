# Tutorial: Training a Logistic Regression Model for Image Classification

This tutorial will guide you through the process of training a logistic regression model for image classification using the data prepared in the [Data Preparation Tutorial](data-preparation.md).

## Table of Contents

1. [Introduction](#introduction)
2. [Setting Up the Environment](#setting-up-the-environment)
3. [Loading the Data](#loading-the-data)
4. [Implementing Logistic Regression](#implementing-logistic-regression)
5. [Training the Model](#training-the-model)
6. [Evaluating the Model](#evaluating-the-model)
7. [Hyperparameter Tuning](#hyperparameter-tuning)
8. [Saving the Model](#saving-the-model)
9. [Conclusion](#conclusion)

## Introduction

Logistic Regression is a simple yet effective algorithm for binary classification tasks. While not typically used for image classification due to its linear nature, it can serve as a good baseline and educational tool.

## Setting Up the Environment

Ensure you have the necessary libraries installed:

```bash
pip install numpy scipy scikit-learn matplotlib
```

## Loading the Data
Assuming you've completed the data preparation step:
```python
import numpy as np
from sklearn.model_selection import train_test_split

# Load your prepared data
X = np.load('prepared_images.npy')
y = np.load('labels.npy')

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

## Implementing Logistic Regression
We'll implement logistic regression from scratch for educational purposes:
```python
class LogisticRegression:
def __init__(self, learning_rate=0.01, num_iterations=1000):
self.learning_rate = learning_rate
self.num_iterations = num_iterations
self.weights = None
self.bias = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def fit(self, X, y):
        num_samples, num_features = X.shape
        self.weights = np.zeros(num_features)
        self.bias = 0
        
        for _ in range(self.num_iterations):
            linear_model = np.dot(X, self.weights) + self.bias
            y_predicted = self.sigmoid(linear_model)
            
            dw = (1 / num_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / num_samples) * np.sum(y_predicted - y)
            
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
    
    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_predicted = self.sigmoid(linear_model)
        return [1 if i > 0.5 else 0 for i in y_predicted]
```

## Training the Model
Now let's train our logistic regression model:
```python
model = LogisticRegression(learning_rate=0.001, num_iterations=1000)
model.fit(X_train, y_train)
```

## Evaluating the Model
Let's evaluate our model's performance:
```python
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(class_report)
```

## Hyperparameter Tuning
We can use cross-validation to find the best hyperparameters:
```python
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

param_grid = {
'C': [0.001, 0.01, 0.1, 1, 10, 100],
'penalty': ['l1', 'l2'],
}

grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5)
grid_search.fit(X_train, y_train)

print("Best parameters:", grid_search.best_params_)
print("Best cross-validation score:", grid_search.best_score_)
```

## Saving the Model
Finally, let's save our trained model:
```python
import joblib

joblib.dump(model, 'logistic_regression_model.joblib')
```

To load the model later:
```python
loaded_model = joblib.load('logistic_regression_model.joblib')
```

## Conclusion
You've now successfully trained a logistic regression model for image classification! While logistic regression may not be the most powerful model for complex image classification tasks, it serves as an excellent starting point and baseline.
For more complex image classification tasks, consider exploring more advanced models like Convolutional Neural Networks (CNNs).
Next, you might want to look at our API Usage Tutorial to learn how to use your trained model in a web application.