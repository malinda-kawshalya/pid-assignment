# Emotion-Based Promotion Recommendation Prototype

This repository contains the full end-to-end implementation for the Emotion-Based Promotion Recommendation System:
- Emotion classification from review text via a dual-model architecture (Baseline/TextBlob and Fine-Tuned BERT).
- Dynamic emotion-to-promotion recommendation mapping engine.
- Modern, interactive Streamlit web interface (Live, Batch, Dashboard).
- Fast and scalable FastAPI backend for Deep Learning inference.
- Business intelligence analytics dashboard.

## Quick Start

1. **Backend Engine (BERT)**:
   Navigate to the `Backend/` folder, ensure model weights are present, and run via Docker:
   ```bash
   cd Backend
   docker build -t restaurant-bert-api .
   docker run -p 8000:8000 restaurant-bert-api
   ```
2. **Frontend Application (Streamlit)**:
   In a new terminal, activate a virtual environment, install dependencies, and run:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or .\.venv\Scripts\Activate.ps1 on Windows
   pip install -r requirements.txt
   streamlit run src/app.py
   ```

## Client PC Installation

If you are moving the project to a new Windows client PC, follow the step-by-step guide in [docs/CLIENT_INSTALLATION_README.md](docs/CLIENT_INSTALLATION_README.md).

## Project Structure

```text
Backend/
  app.py                 # FastAPI backend for BERT inference
  Dockerfile
  model/                 # Fine-tuned model weights (requires manual download)

src/
  app.py                 # Main Streamlit Frontend Application
  train_model.py         # Script to train the baseline Logistic Regression model
  emotion_promo/
    config.py            # Rules and keywords for emotions and promotions
    preprocessing.py     # Text cleaning utilities
    model.py             # Baseline emotion classifier
    recommender.py       # Recommendation mapping logic
    analytics.py         # Session event storage for BI

data/
  sample_reviews.csv

docs/
  CLIENT_INSTALLATION_README.md
  IMPLEMENTATION_PLAN.md
  REPORT_DOCUMENTATION.md # Comprehensive documentation for report writing
```

## Current MVP Behavior
- Uses a lightweight hybrid classifier:
  - Trained model if available in `artifacts/emotion_model.joblib`
  - Heuristic fallback if model is unavailable
- Maps emotions to promotion offers through configurable rules
- Tracks in-session events to show trend charts in dashboard

## Next Implementation Steps
Follow `docs/IMPLEMENTATION_PLAN.md` phase-by-phase.
