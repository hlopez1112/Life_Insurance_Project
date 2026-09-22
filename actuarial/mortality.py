import numpy as np
import pandas as pd


class MortalityCalculator:

    @staticmethod
    def get_qx(df: pd.DataFrame, age: int, risk_class: str, gender: str) -> np.ndarray:

        mask = (
        (df["issue_age"] == age)
        & (df["risk_class"] == risk_class)
        & (df["gender"] == gender)
        )

        result = df.loc[mask]

        if result.empty:
            raise ValueError(f"No mortality data for age {age}")

        return result.drop(columns=["issue_age", "risk_class", "gender"]).values[0]

    @staticmethod
    def death_probabilities(mortality_values: np.ndarray, term: int)-> tuple[np.ndarray, np.ndarray]:

        mortality_term = mortality_values[:term]
        survival_probabilities = np.empty_like(mortality_term)

        survival_probabilities[0] = 1

        survival_probabilities[1:] = np.cumprod(1 - mortality_term)[:-1]
        death_probabilities = survival_probabilities * mortality_term

        return survival_probabilities, death_probabilities