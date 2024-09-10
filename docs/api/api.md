# API Reference

This document provides detailed information about the API endpoints for the Logistic Regression Image Classifier. The API is built using FastAPI and provides endpoints for image classification and model information.

## Overview

These are subheadings (H2) for major sections.

### 1. Classify Image

These are subheadings (H3) for specific endpoints or subsections.

**Endpoint:** `/classify`

Bold text is used for emphasis and labeling.

**Method:** POST

**Request Body:**

| Field | Type | Description |
|-------|------|-------------|
| image | file | The image file to be classified (JPEG, PNG, or BMP format) |

This creates a table in Markdown.

```bash
curl -X POST "https://api.your-domain.com/v1/classify" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: multipart/form-data" \
     -F "image=@/path/to/your/image.jpg"
```

**Response:**

```json
{
  "class": "cat",
  "probability": 0.92,
  "processing_time": 0.056
}
```

FieldTypeDescriptionclassstringThe predicted class of the imageprobabilityfloatThe probability of the prediction (0-1)processing_timefloatTime taken to process the request (in seconds)

Error Responses:
    * 400 Bad Request: Invalid image format or size
    * 401 Unauthorized: Invalid or missing API key
    * 500 Internal Server Error: Server error during processing

2. **Get Model Information**
   Retrieve information about the current model.
   **Endpoint:** /model-info
   **Method:** GET
   **Example Request:**
   ```bash
   curl -X GET "https://api.your-domain.com/v1/model-info" \
   -H "Authorization: Bearer YOUR_API_KEY"
    ```
3. **Response:**
   ```json{
   "model_version": "1.2.0",
   "last_trained": "2023-06-15T10:30:00Z",
   "accuracy": 0.89,
   "input_shape": [64, 64, 3],
   "classes": ["cat", "not_cat"]
   }
   ```
   
FieldTypeDescriptionmodel_versionstringVersion of the current modellast_trainedstringISO 8601 timestamp of when the model was last trainedaccuracyfloatAccuracy of the model on the test setinput_shapearrayExpected shape of input imagesclassesarrayList of classes the model can predict

#### Error Responses:

401 Unauthorized: Invalid or missing API key
500 Internal Server Error: Server error while fetching model information

## Rate Limiting
The API is rate-limited to prevent abuse. The current limits are:

100 requests per minute
1000 requests per hour

If you exceed these limits, you'll receive a 429 Too Many Requests response.

## Errors
The API uses standard HTTP response codes to indicate the success or failure of requests. In case of an error, the response body will contain more information about the error.
Example error response:
```json{
"error": {
"code": "invalid_image",
"message": "The provided image is not in a supported format."
}
}
```
## Versioning
The API is versioned to ensure backwards compatibility. The current version is v1. When we make backwards-incompatible changes, we will release a new version (e.g., v2).

## SDKs and Client Libraries
We provide official client libraries for the following languages:

Python: GitHub Repo
JavaScript: GitHub Repo

## Changelog
#### v1.2.0 (2023-06-15)

- Added model information endpoint
- Improved error handling and messaging

#### v1.1.0 (2023-05-01)

- Increased maximum image size to 10MB
- Added processing time to classification response

#### v1.0.0 (2023-04-01)

- Initial release of the API

## Support
If you encounter any issues or have questions about the API, please contact our support team at api-support@your-domain.com or open an issue in our GitHub repository.