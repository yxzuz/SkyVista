from database import Data
from app import UI
from model import Controller

if __name__ == '__main__':
    my_data_class = Data()
    controller = Controller(my_data_class)
    controller.run()
    # app.run()




