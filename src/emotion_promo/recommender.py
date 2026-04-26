from .config import PROMOTION_RULES


def map_emotion_to_promotion(emotion: str) -> dict:
    """Return promotion details for a predicted emotion."""
    return PROMOTION_RULES.get(
        emotion,
        {
            "offer": "Generic Offer",
            "message": "Get 5% off your next order.",
            "discount": 5,
        },
    )
