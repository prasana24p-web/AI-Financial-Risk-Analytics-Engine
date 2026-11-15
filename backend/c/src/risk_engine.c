#include "risk_engine.h"

double compute_risk_score(double volatility, double exposure, double liquidity,
                          double default_probability, double concentration) {
    double score = 0.35 * volatility + 0.25 * exposure + 0.20 * liquidity +
                  0.12 * default_probability + 0.08 * concentration;

    if (score < 0.0) {
        return 0.0;
    }
    if (score > 100.0) {
        return 100.0;
    }

    return score;
}
