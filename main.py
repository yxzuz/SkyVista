from database import Data
from model import Controller

if __name__ == '__main__':
    # create model
    my_data_class = Data()
    # create controller
    controller = Controller(my_data_class)
    # run the program
    controller.run()




