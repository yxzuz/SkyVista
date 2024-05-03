import pandas as pd
import numpy as np
import calendar
class Data:
    def __init__(self):
        self._df = pd.read_csv('Flights_Cleaned.csv')

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
        return ['MONTH', 'DAY', 'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'ELAPSED_TIME', 'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN', 'ARRIVAL_DELAY']

    # ['MONTH', 'DAY', 'DAY_OF_WEEK', 'SCHEDULED_DEPARTURE',
    #  'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 'AIR_TIME',
    #  'DISTANCE', 'WHEELS_ON', 'TAXI_IN', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME', 'ARRIVAL_DELAY']
    def filtered_attributes_dist(self, orig, dest):
        return self._df[(self._df.ORIGIN_AIRPORT == orig) & (self._df.DESTINATION_AIRPORT == dest)]


    def mean_groupby_df(self, groupby_attr,mean_attr, df):
        mean_delay_by_atr_serie = df.groupby(groupby_attr)[mean_attr].mean()  # serie
        # print(mean_delay_by_atr_serie)

        return pd.DataFrame(mean_delay_by_atr_serie)  # dataframe

    def merge_df_blank(self, mean_delay_by_month_df):
        month_int = [x for x in range(1, 13)]
        blank_month_df = pd.DataFrame({'MONTH': month_int, 'ARRIVAL_DELAY': 0.0})

        merged_df = pd.merge(blank_month_df, mean_delay_by_month_df, on='MONTH', how='left')
        # print(merged_df)
        merged_df['ARRIVAL_DELAY'] = merged_df['ARRIVAL_DELAY_y'].fillna(merged_df['ARRIVAL_DELAY_x'])
        merged_df.drop(['ARRIVAL_DELAY_x', 'ARRIVAL_DELAY_y'], axis=1, inplace=True)
        return merged_df
        # print(merge_df)

    def all_airlines(self):
        return self._df['AIRLINE'].unique().tolist()

if __name__ == '__main__':
    my_data_class = Data()
    data = my_data_class.df
    # print(data.head().DEPARTURE_TIME)
    # print(my_data_class.mean_groupby_df('MONTH',['ARRIVAL_DELAY'],data))
    filtered = data[(data.ORIGIN_AIRPORT == 'CHS') & (data.DESTINATION_AIRPORT == 'IAH')]
    mean_delay_by_month_df = my_data_class.mean_groupby_df('MONTH', 'ARRIVAL_DELAY', filtered)  # dataframe
    month_int = [x for x in range(1, 13)]
    print(mean_delay_by_month_df)
    blank_month_df = pd.DataFrame({'MONTH': month_int, 'ARRIVAL_DELAY': 0.0})
    print('++++++')

    # print(blank_month_df)
    x = my_data_class.merge_df_blank(mean_delay_by_month_df)
    print(55555)
    print(x)
    print('-------------------------')
    # merged_df = pd.merge(blank_month_df,mean_delay_by_month_df, on='MONTH', how='left')
    # print(merged_df)
    # merged_df['ARRIVAL_DELAY'] = merged_df['ARRIVAL_DELAY_y'].fillna(merged_df['ARRIVAL_DELAY_x'])
    # merged_df.drop(['ARRIVAL_DELAY_x',  'ARRIVAL_DELAY_y'], axis=1, inplace=True)
    # print(merged_df)

    # print(blank_month_df.columns)
    # merge_me =


