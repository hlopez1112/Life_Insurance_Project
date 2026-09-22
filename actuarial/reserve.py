import numpy as np


class ReserveCalculator:

    @staticmethod
    def calculate_reserve(survival_probabilities: np.ndarray, death_probabilities: np.ndarray, premium: float, benefit: float, interest_rate: float)-> tuple[np.ndarray, np.ndarray, np.ndarray]:

        v = 1 / (1 + interest_rate)

        reserve_values = []
        npv_benefits = []
        npv_premiums = []

        for t in range(len(death_probabilities)):

            future_qxt = death_probabilities[t:]
            future_px = survival_probabilities[t:]

            years = np.arange(len(future_qxt))

            benefit_npv = np.sum(benefit * future_qxt * v ** (years + 1))

            premium_npv = np.sum(premium * future_px * v ** years)

            reserve = max(benefit_npv - premium_npv, 0)

            reserve_values.append(round(reserve,2))

            npv_benefits.append(benefit_npv)

            npv_premiums.append(premium_npv)

        return (np.array(reserve_values),
                np.array(npv_premiums),
                np.array(npv_benefits))