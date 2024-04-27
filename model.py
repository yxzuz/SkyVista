
# for model and controller
from database import Data
from app import UI
class Model:
    pass

class Controller:
    def __init__(self,data):
        self.data = data

        self.ui = UI(self,self.data.df)

    def run(self):
        self.ui.run()


    def get_all_origin(self):
        return self.data.all_origin()

    def get_all_dest(self,orig):
        return self.data.all_destination(orig)
    def get_all_attributes(self):
        return self.data.all_attributes()

    def get_all_airlines(self):
        return self.data.all_airlines()

    def get_airline_data(self, airline):
        # return list corresponding to airline picked for combobox pick_origin
        # print(11111)
        self.ui.temp_data = self.data.df[self.data.df.AIRLINE == airline] # update temp data
        self.ui.pick_origin['values'] = self.data.df[self.data.df.AIRLINE == airline].ORIGIN_AIRPORT.unique().tolist() # set value for origin


    def get_origin_data(self,airline,origin):
        # filtered data of picked origin for combobox pick_dest
        # print(7777, self.ui.temp_data)
        self.ui.temp_data = self.ui.temp_data[self.ui.temp_data.ORIGIN_AIRPORT == origin]
        self.ui.pick_dest['values'] = self.data.df[(self.data.df.ORIGIN_AIRPORT == origin) & (self.data.df.AIRLINE == airline)].DESTINATION_AIRPORT.unique().tolist()
        # print(self.data.df[(self.data.df.ORIGIN_AIRPORT == 'ADK') & (self.data.df.AIRLINE == 'VX')].DESTINATION_AIRPORT.unique().tolist())

    def get_dest_data(self,dest):
        # filtered data of picked dest for creating hist
        self.ui.temp_data = self.ui.temp_data[self.ui.temp_data.DESTINATION_AIRPORT == dest]
if __name__ == '__main__':
    data = Data()
    c = Controller(data)
    # print(c.get_all_origin())
    print(c.get_airline_data('AA'))
    print(c.get_origin_data('1',2))