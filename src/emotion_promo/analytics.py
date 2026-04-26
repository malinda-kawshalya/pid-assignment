from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import List

import pandas as pd


class SessionEventStore:
    """In-memory event store for dashboard analytics during a Streamlit session."""

    def __init__(self) -> None:
        self._events: List[dict] = []

    def add_event(self, review: str, emotion: str, confidence: float, offer: str, discount: int) -> None:
        self._events.append(
            {
                "timestamp": datetime.now(),
                "review": review,
                "emotion": emotion,
                "confidence": confidence,
                "offer": offer,
                "discount": discount,
            }
        )

    def to_frame(self) -> pd.DataFrame:
        if not self._events:
            return pd.DataFrame(
                columns=["timestamp", "review", "emotion", "confidence", "offer", "discount"]
            )
        return pd.DataFrame(self._events)
