#!/usr/bin/env python3
"""
Generate a formal 10-page PDF report for Business 35137 Final Project.
Machine Learning in NBA Over/Under Betting.
"""

from fpdf import FPDF
import os

IMG_DIR = os.path.join(os.path.dirname(__file__), "Images")


FONT = "Arial"  # registered TTF name


class Report(FPDF):
    page_margin_top = 28

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # Register Arial TTF for full Unicode support
        base = "/System/Library/Fonts/Supplemental/"
        self.add_font(FONT, "", os.path.join(base, "Arial.ttf"), uni=True)
        self.add_font(FONT, "B", os.path.join(base, "Arial Bold.ttf"), uni=True)
        self.add_font(FONT, "I", os.path.join(base, "Arial Italic.ttf"), uni=True)
        self.add_font(FONT, "BI", os.path.join(base, "Arial Bold Italic.ttf"), uni=True)

    def header(self):
        if self.page_no() == 1:
            return  # title page has custom header
        self.set_font(FONT, "I", 8)
        self.set_text_color(120, 120, 120)
        self.set_y(10)
        self.cell(0, 5, "Machine Learning in NBA Over/Under Betting", align="L")
        self.cell(0, 5, f"Page {self.page_no()}", align="R")
        self.ln(8)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_font(FONT, "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, "Business 35137 | Chicago Booth | Winter 2026", align="C")

    def section_title(self, number, title):
        self.set_font(FONT, "B", 13)
        self.set_text_color(20, 40, 80)
        self.cell(0, 7, f"{number}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(20, 40, 80)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def sub_title(self, title):
        self.set_font(FONT, "B", 10.5)
        self.set_text_color(40, 60, 100)
        self.cell(0, 5.5, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font(FONT, "", 9.5)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 4.5, text)
        self.ln(1.2)

    def body_italic(self, text):
        self.set_font(FONT, "I", 9.5)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 4.5, text)
        self.ln(1.2)

    def add_figure(self, filename, caption, width=170):
        path = os.path.join(IMG_DIR, filename)
        if not os.path.exists(path):
            self.body(f"[Figure not found: {filename}]")
            return
        space_needed = 70
        if self.get_y() + space_needed > self.h - 20:
            self.add_page()
        x_offset = (self.w - width) / 2
        self.image(path, x=x_offset, w=width)
        self.ln(1)
        self.set_font(FONT, "I", 8)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 3.5, caption, align="C")
        self.ln(2)


def build_report():
    pdf = Report(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)

    # ══════════════════════════════════════════════════════════════
    # TITLE PAGE
    # ══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font(FONT, "B", 24)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 12, "Machine Learning in", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, "NBA Over/Under Betting", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    pdf.set_draw_color(20, 40, 80)
    center_x = pdf.w / 2
    pdf.line(center_x - 40, pdf.get_y(), center_x + 40, pdf.get_y())
    pdf.ln(8)

    pdf.set_font(FONT, "", 13)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "Business 35137: Machine Learning in Finance", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "The University of Chicago Booth School of Business", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(12)

    pdf.set_font(FONT, "", 12)
    pdf.set_text_color(30, 30, 30)
    for name in ["Alan Donnelly", "Andrew McLaughlin", "Robert Asgeirsson", "Chris Mulligan"]:
        pdf.cell(0, 7, name, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(12)

    pdf.set_font(FONT, "I", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, "Winter 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    # ══════════════════════════════════════════════════════════════
    # 1. INTRODUCTION
    # ══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("1", "Introduction")
    pdf.body(
        "In sports betting, a total (also called an over/under) is the sportsbook's prediction of the "
        "combined points scored by both teams in a game. Bettors wager on whether the actual combined "
        "score will be over or under this number. Standard odds of -110 mean a bettor must risk $110 to "
        "win $100, implying the sportsbook takes a commission (the vig) on every bet. To break even at "
        "-110 odds, a bettor must win at least 52.4% of bets."
    )
    pdf.body(
        "The Vegas line is set by professional oddsmakers who incorporate team statistics, injuries, "
        "matchup history, public betting patterns, and other market signals. It is widely regarded as "
        "the most efficient public forecast of game outcomes. Any model that claims to beat the line "
        "must find a small, repeatable edge that the market has overlooked."
    )
    pdf.body(
        "This report investigates whether machine learning models can predict NBA game totals more "
        "accurately than the Vegas line, and under what conditions selective betting strategies can "
        "generate positive returns. We train six model classes spanning linear, dimension-reduced, "
        "tree-based, and kernel-based approaches using walk-forward validation on 11 NBA seasons "
        "(2013/14 through 2023/24), then test the nominated strategy on a held-out 2024/25 season "
        "that was never used in any modeling decision."
    )

    pdf.sub_title("Approach")
    pdf.body(
        "We construct lagged, within-season team features from box score statistics to avoid lookahead "
        "bias. Six model classes are trained: Ridge, Lasso, ElasticNet, Principal Component Regression "
        "(PCR), XGBoost, and RBF+Ridge (Radial Basis Function kernel approximation combined with Ridge "
        "regression). Models are evaluated via walk-forward backtesting with strict temporal ordering, "
        "tuned on betting accuracy rather than regression error, and subjected to rigorous statistical "
        "testing including Bonferroni-corrected significance tests and McNemar's paired comparison. "
        "Selective betting with confidence thresholds is explored to concentrate bets where the model's "
        "edge is strongest. Finally, bankroll simulations with 10 sizing rules stress-test whether "
        "statistical edge translates into economic viability, and real-world frictions (slippage, "
        "market depth, account restrictions) are quantified."
    )

    # ══════════════════════════════════════════════════════════════
    # 2. DATA
    # ══════════════════════════════════════════════════════════════
    pdf.section_title("2", "Data")
    pdf.body(
        "Two primary data sources cover 18 NBA seasons (2007/08 through 2024/25). Betting data "
        "contains approximately 23,000 games with the Vegas total line, point spread, and final "
        "score. NBA box score data provides team-level statistics for each game: points, field goal "
        "percentage, three-point percentage, free throw percentage, rebounds, assists, steals, blocks, "
        "turnovers, and personal fouls. Historical box scores cover 2007/08 through 2022/23; the "
        "2023/24 and 2024/25 seasons are retrieved via the NBA Stats API and merged with the archive."
    )
    pdf.body(
        "The two sources are merged on date and team matchup. Team abbreviations are standardized to "
        "account for franchise relocations (e.g., NJN to BKN, SEA to OKC). Each game is assigned a "
        "season-end year. The 2024/25 season (1,293 games) is held out entirely from model training "
        "and evaluation; the remaining 21,397 games form the walk-forward training and test pool."
    )

    pdf.add_figure("data_overview.png",
                    "Figure 1: Data coverage by season, NBA scoring trend, and Vegas line accuracy.")

    # ══════════════════════════════════════════════════════════════
    # 3. FEATURE ENGINEERING
    # ══════════════════════════════════════════════════════════════
    pdf.section_title("3", "Feature Engineering")
    pdf.body(
        "Feature engineering transforms raw game data into 114 numerical inputs organized into seven "
        "categories: Vegas line features (3), totals and scoring (18), shooting efficiency (24), "
        "rebounding and hustle (16), playmaking (8), schedule and rest (11), context indicators (6), "
        "and interaction features (28). All features are strictly lagged: rolling means are computed "
        "over each team's previous games within the same season using a shift(1) operation, ensuring "
        "no future information leaks into any prediction."
    )
    pdf.body(
        "Rolling averages are computed at two window sizes: L5 (last 5 games) to capture short-term "
        "form, and L10 (last 10 games) for medium-term stability. For the first game of each team's "
        "season, no prior data is available, so these games are dropped. An early-season indicator "
        "variable flags the first 10 games of each team's season, where rolling statistics are based "
        "on limited observations and are therefore noisier."
    )

    pdf.add_figure("feature_matrix_overview.png",
                    "Figure 2: Feature composition, target distribution, and Vegas line vs. actual outcomes.")

    pdf.body(
        "Univariate correlation analysis confirms that Vegas-derived features and recent scoring "
        "averages are the strongest individual predictors (r = 0.55-0.65), while schedule and rest "
        "features show near-zero marginal correlation. Interaction features (e.g., pace x pace, "
        "spread x total) are included to help linear models capture non-additive effects."
    )

    pdf.add_figure("feature_signal_preview.png",
                    "Figure 3: Top and bottom features ranked by absolute correlation with actual game totals.")

    # ══════════════════════════════════════════════════════════════
    # 4. MODEL TRAINING AND WALK-FORWARD EVALUATION
    # ══════════════════════════════════════════════════════════════
    pdf.section_title("4", "Model Training and Walk-Forward Evaluation")
    pdf.body(
        "Walk-forward backtesting enforces strict temporal ordering: for each of 11 test seasons "
        "(2013/14 through 2023/24), the model trains on all available data before that season and "
        "predicts the test season. The training set grows by approximately 1,300 games per iteration. "
        "Hyperparameters are tuned via 5-fold TimeSeriesSplit within the training set, optimizing "
        "betting accuracy rather than RMSE, since the downstream task is predicting over/under outcomes."
    )
    pdf.body(
        "A key design choice is exponential recency weighting controlled by a half-life parameter, "
        "tuned jointly with model hyperparameters. Each half-life/hyperparameter combination is "
        "evaluated during cross-validation, and the combination that maximizes betting accuracy is "
        "selected for that season. This allows the models to adapt to the NBA's evolving pace and "
        "scoring trends without manually specifying a recency window."
    )
    pdf.body(
        "Pooling predictions across all 11 test seasons yields approximately 11,000-13,000 "
        "out-of-sample bets per model. A no-bet filter excludes games where the model's prediction "
        "is within 0.5 points of the Vegas line."
    )

    pdf.add_figure("model_comparison.png",
                    "Figure 5: Walk-forward results \u2014 betting accuracy, ROI, and overfitting check (train vs. OOS RMSE) for all six models.")

    pdf.sub_title("Key Findings")
    pdf.body(
        "All six models cluster between 50.7% and 52.0% accuracy. The linear models (Ridge at "
        "51.7%, Lasso and ElasticNet at 52.0%) achieve the highest accuracies, while XGBoost "
        "(50.7%) and RBF+Ridge (50.9%) trail behind. No model reaches the 52.4% break-even "
        "threshold when betting every qualifying game, so all ROI values are negative. This is "
        "the expected result in an efficient market."
    )
    pdf.body(
        "Simple models outperform complex ones. The overfitting check (Figure 5, Panel 3) "
        "reveals that linear models show minimal train-vs-OOS RMSE gaps (~0.4 points), while "
        "XGBoost shows a 2.3-point gap, confirming it memorizes training patterns that do not "
        "generalize. In an efficient market where exploitable signal is small and noisy, the "
        "additional flexibility of complex models becomes a liability."
    )

    pdf.add_figure("per_season_accuracy.png",
                    "Figure 6: Per-season accuracy and consistency across 11 walk-forward test seasons.")

    pdf.body(
        "Per-season analysis reveals that accuracy is volatile (48-55% range), with no model "
        "consistently beating 52.4% across all seasons. The linear models tend to move together, "
        "suggesting they extract similar signal. Lasso achieves the highest season-above-50% count "
        "(10 of 11 seasons), demonstrating the most consistent performance."
    )

    # ══════════════════════════════════════════════════════════════
    # 5. STATISTICAL SIGNIFICANCE
    # ══════════════════════════════════════════════════════════════
    pdf.section_title("5", "Statistical Significance Testing")
    pdf.body(
        "With over 11,000 bets per model, even small deviations from 50% require formal "
        "significance testing. We apply four complementary tools: Wilson score confidence intervals, "
        "bootstrap resampling (standard and block bootstrap to account for temporal correlation), "
        "Bonferroni-corrected p-values for multiple comparisons, and McNemar's paired test for "
        "pairwise model comparison."
    )

    pdf.add_figure("statistical_validation.png",
                    "Figure 9: Confidence intervals, significance testing (raw and Bonferroni-corrected), and per-season accuracy distributions.")

    pdf.body(
        "After Bonferroni correction for testing 6 models, four survive with significance against "
        "50%: Ridge, Lasso, ElasticNet, and PCR (all p < 0.006). XGBoost (p = 0.054) fails to "
        "reach significance even before correction. All three CI methods (Wilson, standard bootstrap, "
        "block bootstrap) produce nearly identical intervals, confirming that temporal correlation "
        "does not materially inflate confidence. However, every model's CI includes 52.4%, meaning "
        "we cannot confirm profitability with flat betting."
    )

    pdf.add_figure("mcnemar_heatmap.png",
                    "Figure 10: McNemar pairwise disagreement heatmap. Asterisks denote statistically significant differences (p < 0.05).",
                    width=130)

    pdf.body(
        "McNemar's test confirms that Lasso significantly outperforms PCR, XGBoost, and RBF+Ridge "
        "in pairwise comparisons. The linear models (Ridge, Lasso, ElasticNet) do not differ "
        "significantly from each other, consistent with extracting similar signal from the features."
    )

    # ══════════════════════════════════════════════════════════════
    # 6. SELECTIVE BETTING
    # ══════════════════════════════════════════════════════════════
    pdf.section_title("6", "Selective Betting with Confidence Thresholds")
    pdf.body(
        "Since no model is profitable when betting every game, we test whether restricting bets to "
        "games where the model strongly disagrees with the Vegas line can push accuracy above "
        "break-even. The absolute difference between the model's prediction and the Vegas total "
        "serves as a confidence measure. We sweep thresholds from 0.5 to 20 points, subject to "
        "dual validity constraints: at least 300 total bets globally, and at least 10 bets in every "
        "individual season."
    )

    pdf.add_figure("fig12_threshold_overview.png",
                    "Figure 12: Bet volume decay and ROI by confidence threshold for all six models. Stars mark optimal thresholds.")

    pdf.body(
        "Four models achieve positive ROI at valid thresholds. Ridge leads at +5.4% ROI (55.0% "
        "accuracy, 826 bets at threshold \u2265 4.5), followed by ElasticNet (+2.2%, 1,896 bets at "
        "\u2265 4.0), Lasso (+2.1%, 4,529 bets at \u2265 2.0), and PCR (+0.6%, 5,126 bets at \u2265 2.5). "
        "XGBoost and RBF+Ridge never achieve positive ROI at any valid threshold."
    )
    pdf.body(
        "The explanation lies in prediction variance. Linear models have prediction standard "
        "deviations of 2.4-2.8 points, making conservative adjustments to the efficient Vegas line. "
        "When they strongly disagree with Vegas, it likely reflects genuine signal. XGBoost and "
        "RBF+Ridge have standard deviations of approximately 6 points, routinely making extreme "
        "predictions driven by overfitting rather than genuine market mispricing."
    )

    pdf.add_figure("fig13_base_vs_selective.png",
                    "Figure 14: Comparison of base (all bets) vs. selective betting \u2014 volume, accuracy, and ROI for each model.")

    pdf.body(
        "After Bonferroni correction, five models remain significantly above 50% at their optimal "
        "thresholds. However, no model's selective accuracy is significantly above 52.4%. The "
        "evidence for profitability is suggestive but not statistically conclusive, as the smaller "
        "sample sizes from selective betting widen the confidence intervals."
    )

    # ══════════════════════════════════════════════════════════════
    # 7. BANKROLL SIMULATION AND HOLDOUT
    # ══════════════════════════════════════════════════════════════
    pdf.section_title("7", "Bankroll Simulation and Holdout Deployment")
    pdf.body(
        "The four qualifying models are subjected to bankroll simulations across 10 sizing rules, "
        "ranging from conservative flat dollar amounts to the theoretically optimal Kelly criterion "
        "and its fractional variants. Starting from a $10,000 bankroll, the simulations run across "
        "all 11 walk-forward seasons to evaluate growth, drawdown, and consistency."
    )

    pdf.add_figure("fig16_bet_sizing_backtest.png",
                    "Figure 16: Backtest heatmap of final bankroll values and CAGR across all model-strategy combinations.")

    pdf.body(
        "The simulations reveal that sizing matters as much as accuracy. Flat $500 bets cause "
        "bankruptcy for all four models despite positive edges. Full Kelly achieves the highest "
        "CAGR but with extreme drawdowns (76.6% for Ridge). Fractional Kelly variants consistently "
        "offer better risk-adjusted returns."
    )

    pdf.add_figure("fig18_risk_return.png",
                    "Figure 18: Risk-return scatter of all model-strategy combinations. The Pareto frontier runs through Ridge's conservative strategies.")

    pdf.sub_title("Model Nomination")
    pdf.body(
        "Using only backtest data available before the 2024/25 season, we nominate Lasso with "
        "Flat 2% sizing ($200 per bet) as the deployment strategy. While Ridge offers marginally "
        "higher CAGR (+10.6% vs. +9.5%), Lasso wins on every other criterion: lower maximum "
        "drawdown (57.2% vs. 76.6%), more winning seasons (7/11 vs. 6/11), 5.5 times more bets "
        "(4,529 vs. 826) for greater statistical reliability, and a simpler sizing rule that "
        "requires no win-probability estimation. This nomination is entirely prospective."
    )

    pdf.sub_title("Holdout Results: 2024/25 Season")
    pdf.body(
        "The Lasso model places 256 qualifying bets on the unseen 2024/25 season, achieving 53.1% "
        "accuracy. This is within 0.3 percentage points of its 11-season backtest accuracy of 53.4%, "
        "and sits above the 52.4% break-even threshold. Under Flat 2% sizing, the $10,000 bankroll "
        "grows to $10,727, a +7.3% return with a maximum drawdown of 15.3%."
    )

    pdf.add_figure("fig19_lasso_holdout_deployment.png",
                    "Figure 19: Lasso Flat 2% deployment on the 2024/25 holdout season \u2014 bankroll trajectory and cumulative win rate convergence.")

    pdf.body(
        "The consistency between backtest and holdout is the most important finding: the strategy "
        "nominated prospectively on the basis of 11 seasons of data remains profitable on genuinely "
        "unseen data. As an investment benchmark, the strategy's +7.3% return compares to the S&P "
        "500's +3.7% over the same October 2024 to June 2025 window, with near-zero correlation "
        "to equity markets."
    )
    pdf.body(
        "A single season of 256 bets is statistically underpowered to prove a persistent edge. "
        "The 95% Wilson confidence interval for holdout accuracy spans [47.0%, 59.1%], which "
        "includes both 50% and 52.4%. The positive result is encouraging but not conclusive."
    )

    # ══════════════════════════════════════════════════════════════
    # 8. REAL-WORLD CONSTRAINTS
    # ══════════════════════════════════════════════════════════════
    pdf.section_title("8", "Real-World Implementation Constraints")
    pdf.body(
        "Before drawing conclusions about practical viability, we examine three frictions that "
        "stand between a profitable backtest and actual profits: execution slippage, market depth, "
        "and account restrictions."
    )

    pdf.sub_title("Execution Slippage")
    pdf.body(
        "We simulate scenarios where the betting line shifts 0.5 to 3.0 points against the bet "
        "direction before execution. At zero slippage, Lasso achieves its full +1.9% flat-bet ROI "
        "on 4,529 backtest bets. The break-even slippage is approximately 0.5 points, which falls "
        "at the lower bound of typical NBA line movement (0.5-1.5 points). Even modest execution "
        "delays can eliminate the advantage entirely."
    )

    pdf.add_figure("part8_slippage_analysis.png",
                    "Figure 21: Accuracy and ROI degradation under increasing execution slippage. "
                    "The typical slippage range (grey band) largely overlaps with the unprofitable region.")

    pdf.sub_title("Market Depth and Scalability")
    pdf.body(
        "Sportsbook betting limits cap the maximum bet per game at $2,500-$10,000 depending on the "
        "book. Across approximately 10 accessible US sportsbooks, the maximum deployable capital per "
        "game is roughly $50,000, implying a ceiling bankroll of $2.5 million at Flat 2% sizing. "
        "A $10,000 bankroll generates an expected annual profit of approximately $188; a $250,000 "
        "bankroll generates approximately $4,700. Scaling up capital does not fix the slippage "
        "problem, as break-even slippage is a property of the edge, not the bankroll size."
    )

    pdf.add_figure("part8_scalability_analysis.png",
                    "Figure 22: Expected profit by bankroll size and combined impact of slippage and capital deployment.")

    pdf.sub_title("Account Restrictions")
    pdf.body(
        "The most significant threat is account restrictions. Sportsbooks track betting patterns and "
        "flag accounts that exhibit Closing Line Value (consistently getting better odds than the "
        "final line). Winning accounts are typically limited or closed within 1-3 seasons. Our Lasso "
        "model places approximately 412 bets per season at a thin 53.4% edge, a volume and pattern "
        "that would likely trigger restrictions within 2-3 seasons."
    )

    # ══════════════════════════════════════════════════════════════
    # 9. CONCLUSION
    # ══════════════════════════════════════════════════════════════
    pdf.section_title("9", "Conclusion")
    pdf.body(
        "This project set out to determine whether machine learning models can profitably predict "
        "NBA over/under totals. The answer is nuanced: a genuine statistical edge exists, but "
        "real-world frictions make it extremely difficult to capture reliably."
    )

    pdf.sub_title("The Edge Is Real")
    pdf.body(
        "Linear models (Ridge, Lasso, ElasticNet) achieve betting accuracies of "
        "51.7\u201352.0% on over 11,000 out-of-sample predictions, with p-values below 0.001 after "
        "Bonferroni correction. Selective betting pushes four models above the 52.4% break-even "
        "threshold, with Ridge achieving 55.0% accuracy and +5.4% ROI on 826 high-confidence bets."
    )

    pdf.sub_title("Simple Models Dominate")
    pdf.body(
        "Simple linear models consistently outperform complex nonlinear alternatives (XGBoost, "
        "RBF+Ridge). XGBoost shows a 2.3-point train-vs-OOS RMSE gap, confirming that it "
        "memorizes training patterns that do not generalize. In an efficient market where "
        "exploitable signal is small and noisy, the additional flexibility of complex models "
        "becomes a liability rather than an asset. This is a textbook illustration of the "
        "bias-variance tradeoff in a low-signal environment."
    )

    pdf.sub_title("The Holdout Confirms the Backtest")
    pdf.body(
        "Our prospectively nominated Lasso Flat 2% strategy "
        "achieved 53.1% accuracy on 256 unseen 2024/25 bets, within 0.3 percentage points of its "
        "11-season backtest accuracy of 53.4%. The $10,000 bankroll grew to $10,727 (+7.3% return), "
        "closely tracking the +9.5% annualized CAGR observed in the backtest. This consistency "
        "between prospective nomination and holdout performance is the most important result of "
        "the project, though a single season of 256 bets is insufficient for statistical certainty."
    )

    pdf.sub_title("Real-World Viability Is Limited")
    pdf.body(
        "The strategy passes three of six viability criteria "
        "(backtest accuracy, backtest ROI, holdout confirmation) but fails the remaining three. "
        "The break-even slippage of approximately 0.5 points falls at the lower bound of typical "
        "NBA line movement (0.5\u20131.5 points), meaning even modest execution delays can eliminate "
        "the edge. Sportsbook account restrictions track betting patterns and flag accounts that "
        "exhibit Closing Line Value, imposing a hard time limit of 1\u20133 seasons before the "
        "account is limited or closed."
    )

    pdf.sub_title("Implications for Market Efficiency")
    pdf.body(
        "Our results are consistent with the semi-strong form of market efficiency: publicly "
        "available statistical information is largely priced into the Vegas line. The residual "
        "edge (+1.9% flat-bet ROI in backtest, +7.3% bankroll ROI in the holdout season) is real "
        "but small enough that transaction costs and market structure constraints make it extremely "
        "difficult to capture reliably. From a machine learning perspective, this project "
        "demonstrates that model accuracy and economic viability are fundamentally different "
        "questions. A model can be statistically superior to random chance (p < 0.001) yet still "
        "fail to generate profit after accounting for the market's built-in margin. The gap "
        "between statistical significance and economic significance is the defining challenge "
        "of applied ML in efficient markets."
    )

    # ══════════════════════════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════════════════════════
    out_path = os.path.join(os.path.dirname(__file__), "Final_Report.pdf")
    pdf.output(out_path)
    print(f"Report saved to: {out_path}")
    print(f"Total pages: {pdf.page_no()}")


if __name__ == "__main__":
    build_report()
