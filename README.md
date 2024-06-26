[![CodeFactor](https://www.codefactor.io/repository/github/sadeshs/cnsp/badge)](https://www.codefactor.io/repository/github/sadeshs/cnsp)

# Customer-wise Next Shopping Cart Predictor (CNSP)

## Overview

The CNSP app is designed to predict the contents of a customer's next shopping cart based on historical shopping data. This project is split into two main components: a React-based frontend and a FastAPI-powered backend.

### Architecture

- **Frontend**: Built with React and utilizes Material UI (MUI) for the design framework.
- **Backend**: Developed with FastAPI, it includes two prediction models. The first model uses KNN-DTW for item prediction, based on previous work by [Mathias Kraus](https://github.com/MathiasKraus/MarketBasket). The second model for quantity prediction is built with Meta's Prophet.
- **Model**: Model can be found at [https://github.com/CNSP-FYP-Sadesh/model](https://github.com/CNSP-FYP-Sadesh/model)

## Dockerization

The project is fully dockerized with separate Dockerfiles for the frontend and backend. A Docker Compose file is available in the root directory for easy setup and deployment.

## Hosting

- **Frontend**: Hosted on Firebase at [https://cnsp-fyp.web.app/](https://cnsp-fyp.web.app/)
- **Backend**: Deployed on Google Cloud Run, accessible at [https://cnsp-backend-service-qsw77nkhea-uc.a.run.app/api](https://cnsp-backend-service-qsw77nkhea-uc.a.run.app/api)

## Getting Started

To run the project locally, ensure Docker and Docker Compose are installed on your system. Then, clone this repository and from the root directory, run:

```
docker-compose up --build
```

This command builds and starts both the frontend and backend services. You can access the frontend on `localhost:3000` and the backend on `localhost:8080` by default, unless configured otherwise.

For more detailed information on each component, refer to the respective README.md files in the `frontend` and `backend` directories.
