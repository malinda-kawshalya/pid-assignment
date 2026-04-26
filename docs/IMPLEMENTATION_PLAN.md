# PID Implementation Plan (Step-by-Step)

## Project
Emotion-Based Personalized Promotion Recommendation System for food delivery platforms.

## Goal
Build an end-to-end prototype with:
- Emotion classification from text reviews
- Emotion-to-promotion recommendation engine
- Streamlit web interface for live predictions
- BI-style dashboard for trend and campaign monitoring

## Implementation Strategy
Use incremental delivery in 5 phases. Each phase produces a usable output.

## Phase 0 - Foundation (Week 1)
### Tasks
1. Set up repository structure.
2. Create Python environment and install dependencies.
3. Add code modules for preprocessing, classifier, recommendation engine, and dashboard.
4. Add a Streamlit app skeleton.

### Deliverables
- Running Streamlit app with placeholder outputs
- Source structure and README setup guide

### Exit Criteria
- `streamlit run src/app.py` launches successfully.

## Phase 1 - Full Frontend Experience (Week 2)
### Tasks
1. Build modern Streamlit visual identity (custom theme, typography, responsive layout).
2. Implement all frontend views:
   - Overview
   - Live Recommendation
   - Batch Simulation
   - BI Dashboard
   - Promotion Catalog
3. Add rich interaction components (cards, KPIs, charts, expandable rules, downloadable outputs).
4. Add clear user flow from review input to promotion output.

### Deliverables
- Fully styled multi-view web interface
- Frontend-ready UX flow for end-to-end demonstration

### Exit Criteria
- All planned frontend views are functional on desktop and mobile.

## Phase 2 - Data Layer (Week 3)
### Tasks
1. Import public dataset (Kaggle restaurant reviews).
2. Build synthetic Sri Lankan dataset for local context.
3. Merge into one hybrid dataset.
4. Add validation rules for schema and missing values.

### Deliverables
- `data/hybrid_reviews.csv`
- Data dictionary and cleaning logs

### Exit Criteria
- Dataset includes labels and passes validation checks.

## Phase 3 - NLP + Emotion Model (Week 4-5)
### Tasks
1. Build preprocessing pipeline:
   - Lowercasing, punctuation removal, tokenization
   - Stop-word removal
   - Lemmatization
2. Train baseline model (TF-IDF + Logistic Regression).
3. Evaluate against validation split.
4. Save trained pipeline artifact.

### Deliverables
- `artifacts/emotion_model.joblib`
- Metrics report (accuracy, precision, recall, F1)

### Exit Criteria
- Accuracy >= 85% on test split.

## Phase 4 - Recommendation Mapping Engine (Week 6)
### Tasks
1. Define promotion catalog and business rules.
2. Map each emotion to promotion categories.
3. Add confidence-based fallback logic.
4. Add campaign constraints (max discount, validity windows).

### Deliverables
- Rule map in config
- Functional recommendation service used by Streamlit app

### Exit Criteria
- 100% of emotions map to a valid promotion action.

## Phase 5 - Validation + Submission (Week 7)
### Tasks
1. End-to-end testing.
2. Performance and error handling tests.
3. Document limitations, ethics, and privacy controls.
4. Final report screenshots + evidence pack.

### Deliverables
- Final prototype demo
- Testing summary
- Dissertation/report-ready artifacts

### Exit Criteria
- Demo scenario executed successfully with evidence.

## Backlog (Prioritized)
1. Replace heuristic fallback with fine-tuned transformer model.
2. Add Sinhala/Tamil preprocessing.
3. Add A/B testing simulation for campaigns.
4. Integrate with external BI tools (Power BI).

## Risk Controls (from PID)
- Low model accuracy: start with proven baseline model + iterative tuning.
- Proprietary data access: hybrid data strategy.
- Scope creep: lock MVP to core emotion->promotion loop first.

## Definition of Done
- Functional app with real-time recommendation
- Measured model accuracy and response time
- Dashboard with trend insights
- Reproducible setup and documented workflow
