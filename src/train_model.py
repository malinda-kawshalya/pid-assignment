from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from emotion_promo.preprocessing import clean_text


def train_model(input_csv: str, output_path: str = "artifacts/emotion_model.joblib") -> None:
    df = pd.read_csv(input_csv)

    required = {"review", "emotion"}
    if not required.issubset(df.columns):
        raise ValueError("Training CSV must contain 'review' and 'emotion' columns")

    df = df.dropna(subset=["review", "emotion"]).copy()
    df["review"] = df["review"].astype(str).map(clean_text)

    x_train, x_test, y_train, y_test = train_test_split(
        df["review"],
        df["emotion"],
        test_size=0.2,
        random_state=42,
        stratify=df["emotion"],
    )

    model = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    print(classification_report(y_test, predictions))

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_file)
    print(f"Saved model to {output_file}")


if __name__ == "__main__":
    # Example:
    # python src/train_model.py data/hybrid_reviews.csv
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="Path to training data CSV")
    parser.add_argument("--output", default="artifacts/emotion_model.joblib")
    args = parser.parse_args()

    train_model(args.input_csv, args.output)
