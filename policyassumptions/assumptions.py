from dataclasses import dataclass

@dataclass(frozen=True)
class Assumptions:
    interest_rate: float
    expense_ratio: float
    policy_fee: float
    acquisition_cost: float