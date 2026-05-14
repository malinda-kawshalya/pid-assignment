# System Architecture & Component Documentation

This document provides a comprehensive overview of the Emotion-Based Personalized Promotion Recommendation System. It serves as a technical reference for report writing, detailing the system's architecture, underlying components, integrations, and data flow.

## 1. System Overview

The platform is an intelligent, two-tiered software application designed to help food delivery services dynamically respond to customer feedback. It leverages Natural Language Processing (NLP) to read unstructured text reviews, infer the emotional sentiment of the customer, and autonomously trigger mapped promotional workflows (e.g., dispatching a 20% apology discount to an angry customer).

## 2. High-Level Architecture

The system operates on a decoupled **Client-Server Architecture**:
*   **Presentation & Orchestration Layer (Frontend)**: Built with Python and Streamlit. It manages user interfaces, state management, session-based data analytics, and routing inference requests.
*   **Deep Learning Inference Layer (Backend)**: Built with Python, FastAPI, and PyTorch. It operates as a dedicated microservice for hosting the heavy pre-trained Transformer (BERT) model to ensure rapid inferences without blocking the frontend UI threads.

## 3. Detailed Component Breakdown

### 3.1 Frontend Presentation Layer (`src/app.py`)
The frontend is a rich, interactive web application featuring custom CSS styling and layout injections. It features five primary modular views:
*   **Live Recommendation Studio**: Provides a sandbox for live text input. It calls the active model, retrieves an emotion classification, and displays the mapped offer, dynamic discount rate, and generated copy.
*   **Batch Simulation Lab**: Supports `.csv` upload operations. It iterates over datasets in bulk, processes inferences on an aggregate level, logs events, and provides a downloadable processed dataset.
*   **Business Intelligence Dashboard**: Reads from a custom `SessionEventStore` to generate Plotly-driven interactive visuals (Bar charts for emotion distribution, Pie charts for offer mix, Line graphs for model confidence trends).
*   **Promotion Playbook**: A transparent catalog exposing the internal `PROMOTION_RULES` dictionary for stakeholder review.
*   **System Storyboard**: An educational workflow map illustrating the transition from input layer to actionable output.

### 3.2 Machine Learning Inference Backend (`Backend/app.py`)
To support robust NLP predictions securely and efficiently:
*   **FastAPI Framework**: Exposes a high-performance RESTful API endpoint (`/predict`) configured for JSON-based payloads.
*   **Transformer Model (`BertForSequenceClassification`)**: Hosts a local, fine-tuned BERT model responsible for sequence classification.
*   **Hardware Acceleration**: Actively monitors for CUDA/GPU availability and maps tensors dynamically, ensuring low-latency inference speeds (target < 3 seconds).
*   **Dockerization**: The entire backend is containerized via a `Dockerfile`, abstracting system-level Python dependencies and PyTorch binaries away from the host environment.

### 3.3 Core Business Logic Engine (`src/emotion_promo/`)
The intermediary system bridging AI predictions to business value.
*   **`config.py`**: Defines absolute constants including the `EMOTIONS` vocabulary and the `PROMOTION_RULES` (which binds emotional states to tailored discounts and messaging).
*   **`recommender.py`**: Handles mapping rules and gracefully fails to a generic discovery offer if anomalies arise.
*   **`analytics.py`**: Contains the `SessionEventStore`, a localized pandas-driven memory store holding ephemeral session inputs and outputs to supply the BI Dashboard.

## 4. Data Flow

### Live Inference Data Flow
1.  **Input**: User submits review text via the Streamlit text area.
2.  **Routing**: The app checks `st.session_state` for the chosen model.
3.  **Inference**:
    *   If **TextBlob** is selected, traditional classification executes locally.
    *   If **BERT** is selected, a POST request is transmitted to `http://backend:8000/predict`. The backend tokenizes the text, passes it through BERT, calculates Softmax probabilities, and returns a 1-5 Star Rating and confidence percentage.
4.  **Transformation**: The Streamlit app parses the REST response and maps numeric ratings (e.g., 4-5 Stars) to discrete emotional classes (e.g., "Happy").
5.  **Recommendation Mapping**: The resulting emotion queries the `map_emotion_to_promotion()` function to retrieve the business rule payload.
6.  **Action & Logging**: The UI renders the output securely, and the `SessionEventStore` logs the complete event lifecycle.

## 5. Technology Stack

| Domain | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend Interface** | Streamlit, HTML/CSS | Rapid UI generation and interactive web state. |
| **Web API Framework** | FastAPI, Uvicorn | High-performance async REST API servicing. |
| **Deep Learning** | PyTorch, HuggingFace Transformers | Advanced NLP representation and model serving. |
| **Data Processing** | Pandas | Tabular data manipulation for batch processing. |
| **Data Visualization** | Plotly Express | Dynamic chart generation for BI Dashboard. |
| **Deployment** | Docker | Environment isolation and containerized scaling. |