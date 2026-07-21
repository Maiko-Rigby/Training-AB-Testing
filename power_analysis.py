import numpy as np
from scipy import stats

def required_sample_size(delta, sigma, alpha=0.05, power=0.8):
    """Required n PER GROUP for a two-sample t-test."""
    # Calculate the z-scores for the given alpha and power
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)

    # Calculate the required sample size
    n = 2 * (((z_alpha + z_power)**2 * sigma**2) / delta**2)

    return int(np.ceil(n))

def achieved_power(n, delta, sigma, alpha=0.05):
    """Given a fixed n per group, what power do we actually achieve?"""
    z_alpha = stats.norm.ppf(1 - alpha / 2)

    # With n per group, the standard error of the difference in means is: 
    SE = sigma * np.sqrt(2 / n)

    # How many standard errors is the effect size?
    z_effect = delta / SE

    # Convert this to a probability of detecting the effect (power)
    power = stats.norm.cdf(z_effect - z_alpha)

    return power




if __name__ == "__main__":
    # Example
    SIGMA = 3.0 # kg, the expected varaiablity in strength gain between the climbers
    DELTA = 2.0 # kg, the minimum between-protocol difference worth detecting
    n = 12 # number of climbers per group
    n_needed = required_sample_size(DELTA, SIGMA)
    print(f"Required sample size per group: {n_needed}")

    achieved = achieved_power(n, DELTA, SIGMA)
    print(f"Achieved power with n={n} per group: {achieved:.2f}") # What is the percentage chance of detecting a difference of DELTA kg with n climbers per group?




