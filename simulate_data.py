import numpy as np
import pandas as pd
import os

RNG = np.random.default_rng(seed = 7) # This seed makes it reproducible

N_TREATMENT = 12 # Number of climbers per new protocol group
N_CONTROL = 12 # Number of climbers per control group (max-effort protocol)
TRUE_EFFECT_KG = 1.2 # This value is for the advantage deliberaly placed into the control group.
NOISE_SD = 3.0 # Matches the sigma of the power analysis.

def simulate():
    n_total = N_TREATMENT + N_CONTROL
    climber_id = [f"C{i+1:02d}" for i in range(n_total)]

    group = np.array(["controlled_hangs"] * N_TREATMENT + ["max_effort_hangs"] * N_CONTROL) # Create a list of group labels for each climber
    RNG.shuffle(group) # Shuffle the group

    baseline_crimp_kg = RNG.normal(15, 5, size=n_total)
    climbing_sessions_per_week = RNG.gamma(shape = 5.0,  scale = 0.6, size=n_total) # Average of 3 sessions per week, but some climbers train more than others.

    base_gain = 1.8 # Each climber is expected to gain at least 1.8kg of strength regardless of the protocol they are assigned to.
    treatment_bump = np.where(group == "controlled_hangs", TRUE_EFFECT_KG, 0) # the real effect of the controlled hang protocol.
    volume_bump = 0.4 * climbing_sessions_per_week
    noise = RNG.normal(0, NOISE_SD, size=n_total) # individual climbers will vary

    gain_kg = base_gain + treatment_bump + volume_bump + noise
    week8_crimp_kg = baseline_crimp_kg + gain_kg

    df = pd.DataFrame({
        "climber_id": climber_id,
        "group": group,
        "baseline_crimp_kg": baseline_crimp_kg.round(1),
        "week8_crimp_kg": week8_crimp_kg.round(1),
        "gain_kg": gain_kg.round(1),
        "climbing_sessions_per_week": climbing_sessions_per_week.round(1)
    })

    return df

if __name__ == "__main__":
    df = simulate()
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/simulated_climber_data.csv", index=False)
    print(f"Simulated {len(df)} climbers -> data/experiment_data.csv")
    print(df.groupby("group")["gain_kg"].agg(["mean", "std", "count"]))

