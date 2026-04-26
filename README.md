# Emotion-Based Promotion Recommendation Prototype

This repository contains a step-by-step implementation prototype for your PID project:
- Emotion classification from review text
- Promotion recommendation mapping
- Streamlit web interface
- Basic analytics dashboard

## Quick Start

1. Create and activate virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run app:
   ```bash
   streamlit run src/app.py
   ```

## Client PC Installation

If you are moving the project to a new Windows client PC, follow the step-by-step guide in [docs/CLIENT_INSTALLATION_README.md](docs/CLIENT_INSTALLATION_README.md).

## Project Structure

```text
src/
  app.py
  emotion_promo/
    config.py
    preprocessing.py
    model.py
    recommender.py
    analytics.py

data/
  sample_reviews.csv

docs/
  IMPLEMENTATION_PLAN.md
```

## Current MVP Behavior
- Uses a lightweight hybrid classifier:
  - Trained model if available in `artifacts/emotion_model.joblib`
  - Heuristic fallback if model is unavailable
- Maps emotions to promotion offers through configurable rules
- Tracks in-session events to show trend charts in dashboard

## Next Implementation Steps
Follow `docs/IMPLEMENTATION_PLAN.md` phase-by-phase.
