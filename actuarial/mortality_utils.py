import numpy as np
import pandas as pd



def get_qx(df: pd.DataFrame, age: int, risk_class: str, gender: str) -> np.ndarray:

    '''
    Lookup the mortality rates for a given age, risk class, and gender from the provided DataFrame.
    Returns a numpy array of mortality rates for the specified age, risk class, and gender.
    '''

    # Create a boolean mask to filter the DataFrame based on the provided age, risk class, and gender
    mortality_lookup = (df.set_index(["issue_age", "risk_class", "gender"]))

    try:
        return mortality_lookup.loc[(age, risk_class, gender)]
    except KeyError:
        raise ValueError(f"No mortality data for age {age}, risk class {risk_class}, and gender {gender}")


def death_probabilities(mortality_values: np.ndarray, term: int)-> tuple[np.ndarray, np.ndarray]:
    '''
    Calculate the survival and death probabilities for a given term based on mortality values.  
    Returns a tuple containing two numpy arrays: survival probabilities and death probabilities.
    '''

    # initialize survival probabilities and death probabilities arrays
    mortality_term = mortality_values[:term]
    survival_probabilities = np.empty_like(mortality_term)

    survival_probabilities[0] = 1

    # Calculate the survival probabilities and death probabilities for each year in the term
    survival_probabilities[1:] = np.cumprod(1 - mortality_term)[:-1]
    death_probabilities = survival_probabilities * mortality_term

    return survival_probabilities, death_probabilities