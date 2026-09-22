import numpy as np


class PremiumCalculator:

    @staticmethod
    def apv_annuity_due(survival_probabilities: np.ndarray, interest_rate: float)-> float:

        discount = (1 + interest_rate) ** (-np.arange(len(survival_probabilities)))

        return np.dot(survival_probabilities, discount)

    @staticmethod
    def apv_benefit(probability_dying: np.ndarray, interest_rate: float)-> float:

        discount = (1 + interest_rate) ** (-np.arange(1,len(probability_dying) + 1,))

        return np.dot(probability_dying,discount)

    @staticmethod
    def net_premium(benefit: float, apv_benefit: float, apv_annuity: float) -> float:

        return ((apv_benefit/apv_annuity)* benefit)

    @staticmethod
    def gross_premium(net_premium: float, assumptions, apv_annuity: float):

        acquisition_load = (assumptions.acquisition_cost/apv_annuity)

        return (net_premium + assumptions.policy_fee + acquisition_load) / (1 - assumptions.expense_ratio)