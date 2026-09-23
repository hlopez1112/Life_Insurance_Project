import numpy as np



def apv_annuity_due(survival_probabilities: np.ndarray, interest_rate: float)-> float:
    """
    Calculate the actuarial present value (APV) of an annuity due using annual survival probabilities and interest rate.
    Returns: float: the actuarial present value of the annuity due.
    """
    discount = (1 + interest_rate) ** (-np.arange(len(survival_probabilities)))

    return np.dot(survival_probabilities, discount)


def apv_benefit(probability_dying: np.ndarray, interest_rate: float)-> float:
    """
    Calculate the actuarial present value (APV) of a future benefit using annual death probabilities and interest rates.
    Returns: float: The actuarial present value of the future benefit.
    """
    discount = (1 + interest_rate) ** (-np.arange(1,len(probability_dying) + 1,))

    return np.dot(probability_dying,discount)


def net_premium(benefit: float, apv_benefit: float, apv_annuity: float) -> float:
    """
    Calculate the net premium for a life insurance policy based on the benefit amount and actuarial present values.
    Returns: float: the net premium.
    """
    return ((apv_benefit/apv_annuity)* benefit)


def gross_premium(net_premium: float, assumptions, apv_annuity: float):
    """
    Calculate the gross premium for a life insurance policy based on the net premium, policy fees, acquisition costs, and expense ratio.
    Returns: float: the gross premium.
    """
    acquisition_load = (assumptions.acquisition_cost/apv_annuity)

    return (net_premium + assumptions.policy_fee + acquisition_load) / (1 - assumptions.expense_ratio)