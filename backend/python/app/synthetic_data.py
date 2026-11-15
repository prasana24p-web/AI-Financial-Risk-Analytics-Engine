FEATURE_NAMES = (
    "volatility",
    "exposure",
    "liquidity",
    "default_probability",
    "concentration",
    "asset_count",
)


def synthetic_risk_target(features: dict[str, float | int]) -> float:
    diversification_adjustment = 0.0
    if features["asset_count"] < 5:
        diversification_adjustment = 5.0
    elif features["asset_count"] < 10:
        diversification_adjustment = 2.5

    score = (
        float(features["volatility"]) * 0.35
        + float(features["exposure"]) * 0.25
        + float(features["liquidity"]) * 0.20
        + float(features["default_probability"]) * 0.12
        + float(features["concentration"]) * 0.08
        + diversification_adjustment
    )
    return round(max(0.0, min(100.0, score)), 2)
