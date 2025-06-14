# Network Security System - Phishing URL Detection

This project aims to build an end-to-end machine learning system to detect phishing URLs, leveraging modern MLOps practices and cloud infrastructure. It demonstrates how modular programming, CI/CD automation, and scalable serving can be used to deploy and monitor ML models in production.

---

## Overview

Phishing is a serious threat in the cybersecurity domain, often executed through deceptive URLs that mimic legitimate websites. This project develops and serves a machine learning model capable of classifying whether a URL is **legitimate** or **phishing**.

The project follows a modular and scalable architecture, adopting MLOps practices including experiment tracking, automated deployments, and cloud-based model serving using FastAPI.

---

## Key Features

- **Phishing URL classification** using supervised machine learning.
- **Modular architecture**: Components are separated by concern (data ingestion, transformation, training, evaluation, etc.).
- **MLOps integration** with MLflow and DagsHub for tracking experiments and model versions.
- **Containerized deployment** with Docker and Azure Container Registry.
- **CI/CD pipeline** using GitHub Actions to automate testing and deployment.
- **FastAPI-based model server** deployed on an Azure Virtual Machine.
- **Experiment tracking and lineage** with DagsHub MLflow UI.

---

## Tech Stack

| Category            | Tools / Technologies                                 |
|---------------------|------------------------------------------------------|
| Programming         | Python                                               |
| Machine Learning    | scikit-learn                                         |
| Web Framework       | FastAPI                                              |
| MLOps               | MLflow, DagsHub                                      |
| CI/CD               | GitHub Actions                                       |
| Containerization    | Docker                                               |
| Cloud Infrastructure| Azure Container Registry, Azure Virtual Machine     |

---

## Key Steps in the Pipeline

1. **Data Ingestion**
   Load static dataset (a .csv file) containing labeled phishing and legitimate URLs.

2. **Data Transformation**
   Perform necessary preprocessing from the dataset.

3. **Model Training**
   Train multiple models and choose the best one using classification metrics.

4. **Model Tracking**
   Log metrics, parameters, and artifacts using MLflow (backed by DagsHub).

5. **Model Packaging & Deployment**
   Package the model and FastAPI server in a Docker image and push to Azure Container Registry via GitHub Actions.

6. **Serving the Model**
   Automatically deploy the Docker image on an Azure Virtual Machine and serve predictions via FastAPI.

7. **Endpoints**
   - `GET /train`
  Triggers the full training pipeline — including data ingestion, preprocessing, training, and model logging to MLflow.

    - `POST /predict`
  Accepts input in .csv file format containing the testing dataset to classify and returns whether it is a **phishing** or **legitimate** link.

---

## Project Limitations

- **Static and Synthetic Dataset**: The project uses a static tabular dataset consisting of pre-extracted features from URLs. These features (e.g., having_IP_Address, URL_Length, SSLfinal_State) are already encoded, and no dynamic URL parsing or feature engineering is performed in real time.
- No active data pipeline to fetch or retrain on new URLs dynamically.
- Further enhancements can include live scraping, user feedback loop, or integration with threat intelligence APIs.
