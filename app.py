# view
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("TkAgg") # tells that u want to use tkinter backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # allow to dig canvas and put it on app
from matplotlib.figure import Figure
from PIL import ImageTk, Image
import seaborn as sns
from pandas.plotting import scatter_matrix

class UI(tk.Tk):
    def __init__(self, controller, data):
        super().__init__()
        # self.geometry('700x600')
        self.controller = controller
        self.data = data
        self.title('SkyVista')
        # self.geometry('1000x600')
        self.temp_data = None
        self.init_components()
        # self.configure(bg='#A4D3EE')




    def distribution_tab(self,frame1_2,left_window):
        text_label = ['Origin airport:','Destination airport:','Attribute:']
        Label = tk.Label(frame1_2, text='Distribution graph:', bg='#7171C6')
        Label.grid(row=0, column=0, sticky='w',pady=10)
        Label = tk.Label(frame1_2, text='Airlines:',bg='#7171C6')
        Label.grid(row=1, column=0, sticky='w')
        i=0
        for row in range(3,9,2):
            Label = tk.Label(frame1_2,text=text_label[i],bg='#7171C6')
            Label.grid(row=row,column=0,sticky='w')
            i+=1
        self.airlines = tk.StringVar()
        self.pick_airline = ttk.Combobox(frame1_2,textvariable=self.airlines)
        self.pick_airline['state'] = 'readonly'
        self.pick_airline.grid(row=2,column=0,pady=5)
        self.pick_airline['values'] = self.controller.get_all_airlines()


        self.origin_airport = tk.StringVar()
        self.pick_origin = ttk.Combobox(frame1_2,textvariable=self.origin_airport)
        self.pick_airline.bind("<<ComboboxSelected>>", lambda x: self.controller.get_airline_data(self.airlines.get())) # set values
        self.pick_origin['state'] = 'readonly'
        self.pick_origin.grid(row=4,column=0,pady=5)

        self.dest_airport = tk.StringVar()
        self.pick_dest = ttk.Combobox(frame1_2,textvariable=self.dest_airport)
        self.pick_origin.bind("<<ComboboxSelected>>",
                              lambda x: self.controller.get_origin_data(self.airlines.get(),self.origin_airport.get()))
        self.pick_dest['state'] = 'readonly'
        self.pick_dest.grid(row=6,column=0,pady=5)
        self.pick_dest.bind("<<ComboboxSelected>>", lambda x: self.controller.get_dest_data(self.dest_airport.get()))

        self.attributes = tk.StringVar()  # pick attribute
        self.pick_atr = ttk.Combobox(frame1_2,textvariable=self.attributes)
        self.pick_atr['state'] = 'readonly'
        self.pick_atr['values'] = self.controller.get_all_attributes()
        self.pick_atr.grid(row=8,column=0,pady=5)


        # self.type = tk.StringVar() # pick graph type: histogram, boxplot
        # pick_type = ttk.Combobox(left_window,textvariable=self.type)
        # pick_type['values'] = ['Histogram','Boxplot']
        # pick_type['state'] = 'readonly'
        # pick_type.place(x=210,y=390,width=100)


        button = tk.Button(left_window, text='Generate', width=10, command=lambda : self.draw_dist(self.temp_data, self.attributes.get()))
        button.pack(pady=35,ipady=10)

        Reset_btn = tk.Button(left_window, text='Reset', width=10, command=self.reset)
        Reset_btn.pack(ipady=10)



    def draw_dist(self, data, attribute, type=None):
        self.ax.clear()
        self.canvas.draw()
        self.ax.hist(data[attribute])
        # print(self.temp_data.loc[:,['ORIGIN_AIRPORT','DESTINATION_AIRPORT','AIRLINE']])
        self.ax.set_title(f'Distribution of airline {self.airlines.get()} on {attribute} from {self.origin_airport.get()} to {self.dest_airport.get()} airport')
        self.ax.set_ylabel('Frequency',fontsize=8)
        self.ax.set_xlabel(attribute.lower().upper(),fontsize=8)
        # self.ax.plot(x, x ** 2)
        self.canvas.draw()
        self.reset_combo()


    def reset_combo(self):
        self.pick_airline.set('')
        self.pick_atr.set('')
        self.pick_origin.set('')
        self.pick_dest.set('')
    def reset(self):
        self.ax.clear()
        self.canvas.draw()
        self.pick_airline.set('')
        self.pick_atr.set('')
        self.pick_origin.set('')
        self.pick_dest.set('')
        self.temp_data = None

    def update_dest(self,pick_dest):
        pick_dest['values'] = self.controller.get_all_dest(self.origin_airport.get())

    def init_components(self):
        self.notebook = ttk.Notebook(self,width=900,height=500) #width=1200,height=800
        self.notebook.pack(pady=10, expand=True)

        # create frames
        frame1 = tk.Frame(self.notebook,bg='#A4D3EE',width=900,height=800)
        frame2 = tk.Frame(self.notebook, width=700, height=600)
        frame3 = ttk.Frame(self.notebook, width=700, height=600)
        frame4 = ttk.Frame(self.notebook, width=700, height=600)
        # frame1.pack()
        frame1.pack(fill='both', expand=True)
        left_window = tk.Frame(frame1) #,width=400, height=800
        # left_window = tk.Frame(frame1, width=400, height=600)
        left_window.configure(bg='#A4D3EE')
        left_window.grid(row=0,column=0, columnspan=3,sticky='ns')

        right_window = tk.Frame(frame1,width=800, height=1200) #,width=800, height=1200
        right_window.configure(bg='#6CA6CD') #
        right_window.grid(row=0,column=3,columnspan=2,) #sticky='e'


        # frame2.pack(fill='both', expand=True)

        # self.generate_btn = Image.open('Generate.png').resize((100,30))
        # self.generate_btn_tk = ImageTk.PhotoImage(self.generate_btn)
        # Label = tk.Label(left_window,text='Select criteria:',font=('Helvatic',30))
        # Label.place(x=40,y=0)


        frame1_2 = tk.Frame(left_window,background='#7171C6')
        frame1_2.pack(ipady=10)
        # text_label = ['Origin airport','Destination airport:','Attribute:']
        # Label = tk.Label(frame1_2, text='Distribution graph:', bg='#7171C6')
        # Label.grid(row=0, column=0, sticky='w',pady=10)
        # Label = tk.Label(frame1_2, text='Airlines:',bg='#7171C6')
        # Label.grid(row=1, column=0, sticky='w')
        # i=0
        # for row in range(3,9,2):
        #     Label = tk.Label(frame1_2,text=text_label[i],bg='#7171C6')
        #     Label.grid(row=row,column=0,sticky='w')
        #     i+=1

        # Label2 = tk.Label(frame1_2,text='Airlines:')
        # # Label2.place(x=80,y=165)
        # Label2.grid(row=1,column=0,columnspan=1,sticky='w')
        #
        # Label3 = tk.Label(frame1_2, text='Origin airport')
        # Label3.grid(row=2,column=0)
        #
        # Label4 = tk.Label(frame1_2,text='Destination airport:')
        # # Label4.place(x=65,y=315)
        # Label4.grid(row=3,column=0)
        # #
        # Label5 = tk.Label(frame1_2,text='Attribute:')
        # # Label4.place(x=65,y=315)
        # Label5.grid(row=4,column=0)


        # add frames to notebook

        self.notebook.add(frame1, text='Distribution')
        self.notebook.add(frame2, text='Correlation')
        self.notebook.add(frame3, text='Graphs')
        self.notebook.add(frame4, text='Descriptive Statistic')



        fig = Figure()
        self.ax = fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(fig,master=right_window)
        self.canvas.get_tk_widget().pack(padx=30,pady=10)

        # # , image = self.generate_btn
        # self.bg = Image.open('page1.png')
        # self.page1_tk = ImageTk.PhotoImage(self.bg)
        # self.canvas2 = tk.Canvas(left_window,bg='grey',width=400,height=600,bd= 0, highlightthickness= 0, relief= 'ridge')
        # self.canvas2.pack(fill='both',expand=True)
        #
        # # # Place the image on the Canvas
        # self.canvas2.create_image(0,0,image=self.page1_tk,anchor='nw')

        # button = ttk.Button(self.canvas2, text='Generate', command=self.draw_graph)
        # button.place(x=70,y=500)
        # Reset_btn = tk.Button(self.canvas2,text='Reset',command=self.reset,bg='red')
        # Reset_btn.place(x=230,y=500)

        self.distribution_tab(frame1_2, left_window)




    def run(self):
        self.mainloop()


# if __name__ == '__main__':
#     app = UI()
#     app.run()