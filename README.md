# Machine Learning in NBA Over/Under Betting

**Business 35137: Machine Learning in Finance**
The University of Chicago Booth School of Business (January - March 2026)

**Team:** Alan Donnelly, Andrew McLaughlin, Robert Asgeirsson, Chris Mulligan

---

## Overview

This project investigates whether machine learning models can identify exploitable inefficiencies in NBA over/under (total points) betting markets. The Vegas line is set by professional oddsmakers and is widely regarded as the most efficient public forecast of game outcomes. To be profitable at standard -110 odds, a model must win more than **52.4%** of bets.

We train six model classes on 11 NBA seasons of walk-forward backtesting, then evaluate a prospectively nominated strategy on a fully held-out 2024/25 season that was never used in any modeling decision.

---

## Key Results

| Model | Base Accuracy | Best Selective Accuracy | Selective ROI |
|---|---|---|---|
| Lasso | 52.0% | 53.4% (≥2.0 threshold, 4,529 bets) | +1.9% |
| ElasticNet | 52.0% | 53.7% (≥4.0 threshold, 1,896 bets) | +2.2% |
| Ridge | 51.7% | 55.0% (≥4.5 threshold, 826 bets) | +5.4% |
| PCR | 51.4% | 52.1% (≥2.5 threshold, 5,126 bets) | +0.6% |
| XGBoost | 50.7% | Never profitable | — |
| RBF+Ridge | 50.9% | Never profitable | — |

**Holdout (2024/25 season):** The prospectively nominated Lasso Flat 2% strategy placed 256 bets, achieving **53.1% accuracy** and growing a $10,000 bankroll to **$10,727 (+7.3%)** — vs. the S&P 500's +3.7% over the same period.

Simple linear models consistently outperform complex alternatives. XGBoost shows a 2.3-point train-vs-OOS RMSE gap, confirming overfitting. In a low-signal efficient market, model flexibility is a liability, not an asset.

---

## Methodology

### Data
- **Betting data:** ~23,000 NBA games (2007/08–2024/25) with Vegas total lines and final scores
- **Box score data:** Team-level game statistics from the NBA Stats API and a historical archive
- **Hold-out:** The entire 2024/25 season (1,293 games) was withheld from all modeling decisions

### Feature Engineering
114 features organized into seven categories: Vegas line features, totals/scoring, shooting efficiency, rebounding/hustle, playmaking, schedule/rest, and interaction terms. All features are strictly **lagged** using a `shift(1)` operation — no future data ever enters a prediction.

### Walk-Forward Backtesting
For each of 11 test seasons (2013/14–2023/24), models are trained on all prior seasons and predict the next. Hyperparameters are tuned via 5-fold `TimeSeriesSplit` within the training window, optimizing betting accuracy rather than RMSE. Exponential recency weighting (tuned half-life) allows models to adapt to the NBA's evolving pace without manual intervention.

### Selective Betting
Bets are filtered to games where the model's prediction deviates most from the Vegas line. Thresholds are swept from 0.5 to 20 points; valid thresholds require ≥300 total bets and ≥10 bets in every individual season.

### Bankroll Simulation
Ten sizing rules are stress-tested — from conservative flat amounts to full Kelly and fractional Kelly variants — across all 11 backtest seasons starting from a $10,000 bankroll.

### Statistical Validation
Wilson score confidence intervals, block bootstrap, Bonferroni-corrected p-values, and McNemar's paired test for pairwise model comparison.

---

## Real-World Viability

Despite a genuine statistical edge, practical deployment faces three hard constraints:

1. **Slippage:** Break-even slippage is ~0.5 points — the lower bound of typical NBA line movement. Modest execution delays can eliminate the edge entirely.
2. **Market depth:** Sportsbook limits cap deployable capital at ~$2.5M; a $10,000 bankroll generates ~$188/year in expected profit.
3. **Account restrictions:** Sportsbooks flag winning accounts within 1–3 seasons. The strategy's volume and CLV pattern would likely trigger limits before the edge compounds meaningfully.

---

## Repository Structure

```
├── nba_betting_ml_analysis.ipynb   # Main analysis notebook (walk-forward backtest, all figures)
├── scrape_nba_data.py              # Data collection script (NBA Stats API, no auth required)
├── Data/
│   ├── Betting Data/
│   │   └── nba_2008-2025.csv       # Vegas lines and scores, 18 seasons
│   └── Game Data/                  # NBA box score CSVs (historical archive + API pulls)
├── Images/                         # All 16 analysis figures
├── Writeup_Chris.pdf               # Final paper
├── Writeup_Chris_Latex.tex         # LaTeX source
└── Presentation_Robert.pptx        # Class presentation
```

---

## Reproducing the Analysis

All data is included in the repo. To re-run the notebook:

```bash
pip install pandas numpy scikit-learn xgboost nba_api matplotlib seaborn scipy
jupyter notebook nba_betting_ml_analysis.ipynb
```

To refresh the 2024/25 season data from the NBA Stats API:

```bash
pip install nba_api
python scrape_nba_data.py
```

No API keys or authentication required.

---

## Conclusions

The evidence is consistent with **semi-strong market efficiency**: publicly available box score statistics are largely priced into the Vegas line. A small, statistically significant residual edge exists ($p < 0.001$ after Bonferroni correction), but the gap between statistical significance and economic viability is the defining challenge of applied ML in efficient markets. The project demonstrates that model accuracy and profitability are fundamentally different questions.
