import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
# %matplotlib inline
# df = pd.read_csv('flights_cut_20240418.csv')
# print(df.shape)
# print(df.columns)
# print(df[df.CANCELLED == 1])
# print(df)
class Data:
    def __init__(self):
        self._df = pd.read_csv('flights_cut_20240418.csv')

    @property
    def df(self):
        return self._df

    def all_origin(self, dest=None) -> list:
        """
        :param dest: str
        :return: list of airports corresponding to the origin
        """
        if dest is None:
            return self._df.ORIGIN_AIRPORT.unique().tolist()
        filtered = self._df[self._df.ORIGIN_AIRPORT == dest]
        return filtered.DESTINATION_AIRPORT.unique().tolist()

    def all_destination(self, orig=None) -> list:
        """
        :param orig: str
        :return: list of airports corresponding to the destination
        """
        if orig is None:
            return self._df.DESTINATION_AIRPORT.unique().tolist()
        filtered = self._df[self._df.ORIGIN_AIRPORT == orig]
        return filtered.DESTINATION_AIRPORT.unique().tolist()

    def all_attributes(self):
        return ['MONTH', 'DAY', 'DAY_OF_WEEK', 'SCHEDULED_DEPARTURE',
                'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME', 'ARRIVAL_DELAY']
    def filtered_attributes_dist(self, orig, dest):
        return self._df[(self._df.ORIGIN_AIRPORT == orig) & (self._df.DESTINATION_AIRPORT == dest)]

    def all_airlines(self):
        return self._df['AIRLINE'].unique().tolist()

if __name__ == '__main__':
    my_data_class = Data()
    data = my_data_class.df
    # print(my_data_class.all_origin())
    # print(type(data['AIRLINE'].unique()))

    print(my_data_class.all_attributes())
    # filtered = data[data.ORIGIN_AIRPORT == 'PHX']
    # print(filtered.loc[:,['ORIGIN_AIRPORT','DESTINATION_AIRPORT']])
    #       # (['ORIGIN_AIRPORT','DESTINATION_AIRPORT'],:)
    # print(filtered.DESTINATION_AIRPORT.unique().tolist())


