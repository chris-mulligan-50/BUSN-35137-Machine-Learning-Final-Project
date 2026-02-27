# Speaker Script
## Machine Learning in NBA Over/Under Betting
### Business 35137 | Chicago Booth | Winter 2026
---

## Slide 1 — Title Slide [0:00 – 0:30]

> "Good morning/afternoon. We're Alan, Andrew, Robert, and Chris. Today we'll walk you through our final project for Machine Learning in Finance, where we set out to answer a deceptively simple question: can machine learning models beat the Vegas line in NBA over/under betting — and can that edge actually make money?"

*[Click to next slide]*

---

## Slide 2 — Research Question [0:30 – 2:00]

> "First, some quick context. In an over/under bet, the sportsbook sets a total — say 220.5 points — and you bet whether the actual combined score lands over or under that number. The standard odds are minus-110, meaning you risk $110 to win $100. That vig — the sportsbook's commission — means you need to win at least 52.4% of your bets just to break even. Not 50%. 52.4%."

> "The Vegas line itself is set by professional oddsmakers who incorporate everything from team stats and injuries to public betting flow. It's widely considered the single most efficient public forecast of game outcomes. So any model that claims to beat it needs to find a small, repeatable edge that the market has somehow missed."

> "Our approach: we train six different model classes — spanning linear, dimension-reduced, tree-based, and kernel-based methods — using a walk-forward validation scheme on 11 NBA seasons. Then we test our nominated strategy on a completely held-out 2024/25 season that was never used in any modelling decision."

*[Click to next slide]*

---

## Slide 3 — Data and Feature Engineering [2:00 – 3:30]

> "Our dataset covers 18 NBA seasons — about 23,000 games — combining two sources: betting data with Vegas lines, point spreads, and final scores, and NBA box-score statistics with team-level performance metrics."

> "From these raw inputs we engineer 114 features across seven categories. The most important design principle is strict lagging: every rolling average uses a shift-one operation, meaning we only use data that was available before the game was played. No future information ever leaks in."

> "We compute rolling means at two window sizes — last 5 games for short-term form and last 10 for medium-term stability. The 2024/25 season — about 1,300 games — is held out entirely."

> "The figure on screen shows our data coverage by season, the NBA's rising scoring trend over time, and how tightly the Vegas line tracks actual outcomes."

*[Click to next slide]*

---

## Slide 4 — Feature Signal Analysis [3:30 – 4:30]

> "Before training models, we check which features carry the most predictive signal. This bar chart ranks features by their absolute correlation with actual game totals."

> "Vegas-derived features dominate — correlations of 0.55 to 0.65. This makes sense: the Vegas line already incorporates most publicly available information. Our model's job is to find the residual signal that Vegas missed."

> "At the bottom, schedule and rest features show near-zero marginal correlation. They might still matter in combination, which is why we include interaction features like pace-times-pace and spread-times-total to help linear models capture non-additive effects."

*[Click to next slide]*

---

## Slide 5 — Walk-Forward Methodology [4:30 – 6:00]

> "Our evaluation framework is walk-forward backtesting. For each of the 11 test seasons from 2013/14 through 2023/24, the model trains on all available data before that season and predicts the test season. The training set grows by roughly 1,300 games per iteration."

> "Hyperparameters are tuned via 5-fold TimeSeriesSplit within the training set. Critically, we optimise for betting accuracy — not RMSE — because our downstream task is predicting over/under outcomes, not minimising point prediction error."

> "A key innovation is exponential recency weighting controlled by a half-life parameter that's tuned jointly with the model hyperparameters. A half-life of 2 years means a game from 2 years ago gets half the weight of the most recent game. This lets the models adapt to the NBA's evolving pace and scoring trends without us manually specifying a window."

> "We test six model classes: Ridge, Lasso, and ElasticNet as our linear models; PCR for dimensionality reduction; XGBoost as our tree-based model; and RBF+Ridge as our kernel-based model."

*[Click to next slide]*

---

## Slide 6 — Model Comparison: Simple Beats Complex [6:00 – 7:30]

> "This is one of the most important figures in the project. Three panels, left to right."

> "Panel 1: betting accuracy. All six models cluster between 50.7% and 52.0%. The linear models — Ridge at 51.7%, Lasso and ElasticNet at 52.0% — are at the top. XGBoost and RBF+Ridge trail noticeably. The dashed line at 52.4% is break-even, and no model reaches it when betting every game."

> "Panel 2: ROI. All bars are red — negative. Even the best models lose roughly 1% per bet when betting every qualifying game. This is the expected result in an efficient market."

> "Panel 3, the overfitting check: the blue bars are training RMSE, the orange bars are out-of-sample RMSE. For the linear models, the gap is tiny — about 0.4 points. For XGBoost, it's 2.3 points. XGBoost is memorising training patterns that don't generalise. This is a textbook bias-variance tradeoff: in a low-signal environment, model flexibility becomes a liability."

*[Click to next slide]*

---

## Slide 7 — Per-Season Accuracy [7:30 – 8:30]

> "This figure tracks each model's accuracy across the 11 individual test seasons. Two things jump out."

> "First, the volatility. Every model swings between roughly 48% and 55% depending on the year. With only about 1,200 bets per season, random variation alone can shift accuracy by plus or minus 2 percentage points."

> "Second, the linear models move together — their lines overlap substantially because they're extracting similar signal from the same features. Lasso is the most consistent, finishing above 50% in 10 of 11 seasons."

> "The heatmap on the right gives the exact numbers. Green cells are above break-even, red cells are below 50%. No model stays green across all seasons — that's what an efficient market looks like."

*[Click to next slide]*

---

## Slide 8 — Statistical Significance [8:30 – 10:00]

> "With over 11,000 bets per model, we need formal significance testing. We apply four complementary tools: Wilson confidence intervals, two forms of bootstrap resampling, and Bonferroni-corrected p-values."

> "After Bonferroni correction for testing 6 models simultaneously, four survive with significance against 50%: Ridge, Lasso, ElasticNet, and PCR — all with p-values below 0.006. XGBoost fails significance even before correction."

> "But here's the critical nuance: every model's confidence interval includes 52.4%. So we can confidently say these models beat a coin flip, but we cannot conclusively say they beat the break-even threshold with flat betting. This distinction between beating 50% and beating 52.4% is central to the project."

*[Click to next slide]*

---

## Slide 9 — Selective Betting [10:00 – 11:30]

> "Since flat betting isn't profitable, we ask: what if we only bet when the model strongly disagrees with Vegas? We use the absolute difference between the model's prediction and the Vegas total as a confidence measure, and sweep thresholds from 0.5 to 20 points."

> "Four models achieve positive ROI at valid thresholds. Ridge leads at +5.4% ROI with 55% accuracy, but on only 826 bets. Lasso hits +2.1% ROI at 53.4% accuracy on 4,529 bets — a much more statistically reliable sample."

> "The key insight: linear models have a prediction standard deviation of about 2.5 points — they make small, conservative adjustments to the Vegas line. When they strongly disagree, it likely reflects genuine signal. XGBoost has a standard deviation of 6 points — it routinely makes extreme predictions driven by overfitting rather than genuine market mispricing."

*[Click to next slide]*

---

## Slide 10 — Base vs. Selective Performance [11:30 – 12:30]

> "This figure shows the contrast between flat betting and selective betting side by side. The blue bars are base performance; the orange bars are selective."

> "You can see that selective betting lifts accuracy above the break-even threshold for four models. However, the smaller sample sizes from selective betting widen the confidence intervals, so the improvement is suggestive but not yet statistically conclusive above 52.4%."

> "This sets up our next question: if the edge is real, does it survive when we simulate actual bankroll management?"

*[Click to next slide]*

---

## Slide 11 — Bankroll Simulation & Strategy Selection [12:30 – 14:00]

> "We subject all four qualifying models to bankroll simulations with 10 different sizing rules, starting from a $10,000 bankroll. The sizing rules range from conservative flat-dollar amounts to the theoretically optimal Kelly criterion."

> "The heatmap shows the results. Flat $500 bets — betting 5% of the initial bankroll per game — cause bankruptcy for all four models despite their positive edges. Full Kelly achieves the highest growth rate but with extreme drawdowns: 76.6% for Ridge. The sweet spot is fractional Kelly or conservative flat-percentage rules."

> "Now we need to nominate one model and sizing rule for deployment. Using only backtest data — no 2024/25 information — we select Lasso with Flat 2% sizing. Why? Lower maximum drawdown than Ridge, 5.5 times more bets for greater statistical reliability, and a simpler sizing rule that doesn't require estimating win probabilities. This is a prospective decision."

*[Click to next slide]*

---

## Slide 12 — Holdout: 2024/25 Season Results [14:00 – 16:00]

> "Now the moment of truth. We apply the Lasso model with the locked threshold and Flat 2% sizing to the 2024/25 season — data the model has never seen in any form."

> "The results: 256 qualifying bets, 53.1% accuracy. Compare that to the 11-season backtest accuracy of 53.4% — the difference is just 0.3 percentage points. The strategy we nominated before seeing any 2024/25 data performed almost identically on unseen data."

> "The $10,000 bankroll grows to $10,727 — a 7.3% return over the season, with a maximum drawdown of only 15.3%. For context, the S&P 500 returned 3.7% over the same October 2024 to June 2025 window, with much higher volatility and obviously zero-sum correlation."

> "The left panel shows the bankroll trajectory — you can see the gradual climb with some drawdown periods. The right panel shows the cumulative win rate converging toward 53.1%."

> "An important caveat: 256 bets is statistically underpowered. The 95% Wilson confidence interval spans from 47.0% to 59.1%, which includes both 50% and 52.4%. So this is an encouraging result, not a definitive proof."

*[Click to next slide]*

---

## Slide 13 — Real-World Constraints [16:00 – 17:30]

> "Before claiming victory, we stress-test against three real-world frictions."

> "First, execution slippage. If the line moves against us before we place the bet, our edge shrinks. The break-even slippage is approximately 0.5 points — and typical NBA line movement is 0.5 to 1.5 points. So even a modest delay in execution can wipe out the advantage. The chart shows accuracy and ROI degrading as slippage increases, with the grey band marking the typical slippage range."

> "Second, market depth. A $10,000 bankroll at Flat 2% generates only about $188 in expected annual profit. Scaling up helps — at $250,000, expected profit is roughly $4,700 — but sportsbook limits cap the maximum bet at $2,500 to $10,000 per game."

> "Third, and most importantly: account restrictions. Sportsbooks track Closing Line Value — whether you're consistently getting better odds than the final line — and flag winning accounts. Our model places about 412 bets per season at a thin 53.4% edge, a pattern that would likely trigger restrictions within 2 to 3 seasons."

*[Click to next slide]*

---

## Slide 14 — Conclusions [17:30 – 19:00]

> "So what did we learn?"

> "First, the edge is real. Linear models achieve betting accuracies significantly above 50%, with p-values below 0.001 after Bonferroni correction."

> "Second, simple models dominate. In an efficient market where exploitable signal is small and noisy, the additional flexibility of complex models like XGBoost becomes a liability. This is one of the cleanest demonstrations of the bias-variance tradeoff you'll find in practice."

> "Third, the holdout confirms the backtest. Our prospectively nominated Lasso strategy achieved 53.1% accuracy on genuinely unseen data, matching the backtest almost exactly."

> "Fourth, real-world viability is limited. Slippage, betting limits, and account restrictions all erode or cap the edge."

> "And the overarching insight: statistical significance is not economic significance. A model can beat a coin flip with p < 0.001 and still fail to generate profit after accounting for the market's built-in margin. That gap between statistical and economic significance is the defining challenge of applied machine learning in efficient markets."

*[Click to next slide]*

---

## Slide 15 — Questions [19:00 – 20:00]

> "Thank you. We're happy to take any questions."

---

## Q&A Preparation Notes

**Likely questions and suggested responses:**

**Q: Why not use neural networks or deep learning?**
A: We considered this. With only ~1,300 games per season and a low signal-to-noise ratio, deep learning would very likely overfit even more than XGBoost did. The project demonstrates that simpler models are better suited to this regime.

**Q: Could you improve by adding more features (e.g., player-level data, injury reports)?**
A: Possibly, but Vegas oddsmakers already incorporate this information. Our features are team-level aggregates that capture the same signals. Adding player-level data might improve predictions marginally, but it would also increase the risk of overfitting.

**Q: Is the 2024/25 result just luck?**
A: It could be — 256 bets is a small sample. The 95% CI includes 50%. But the consistency with the 11-season backtest (53.4% vs 53.1%) is reassuring. You'd need 2-3 more seasons of out-of-sample data to make a confident claim.

**Q: Could you actually deploy this?**
A: Technically yes, but practically it's very difficult. The break-even slippage of 0.5 points means you'd need to execute bets almost instantly when lines are posted. And sportsbooks would likely restrict the account within 1-3 seasons.

**Q: What about betting exchanges (Betfair, etc.) instead of sportsbooks?**
A: Exchanges charge a commission (typically 2-5%) instead of vig, and don't restrict winners. However, NBA liquidity on exchanges is much lower than in the US sportsbook market, making execution at scale difficult.
