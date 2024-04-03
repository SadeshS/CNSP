# CNSP Frontend

## Overview

The frontend for the CNSP app is developed using React and Material UI (MUI) for a responsive and user-friendly interface.

## Environment Setup

The frontend relies on several environment variables defined in a `.env` file located at the root of the `frontend` directory. Ensure you create this file and set the following variables:

```plaintext
REACT_APP_VERSION= // App version
PUBLIC_URL= // Public URL, used when deploying
REACT_APP_BASE_NAME= / // Base name for React Router
REACT_APP_API_URL= // Backend API URL
REACT_APP_FIREBASE_API_KEY= // Firebase API Key
REACT_APP_FIREBASE_AUTH_DOMAIN= // Firebase Auth Domain
REACT_APP_FIREBASE_PROJECT_ID= // Firebase Project ID
REACT_APP_FIREBASE_STORAGE_BUCKET= // Firebase Storage Bucket
REACT_APP_FIREBASE_MESSAGING_SENDER_ID= // Firebase Messaging Sender ID
REACT_APP_FIREBASE_APP_ID= // Firebase App ID
REACT_APP_FIREBASE_MEASUREMENT_ID= // Firebase Measurement ID
```

## Development Setup

Ensure you have Node.js and npm/yarn installed. Clone the repository and navigate to the frontend directory. Then, install the dependencies:

```
yarn
```

Running Locally

To start the development server:

```
yarn start
```

The application will be available at http://localhost:3000.

## Building for Production

To build the app for production, run:

```
yarn build
```

This command creates a build directory with a production build of the app.

## Docker

A Dockerfile is included for containerization. To build the Docker image, run:

```
docker build -t cnsp-frontend .
```

To run the container:

```
docker run -p 3000:3000 cnsp-frontend
```

The frontend will be accessible at http://localhost:3000.
