# Phishing Check - Monolith Architecture

This repository contains the initial monolithic architecture for the Phishing Check application. In this design, the entire system (web server, API logic, ML model loading, and database interaction) runs as a single process.

## 1. Architecture Overview

It uses FastAPI as the web framework, SQLAlchemy for database communication, and Joblib to load a pre-trained Scikit-learn model directly into memory.

![Simple Architecture Diagram](/SimpleArchitecture.drawio.png)

## 2. Core Components & Technologies

- **Application Server (`backend`)**:
  - **Technology:** Python, FastAPI
  - **Purpose:** A single process that handles:
    - Serving the API endpoint (`/api/predict`).
    - Loading the ML model and vectorizer at startup using Joblib.
    - Performing predictions and probability calculations.
    - Interacting with the PostgreSQL database using SQLAlchemy.
    - Saving prediction results to the database.
- **PostgreSQL Database**:
  - **Technology:** PostgreSQL (Local Instance)
  - **Purpose:** Stores the results of each prediction.
- **Machine Learning Model**:
  - **Technology:** Scikit-learn (SVM), Joblib
  - **Purpose:** A pre-trained Support Vector Machine (SVM) model (`svm_model_phishing.joblib`) and its corresponding TfidfVectorizer (`svm_vectorizer_phishing.joblib`) used for classification.

## 3. Request Flow

1.  A client sends a `POST` request with text to `http://localhost:8000/api/predict`.
2.  The FastAPI application receives the request.
3.  The `/api/predict` route handler:
    - Uses the in-memory vectorizer to transform the input text.
    - Uses the in-memory SVM model to predict if it's phishing.
    - Calculates the prediction probability.
    - Creates a `PhishingResult` object.
    - Opens a database session and saves the result to PostgreSQL.
    - Returns the prediction result to the client.

## 4. How to Run (Monolith)

1.  **Database Setup:**
    - Ensure a local PostgreSQL server is running.
    - Create the necessary database.
    - Configure the connection string in `.env.development`.
2.  **ML Models:**
    - Place the `svm_model_phishing.joblib` and `svm_vectorizer_phishing.joblib` files in the `./ml_model/` directory (relative to where `predict.py` expects them).
3.  **Install Dependencies:**
    - Navigate to the `backend` directory.
    - Create a virtual environment (recommended).
    - Run `pip install -r requirements.txt`.
4.  **Run the Server:**
    - Run `uvicorn main:app --reload` (or your preferred Uvicorn command) from the `backend` directory.
5.  **Access:**
    - The API will be available at `http://localhost:8000`.
    - API docs at `http://localhost:8000/docs`.

## 5. Limitations

This monolithic architecture, while simple to start, faced limitations that led to the development of the scalable version:

- **Scalability:** The entire application must be scaled as a single unit, even if only one part (e.g., ML prediction) is the bottleneck.
- **Resource Management:** The web server and ML model compete for the same resources (CPU/Memory).
- **Deployment:** Changes to any part require redeploying the entire application.
- **Resilience:** A failure in one component (e.g., ML model loading) can bring down the entire application.

These limitations prompted the move towards a microservices architecture orchestrated by Kubernetes.
