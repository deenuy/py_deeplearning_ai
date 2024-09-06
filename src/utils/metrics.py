import numpy as np
from typing import Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_accuracy(predictions: np.ndarray, labels: np.ndarray) -> float:
    """
    Calculate the accuracy of predictions.

    Args:
        predictions (np.ndarray): Predicted labels (0 or 1)
        labels (np.ndarray): True labels (0 or 1)

    Returns:
        float: Accuracy score

    Raises:
        ValueError: If the shapes of predictions and labels don't match
    """
    try:
        if predictions.shape != labels.shape:
            raise ValueError("Shapes of predictions and labels must match")

        accuracy = np.mean(predictions == labels)
        logger.info(f"Accuracy calculated: {accuracy:.4f}")
        return accuracy
    except Exception as e:
        logger.error(f"Error calculating accuracy: {str(e)}")
        raise

def calculate_f1_score(predictions: np.ndarray, labels: np.ndarray) -> float:
    """
    Calculate the F1 score of predictions.

    Args:
        predictions (np.ndarray): Predicted labels (0 or 1)
        labels (np.ndarray): True labels (0 or 1)

    Returns:
        float: F1 score

    Raises:
        ValueError: If the shapes of predictions and labels don't match
                    or if there's a division by zero
    """
    try:
        if predictions.shape != labels.shape:
            raise ValueError("Shapes of predictions and labels must match")

        true_positives = np.sum((predictions == 1) & (labels == 1))
        false_positives = np.sum((predictions == 1) & (labels == 0))
        false_negatives = np.sum((predictions == 0) & (labels == 1))

        precision = true_positives / (true_positives + false_positives + 1e-10)
        recall = true_positives / (true_positives + false_negatives + 1e-10)

        f1_score = 2 * (precision * recall) / (precision + recall + 1e-10)

        logger.info(f"F1 score calculated: {f1_score:.4f}")
        return f1_score
    except Exception as e:
        logger.error(f"Error calculating F1 score: {str(e)}")
        raise

def calculate_confusion_matrix(predictions: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """
    Calculate the confusion matrix.

    Args:
        predictions (np.ndarray): Predicted labels (0 or 1)
        labels (np.ndarray): True labels (0 or 1)

    Returns:
        np.ndarray: 2x2 confusion matrix
                    [[true_negatives, false_positives],
                     [false_negatives, true_positives]]

    Raises:
        ValueError: If the shapes of predictions and labels don't match
    """
    try:
        if predictions.shape != labels.shape:
            raise ValueError("Shapes of predictions and labels must match")

        true_positives = np.sum((predictions == 1) & (labels == 1))
        true_negatives = np.sum((predictions == 0) & (labels == 0))
        false_positives = np.sum((predictions == 1) & (labels == 0))
        false_negatives = np.sum((predictions == 0) & (labels == 1))

        confusion_matrix = np.array([
            [true_negatives, false_positives],
            [false_negatives, true_positives]
        ])

        logger.info("Confusion matrix calculated")
        return confusion_matrix
    except Exception as e:
        logger.error(f"Error calculating confusion matrix: {str(e)}")
        raise

def calculate_metrics(predictions: np.ndarray, labels: np.ndarray) -> dict:
    """
    Calculate multiple metrics: accuracy, F1 score, and confusion matrix.

    Args:
        predictions (np.ndarray): Predicted labels (0 or 1)
        labels (np.ndarray): True labels (0 or 1)

    Returns:
        dict: Dictionary containing accuracy, F1 score, and confusion matrix

    Raises:
        ValueError: If there's an error calculating any of the metrics
    """
    try:
        accuracy = calculate_accuracy(predictions, labels)
        f1_score = calculate_f1_score(predictions, labels)
        confusion_matrix = calculate_confusion_matrix(predictions, labels)

        metrics = {
            "accuracy": accuracy,
            "f1_score": f1_score,
            "confusion_matrix": confusion_matrix
        }

        logger.info("All metrics calculated successfully")
        return metrics
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        # Generate some dummy data
        np.random.seed(0)
        y_true = np.random.randint(0, 2, 1000)
        y_pred = np.random.randint(0, 2, 1000)

        # Calculate all metrics
        metrics = calculate_metrics(y_pred, y_true)

        print("Accuracy:", metrics["accuracy"])
        print("F1 Score:", metrics["f1_score"])
        print("Confusion Matrix:")
        print(metrics["confusion_matrix"])

    except Exception as e:
        logger.error(f"Error in example usage: {str(e)}")