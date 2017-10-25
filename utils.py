import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from tqdm import tqdm_notebook as tqdm
import torch
from torch.autograd import Variable
from torch import Tensor
import io
# import requests

def filter_coords(df):
    """
    filter coordinates on df to trim unreasonable coordinates

    Inputs
    -----
    df : pd.DataFrame
        DataFrame wanting to filter

    Returns
    -----
    df : pd.DataFrame
        Filtered DataFrame
    """
    lon_l, lon_r = -74.1, -73.7
    lat_l, lat_r = 40.65, 40.85

    for c in filter(lambda c: c.endswith('_Lon'), df.columns):
        df = df[(df[c] <= lon_r) & (df[c] >= lon_l)]

    for c in filter(lambda c: c.endswith('_Lat'), df.columns):
        df = df[(df[c] <= lat_r) & (df[c] >= lat_l)]

    return df

def filter_cols(df):
    """
    Get columns we want
    """
    cols = ['Trip_Pickup_DateTime', 'Trip_Dropoff_DateTime', 'Trip_Distance','Start_Lon',
        'Start_Lat','End_Lon','End_Lat']

    h = df[cols]
    h['Trip_Dropoff_DateTime'] = pd.to_datetime(h['Trip_Dropoff_DateTime'])
    h['Trip_Pickup_DateTime'] = pd.to_datetime(h['Trip_Pickup_DateTime'])
    return h

def df_to_torch(df_clean):
    y = Variable(torch.from_numpy(df_clean['duration'].as_matrix()).float(),requires_grad=False)
    x = Variable(torch.from_numpy(df_clean.drop(['duration'], axis=1).as_matrix()).float())
    return x, y

