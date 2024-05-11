"""Model in MVC"""
import pandas as pd
class Data:
    """this class read csv and provides method for manipulating data"""
    def __init__(self):
        self._df = pd.read_csv('Flights_Cleaned.csv')

    @property
    def df(self):
        """original dataframe getter"""
        return self._df

    def all_origin(self, dest=None) -> list:
        """list of airports corresponding to the origin"""
        if dest is None:
            return self._df.ORIGIN_AIRPORT.unique().tolist()
        filtered = self._df[self._df.ORIGIN_AIRPORT == dest]
        return filtered.DESTINATION_AIRPORT.unique().tolist()

    def all_destination(self, orig=None) -> list:
        """list of airports corresponding on origin airport"""
        if orig is None:
            return self._df.DESTINATION_AIRPORT.unique().tolist()
        filtered = self._df[self._df.ORIGIN_AIRPORT == orig]
        return filtered.DESTINATION_AIRPORT.unique().tolist()

    def all_attributes(self):
        """return all attribute"""
        return ['MONTH', 'DAY', 'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF',
                'ELAPSED_TIME', 'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN', 'ARRIVAL_DELAY']

    def num_attributes(self):
        """return numerical attributes"""
        return ['DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'ARRIVAL_DELAY',
               'ELAPSED_TIME', 'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN']

    def filtered_attributes_dist(self, orig, dest):
        """return filtered dataframe based on origin and destination airport"""
        return self._df[(self._df.ORIGIN_AIRPORT == orig) & (self._df.DESTINATION_AIRPORT == dest)]

    def create_series(self, col, values):
        """create a series from dictionary"""
        temp_dict = {}
        for column, value in zip(col, values):
            temp_dict[column] = value
        temp = pd.Series(temp_dict)
        return temp

    def mean_groupby_df(self, groupby_attr, mean_attr, df):
        """find mean, groupby and return new dataframe"""
        mean_delay_by_atr_serie = df.groupby(groupby_attr)[mean_attr].mean()  # series
        return pd.DataFrame(mean_delay_by_atr_serie)  # dataframe

    def merge_df_blank(self, mean_delay_by_month_df, agg_attribute):
        """merge dataframe and aggregate"""
        month_int = list(range(1, 13))
        blank_month_df = pd.DataFrame({'MONTH': month_int, agg_attribute: 0.0})
        merged_df = pd.merge(blank_month_df, mean_delay_by_month_df, on='MONTH', how='left')
        label_x = agg_attribute + '_x'
        label_y = agg_attribute + '_y'
        merged_df[agg_attribute] = merged_df[label_y].fillna(merged_df[label_x])
        merged_df.drop([label_x, label_y], axis=1, inplace=True)
        return merged_df

    def all_airlines(self):
        """return list of all airlines"""
        return self._df['AIRLINE'].unique().tolist()

    def get_correlation(self, df, x, y):
        """return correlation of x and y"""
        return round(df[x].corr(df[y]), 2)
