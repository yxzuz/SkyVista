
# for controller
from database import Data
from app import UI,UI1,UI2
import numpy as np

class Controller:
    def __init__(self,data):
        self.data = data
        #default
        # self.ui1 = UI1(self,self.data.df)
        # self.ui2 = None
        # self.state = 1
        # page 2 first
        self.state = 2
        self.ui2 = UI2(self, self.data.df)

    def switch_mode(self, mode):
        # change application state and switch the mode
        print('state', self.state)
        if mode == 'Explore' and self.state == 2:
            self.ui2.destroy()
            self.ui1 = UI1(self, self.data.df)
            self.state = 1
            # self.ui1.run()
            # self.ui2.destroy()
        elif mode == 'Story' and self.state == 1:
            self.ui1.destroy()
            self.ui2 = UI2(self, self.data.df)
            self.state = 2
            # self.ui2.run()

    def run(self):
        # self.ui1.run()
        #page 2 first
        self.ui2.run()

    def df_groupby(self, groupby_attr, mean_attr, df):
        # return dataframe of groupby atr and find mean
        return self.data.mean_groupby_df(groupby_attr, mean_attr, df)


    def get_unique_airlines(self,df):
        return df.AIRLINE.unique().tolist()

    def get_all_origin(self):
        return self.data.all_origin()

    def get_all_dest(self,orig):
        self.ui2.pick_dest['values'] = self.data.all_destination(orig)
        # return self.data.all_destination(orig)

    def filter_origin_and_dest(self, orig, dest):
        self.ui2.temp_data = self.data.filtered_attributes_dist(orig, dest)

    def get_all_attributes(self):
        return self.data.all_attributes()

    def get_all_airlines(self):
        return self.data.all_airlines()

    def stat_columns(self):
        columns_atr = ["STATISTICS",'ARRIVAL_DELAY', 'AIR_TIME', 'DISTANCE', 'ELAPSED_TIME']
        stat = ['mean', 'std', 'min', 'q1', 'q2', 'q3', 'max']
        label = ['Statistics', 'Arrival delay', 'Air time', 'Distance','Elapsed time']
        return columns_atr, stat, label

    def tree_view_data(self, stat, df):
        function = {
            'mean': lambda df: round(df.mean(),2).tolist(),
            'std': lambda df: round(df.std(), 2).tolist(),
            'min': lambda df: df.min().tolist(),
            'q1': lambda df: round(df.quantile(0.25),2).tolist(),
            'q2': lambda df: round(df.quantile(0.50),2).tolist(),
            'q3': lambda df: round(df.quantile(0.75),2).tolist(),
            'max': lambda df: df.max().tolist()
        }
        data = {
        #     # "mean": [6.6, 158.6, 925.0, 179.4]
        #     # "std": [19.58, 12.6, 0.0, 17.34],
        #     # "min": [-15.0, 141.0, 925.0, 158.0],
        #     # "q1": [-2.0, 151.0, 925.0, 166.0],
        #     # "q2": [-1.0, 163.0, 925.0, 182.0],
        #     # "q3" : [15.0, 165.0, 925.0, 191.0],
        #     # "max" : [36.0, 173.0, 925.0, 200.0]
        #
        #
        #     # "ARRIVAL_DELAY": [4.494781, 60.054968, -56, -15, -6, 7, 1201],
        #     # "AIR_TIME": [118.202505, 74.476176, 32, 57, 103, 160, 423],
        #     # "DISTANCE": [800.959041, 573.256670, 184, 280, 666, 1242, 2611],
        #     # "ELAPSED_TIME": [145.739040, 76.236987, 49, 90, 129, 185.75, 447],
        }
        # print(df.head())
        tree_view = []
        for row in stat:
            lst = function[row](df)
            data[row] = lst
            # tree_view.append((row, lst))
        # print(7777,data)
        # for row in range(len(col)):
        # function['mean'](my_df)



        for index, c in zip(stat, range(len(stat))):
            temp = []
            temp.append(index)
            for val in data[index]:
                temp.append(val)
            tree_view.append(temp)
            # tree_view.append((index, data[index][c], data[index][c], data[index][c], data[index][c]))
        return tree_view

    def get_airline_data(self, airline,ui_num=1):
        # return list corresponding to airline picked for combobox pick_origin
        # print('airline:', airline)
        # print(ui_num)
        if ui_num == 1:
            self.ui1.temp_data = self.data.df[self.data.df.AIRLINE == airline] # update temp data
            self.ui1.pick_origin['values'] = self.data.df[self.data.df.AIRLINE == airline].ORIGIN_AIRPORT.unique().tolist() # set value for origin
        else:
            self.ui2.temp_data = self.data.df[self.data.df.AIRLINE == airline] # update temp data
            self.ui2.pick_origin['values'] = self.data.df[self.data.df.AIRLINE == airline].ORIGIN_AIRPORT.unique().tolist() # set value for origin



    def get_origin_data(self,airline,origin,ui_num=1):
        # filtered data of picked origin for combobox pick_dest
        # print(7777, self.ui.temp_data)
        # print('get origin')
        if ui_num == 1:
            self.ui1.temp_data = self.ui1.temp_data[self.ui1.temp_data.ORIGIN_AIRPORT == origin]
            self.ui1.pick_dest['values'] = self.data.df[(self.data.df.ORIGIN_AIRPORT == origin) & (self.data.df.AIRLINE == airline)].DESTINATION_AIRPORT.unique().tolist()
            # print(self.data.df[(self.data.df.ORIGIN_AIRPORT == 'ADK') & (self.data.df.AIRLINE == 'VX')].DESTINATION_AIRPORT.unique().tolist())
        else:
            self.ui2.temp_data = self.ui2.temp_data[self.ui2.temp_data.ORIGIN_AIRPORT == origin]
            self.ui2.pick_dest['values'] = self.data.df[(self.data.df.ORIGIN_AIRPORT == origin) & (self.data.df.AIRLINE == airline)].DESTINATION_AIRPORT.unique().tolist()


    def get_dest_data(self,dest,ui_num=1):
        # filtered data of picked dest for creating hist
        # print('destttt')
        if ui_num == 1:
            self.ui1.temp_data = self.ui1.temp_data[self.ui1.temp_data.DESTINATION_AIRPORT == dest]
        else:
            self.ui2.temp_data = self.ui2.temp_data[self.ui2.temp_data.DESTINATION_AIRPORT == dest]
        # print(self.ui2.temp_data.loc[:,['DESTINATION_AIRPORT','ORIGIN_AIRPORT']])
    def total_flights_count(self, sorted_df):
        return np.array(sorted_df['AIRLINE'].value_counts().tolist())

    def arrival_delay_counts(self, sorted_df, total_flights):
        delayed_flights = sorted_df[sorted_df.ARRIVAL_DELAY > 0]['AIRLINE'].value_counts().tolist()
        while len(total_flights) != len(delayed_flights):
            delayed_flights.append(0)
        return np.array(delayed_flights)


if __name__ == '__main__':
    data = Data()
    c = Controller(data)
    stat = ['mean', 'std', 'min', 'q1', 'q2', 'q3', 'max']
    col = ['ARRIVAL_DELAY', 'AIR_TIME', 'DISTANCE', 'ELAPSED_TIME']

    """
    ARRIVAL_DELAY
    AIR_TIME
    DISTANCE
    ELAPSED_TIME
    """
    """
    """
    print('-------')
    filtered = data.df[(data.df.ORIGIN_AIRPORT == 'CHS') & (data.df.DESTINATION_AIRPORT == 'IAH')]
    my_df = filtered.loc[:,col].head()
    tree_view = c.tree_view_data(stat, my_df)
    print(43434,tree_view)
    print('+++++')
    print(my_df.mean().tolist()) # Mean
    print(round(my_df.std(),2).tolist())  # std
    print(my_df.min().tolist())  # min
    print(my_df.quantile(0.25).tolist())  # 25
    print(my_df.quantile(0.5).tolist()) # 50
    print(my_df.quantile(0.75).tolist()) # 75
    print(my_df.max().tolist()) # max



    # function = {
    #             'mean': lambda df: df.mean().tolist(),
    #             'std': lambda df: round(df.std(), 2).tolist(),
    #             'min': lambda df: df.min().tolist(),
    #             'q1': lambda df: df.quantile(0.25).tolist(),
    #             'q2': lambda df: df.quantile(0.50).tolist(),
    #             'q3': lambda df: df.quantile(0.75).tolist(),
    #             'max': lambda df: df.max().tolist()
    #             }
    # print(888888, function['mean'](my_df))
    # _mean = lambda df: df.mean().tolist()
    # _std = lambda df: df.std().tolist()
    # _min = lambda df: df.min().tolist()
    # _25 = lambda df: df.quantile(0.25).tolist()
    # _50 = lambda df: df.quantile(0.50).tolist()
    # _75 = lambda df: df.quantile(0.75).tolist()
    # _max = lambda df: df.max().tolist()

    # for c in range(len(stat)):
    # for i,c in zip(stat,len(stat):
    # # for i,d in zip(stat,x):
    #     print(f'({i},{x['ARRIVAL_DELAY'][c]},{x['AIR_TIME'][c]},{x['DISTANCE'][c]},,{x['ELAPSED_TIME'][c]})')

    # for i, c in zip(stat, range(len(stat))):
    #     print(f'({i},{x["ARRIVAL_DELAY"][c]},{x["AIR_TIME"][c]},{x["DISTANCE"][c]},{x["ELAPSED_TIME"][c]})')

    # print(c.get_all_origin())
    #
    # print(c.get_airline_data('AA'))
    # print(c.get_origin_data('1',2))