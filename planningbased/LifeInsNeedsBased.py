# %%
class NeedsBasedCalculator:

    def __init__(self, age: int, annual_income: float):
        self.age = age
        self.annual_income = annual_income
        self.expenses = 0
        self.income_replacement = 0
        self.education_expenses = 0 

        self.existing_life_insurance = 0
        self.existing_assets = 0 

    def set_expenses(self, mortgage: float, auto_loan: float, credit_card: float, burial: float, estate: float):
        self.expenses = mortgage + auto_loan + credit_card + burial + estate

    def set_education_expenses(self, college_fund: float, k_12: float):
        self.education_expenses = college_fund + k_12

    def set_income_replacement(self, years_to_replace: int, percentage_to_replace: float = .80):
        self.income_replacement = self.annual_income *years_to_replace*percentage_to_replace

    def set_existing_assets(self, cash_savings: float, investments: float, retirement_account: float, lifeinsurance: float):
        self.existing_assets = cash_savings + investments + retirement_account
        self.existing_life_insurance = lifeinsurance

    def calc_needs_based(self):
        self.total_obligations = self.expenses + self.education_expenses + self.income_replacement
        self.total_assets = self.existing_assets + self.existing_life_insurance
        self.net_need = max(0, self.total_obligations - self.total_assets)

    def client_summary(self) -> dict:

        return {
            "age": self.age,
            "annual_income": self.annual_income,
            "expenses": round(self.expenses, 2),
            "education": round(self.education_expenses, 2),
            "income_replacement": round(self.income_replacement, 2),
            "total_obligations": round(self.total_obligations, 2),
            "total_assets": round(self.total_assets, 2),
            "net_insurance_need": round(self.net_need, 2)}



    


