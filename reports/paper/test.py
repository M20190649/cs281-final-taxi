import numpy as np
from tqdm import tqdm_notebook as tqdm
import pandas as pd
import json
import pickle

def test(predict, result_file,
         test_file="data/split_test/JC_week1_hour8_test_40x140.csv"):
    df = pd.read_csv(test_file)
    df = df.loc[:, ['duration', 'sx', 'sy', 'tx', 'ty']]


    errs = []
    for _, duration, sx, sy, tx, ty in tqdm(df.itertuples()):
        pred = predict(sx, sy, tx, ty)
        errs.append(duration - pred)

    errs = pd.Series(errs)

    stat = {
        'sd_duration' : df['duration'].std(),
        'mean_err': errs.mean(),
        'sd_err': errs.std(),
        'mean_abs_err': errs.abs().mean(),
        'median_abs_err': errs.abs().median(),
        '99pct_abs_err' : np.percentile(errs.abs(), 99),
        'test_r2' : 1 - np.std(errs) ** 2 / (df['duration'].std() ** 2)
    }

    json.dump(stat, open(result_file, 'w'))
    pickle.dump(errs, open(result_file + '.raw', 'wb'))

    return errs
