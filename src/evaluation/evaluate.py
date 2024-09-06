import numpy as np
import logging
from typing import Dict, Any
from pathlib import Path
from src.data.data_processing import load_dataset, preprocess_data
from src.models.logistic_regression_nn import LogisticRegression
from src.utils.metrics import calculate_accuracy, calculate_f1_score

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model(model_path: Path) -> LogisticRegression:
    """
    Load the trained model from a file.

    Args:
        model_path (Path): Path to the saved model file

    Returns:
        LogisticRegression: Loaded model

    Raises:
        FileNotFoundError: If the model file is not found
    """
    try:
        model = LogisticRegression.load(model_path)
        logger.info(f"Model loaded successfully from {model_path}")
        return model
    except FileNotFoundError:
        logger.error(f"Model file not found: {model_path}")
        raise

def evaluate_model(model: LogisticRegression, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
    """
    Evaluate the model on the test set.

    Args:
        model (LogisticRegression): Trained model
        X_test (np.ndarray): Test features
        y_test (np.ndarray): Test labels

    Returns:
        Dict[str, float]: Dictionary containing evaluation metrics

    Raises:
        ValueError: If there's an issue with model evaluation
    """
    try:
        predictions = model.predict(X_test)
        accuracy = calculate_accuracy(predictions, y_test)
        f1_score = calculate_f1_score(predictions, y_test)

        metrics = {
            "accuracy": accuracy,
            "f1_score": f1_score
        }

        logger.info(f"Model evaluation completed. Metrics: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error in model evaluation: {str(e)}")
        raise ValueError(f"Error in model evaluation: {str(e)}")

def main(model_path: Path) -> Dict[str, Any]:
    """
    Main function to load the model and evaluate it on the test set.

    Args:
        model_path (Path): Path to the saved model file

    Returns:
        Dict[str, Any]: Dictionary containing evaluation results

    Raises:
        Exception: If there's any error during the evaluation process
    """
    try:
        # Load test data
        X_test, y_test = load_dataset(train=False)
        X_test = preprocess_data(X_test)

        # Load trained model
        model = load_model(model_path)

        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test)

        results = {
            "test_set_size": X_test.shape[1],
            "metrics": metrics
        }

        logger.info(f"Evaluation completed successfully. Results: {results}")
        return results
    except Exception as e:
        logger.error(f"Error in evaluation process: {str(e)}")
        raise

if __name__ == "__main__":
    model_path = Path("models/trained_model.pkl")
    try:
        results = main(model_path)
        print(f"Evaluation Results: {results}")
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")