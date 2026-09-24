
from math import ceil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_gender_premiums(df:pd.DataFrame, gender: str, face_amount: float):


    filtered_df = df[df["gender"] == gender]

    if gender == 'male':
        colors =[ "#85C6C9", "#16C8F5", "#0C85E7"]
    else: 
        colors = ['pink', 'hotpink', 'violet']

    plt.figure(figsize=(14, 6))

    sns.barplot(
        data=filtered_df,
        x="age",
        y="net_premium",
        hue="risk_class",
        errorbar=None,
        palette = colors, 
        width=.8
        )

    plt.title(f"{gender.title()}, ${face_amount:,}, 20-Year Term, Pure Premium", weight = 'bold', fontfamily = 'serif')
    plt.xlabel("Issue Age", fontfamily = 'serif')

    max = int(filtered_df["net_premium"].max())

    scale_step = round((max/10)/500)*500

    plt.ylabel("Premium", fontfamily = 'serif')
    plt.yticks(np.arange(0, max, step= scale_step))

    plt.legend(labels = ["Super Preferred", 'Preferred', 'Standard'], loc= 'upper center', bbox_to_anchor=(0.5, 1.0), ncols=3, frameon = False)
    plt.tight_layout()
    

    return plt.gcf()


def plot_percent_difference(df:pd.DataFrame, riskclass: str, premium: str, ax):

    filtered_df = (
                df.loc[df["risk_class"].eq(riskclass)]
                .copy()
                )
    
    # Calculate age-to-age percentage change by gender
    filtered_df["perc_diff"] = (
                filtered_df.groupby("age")[premium]
                .pct_change()
                .mul(100)
                .round(2)
                )
                    
    df_pct = filtered_df[['age', 'perc_diff']].dropna(subset=["perc_diff"]).copy()
    
    # Bar plots treat age as a categorical variable, so map each age
    # to its corresponding categorical x-axis position.
    age_order = sorted(filtered_df["age"].unique())
    age_positions = {age: position for position, age in enumerate(age_order)}
    
    df_pct["age_position"] = df_pct["age"].map(age_positions)
    
    sns.lineplot(
                data=df_pct,
                x="age_position",
                y="perc_diff",
                marker="o",
                ax=ax,
                color = 'red',
                legend=False
                )
    
    
    max = int(df_pct['perc_diff'].max()) 
    scale_step = round((max/11)/5)*5
    
    ax.set_ylabel("Premium Difference (%)", fontfamily="serif")
    ax.set_yticks(np.arange(0, max + 10, step= scale_step))
    ax.legend(labels = ['Male & Female Premium Diff (%)'], loc= 'upper center', bbox_to_anchor=(0.5,.95), ncols=1, frameon = False)
    
    return ax


def plot_riskclass_premiums(df: pd.DataFrame, riskclass: str, face_amount: float, gross_prem = False, percent_diff = False):

    filtered_df = df[df["risk_class"] == riskclass]

    fig, ax1 = plt.subplots(figsize=(16, 6))

    if gross_prem:
        premium = 'gross_premium'
        label = 'Gross Premium'
    else: 
        premium = 'net_premium'
        label = 'Pure Premium'

    sns.barplot(
        data=filtered_df,
        x="age",
        y= premium,
        hue="gender",
        errorbar=None,
        palette = ['hotpink', 'dodgerblue'],
        ax = ax1, width= .7
        )

    if percent_diff:
        ax2= ax1.twinx()
        plot_percent_difference(df= filtered_df, riskclass= riskclass, premium = premium, ax= ax2)

    if riskclass == 'superpreferred':
        riskclass = 'Super Preferred'
        
    ax1.set_title(f"{riskclass.title()}, ${face_amount:,}, 20-Year Term, {label}", weight = 'bold', fontfamily = 'serif')
    ax1.legend(labels = ['Female', 'Male'], loc= 'upper center', bbox_to_anchor=(0.5, 1.0), ncols=2, frameon = False)

    ax1.set_xlabel("Issue Age", fontfamily = 'serif')
    ax1.set_xlim(-0.50, len(filtered_df["age"].unique()) - 0.45)

    max = int(filtered_df[premium].max()) 
    scale_step = round((max/10)/500)*500

    ax1.set_ylabel("Premium", fontfamily = 'serif')
    ax1.set_yticks(np.arange(0, max + 4000, step= scale_step))

    
    fig.tight_layout()
    

    return fig


def plot_term_reserves(
        reserve_values, 
        prem_npv, 
        bene_npv, 
        term_duration
        ):

        x_values = np.arange(len(prem_npv))
        width = 0.35

        max_idx = np.argmax(reserve_values)
        max_reserve = reserve_values[max_idx]

        fig, (ax1, ax2) = plt.subplots(nrows=2,figsize=(12, 10))

        # ------------------
        # NPV Bar Chart
        # ------------------
        ax1.bar(x_values - width / 2, prem_npv, width=width,
                color="dodgerblue",
                label="NPV Future Premiums"
                )

        ax1.bar(x_values + width / 2, bene_npv,
                width=width,
                color="navy",
                label="NPV Future Death Benefits"
                )

        ax1.set_xlabel(
                "Policy Year",
                fontsize=10,
                fontfamily="serif"
                )

        ax1.set_xticks(x_values)
        ax1.set_xticklabels(np.arange(1, len(prem_npv) + 1))
        ax1.set_xlim(-0.5, len(prem_npv) - 0.5)

        ax1.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15),
                ncols=2,
                frameon=False, fontsize = 10
                )

        # ------------------
        # Reserve Line Plot
        # ------------------
        sns.lineplot(x=x_values, y=reserve_values,
        marker="o", color="#85a1b8", ax=ax2
        )

        ax2.plot(max_idx, max_reserve,
                marker="o", color="red",
                markersize=6
                
                )


        ax2.set_xticks(x_values)
        ax2.set_xticklabels(np.arange(1, len(prem_npv) + 1))

        if 100000 < max_reserve:
                scale_step = ceil((max_reserve/10)/20000)*20000
                label_offset = 10000


        elif 50000 <= max_reserve <= 100000:
                scale_step = ceil((max_reserve/10)/5000)*5000
                label_offset = 5000

                
        elif  30000 <= max_reserve < 50000:
                scale_step = ceil((max_reserve/10)/2000)*2000
                label_offset = 2000

                
        elif max_reserve < 30000:
                scale_step = ceil((max_reserve/10)/500)*500
                label_offset = 700

                
        ax2.set_yticks(
        np.arange(0, max_reserve + scale_step, scale_step)
        )

        
        ax2.annotate(
                f"${max_reserve:,.2f}",
                xy=(max_idx, max_reserve),
                xytext=(max_idx, max_reserve + label_offset),
                color="red",
                fontsize=9,
                ha="center",
                )

        ax2.set_xlabel("Policy Year",
                fontsize=10,
                fontfamily="serif"
                )

        ax2.set_title( f"{term_duration}-Year Term Insurance Net Premium Reserve\n",
                        fontsize = 10
                        )

        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        plt.subplots_adjust(hspace=.6)
        

        return fig