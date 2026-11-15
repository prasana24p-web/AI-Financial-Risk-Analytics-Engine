from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import joblib
from sklearn import __version__ as sklearn_version
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor

from app.config import MODEL_PATH
from app.models import PortfolioInput
from app.synthetic_data import FEATURE_NAMES


@dataclass
class RiskResult:
    risk_score: float
    risk_band: str
    alert_level: str
    alerts: list[str]
    methodology: str
    algorithm: str
    preprocessing: str
    training_dataset: str
    saved_artifact: str


@lru_cache(maxsize=1)
def _load_model_bundle() -> dict[str, Any]:
    if not MODEL_PATH.is_file():
        raise RuntimeError(
            f"Trained risk model not found at {MODEL_PATH}. "
            "Run `python backend/python/train_model.py` from the project root."
        )

    bundle = joblib.load(MODEL_PATH)
    if not isinstance(bundle, dict):
        raise RuntimeError(f"Trained risk model bundle at {MODEL_PATH} is invalid.")
    if bundle.get("scikit_learn_version") != sklearn_version:
        raise RuntimeError(
            f"Trained risk model at {MODEL_PATH} requires scikit-learn "
            f"{bundle.get('scikit_learn_version')}; installed version is {sklearn_version}. "
            "Install the project's pinned requirements or retrain the model."
        )
    if bundle.get("feature_names") != FEATURE_NAMES:
        raise RuntimeError(
            f"Trained risk model features in {MODEL_PATH} do not match this application."
        )
    pipeline = bundle.get("pipeline")
    if not isinstance(pipeline, Pipeline):
        raise RuntimeError(f"Trained risk model at {MODEL_PATH} has no preprocessing pipeline.")
    if not isinstance(pipeline.named_steps.get("preprocessing"), SimpleImputer):
        raise RuntimeError(
            f"Trained risk model at {MODEL_PATH} has an unsupported preprocessing step."
        )
    if not isinstance(pipeline.named_steps.get("model"), DecisionTreeRegressor):
        raise RuntimeError(
            f"Trained risk model at {MODEL_PATH} is not a DecisionTreeRegressor."
        )
    return bundle


def _band_for_score(score: float) -> str:
    if score <= 35:
        return "Low"
    if score <= 60:
        return "Moderate"
    if score <= 80:
        return "High"
    return "Severe"


def _compute_alerts(score: float, metrics: PortfolioInput) -> list[str]:
    alerts: list[str] = []

    if score >= 70:
        alerts.append("Portfolio risk exceeds the elevated threshold and requires escalation.")
    if metrics.volatility >= 65:
        alerts.append("Volatility is elevated relative to the risk appetite.")
    if metrics.exposure >= 60:
        alerts.append("Balance sheet exposure concentration is materially high.")
    if metrics.liquidity >= 70:
        alerts.append("Liquidity stress may impair timely risk mitigation.")
    if metrics.default_probability >= 50:
        alerts.append("Counterparty default probability is elevated.")
    if metrics.concentration >= 65:
        alerts.append("Concentration risk may amplify losses under adverse conditions.")
    if metrics.asset_count <= 3:
        alerts.append("Portfolio diversification is weak and should be reviewed.")

    return alerts


def _predict_risk_score(metrics: PortfolioInput) -> float:
    bundle = _load_model_bundle()
    features = {
        "volatility": float(metrics.volatility),
        "exposure": float(metrics.exposure),
        "liquidity": float(metrics.liquidity),
        "default_probability": float(metrics.default_probability),
        "concentration": float(metrics.concentration),
        "asset_count": float(metrics.asset_count),
    }
    values = [[features[name] for name in FEATURE_NAMES]]
    prediction = bundle["pipeline"].predict(values)[0]
    return round(max(0.0, min(100.0, float(prediction))), 2)


def calculate_risk_score(metrics: PortfolioInput) -> RiskResult:
    bundle = _load_model_bundle()
    risk_score = _predict_risk_score(metrics)
    band = _band_for_score(risk_score)
    alerts = _compute_alerts(risk_score, metrics)
    alert_level = "Critical" if risk_score >= 80 else "High" if risk_score >= 60 else "Moderate" if risk_score >= 35 else "Low"

    return RiskResult(
        risk_score=risk_score,
        risk_band=band,
        alert_level=alert_level,
        alerts=alerts,
        methodology=(
            "DecisionTreeRegressor prediction using volatility, exposure, liquidity, "
            "default probability, concentration, and asset count. It was trained on "
            "synthetic examples labeled with the project's weighted-risk formula; "
            "it has not been validated on real financial data."
        ),
        algorithm=bundle["algorithm"],
        preprocessing=bundle["preprocessing"],
        training_dataset=bundle["training_dataset"],
        saved_artifact=MODEL_PATH.name,
    )


def compute_portfolio_risk(payload: PortfolioInput) -> dict[str, Any]:
    result = calculate_risk_score(payload)
    return {
        "portfolio_value": payload.portfolio_value,
        "volatility": payload.volatility,
        "exposure": payload.exposure,
        "liquidity": payload.liquidity,
        "default_probability": payload.default_probability,
        "concentration": payload.concentration,
        "asset_count": payload.asset_count,
        "scenario": payload.scenario,
        "risk_score": result.risk_score,
        "risk_band": result.risk_band,
        "alert_level": result.alert_level,
        "alerts": result.alerts,
        "methodology": result.methodology,
        "algorithm": result.algorithm,
        "preprocessing": result.preprocessing,
        "training_dataset": result.training_dataset,
        "saved_artifact": result.saved_artifact,
    }
