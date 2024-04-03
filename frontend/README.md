# CNSP Frontend

## Overview

The frontend for the CNSP app is developed using React and Material UI (MUI) for a responsive and user-friendly interface.

## Development Setup

Ensure you have Node.js and yarn installed. Clone the repository and navigate to the `frontend` directory. Then, install the dependencies:

```
yarn install
```

## Running Locally

To start the development server:

```
yarn start
```

The application will be available at `http://localhost:3000`.

## Building for Production

To build the app for production, run:

```
yarn build
```

This command creates a `build` directory with a production build of the app.

## Docker

A Dockerfile is included for containerization. To build the Docker image, run:

```
docker build -t cnsp-frontend .
```

To run the container:

```
docker run -p 3000:3000 cnsp-frontend
```

The frontend will be accessible at `http://localhost:3000`.
