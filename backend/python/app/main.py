from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import PortfolioInput, RiskAnalysisResponse
from app.risk_engine import compute_portfolio_risk

app = FastAPI(title="AI Financial Risk Analytics Engine API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AI Financial Risk Analytics Engine"}


@app.post("/api/risk/portfolio", response_model=RiskAnalysisResponse)
def analyze_portfolio(payload: PortfolioInput):
    result = compute_portfolio_risk(payload)
    return RiskAnalysisResponse(**result)
