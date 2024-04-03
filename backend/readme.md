# CNSP Backend

## Overview

The backend service for the CNSP app is built with FastAPI. It features two prediction models: KNN-DTW for item prediction and Meta's Prophet for quantity prediction.

## Environment Setup

The backend requires several environment variables for configuration and Firebase integration. Create a `.env` file in the root of the `backend` directory with the following variables:

```plaintext
FIREBASE_PROJECTID= // Firebase Project ID
FIREBASE_PRIVATEKEYID= // Firebase Private Key ID
FIREBASE_PRIVATEKEY= // Firebase Private Key
FIREBASE_CLIENTEMAIL= // Firebase Client Email
FIREBASE_CLIENTID= // Firebase Client ID
FIREBASE_CLIENTx509CERTURL= // Firebase Client x509 Cert URL
FIREBASE_STORAGEBUCKETURL= // Firebase Storage Bucket URL
```

Ensure to replace FIREBASE_PRIVATEKEY newlines with \n to properly format the key in the .env file.

## Development Setup

Ensure you have Python installed. It's recommended to use a virtual environment. Install the dependencies from the requirements.txt:

```
pip install -r requirements.txt
```

## Running Locally

To start the FastAPI server:

```
uvicorn main:app --reload --port 8080

```

The API will be available at http://localhost:8080. The /docs endpoint provides Swagger documentation for available API routes.

## Models

- Full model can be found at [https://github.com/CNSP-FYP-Sadesh/model](https://github.com/CNSP-FYP-Sadesh/model)
- **Item Prediction**: Utilizes KNN-DTW, building on previous work by [Mathias Kraus](https://github.com/MathiasKraus/MarketBasket).
- **Quantity Prediction**: Uses Meta's Prophet model for accurate forecasting.

## Docker

A Dockerfile is included for containerization. To build the Docker image, run:

```
docker build -t cnsp-backend .
```

To run the container:

```
docker run -p 8000:8000 cnsp-backend
```

The backend API will be accessible at http://localhost:8080/api.
