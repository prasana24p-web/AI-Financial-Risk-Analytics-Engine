from app.models import PortfolioInput, RiskAnalysisResponse
from app.risk_engine import calculate_risk_score, compute_portfolio_risk


def test_calculate_risk_score_low_risk():
    payload = PortfolioInput(
        portfolio_value=1000000,
        volatility=20,
        exposure=15,
        liquidity=25,
        default_probability=10,
        concentration=12,
        asset_count=10,
    )
    result = calculate_risk_score(payload)
    assert result.risk_score > 0
    assert result.risk_band in {"Low", "Moderate"}
    assert result.algorithm == "DecisionTreeRegressor"
    assert result.preprocessing == "SimpleImputer(strategy='median')"
    assert result.training_dataset == "data/synthetic_portfolio_risk.csv"
    assert result.saved_artifact == "portfolio_risk_decision_tree.joblib"
    assert "synthetic" in result.methodology
    response = RiskAnalysisResponse(**compute_portfolio_risk(payload))
    assert response.algorithm == "DecisionTreeRegressor"
    assert response.preprocessing == "SimpleImputer(strategy='median')"


def test_calculate_risk_score_high_risk():
    payload = PortfolioInput(
        portfolio_value=25000000,
        volatility=80,
        exposure=75,
        liquidity=80,
        default_probability=65,
        concentration=70,
        asset_count=3,
    )
    result = calculate_risk_score(payload)
    assert result.risk_band in {"High", "Severe"}
    assert result.alert_level in {"High", "Critical"}
