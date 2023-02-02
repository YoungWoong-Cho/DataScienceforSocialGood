import utils as utils
import pandas as pd
from apyori import apriori
import seaborn as sns
import matplotlib.pyplot as plt


def market_basket():
    # Select data that has small number of categories
    # Can be replaced by choosing desired columns only (e.g. household size, race, etc)
    unique_answer_thres = 3
    survey = survey[[col for col in survey.columns if len(pd.unique(survey[col])) <= unique_answer_thres]]
    
    # Arbitrarily choose first 8 columns. If you use all columns, it takes so much time
    # Should find a better way to speed up (by filtering) and get rid of this line
    survey = survey.iloc[:, :8]

    # Create market basket data
    basket = []
    for row in range(len(survey)):
        transaction = []
        for col in survey.columns:
            if str(survey[col][row]) != 'nan':
                # Create an item data in a form of '{question}{answer}'
                # For example: 'Do you currently receive EITC (Earned Income Tax Credit) or other income-based tax relief?Yes'
                item = col + str(survey[col][row])
                transaction.append(item)
        basket.append(transaction)

    results = list(apriori(basket, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2))
    results = utils.inspect(results)
    return results
    """
    Sample output:
                                            Left_Hand_Side                                    Right_Hand_Side   Support  Confidence      Lift
    0    Do you currently receive SSI (Supplemental Sec...  Do you currently receive Rental Assistance, th...  0.011804    0.333333  5.647619
    1    Do you currently receive TANF assistance (Temp...  Do you currently receive SNAP/WIC (Supplementa...  0.037099    0.846154  3.982295
    2    Do you currently receive EITC (Earned Income T...  Do you currently receive Medicaid, CHIP (Child...  0.011804    0.875000  3.242969
    3    Do you currently receive EITC (Earned Income T...  Do you currently receive Rental Assistance, th...  0.003373    0.222222  3.765079
    4    Do you currently receive TANF assistance (Temp...  Do you currently receive EITC (Earned Income T...  0.011804    0.269231  3.130468
    ..                                                 ...                                                ...       ...         ...       ...
    799  Do you currently receive SSI (Supplemental Sec...        Do you currently receive Social Security?No  0.003373    0.333333  5.647619
    800  Do you currently receive Rental Assistance, th...        Do you currently receive Social Security?No  0.023609    0.205882  3.052206
    801  Do you currently receive EITC (Earned Income T...        Do you currently receive Social Security?No  0.005059    0.500000  7.602564
    802  Do you currently receive TANF assistance (Temp...        Do you currently receive Social Security?No  0.008432    0.555556  7.661499
    803  Do you currently receive Rental Assistance, th...        Do you currently receive Social Security?No  0.005059    0.272727  4.043182
    """

def correlation():
    debt_cols = ['How much (bank loans)?',
                'How much (car/auto)?',
                'How much (credit card)?',
                'How much (mortgage/housing)?',
                'How much (other)?',
                'How much (student/education)?']
    numeric_cols = ['What is your household size (how many people live in your home, including you)?',
                    'How much do you have in savings?',
                    'Completed Loan Cycles',
                    'Loans Balance']
    categorical_cols = ['How many hours per week do you dedicate to your business activity?',
                        'How many hours per week do you dedicate to a job or other income-generating activities OUTSIDE of your business?',
                        'How much money do you spend on your business activity each month?',
                        'How much money do you earn from the business each month before expenses?',
                        'LAST MONTH, what was YOUR total income/total contribution to the household income (including wages from a job, business income, government or other benefits, child support, and any other form of income?',
                        'LAST MONTH, what was the REST OF YOUR HOUSEHOLD\'s contribution (not including yours) to the household income?',
                        'What is the current balance in this CHECKING account / Cual es el balance actual en esta cuenta CORRIENTE? ($)']
    optimism_cols = ['Most people are basically honest',
                     'The people in my social circle are basically honest',
                     'Most people are basically good and kind',
                     'The people in my social circle are basically good and kind',
                     'Most people are trustful of others',
                     'The people in my social circle are trustful of others',
                     'Most people are trustworthy',
                     'The people in my social circle are trustworthy']
    CATEGORY_TO_NUMERIC = {
        'Strongly Disagree': 1.0,
        'Disagree': 2.0,
        'Neither Agree Nor Disagree': 3.0,
        'Agree': 4.0,
        'Strongly Agree': 5.0
    }

    data = utils.read_xlsx('./data/survey.xlsx')


    # NUMERIC DF
    # Sum up debt and include it to numeric df
    debt = data[debt_cols].fillna(0)
    debt = debt.sum('columns')
    numeric = data[numeric_cols]
    numeric['What is your household size (how many people live in your home, including you)?'] = numeric['What is your household size (how many people live in your home, including you)?'].fillna(1)
    numeric['How much do you have in savings?'] = numeric['How much do you have in savings?'].fillna(0)
    numeric['debt'] = debt.values

    # Get an optimism scores
    # Fill NaN as Neither Agree Nor Disagree value
    optimism = data[optimism_cols].fillna(3.0)
    for col in optimism.columns:
        for key, val in CATEGORY_TO_NUMERIC.items():
            optimism.loc[optimism[col] == key, col] = val
    numeric['optimism_score'] = optimism.sum('columns')
    numeric.rename(columns={"What is your household size (how many people live in your home, including you)?": "Household size",
                            "How much do you have in savings?": "Amount in savings"}, inplace=True)
    sns.pairplot(numeric, kind="reg", plot_kws={'line_kws':{'color':'red'}})
    plt.savefig('plot.png')
    sns.pairplot(numeric, kind="reg", hue='Household size')
    plt.savefig('plot2.png')


if __name__ == '__main__':
    correlation()
