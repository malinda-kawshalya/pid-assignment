from dataclasses import dataclass

EMOTIONS = ["Happy", "Sad", "Frustrated", "Neutral"]

PROMOTION_RULES = {
    "Happy": {
        "offer": "Loyalty Booster",
        "message": "Enjoy 10% off on your next favorite meal.",
        "discount": 10,
    },
    "Sad": {
        "offer": "Comfort Meal Deal",
        "message": "Here is 15% off on comfort food selections.",
        "discount": 15,
    },
    "Frustrated": {
        "offer": "Service Recovery Voucher",
        "message": "Sorry for the experience. Get LKR 300 off your next order.",
        "discount": 20,
    },
    "Neutral": {
        "offer": "Discovery Offer",
        "message": "Try a new restaurant with 8% off.",
        "discount": 8,
    },
}

FRUSTRATION_KEYWORDS = {
    "late",
    "delay",
    "bad",
    "cold",
    "worst",
    "angry",
    "rude",
    "frustrated",
    "terrible",
    "awful",
}

SAD_KEYWORDS = {
    "sad",
    "upset",
    "disappointed",
    "unhappy",
    "depressed",
}

HAPPY_KEYWORDS = {
    "great",
    "amazing",
    "good",
    "awesome",
    "excellent",
    "delicious",
    "love",
    "happy",
}


@dataclass
class Prediction:
    emotion: str
    confidence: float
