import utils as utils
import pandas as pd
from apyori import apriori

if __name__ == '__main__':
    survey = utils.read_xlsx('./data/survey.xlsx')
    unique_answer_thres = 3
    survey = survey[[col for col in survey.columns if len(pd.unique(survey[col])) <= unique_answer_thres]]
    survey = survey.iloc[:, :8]

    # Create market basket data
    basket = []
    for row in range(len(survey)):
        transaction = []
        for col in survey.columns:
            if str(survey[col][row]) != 'nan':
                item = col + str(survey[col][row])
                transaction.append(item)
        basket.append(transaction)
    

    results = list(apriori(basket, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2))
    results = utils.inspect(results)
    print(results)