import os

import httpx
import streamlit as st


st.set_page_config(
    page_title="Portfolio Risk | Risk Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #13243a;
        --muted: #718096;
        --line: #e4eaf2;
        --accent: #176b5b;
        --surface: #ffffff;
        --canvas: #f3f6fa;
    }

    .stApp {
        background: var(--canvas);
        color: var(--ink);
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--canvas);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(243, 246, 250, 0.94);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: #ffffff;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: var(--ink) !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--muted);
    }

    [data-testid="stNumberInput"] input {
        background: #ffffff !important;
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        opacity: 1 !important;
    }

    h1, h2, h3 {
        color: var(--ink);
        font-family: 'Segoe UI', Arial, sans-serif;
        letter-spacing: -0.04em;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1440px;
        padding-top: 4rem;
    }

    .brand-bar {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0 0 1.6rem;
        border-bottom: 1px solid var(--line);
        margin-bottom: 1.8rem;
    }

    .brand-mark {
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        border-radius: 12px;
        background: #12392f;
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 700;
    }

    .brand-name {
        color: var(--ink);
        font-size: 0.84rem;
        font-weight: 800;
        letter-spacing: 0.09em;
        line-height: 1.25;
        margin: 0;
    }

    .brand-detail {
        color: var(--muted);
        font-size: 0.65rem;
        letter-spacing: 0.12em;
        line-height: 1.25;
        margin: 3px 0 0;
        text-transform: uppercase;
        white-space: nowrap;
    }

    .workspace-status {
        margin-left: auto;
        border: 1px solid #d5e8e1;
        border-radius: 999px;
        padding: 6px 9px;
        background: #f1f8f5;
        color: #176b5b;
        font-size: 0.68rem;
        font-weight: 700;
        white-space: nowrap;
    }

    .workspace-status span {
        color: #1c9a72;
        margin-right: 6px;
    }

    .page-title {
        color: var(--ink);
        font-size: clamp(2rem, 3vw, 2.7rem);
        font-weight: 750;
        letter-spacing: -0.055em;
        line-height: 1.1;
        margin: 0;
    }

    .page-subtitle {
        color: var(--muted);
        font-size: 1rem;
        margin: 0.65rem 0 1.5rem;
    }

    .section-heading {
        color: var(--ink);
        font-size: 1.16rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin: 1.8rem 0 0.35rem;
    }

    .section-caption {
        color: var(--muted);
        font-size: 0.88rem;
        margin: 0 0 1rem;
    }

    .score-card {
        position: relative;
        overflow: hidden;
        min-height: 186px;
        background: linear-gradient(120deg, #102d29 0%, #16473d 100%);
        border: 1px solid #214f45;
        border-radius: 16px;
        padding: 1.45rem 1.6rem 1.3rem;
        margin: 0.2rem 0 1.25rem;
        box-shadow: 0 12px 30px rgba(19, 53, 46, 0.14);
    }

    .score-card::after {
        content: "";
        position: absolute;
        width: 210px;
        height: 210px;
        right: -80px;
        top: -110px;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 50%;
        box-shadow: 0 0 0 22px rgba(255,255,255,0.035), 0 0 0 45px rgba(255,255,255,0.025);
    }

    .score-card.low { background: linear-gradient(120deg, #102d29, #176b5b); }
    .score-card.moderate { background: linear-gradient(120deg, #3c3017, #795315); border-color: #87631f; }
    .score-card.high, .score-card.severe { background: linear-gradient(120deg, #3b2022, #8b3437); border-color: #934246; }

    .score-topline {
        position: relative;
        z-index: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
    }

    .score-label {
        color: rgba(255,255,255,0.75);
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .score-status {
        color: #ffffff;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 999px;
        padding: 6px 10px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .score-value {
        position: relative;
        z-index: 1;
        color: #ffffff;
        font-size: clamp(2.6rem, 4vw, 3.5rem);
        font-weight: 750;
        letter-spacing: -0.06em;
        line-height: 1.15;
        margin: 0.5rem 0 0.1rem;
    }

    .score-band {
        position: relative;
        z-index: 1;
        color: rgba(255,255,255,0.76);
        font-size: 0.88rem;
    }

    .score-meter {
        position: relative;
        z-index: 1;
        height: 5px;
        margin-top: 1rem;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(255,255,255,0.19);
    }

    .score-meter-fill {
        height: 100%;
        border-radius: inherit;
        background: #ffffff;
    }

    .summary-card {
        min-height: 145px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.25rem;
        margin: 0.2rem 0 1.25rem;
        box-shadow: 0 8px 24px rgba(24, 44, 71, 0.04);
    }

    .summary-label {
        color: var(--muted);
        font-size: 0.75rem;
        font-weight: 600;
        white-space: nowrap;
    }

    .summary-value {
        color: var(--ink);
        font-size: clamp(1.05rem, 1.8vw, 1.65rem);
        font-weight: 700;
        letter-spacing: -0.045em;
        line-height: 1.15;
        white-space: nowrap;
    }

    .summary-foot {
        color: #8591a3;
        font-size: 0.76rem;
    }

    .factor-card {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 13px;
        padding: 1rem 1.05rem 0.95rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 5px 16px rgba(24, 44, 71, 0.035);
    }

    .factor-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        margin-bottom: 0.9rem;
    }

    .factor-label {
        color: #526176;
        font-size: 0.83rem;
        font-weight: 600;
    }

    .factor-value {
        color: var(--ink);
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: -0.035em;
    }

    .factor-track {
        height: 5px;
        background: #edf1f5;
        border-radius: 999px;
        overflow: hidden;
    }

    .factor-fill {
        height: 100%;
        background: linear-gradient(90deg, #318b76, #176b5b);
        border-radius: inherit;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: var(--accent) !important;
        border: 1px solid var(--accent);
        border-radius: 9px;
        font-weight: 700;
        min-height: 3rem;
        transition: background 0.15s ease, transform 0.15s ease;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {
        background: #105649 !important;
        border-color: #105649 !important;
        transform: translateY(-1px);
    }

    [data-testid="stSlider"] [role="slider"] {
        border-color: var(--accent) !important;
        background-color: var(--accent) !important;
    }

    [data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: var(--accent) !important;
    }

    [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
        background: var(--accent);
    }

    [data-testid="stAlert"] {
        background: #fff7e8 !important;
        border: 1px solid #f0d7a8 !important;
        border-left: 4px solid #c47b08 !important;
        border-radius: 10px !important;
        margin-bottom: 0.65rem;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"],
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
        color: #633d00 !important;
        -webkit-text-fill-color: #633d00 !important;
        opacity: 1 !important;
    }

    [data-testid="stAlert"] svg {
        fill: #9a5d00 !important;
        color: #9a5d00 !important;
    }

    div.stFormSubmitButton > button,
    div.stFormSubmitButton > button *,
    div.stFormSubmitButton > button p {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }

    [data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 12px;
    }

    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1.25rem 1rem 2rem;
        }

        .workspace-status {
            font-size: 0.67rem;
            padding: 6px 8px;
        }

        .score-card, .summary-card {
            min-height: 155px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

api_url = os.getenv("RISK_API_URL", "http://127.0.0.1:8000").rstrip("/")

with st.sidebar:
    st.markdown("### Portfolio assumptions")
    st.caption("Adjust the inputs and run an updated assessment.")

    with st.form("portfolio-risk-form"):
        portfolio_value = st.number_input(
            "Portfolio value",
            min_value=0.0,
            value=8_500_000.0,
            step=100_000.0,
            format="%.0f",
            help="Total portfolio value in your local currency.",
        )
        volatility = st.slider("Volatility", 0.0, 100.0, 18.5, 0.5, format="%.1f%%")
        exposure = st.slider("Exposure", 0.0, 100.0, 62.0, 0.5, format="%.1f%%")
        liquidity = st.slider("Liquidity stress", 0.0, 100.0, 70.0, 0.5, format="%.1f%%")
        default_probability = st.slider(
            "Default probability", 0.0, 100.0, 15.0, 0.5, format="%.1f%%"
        )
        concentration = st.slider(
            "Concentration", 0.0, 100.0, 58.0, 0.5, format="%.1f%%"
        )
        asset_count = st.number_input(
            "Number of assets",
            min_value=1,
            value=12,
            step=1,
        )
        submitted = st.form_submit_button(
            "Run risk analysis",
            type="primary",
            use_container_width=True,
        )

st.markdown(
    """
    <div class="brand-bar">
        <div class="brand-mark">R</div>
        <div class="brand-copy">
            <div class="brand-name">RISK INTELLIGENCE</div>
            <div class="brand-detail">Portfolio analytics</div>
        </div>
        <div class="workspace-status"><span>●</span> Monitoring workspace</div>
    </div>
    <h1 class="page-title">Portfolio overview</h1>
    <p class="page-subtitle">Monitor exposure, identify emerging risk signals, and review portfolio health.</p>
    """,
    unsafe_allow_html=True,
)

workflow_columns = st.columns(5)
workflow_steps = [
    ("1. Dataset", "Synthetic portfolio examples"),
    ("2. Preprocessing", "Median imputation"),
    ("3. ML model", "Decision Tree"),
    ("4. Risk prediction", "Score, band, and alerts"),
    ("5. Dashboard", "Streamlit results"),
]
for column, (step, description) in zip(workflow_columns, workflow_steps):
    column.markdown(f"**{step}**")
    column.caption(description)

if submitted:
    payload = {
        "portfolio_value": portfolio_value,
        "volatility": volatility,
        "exposure": exposure,
        "liquidity": liquidity,
        "default_probability": default_probability,
        "concentration": concentration,
        "asset_count": asset_count,
        "scenario": "streamlit_dashboard",
    }
    try:
        response = httpx.post(
            f"{api_url}/api/risk/portfolio",
            json=payload,
            timeout=10.0,
        )
        response.raise_for_status()
        st.session_state["risk_result"] = response.json()
    except httpx.HTTPStatusError as error:
        st.session_state.pop("risk_result", None)
        st.error(f"Risk API returned HTTP {error.response.status_code}. Check the submitted values and API logs.")
    except httpx.RequestError as error:
        st.session_state.pop("risk_result", None)
        st.error(f"Could not reach the risk API at {api_url}: {error}")
    except ValueError as error:
        st.session_state.pop("risk_result", None)
        st.error(f"The risk API returned an invalid response: {error}")

result = st.session_state.get("risk_result")
if result is None:
    st.info("Enter portfolio inputs in the sidebar and run an analysis to view the risk assessment.")
else:
    risk_score = float(result["risk_score"])
    risk_band = str(result["risk_band"])
    risk_class = risk_band.lower() if risk_band.lower() in {"low", "moderate", "high", "severe"} else "moderate"
    alerts = result["alerts"]
    score_percent = min(100, max(0, risk_score))

    st.markdown(
        f"""
        <div class="score-card {risk_class}">
            <div class="score-topline">
                <div class="score-label">Composite portfolio risk</div>
                <div class="score-status">{risk_band} risk</div>
            </div>
            <div class="score-value">{risk_score:.2f}<span style="font-size: 1rem; color: rgba(255,255,255,.72); font-weight: 500; letter-spacing: 0;"> / 100</span></div>
            <div class="score-band">{result["alert_level"]} alert level · Based on submitted portfolio indicators</div>
            <div class="score-meter"><div class="score-meter-fill" style="width: {score_percent:.2f}%;"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(3, gap="medium")
    metric_values = [
        ("Portfolio value", f"{result['portfolio_value']:,.0f}", "Assessed AUM"),
        ("Assets", f"{result['asset_count']:,}", "Positions monitored"),
        ("Risk signals", f"{len(alerts):,}", "Items for review"),
    ]
    for column, (label, value, footnote) in zip(metric_columns, metric_values):
        column.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">{label}</div>
                <div class="summary-value">{value}</div>
                <div class="summary-foot">{footnote}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-heading">Risk alerts</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Signals that may need portfolio or liquidity review.</div>',
        unsafe_allow_html=True,
    )
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("No material alerts identified for the submitted portfolio.")

    st.markdown('<div class="section-heading">Risk indicators</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Current portfolio inputs used in the composite assessment.</div>',
        unsafe_allow_html=True,
    )
    factors = [
        ("Volatility", result["volatility"]),
        ("Exposure", result["exposure"]),
        ("Liquidity stress", result["liquidity"]),
        ("Default probability", result["default_probability"]),
        ("Concentration", result["concentration"]),
    ]
    for row_start in range(0, len(factors), 2):
        factor_columns = st.columns(2)
        for column, (label, value) in zip(factor_columns, factors[row_start : row_start + 2]):
            factor_percent = min(100, max(0, float(value)))
            column.markdown(
                f"""
                <div class="factor-card">
                    <div class="factor-head">
                        <span class="factor-label">{label}</span>
                        <span class="factor-value">{float(value):.1f}%</span>
                    </div>
                    <div class="factor-track">
                        <div class="factor-fill" style="width: {factor_percent:.1f}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander("Scoring methodology"):
        st.write(result["methodology"])
        st.caption(
            f"Model: {result['algorithm']} · Preprocessing: {result['preprocessing']} · "
            f"Dataset: {result['training_dataset']} · "
            f"Saved artifact: {result['saved_artifact']}. Training data is synthetic "
            "and is not validated against real financial outcomes."
        )
