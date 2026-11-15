import csv
import random
from pathlib import Path

import joblib
from sklearn import __version__ as sklearn_version
from sklearn.tree import DecisionTreeRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from app.config import MODEL_PATH, TRAINING_DATA_PATH
from app.synthetic_data import FEATURE_NAMES, synthetic_risk_target


TRAINING_ROWS = 8000
RANDOM_SEED = 42


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    rows: list[dict[str, float | int]] = []

    for _ in range(TRAINING_ROWS):
        features: dict[str, float | int] = {
            "volatility": round(rng.uniform(0, 100), 2),
            "exposure": round(rng.uniform(0, 100), 2),
            "liquidity": round(rng.uniform(0, 100), 2),
            "default_probability": round(rng.uniform(0, 100), 2),
            "concentration": round(rng.uniform(0, 100), 2),
            "asset_count": rng.randint(1, 100),
        }
        rows.append({**features, "risk_score": synthetic_risk_target(features)})

    TRAINING_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TRAINING_DATA_PATH.open("w", newline="", encoding="utf-8") as data_file:
        writer = csv.DictWriter(data_file, fieldnames=(*FEATURE_NAMES, "risk_score"))
        writer.writeheader()
        writer.writerows(rows)

    with TRAINING_DATA_PATH.open(newline="", encoding="utf-8") as data_file:
        dataset_rows = list(csv.DictReader(data_file))

    x = [[float(row[name]) for name in FEATURE_NAMES] for row in dataset_rows]
    y = [float(row["risk_score"]) for row in dataset_rows]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=RANDOM_SEED
    )

    model_pipeline = Pipeline(
        steps=[
            ("preprocessing", SimpleImputer(strategy="median")),
            (
                "model",
                DecisionTreeRegressor(
                    max_depth=20,
                    min_samples_leaf=3,
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )
    model_pipeline.fit(x_train, y_train)
    predictions = model_pipeline.predict(x_test)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    bundle = {
        "pipeline": model_pipeline,
        "feature_names": FEATURE_NAMES,
        "algorithm": "DecisionTreeRegressor",
        "preprocessing": "SimpleImputer(strategy='median')",
        "scikit_learn_version": sklearn_version,
        "training_dataset": TRAINING_DATA_PATH.relative_to(
            Path(__file__).resolve().parents[2]
        ).as_posix(),
        "training_rows": len(dataset_rows),
        "random_seed": RANDOM_SEED,
        "label_definition": (
            "Weighted formula: 0.35*volatility + 0.25*exposure + "
            "0.20*liquidity + 0.12*default_probability + "
            "0.08*concentration + diversification adjustment."
        ),
        "validation": {
            "mae": float(mean_absolute_error(y_test, predictions)),
            "r2": float(r2_score(y_test, predictions)),
        },
    }
    joblib.dump(bundle, MODEL_PATH)

    print(f"Training rows: {TRAINING_ROWS}")
    print(f"Model: {bundle['algorithm']}")
    print(f"Validation MAE: {bundle['validation']['mae']:.3f}")
    print(f"Validation R2: {bundle['validation']['r2']:.4f}")
    print(f"Dataset saved to: {TRAINING_DATA_PATH}")
    print(f"Model saved to: {MODEL_PATH}")
    print("Dataset labels are synthetic and are not real-world financial outcomes.")


if __name__ == "__main__":
    main()
