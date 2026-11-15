CREATE TABLE IF NOT EXISTS risk_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_value REAL NOT NULL,
    volatility REAL NOT NULL,
    exposure REAL NOT NULL,
    liquidity REAL NOT NULL,
    default_probability REAL NOT NULL,
    concentration REAL NOT NULL,
    asset_count INTEGER NOT NULL,
    scenario TEXT DEFAULT 'baseline',
    risk_score REAL NOT NULL,
    risk_band TEXT NOT NULL,
    alert_level TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active_version TEXT NOT NULL,
    methodology TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
