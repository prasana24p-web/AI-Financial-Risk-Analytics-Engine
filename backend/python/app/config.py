import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = BASE_DIR / "backend"
C_ENGINE_DIR = BACKEND_DIR / "c"
MODEL_PATH = BACKEND_DIR / "python" / "models" / "portfolio_risk_decision_tree.joblib"
TRAINING_DATA_PATH = BASE_DIR / "data" / "synthetic_portfolio_risk.csv"

PROJECT_NAME = "AI Financial Risk Analytics Engine"
API_TITLE = "AI Financial Risk Analytics Engine API"
API_VERSION = "1.0.0"

RISK_LIBRARY_PATH = C_ENGINE_DIR / "build" / ("libriskengine.so" if os.name != "nt" else "riskengine.dll")
