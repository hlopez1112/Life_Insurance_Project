# **🛡️ Term Life Insurance Pricing & Needs Analysis Engine**

## **Overview**

This project is a Python-based actuarial term pricing exercise that demonstrates the principles behind term life insurance pricing, needs-based life insurance analysis, and reserve calculations.

The model estimates level term insurance premiums using mortality assumptions, projects policy reserves, analyzes premium differences across underwriting classes and genders, and determines recommended coverage amounts using the Needs Approach commonly used in financial planning and life insurance sales.

The goal of this project is to showcase an understanding of actuarial concepts including:
  * Mortality modeling
  * Present value calculations
  * Net and gross premium determination
  * Reserve development
  * Underwriting risk classification
  * Needs-based life insurance analysis

## **Key Features**
## **Term Insurance Pricing**

Calculate:
  * Net premiums
  * Gross premiums
  * Present value of future premiums
  * Present value of future death benefits

The pricing model incorporates mortality assumptions and interest rate discounting to determine level annual premiums.

## **Reserve Analysis**

Project and visualize annual policy reserves throughout the term duration.
The reserve analysis chart:
  * Displays policy reserves for each policy year
  * Highlights the maximum reserve value
  * Shows reserve emergence and runoff over the life of the policy
    
**Key Findings**
  * Reserves increase during the early policy years.
  * The maximum reserve occurs in Policy Year 13.
  * Reserves begin declining around Policy Year 15 as future liabilities decrease and the remaining coverage period shortens.

## **Underwriting Risk Class Analysis**

Compare premiums across three common underwriting classes:
  * Super Preferred Non-Tobacco
  * Preferred Non-Tobacco
  * Standard Non-Tobacco


**Risk Class Premium Charts**

Model generates visualizations illustrating pure premiums across multiple issue ages.

**Key Findings**
* Super Preferred premiums are the lowest.
* Standard premiums are the highest.
* Premiums increase as issue age increases.
* The highest premiums occur at older ages within the Standard risk class.


**Male vs. Female Premium Analysis**

Compare premium rates between genders across underwriting classes.

**Key Findings**
* Female premiums are consistently lower than male premiums.
* Premiums increase with age for both genders.
* Premium differences are smallest around the mid-30s.
* Premium differences widen beginning around age 40 as mortality differences become more pronounced.

## **Actuarial Assumptions**
The pricing model utilizes mortality assumptions derived from industry mortality tables.
Potential assumptions include:
  * 2015 VBT
  * Relative Risk Multiples (RR)

Example:

Risk Class         | 2015 VBT RR  |
---                |---           |
Super Preferred NT | RR60         |
Preferred NT	     | RR80         |
Standard NT	       | RR100        |

Future Enhancements

## **Planned improvements include:**
* Adjustment to the mortality rates based on carrier experience
* Expense assumptions
* Policy lapse assumptions
* Cash value illustrations
