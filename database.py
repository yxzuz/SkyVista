import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
# %matplotlib inline
df = pd.read_csv('flights_cut_20240418.csv')
# print(df.shape)
print(df.columns)
print(df[df.CANCELLED == 1])
# print(df)
class Data:
    def __init__(self):
        pass

    def origin(self, dest=None) -> list:
        """
        :param dest: str
        :return: list of airports corresponding to the origin
        """
        pass

    def destination(self, orig=None) -> list:
        """
        :param orig: str
        :return: list of airports corresponding to the destination
        """



