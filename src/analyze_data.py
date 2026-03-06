import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


INPUT_FILE = "data/competitor_data.csv"
OUTPUT_FILE = "output/competitor_scores.csv"
BAR_CHART_FILE = "output/competitor_score_chart.png"
RADAR_CHART_FILE = "output/feature_radar_chart.png"
SUMMARY_FILE = "output/executive_summary.md"


SCORE_WEIGHTS = {
    "api_docs": 0.20,
    "developer_tools": 0.20,
    "ease_of_integration": 0.20,
    "transparent_pricing": 0.10,
    "subscription_billing": 0.10,
    "fraud_tools": 0.10,
    "global_payments": 0.05,
    "pos_support": 0.05,
}


def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def validate_data(df: pd.DataFrame):
    required_columns = ["company", "notes"] + list(SCORE_WEIGHTS.keys())

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")


def calculate_weighted_scores(df: pd.DataFrame) -> pd.DataFrame:

    weighted_score = 0

    for column, weight in SCORE_WEIGHTS.items():
        weighted_score += df[column] * weight

    df["weighted_score"] = weighted_score.round(2)

    df = df.sort_values(by="weighted_score", ascending=False).reset_index(drop=True)

    df["rank"] = range(1, len(df) + 1)

    return df


def save_scores(df: pd.DataFrame):

    os.makedirs("output", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)


def create_bar_chart(df: pd.DataFrame):

    plt.figure(figsize=(10, 6))

    plt.bar(df["company"], df["weighted_score"])

    plt.title("Fintech Competitor Weighted Scores")

    plt.xlabel("Company")

    plt.ylabel("Weighted Score")

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.savefig(BAR_CHART_FILE)

    plt.close()


def create_radar_chart(df: pd.DataFrame):

    categories = list(SCORE_WEIGHTS.keys())

    labels = [c.replace("_", " ").title() for c in categories]

    num_vars = len(categories)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})

    for _, row in df.iterrows():

        values = row[categories].tolist()

        values += values[:1]

        ax.plot(angles, values, label=row["company"])

        ax.fill(angles, values, alpha=0.05)

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(labels)

    ax.set_ylim(0, 5)

    ax.set_title("Fintech Feature Comparison")

    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.tight_layout()

    plt.savefig(RADAR_CHART_FILE)

    plt.close()


def generate_executive_summary(df: pd.DataFrame):

    top_company = df.iloc[0]["company"]

    top_score = df.iloc[0]["weighted_score"]

    fiserv_row = df[df["company"] == "Fiserv"].iloc[0]

    fiserv_score = fiserv_row["weighted_score"]

    summary = f"""
# Executive Summary

## Objective
Compare Fiserv with major fintech competitors using a developer-adoption weighted scoring model.

## Top Ranked Platform
{top_company} with a score of {top_score}

## Fiserv Position
Fiserv scored {fiserv_score}

## Insight
API-first platforms such as Stripe score highly due to strong developer tooling, documentation, and integration simplicity.

## Product Opportunity
Improving developer onboarding, documentation clarity, and integration simplicity could strengthen Fiserv's developer ecosystem adoption.
"""

    with open(SUMMARY_FILE, "w") as file:
        file.write(summary)


def main():

    os.makedirs("output", exist_ok=True)

    df = load_data(INPUT_FILE)

    validate_data(df)

    scored_df = calculate_weighted_scores(df)

    save_scores(scored_df)

    create_bar_chart(scored_df)

    create_radar_chart(scored_df)

    generate_executive_summary(scored_df)

    print("\nCompetitor Ranking:\n")

    print(scored_df[["rank", "company", "weighted_score"]])


if __name__ == "__main__":

    main()