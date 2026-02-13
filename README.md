# Final Project Hand-Off Guide

## What this project does
This notebook builds machine learning models to predict NBA game totals and compares those predictions to the Vegas total. We then test how selective betting and bet sizing would perform if you only bet when the model strongly disagrees with the market.

## How the model works (plain language)
For each game on date t:
1. Find the two teams and their prior game histories in the same season.
2. Compute rolling L5/L10 averages for each team (scoring, efficiency, rebounds, turnovers, rest).
3. Combine home and away features into a single game row, plus the Vegas total and spread.
4. Feed that row into the trained model to predict total points.
5. Compare prediction vs Vegas line to decide Over or Under.

## Key files
- FINALPROJECT.ipynb: main analysis notebook
- FINALPROJECT.html / FINALPROJECT.pdf: rendered exports (if you export)
- Data/: input data (betting lines and box scores)
- Images/: figures saved by the notebook

## Large data download (not in repo)
Two oversized files are excluded from GitHub due to the 2 GB limit:
- Data/Game Data/nba.sqlite
- Data/Game Data/play_by_play.csv

Download them from Kaggle and place them in the same paths above:
https://www.kaggle.com/datasets/wyattowalsh/basketball

## Run order (recommended)
1. Open FINALPROJECT.ipynb.
2. Restart kernel.
3. Run all cells top to bottom.

Notes:
- The model training cell caches results to Data/model_training_cache.pkl. If the cache exists and matches the current feature set, it will load instead of retraining.
- The NBA Stats API call is cached in Data/Game Data. If you re-run with new seasons, it may take time and can be rate-limited.
- The notebook writes plots to Images/.

## Model comparison policy
- Parts 4-5 compare all models side-by-side.
- From Part 6 onward, we focus on the top set (PCR, Ridge, RBF+Ridge) and drop the others because their selective ROI is weak or unstable.

## How to complete Parts 9-11 (teammate instructions)
### Part 9: Alternative Data and Advanced Models
Goal: propose realistic data additions and model upgrades that could improve prediction quality.
Suggested content:
- Alternative data: injuries, lineup changes, travel distance, rest quality, pace, and betting market signals.
- Advanced models: tree ensembles (XGBoost/RandomForest), calibrated probability models, regime-aware models.
- Explain why each addition could add incremental signal beyond the Vegas line.

### Part 10: Real-World Implementation Constraints
Goal: describe practical frictions in live betting and how they change results.
Suggested content:
- Data latency and availability; how late-breaking injuries affect predictions.
- Line movement, price slippage, and betting limits.
- Risk controls, bet sizing caps, and exposure constraints.
- Compliance and transparency for any automated system.

### Part 11: 2025-26 Season / Bulls Tracker Demo
Goal: outline a live demonstration for the presentation.
Suggested content:
- Pick a team (e.g., Bulls) or full-season tracker.
- Weekly update workflow: ingest latest games, recompute features, update predictions.
- Show predictions vs Vegas, decisions, and realized outcomes in a simple table or chart.

## Common gotchas
- If results in text and tables do not match, re-run the notebook after any code change.
- Small sample sizes at high thresholds can produce unstable ROI.

## Suggested handoff checklist
- Re-run all cells.
- Verify plots in Images/ update correctly.
- Replace Part 9-11 outlines with final content.
- Export HTML or PDF for presentation.
