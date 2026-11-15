# AI Financial Risk Analytics Engine Final Report

## 1. Executive Summary

The AI Financial Risk Analytics Engine is a prototype platform for assessing portfolio-level financial risk. It combines Python services, a saved scikit-learn Decision Tree model, a native C risk-scoring library, and a browser-based dashboard to evaluate risk across key factors, including market volatility, exposure, liquidity, default likelihood, concentration, and diversification. The current API scoring path uses the Python model; the C library is not invoked by that path.

## 2. Problem Statement

Financial institutions require rapid and reliable portfolio-level risk assessment to support lending, trading, treasury, and capital allocation decisions. Traditional spreadsheets and monitoring tools often lack a scalable analytical engine that can merge structured risk features with actionable outputs.

## 3. Objectives

- Build a modular financial risk analytics solution.
- Use Python for API orchestration and analytics workflows.
- Use C for performance-sensitive risk computations.
- Provide a clean web-based interface for real-time monitoring.
- Include a SQL-ready persistence layer for risk history.
- Deliver a complete, runnable project structure.

## 4. Architecture

- Frontend layer: Streamlit portfolio risk dashboard.
- Python API layer: FastAPI service that validates inputs and orchestrates predictions.
- Model layer: a saved preprocessing and `DecisionTreeRegressor` pipeline.
- C engine layer: native scoring library, not used by the current API scoring path.

## 5. End-to-End Workflow

1. **Dataset:** generate 8,000 synthetic labeled portfolio examples in `data/synthetic_portfolio_risk.csv`.
2. **Preprocessing:** load the CSV feature columns and apply median imputation through a scikit-learn `Pipeline`. Feature scaling is unnecessary for tree-based models.
3. **ML model:** fit a `DecisionTreeRegressor` after splitting training and holdout data; save preprocessing and model together in the joblib artifact.
4. **Risk prediction:** FastAPI loads the saved pipeline, predicts a numeric score, and derives the risk band and alerts.
5. **Streamlit dashboard:** collect portfolio inputs, call the API, and show the prediction, risk indicators, and alerts.

## 6. Risk Model

The Decision Tree model uses the following input features:

- volatility
- exposure
- liquidity stress
- default probability
- concentration
- asset count (diversification)

The model predicts a numeric 0–100 risk score; the application derives the risk band and alerts from that score. The following formula generates the synthetic training targets (the runtime API uses the trained decision tree to predict the score):

$$
R = 0.35V + 0.25E + 0.20L + 0.12D + 0.08C + A
$$

where:

- $V$ = volatility
- $E$ = exposure
- $L$ = liquidity score
- $D$ = default probability
- $C$ = concentration risk
- $A$ = diversification adjustment (5 for fewer than 5 assets, 2.5 for fewer than 10 assets, otherwise 0)

## 7. Model, Training Data, and Saved Artifact

- **Algorithm:** `sklearn.tree.DecisionTreeRegressor` (scikit-learn 1.9.1; maximum depth 20, minimum 3 samples per leaf).
- **Training script:** `backend/python/train_model.py`.
- **Training dataset:** `data/synthetic_portfolio_risk.csv`, generated deterministically with 8,000 examples and random seed 42.
- **Preprocessing:** `SimpleImputer(strategy="median")`, fitted inside the training pipeline; feature scaling is not used because tree models do not require it.
- **Saved model:** `backend/python/models/portfolio_risk_decision_tree.joblib`. The artifact includes the preprocessing/model pipeline, feature order, dataset description, label definition, and holdout metrics.
- **Target labels:** synthetic scores from the weighted formula in this report, with a diversification adjustment of 5 points for fewer than 5 assets or 2.5 points for fewer than 10 assets; scores are bounded to 0–100.
- **Validation:** the training script reports holdout MAE and R², which only measure how well this model approximates those synthetic formula labels.

This is a reproducible ML demonstration, not a model trained on observed market, credit, or portfolio outcomes. The generated examples and reported holdout metrics do not establish real-world predictive validity and should not be used alone for financial decisions. Replace the synthetic dataset and validate/calibrate the model against suitable, legally usable, representative real data before production use.

## 8. Business Value

This engine supports:

- early warning alerts for elevated portfolio risk
- stress scenario evaluation
- stronger risk governance workflows
- data-driven capital allocation decisions
- improved communication between front-office and risk teams

## 9. Implementation Notes

The project includes:

- API endpoint for health checks and portfolio scoring
- C library for high-performance scoring
- SQL schema for saving risk events
- Streamlit analytics dashboard
- pytest-based validation for scoring logic
- Decision Tree training pipeline and persisted model artifact

## 10. Future Expansion

Potential upgrades include:

- training and validating on representative real portfolio outcomes
- Kafka or message queue integration
- AML and fraud analytics modules
- multi-entity financial data ingestion
- cloud deployment with Docker and Kubernetes

## 11. Conclusion

This project demonstrates an end-to-end structure for an AI-powered financial risk analytics platform. It is intentionally designed to be extensible, educational, and production-oriented, while also remaining clean and modular for further development.
