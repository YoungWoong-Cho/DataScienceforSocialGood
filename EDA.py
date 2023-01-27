import utils as utils
import pandas as pd
from apyori import apriori

if __name__ == '__main__':
    survey = utils.read_xlsx('./data/survey.xlsx')
    
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
    print(results)

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