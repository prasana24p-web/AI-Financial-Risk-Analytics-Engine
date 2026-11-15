from typing import Optional

from pydantic import BaseModel, Field


class PortfolioInput(BaseModel):
    portfolio_value: float = Field(..., ge=0, description="Portfolio value in local currency")
    volatility: float = Field(..., ge=0, le=100, description="Volatility risk indicator")
    exposure: float = Field(..., ge=0, le=100, description="Exposure concentration indicator")
    liquidity: float = Field(..., ge=0, le=100, description="Liquidity stress indicator")
    default_probability: float = Field(..., ge=0, le=100, description="Default probability indicator")
    concentration: float = Field(..., ge=0, le=100, description="Sector or issuer concentration risk")
    asset_count: int = Field(..., ge=1, description="Number of assets in the portfolio")
    scenario: Optional[str] = Field(default="baseline", description="Optional scenario label")


class RiskAnalysisResponse(BaseModel):
    portfolio_value: float
    volatility: float
    exposure: float
    liquidity: float
    default_probability: float
    concentration: float
    asset_count: int
    scenario: str
    risk_score: float
    risk_band: str
    alert_level: str
    alerts: list[str]
    methodology: str
    algorithm: str
    preprocessing: str
    training_dataset: str
    saved_artifact: str
