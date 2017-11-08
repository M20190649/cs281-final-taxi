import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook as tqdm
import torch
from torch.autograd import Variable
from torch import Tensor
import io
# import requests


def filter_coords(df):
  """
  Filter coordinates on df to trim unreasonable coordinates.

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


def filter_durations(df):
  """
  Filter durations on df to trip unreasonable durations (i.e. negative values
  and durations that are too long.

  Inputs
  ------
  df : pd.DataFrame
      Dataframe you want to filter.

  Returns
  -------
  df : pd.DataFrame
      Filtered DataFrame
  """

  return df[(df.duration > 0) & (df.duration < 24 * 60 * 60)]


def filter_cols(df):
  """
  Get columns we want. DEPRECATED.
  """
  cols = [
      'Trip_Pickup_DateTime',
      'Trip_Dropoff_DateTime',
      'Trip_Distance',
      'Start_Lon',
      'Start_Lat',
      'End_Lon',
      'End_Lat',
  ]

  h = df[cols]
  h['Trip_Dropoff_DateTime'] = pd.to_datetime(h['Trip_Dropoff_DateTime'])
  h['Trip_Pickup_DateTime'] = pd.to_datetime(h['Trip_Pickup_DateTime'])
  return h


def df_to_torch(df_clean):
  y = Variable(
      torch.from_numpy(
          df_clean['duration'].as_matrix()
      ).float(),
      requires_grad=False)

  x = Variable(
      torch.from_numpy(
          df_clean.drop(['duration'],
                        axis=1).as_matrix()
      ).float())

  return x, y


def unnormalize(df):
  """
  unnormalize Start_Lon, Start_Lat, End_Lon, End_Lat
  """
  df['start_lon_raw'] = - 73.97826142142969 + \
      0.0239235715736219 * df['Start_Lon']
  df['start_lat_raw'] = 40.753207908605766 + \
      0.02262721225173857 * df['Start_Lat']
  df['end_lon_raw'] = -73.97635609080373 + 0.025989097948950303 * df['End_Lon']
  df['end_lat_raw'] = 40.753145629515345 + 0.025820804247699374 * df['End_Lat']
  return df


def filter_manhattan(df):
  def lower(x): return (40.84 - 40.66) / (74.03 - 73.87) * x + \
      (40.66 - (40.84 - 40.66) / (74.03 - 73.87) * -74.03)

  def upper(x): return (40.7 - 40.86) / (-74.05 + 73.93) * x + \
      (40.7 - (40.7 - 40.86) / (-74.05 + 73.93) * -74.05)

  return df[(df['start_lat_raw'] > lower(df['start_lon_raw']))
            & (df['start_lat_raw'] < upper(df['start_lon_raw']))
            & (df['end_lat_raw'] > lower(df['end_lon_raw']))
            & (df['end_lat_raw'] < upper(df['end_lon_raw']))]


def rotate_manhattan(df):
  rotmat = np.array([[0.82764898, -0.56124608],
                     [0.56124608, 0.82764898]])
  starts = df[['start_lon_raw', 'start_lat_raw']].as_matrix() @ rotmat.T
  df['start_x'] = (starts[:, 0] + 84.125113) / 0.005
  df['start_y'] = (starts[:, 1] + 7.853407) / 0.005

  ends = df[['end_lon_raw', 'end_lat_raw']].as_matrix() @ rotmat.T
  df['end_x'] = (ends[:, 0] + 84.125113) / 0.005
  df['end_y'] = (ends[:, 1] + 7.853407) / 0.005
  return df


def affine_transform(vec):
  rotmat = np.array([[0.82764898, -0.56124608],
                     [0.56124608, 0.82764898]])
  return (rotmat @ vec + np.array([84.125113, 7.853407])) / 0.005


def inverse_affine_transform(vec):
  rotmat = np.array([[0.82764898, -0.56124608],
                     [0.56124608, 0.82764898]])
  return np.inv(rotmat) @ (0.005 * vec - np.array([84.125113, 7.853407]))
