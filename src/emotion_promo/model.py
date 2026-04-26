from __future__ import annotations

from pathlib import Path
from typing import Optional

import joblib
from textblob import TextBlob

from .config import FRUSTRATION_KEYWORDS, HAPPY_KEYWORDS, Prediction, SAD_KEYWORDS
from .preprocessing import clean_text


class EmotionClassifier:
    """Hybrid classifier: model artifact first, heuristic fallback second."""

    def __init__(self, model_path: str = "artifacts/emotion_model.joblib") -> None:
        self.model_path = Path(model_path)
        self.model = self._load_model()

    def _load_model(self) -> Optional[object]:
        if self.model_path.exists():
            return joblib.load(self.model_path)
        return None

    def predict(self, text: str) -> Prediction:
        normalized = clean_text(text)

        if self.model is not None:
            label = self.model.predict([normalized])[0]
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba([normalized])[0]
                confidence = float(max(probabilities))
            else:
                confidence = 0.8
            return Prediction(emotion=str(label), confidence=round(confidence, 3))

        return self._heuristic_predict(normalized)

    def _heuristic_predict(self, text: str) -> Prediction:
        tokens = set(text.split())

        if tokens & FRUSTRATION_KEYWORDS:
            return Prediction(emotion="Frustrated", confidence=0.82)

        if tokens & SAD_KEYWORDS:
            return Prediction(emotion="Sad", confidence=0.78)

        if tokens & HAPPY_KEYWORDS:
            return Prediction(emotion="Happy", confidence=0.80)

        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2:
            return Prediction(emotion="Happy", confidence=0.72)
        if polarity < -0.2:
            return Prediction(emotion="Frustrated", confidence=0.72)

        return Prediction(emotion="Neutral", confidence=0.65)
