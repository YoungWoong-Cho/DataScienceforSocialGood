import pandas as pd

def read_xlsx(fpath):
    data = pd.read_excel(fpath)
    return data

def inspect(output):
    lhs         = [tuple(result[2][0][0])[0] for result in output]
    rhs         = [tuple(result[2][0][1])[0] for result in output]
    support    = [result[1] for result in output]
    confidence = [result[2][0][2] for result in output]
    lift       = [result[2][0][3] for result in output]
    result = list(zip(lhs, rhs, support, confidence, lift))
    return pd.DataFrame(result, columns = ['Left_Hand_Side', 'Right_Hand_Side', 'Support', 'Confidence', 'Lift'])