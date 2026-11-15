#ifndef RISK_ENGINE_H
#define RISK_ENGINE_H

#ifdef __cplusplus
extern "C" {
#endif

double compute_risk_score(double volatility, double exposure, double liquidity,
                          double default_probability, double concentration);

#ifdef __cplusplus
}
#endif

#endif
