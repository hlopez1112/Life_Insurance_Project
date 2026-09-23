import actuarial.mortality_utils as MortalityCalculator
import actuarial.premium_utils as PremiumCalculator


class PricingService:
    """
    A service for calculating life insurance premiums based on mortality data and policy assumptions.
    Returns a dictionary containing survival probabilities, death probabilities, actuarial present values, and calculated premiums.
    """
    def __init__(self, mortality_df):

        self.mortality_df = mortality_df

    def quote(self, policy, assumptions):

        mortality_rates = (MortalityCalculator.get_qx(self.mortality_df, policy.issue_age, policy.risk_class, policy.gender))

        survival_probabilities, death_probabilities = (MortalityCalculator.death_probabilities(mortality_rates , policy.term_duration))

        apv_ann = (PremiumCalculator.apv_annuity_due(survival_probabilities, assumptions.interest_rate))

        apv_bene = (PremiumCalculator.apv_benefit(death_probabilities, assumptions.interest_rate))

        net_premium = (PremiumCalculator.net_premium(policy.face_amount, apv_bene, apv_ann))

        gross_premium = (PremiumCalculator.gross_premium(net_premium, assumptions, apv_ann))

        return {
        "survival_probabilities": survival_probabilities,
        "death_probabilities": death_probabilities,
        'apv_ann': apv_ann,
        'apv_benefit': apv_bene,
        "net_premium": round(net_premium,2),
        "gross_premium": round(gross_premium,2),
        }