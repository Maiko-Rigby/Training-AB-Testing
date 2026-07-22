import numpy as np
from scipy import stats
import pandas as pd

def baseline_balance_check(df, alpha = 0.05):
    treat = df[df["group"] == "controlled_hangs"]["baseline_crimp_kg"]
    control = df[df["group"] == "max_effort_hangs"]["baseline_crimp_kg"]

    t_stat, p_value = stats.ttest_ind(treat, control, equal_var = False) # Welch's t-test

    balance = p_value > alpha
    print(f"Baseline balance check: t-statistic = {t_stat:.3f}, p-value = {p_value:.3f}, balanced = {balance}")

def confounder_balance_check(df, alpha = 0.05):
    treat = df[df["group"] == "controlled_hangs"]["climbing_sessions_per_week"]
    control = df[df["group"] == "max_effort_hangs"]["climbing_sessions_per_week"]

    t_stat, p_value = stats.ttest_ind(treat, control, equal_var = False) # Welch's t-test

    balance = p_value > alpha
    print(f"Confounder balance check: t-statistic = {t_stat:.3f}, p-value = {p_value:.3f}, balanced = {balance}")

if __name__ == "__main__":
    df = pd.read_csv("data/simulated_climber_data.csv")
    baseline_balance_check(df)
    confounder_balance_check(df)
