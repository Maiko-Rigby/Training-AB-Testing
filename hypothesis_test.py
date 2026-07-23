import numpy as np
import pandas as pd
from scipy import stats

def run_test(df, alpha = 0.05): # Is the difference in strength gain between the two protocols statistically significant?
    treat = df[df["group"] == "controlled_hangs"]["gain_kg"]
    control = df[df["group"] == "max_effort_hangs"]["gain_kg"]

    t_stat, p_value = stats.ttest_ind(treat, control, equal_var = False) # Welch's t-test
    significant = p_value < alpha
    print(f"t-statistic = {t_stat:.3f}, p-value = {p_value:.3f}, significant = {significant}")

def cohans_d(a, b): # How many standard deviations apart are the two groups? mean difference / pooled standard deviation
    n1, n2 = len(a), len(b)
    pooled_sd = np.sqrt(((n1 - 1) * np.var(a, ddof=1) + (n2 - 1) * np.var(b, ddof=1)) / (n1 + n2 - 2))
    return (a.mean() - b.mean()) / pooled_sd

def welch_ci(a, b, alpha=0.05): # Calculates the confidence interval for the difference in means between two groups
    diff = a.mean() - b.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    # Degrees of freedom for Welch's t-test
    df = (a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)) ** 2 / (
        (a.var(ddof=1) / len(a)) ** 2 / (len(a) - 1)
        + (b.var(ddof=1) / len(b)) ** 2 / (len(b) - 1)
    )
    t_crit = stats.t.ppf(1 - alpha/2, df)
    return diff - t_crit * se, diff + t_crit * se

if __name__ == "__main__":
    df = pd.read_csv("data/simulated_climber_data.csv")
    treat = df[df["group"] == "controlled_hangs"]["gain_kg"]
    control = df[df["group"] == "max_effort_hangs"]["gain_kg"]
    run_test(df)
    print(f"Cohen's d = {cohans_d(treat, control):.2f}")
    # If the experiment were repeated many times, the true difference in means would fall within this interval 95% of the time
    ci_low, ci_high = welch_ci(treat, control)
    print(f"Difference: {treat.mean() - control.mean():.2f} kg, 95% CI [{ci_low:.2f}, {ci_high:.2f}]")