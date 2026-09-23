from pathlib import Path
import numpy as np
import pandas as pd
from typing import Any
import actuarial.reserve_utils as ReserveCalculator
import data.mortality_loader as MortalityLoader
from models.assumptions import Assumptions
from models.policy import Policy
from planningbased.LifeInsNeedsBased import NeedsBasedCalculator
from productpricing.pricing_calculator import PricingTerm
from visualization.charts import (
    plot_gender_premiums,
    plot_term_reserves,
)


DATA_DIR = Path("data/tables")

EXPENSES = {
    "mortgage": 750000,
    "auto_loan": 10000,
    "credit_card": 5000,
    "burial": 20000,
    "estate": 25000,
}

EDUCATION_EXPENSES = {
    "college_fund": 150000,
    "k_12": 50000,
}

INCOME_REPLACEMENT = {
    "years_to_replace": 25,
    "percentage_to_replace": 0.80,
}

EXISTING_ASSETS = {
    "cash_savings": 50000,
    "investments": 100000,
    "retirement_account": 250000,
    "lifeinsurance": 250000,
}


def build_client(
    age: int,
    annual_income: float,
    expenses: dict[str, float],
    education_expenses: dict[str, float],
    income_replacement: dict[str, float],
    existing_assets: dict[str, float],
) -> dict[str, Any]:
    """Calculate and return a client's insurance-needs summary."""

    client = NeedsBasedCalculator(
        age=age,
        annual_income=annual_income,
    )

    client.set_expenses(**expenses)
    client.set_education_expenses(**education_expenses)
    client.set_income_replacement(**income_replacement)
    client.set_existing_assets(**existing_assets)
    client.calc_needs_based()

    return client.client_summary()


def build_policy_quote(
    pricing_service: PricingTerm,
    assumptions: Assumptions,
    age: int,
    gender: str,
    risk_class: str,
    term_duration: int,
    face_amount: float,
) -> tuple[Policy, dict[str, Any]]:
    """Create a policy and calculate its corresponding quote."""

    policy = Policy(
        issue_age=age,
        gender=gender,
        risk_class=risk_class,
        term_duration=term_duration,
        face_amount=face_amount,
    )

    quote = pricing_service.quote(
        policy=policy,
        assumptions=assumptions,
    )

    quote.update(
        {
            "age": age,
            "gender": gender,
            "risk_class": risk_class,
            "term_duration": term_duration,
            "face_amount": face_amount,
        }
    )

    return policy, quote


def build_comparison_dataframe(
        pricing_service: PricingTerm,
        assumptions: Assumptions,
        face_amount: float,
        term_duration: int,
        genders: tuple[str, ...] = ("male", "female")) -> pd.DataFrame:
    
    """Build premium comparisons by age, risk class, and gender."""

    ages = np.arange(24, 62, step=2)

    risk_classes = (
        pricing_service.mortality_df["risk_class"]
        .dropna()
        .unique()
    )

    results = []

    for age in ages:
        for risk_class in risk_classes:
            for gender in genders:
                _, quote = build_policy_quote(
                    pricing_service=pricing_service,
                    assumptions=assumptions,
                    age=int(age),
                    gender=gender,
                    risk_class=risk_class,
                    term_duration=term_duration,
                    face_amount=face_amount,
                )

                results.append(quote)

    return (
        pd.DataFrame(results)
        .sort_values(
            by=["age", "net_premium"],
            ignore_index=True,
        )
    )


def main():
    mortality_df = MortalityLoader.load_mortality_files(data_dir=DATA_DIR)
    pricing_service = PricingTerm(mortality_df)

    assumptions = Assumptions(
        interest_rate=0.05,
        expense_ratio=0.10,
        policy_fee=50,
        acquisition_cost=500,
    )

    client_summary = build_client(
        age=40,
        annual_income=150_000,
        expenses=EXPENSES,
        education_expenses=EDUCATION_EXPENSES,
        income_replacement=INCOME_REPLACEMENT,
        existing_assets=EXISTING_ASSETS,
    )

    face_amount = round(
        client_summary["net_insurance_need"]
    )

    policy, quote = build_policy_quote(
        pricing_service=pricing_service,
        assumptions=assumptions,
        age=int(client_summary["age"]),
        gender="male",
        risk_class="standard",
        term_duration=20,
        face_amount=face_amount,
    )


    reserves, premium_npv, benefit_npv = ReserveCalculator.calculate_reserve(
        survival_probabilities=quote[
            "survival_probabilities"
        ],
        death_probabilities=quote[
            "death_probabilities"
        ],
        premium=quote["net_premium"],
        benefit=policy.face_amount,
        interest_rate=assumptions.interest_rate,
    )  


    plot_term_reserves(
        reserve_values=reserves,
        prem_npv=premium_npv,
        bene_npv=benefit_npv,
        term_duration=policy.term_duration,
    )

    comparison_df = build_comparison_dataframe(
        pricing_service=pricing_service,
        assumptions=assumptions,
        face_amount=face_amount,
        term_duration=policy.term_duration,
    )

    plot_gender_premiums(
        comparison_df,
        "male",
        face_amount,
    )

    plot_gender_premiums(
        comparison_df,
        "female",
        face_amount,
    )


if __name__ == "__main__":
    main()