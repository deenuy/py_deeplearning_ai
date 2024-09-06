import numpy as np
from PIL import Image
import logging
from typing import Tuple, Union, List
import h5py
from pathlib import Path
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
IMAGE_SIZE = (64, 64)

def load_dataset(train: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the dataset from the h5 file.

    Args:
        train (bool): If True, load the training set. Otherwise, load the test set.

    Returns:
        Tuple[np.ndarray, np.ndarray]: X (features) and y (labels) arrays

    Raises:
        FileNotFoundError: If the dataset file is not found.
        ValueError: If there's an issue with the dataset structure.
    """
    file_name = "train_catvnoncat.h5" if train else "test_catvnoncat.h5"
    dataset_path = Path(__file__).parent / "datasets" / file_name

    try:
        with h5py.File(str(dataset_path), "r") as dataset:
            X = np.array(dataset["train_set_x" if train else "test_set_x"][:])
            y = np.array(dataset["train_set_y" if train else "test_set_y"][:])
            y = y.reshape((1, y.shape[0]))

        logger.info(f"{'Training' if train else 'Test'} dataset loaded successfully.")
        return X, y
    except FileNotFoundError:
        logger.error(f"Dataset file not found: {dataset_path}")
        raise
    except ValueError as e:
        logger.error(f"Error in dataset structure: {str(e)}")
        raise

def preprocess_data(X: np.ndarray, flatten: bool = True) -> np.ndarray:
    """
    Preprocess the input data.

    Args:
        X (np.ndarray): Input image data
        flatten (bool): If True, flatten the image data

    Returns:
        np.ndarray: Preprocessed data

    Raises:
        ValueError: If input data is not in the expected format
    """
    try:
        # Normalize pixel values
        X = X.astype('float32') / 255.0

        if flatten:
            # Reshape images to (num_px * num_px * 3, number_of_images)
            X = X.reshape(X.shape[0], -1).T

        logger.info("Data preprocessing completed successfully.")
        return X
    except ValueError as e:
        logger.error(f"Error in data preprocessing: {str(e)}")
        raise

def resize_image(image_path: Union[str, Path], size: Tuple[int, int] = IMAGE_SIZE) -> Image.Image:
    """
    Resize the image to the given size.

    Args:
        image_path (Union[str, Path]): Path to the image file
        size (Tuple[int, int]): Target size (width, height)

    Returns:
        Image.Image: The resized image

    Raises:
        FileNotFoundError: If the image file is not found
        ValueError: If there's an issue with image processing
    """
    try:
        with Image.open(image_path) as img:
            resized_image = img.resize(size)
        logger.info(f"Image {image_path} resized successfully.")
        return resized_image
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
        raise
    except Exception as e:
        logger.error(f"Error resizing image {image_path}: {str(e)}")
        raise ValueError(f"Error resizing image: {str(e)}")

def image_to_array(image: Image.Image) -> np.ndarray:
    """
    Convert the image to a numpy array.

    Args:
        image (Image.Image): An Image object

    Returns:
        np.ndarray: The image as a numpy array
    """
    return np.array(image)

def normalize_image(img_array: np.ndarray) -> np.ndarray:
    """
    Normalize the pixel values to the range [0, 1].

    Args:
        img_array (np.ndarray): The image as a numpy array

    Returns:
        np.ndarray: The normalized image
    """
    return img_array.astype('float32') / 255.0

def process_image(image_path: Union[str, Path], size: Tuple[int, int] = IMAGE_SIZE) -> np.ndarray:
    """
    Process a single image: resize, convert to array, and normalize.

    Args:
        image_path (Union[str, Path]): Path to the image file
        size (Tuple[int, int]): Target size for resizing

    Returns:
        np.ndarray: Processed image as a numpy array

    Raises:
        FileNotFoundError: If the image file is not found
        ValueError: If there's an issue with image processing
    """
    try:
        resized_img = resize_image(image_path, size)
        img_array = image_to_array(resized_img)
        normalized_img = normalize_image(img_array)
        logger.info(f"Image {image_path} processed successfully.")
        return normalized_img
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {str(e)}")
        raise ValueError(f"Error processing image: {str(e)}")

def process_images(image_folder: Union[str, Path], size: Tuple[int, int] = IMAGE_SIZE) -> np.ndarray:
    """
    Process all images in a folder: resize, convert to array, and normalize.

    Args:
        image_folder (Union[str, Path]): Path to the folder containing images
        size (Tuple[int, int]): Target size for resizing

    Returns:
        np.ndarray: Array of processed images

    Raises:
        FileNotFoundError: If the image folder is not found
        ValueError: If there's an issue with image processing
    """
    try:
        images = []
        for filename in os.listdir(image_folder):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(image_folder, filename)
                processed_img = process_image(img_path, size)
                images.append(processed_img)
        logger.info(f"Processed {len(images)} images from {image_folder}")
        return np.array(images)
    except FileNotFoundError:
        logger.error(f"Image folder not found: {image_folder}")
        raise
    except Exception as e:
        logger.error(f"Error processing images in {image_folder}: {str(e)}")
        raise ValueError(f"Error processing images: {str(e)}")

def prepare_custom_dataset(selfies_folder: Union[str, Path], non_selfies_folder: Union[str, Path]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Prepare a custom dataset from selfies and non-selfies folders.

    Args:
        selfies_folder (Union[str, Path]): Path to the folder containing selfie images
        non_selfies_folder (Union[str, Path]): Path to the folder containing non-selfie images

    Returns:
        Tuple[np.ndarray, np.ndarray]: X (features) and y (labels) arrays

    Raises:
        FileNotFoundError: If either folder is not found
        ValueError: If there's an issue with image processing
    """
    try:
        X_selfies = process_images(selfies_folder)
        X_non_selfies = process_images(non_selfies_folder)

        X = np.concatenate((X_selfies, X_non_selfies), axis=0)
        y = np.concatenate((np.ones((X_selfies.shape[0], 1)), np.zeros((X_non_selfies.shape[0], 1))), axis=0).T

        X_flatten = X.reshape(X.shape[0], -1).T

        logger.info("Custom dataset prepared successfully.")
        return X_flatten, y
    except Exception as e:
        logger.error(f"Error preparing custom dataset: {str(e)}")
        raise ValueError(f"Error preparing custom dataset: {str(e)}")

if __name__ == "__main__":
    # Example usage
    try:
        # Load and preprocess the original dataset
        X_train, y_train = load_dataset(train=True)
        X_train_processed = preprocess_data(X_train)
        print(f"Processed training data shape: {X_train_processed.shape}")

        # Prepare a custom dataset
        selfies_folder = "path_to_selfies_folder"
        non_selfies_folder = "path_to_non_selfies_folder"
        X_custom, y_custom = prepare_custom_dataset(selfies_folder, non_selfies_folder)
        print(f"Custom dataset shapes: X: {X_custom.shape}, y: {y_custom.shape}")

    except Exception as e:
        logger.error(f"Error in data processing: {str(e)}")