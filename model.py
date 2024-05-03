
# for model and controller
from database import Data
from app import UI,UI1,UI2
import numpy as np

class Model:
    pass

class Controller:
    def __init__(self,data):
        self.data = data
        #default
        # self.ui1 = UI1(self,self.data.df)
        # self.ui2 = None
        # self.state = 1
        self.state = 2
        self.ui2 = UI2(self, self.data.df)

    def switch_mode(self, mode):
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
        self.ui2.run()

    def df_groupby(self,groupby_attr,mean_attr, df):
        return self.data.mean_groupby_df(groupby_attr,mean_attr, df)


    def get_unique_airlines(self,df):
        return df.AIRLINE.unique().tolist()

    def get_all_origin(self):
        return self.data.all_origin()

    def get_all_dest(self,orig):
        return self.data.all_destination(orig)

    def filter_origin_and_dest(self, orig, dest):
        self.ui2.temp_data = self.data.filtered_attributes_dist(orig, dest)

    def get_all_attributes(self):
        return self.data.all_attributes()

    def get_all_airlines(self):
        return self.data.all_airlines()

    def stat_columns(self):
        columns_atr = ["STATISTICS",'ARRIVAL_DELAY', 'AIR_TIME', 'DISTANCE', 'ELAPSED_TIME']
        stat = ['Mean', 'Std', 'Min', '25', '50', '75', 'Max']
        label = ['Statistics','Arrival delay', 'Air time', 'Distance','Elapsed time']
        return columns_atr, stat, label

    def tree_view_data(self, stat):
        data = {
            # "Mean": [4.494781, 118.202505, 800.959041, 145.739040],
            # "Std": [60.054968, 74.476176, 573.256670, 76.236987],
            # "Min": [-56.000000, 32.000000, 184.000000,9.000000],
            # "25%": [-15.000000, 57.000000, 280.000000, 90.000000],
            # "50%": [-6.000000, 103.000000, 666.000000, 129.000000]
            "ARRIVAL_DELAY": [4.494781, 60.054968, -56, -15, -6, 7, 1201],
            "AIR_TIME": [118.202505, 74.476176, 32, 57, 103, 160, 423],
            "DISTANCE": [800.959041, 573.256670, 184, 280, 666, 1242, 2611],
            "ELAPSED_TIME": [145.739040, 76.236987, 49, 90, 129, 185.75, 447],
        }
        # print(data)
        # print(self.data.df.loc[:1000,col].describe())
        # print(self.data.df[0:1000])
        # for i,df in zip(stat, self.data.df):
        #     print(i,df.ARRIVAL_DELAY.mean())
        tree_view = []
        for i, c in zip(stat, range(len(stat))):
            tree_view.append((i, data["ARRIVAL_DELAY"][c], data["AIR_TIME"][c], data["DISTANCE"][c], data["ELAPSED_TIME"][c]))
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
    stat = ['Mean', 'Std', 'Min', '25', '50', '75', 'Max']
    col = ['ARRIVAL_DELAY', 'AIR_TIME', 'DISTANCE', 'ELAPSED_TIME']
    x = c.tree_view_data()
    # for i in x:
    #     print(i)
    print(x)
    """
    ARRIVAL_DELAY
    AIR_TIME
    DISTANCE
    ELAPSED_TIME
    """
    print('-------')

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