# view
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
# import seaborn as sns
from tkinter import ttk
from tkinter.font import Font
from abc import ABC, abstractmethod
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # allow to dig canvas and put it on app
from matplotlib.figure import Figure
import calendar
matplotlib.use("TkAgg")  # tells that u want to use tkinter backend
# from PIL import ImageTk, Image
from pandas.plotting import scatter_matrix


class UI(tk.Tk):
    def __init__(self, controller, data):
        super().__init__()
        # self.geometry('700x600')
        self.controller = controller
        self.data = data
        # self.geometry('1000x600')
        self.temp_data = None
        # self.customFont = Font(family='GungsuhChe', size=24)
        self.init_components()
        # self.configure(bg='#A4D3EE')

    @abstractmethod
    def reset_combo(self):
        pass


    @abstractmethod
    def reset(self):
        pass

    def menubar(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        # create a menu
        file_menu = tk.Menu(self.menu)

        file_menu.add_command(
            label='Data exploring',
            command=lambda: self.controller.switch_mode('Explore'),
        )
        file_menu.add_command(
            label='Storytelling',
            command=lambda: self.controller.switch_mode('Story'),
        )

        # add a menu item to the menu
        file_menu.add_command(
            label='Exit',
            command=self.destroy
        )
        # add the File menu to the menubar
        self.menu.add_cascade(
            label="Menu",
            menu=file_menu
        )

    # def switch_mode(self, mode):
    #     if mode == 'Explore':
    #         self.init_components()
    #     else:
    #         self.notebook.destroy()
    #         self.init_components2()
        # selected_mode = event.widget['label']
        # print(selected_mode)

        # print(event.cget())

    @abstractmethod
    def init_components(self):
        pass



class UI2(UI):

    def __init__(self,controller, data):
        super().__init__(controller, data)
        self.title('SkyVistaStory')


    def reset_combo(self):
        self.pick_origin.set('')
        self.pick_dest.set('')

    def reset(self):
        self.ax.clear()
        self.canvas.draw()
        self.pick_airline.set('')
        self.pick_origin.set('')
        self.pick_dest.set('')
        self.temp_data = None

    def draw_stacked(self):
        #TODO


        # self.ax[0, 0]
        self.temp_data.reset_index()
        print(self.temp_data.loc[:,['ARRIVAL_DELAY','ORIGIN_AIRPORT','AIRLINE','DESTINATION_AIRPORT']])
        total_flights = self.controller.total_flights_count(self.temp_data)
        delayed_flights = self.controller.arrival_delay_counts(self.temp_data, total_flights)
        print(total_flights, delayed_flights)
        base = total_flights - delayed_flights
        self.color_arr = ['#CD6889', '#6495ED', '#FFAEB9','#872657']

        print(base)
        # print(self.temp_data.loc[:,['ORIGIN_AIRPORT','DESTINATION_AIRPORT','DISTANCE','ARRIVAL_DELAY','MONTH']])

        airlines_arr = self.temp_data.AIRLINE.unique()
        # print(airlines_arr)

        # self.ax[0, 0].clear()
        # # Plotting total flights
        self.ax[0].bar(airlines_arr, base, color=self.color_arr[1], label='Total Flights')
        #
        # # Plotting delayed flights on top of total flights
        self.ax[0].bar(airlines_arr, delayed_flights, bottom=base, color=self.color_arr[0], label='Delayed Flights')

        self.ax[0].set_xlabel('Airlines')
        self.ax[0].set_ylabel('Number of flights')
        self.ax[0].set_title('Number of delayed flights out of total flights')
        self.ax[0].legend()

    def draw_scatter(self):
        self.ax[1].scatter(x=self.data['DISTANCE'], y=self.data['ARRIVAL_DELAY'], c=self.color_arr[0])
        self.ax[1].set_ylabel('Arrival delay')
        self.ax[1].set_xlabel('Distance')
        self.ax[1].set_title('Relationship between distance and arrival delay')

    def draw_hist(self):
        #TOdo
        airline_choices = self.controller.get_unique_airlines(self.temp_data)
        for index, airline in enumerate(airline_choices):
            self.ax2[0].hist(self.temp_data[self.temp_data.AIRLINE == airline].ARRIVAL_DELAY, alpha=0.8, label=airline,
                    histtype='bar',color=self.color_arr[index])

        self.ax2[0].legend()
        self.ax2[0].set_title('Histogram of arrival delay by airlines')
        self.ax2[0].set_ylabel('Frequency')
        self.ax2[0].set_xlabel('Arrival delay (minutes)')


    def draw_line(self):
        abbre_month = [calendar.month_abbr[x] for x in range(1, 13)]
        month_int = [x for x in range(1, 13)]
        mean_delay_by_month_df = self.controller.df_groupby('MONTH', 'ARRIVAL_DELAY', self.temp_data) # dataframe
        print('drawline')
        print(mean_delay_by_month_df.shape)
        line_df = self.controller.data.merge_df_blank(mean_delay_by_month_df)
        print('result')
        print(mean_delay_by_month_df)
        print(line_df)
        # print(3333,type(line_df))

        self.ax2[1].plot(month_int, line_df['ARRIVAL_DELAY'], color= self.color_arr[2])
        self.ax2[1].set_xlim(1, 13)
        self.ax2[1].set_xticks(month_int, abbre_month)
        self.ax2[1].set_title('Monthly trends of arrival delay')
        self.ax2[1].set_ylabel('Arrival delay ( Minutes)')
        self.ax2[1].set_xlabel('Month')

    def on_origin_select(self, event):
        selected_origin = self.origin_airport.get()
        all_dest = self.controller.get_all_dest(selected_origin)
        self.pick_dest['values'] = all_dest

    def init_components(self):
        self.menubar()
        self.frame2 = tk.Frame(self, bg='black')
        self.frame2.grid(column=0, row=0,sticky='nsew')

        frame = tk.Frame(self, bg='#7D9EC0')
        frame.grid(column=0,row=0,sticky='nsew')
        # frame.pack(fill=tk.BOTH, expand=True)
        Label = tk.Label(frame, text='Flight\'s arrival delay insights', font=('Helvatic', 20))
        Label.grid(row=0, column=0, padx=30)

        text_label = ['Origin airport:', 'Destination airport:']

        label = tk.Label(frame, text=text_label[0],font=('Helvatica',30))
        label.grid(row=1, column=0, pady=50, padx=50)

        label2 = tk.Label(frame, text=text_label[1],font=('Helvatica',30))
        label2.grid(row=2, column=0, pady=50, padx=30)

        # origin combobox
        self.origin_airport = tk.StringVar()
        self.pick_origin = ttk.Combobox(frame, textvariable=self.origin_airport, width=6, font=('Helvatica',20))
        self.pick_origin['values'] = self.controller.get_all_origin()
        self.pick_origin['state'] = 'readonly'
        self.pick_origin.grid(row=1, column=1)
        self.pick_origin.bind("<<ComboboxSelected>>", self.on_origin_select)

        # # dest combobox
        self.dest_airport = tk.StringVar()
        self.pick_dest = ttk.Combobox(frame, textvariable=self.dest_airport, width=6, font=('Helvatica',20))
        self.pick_dest.grid(row=2, column=1, padx=5)
        self.pick_dest['state'] = 'readonly'

        button = tk.Button(frame, text='Generate', width=10,
                           command=lambda:self.change_page())
        button.grid(row=3, column=0, pady=35, ipady=10)

        Reset_btn = tk.Button(frame, text='Reset', width=10, command=self.reset_combo)
        Reset_btn.grid(row=3, column=1, ipady=10, padx=4)



    def change_page(self):
        self.frame2.tkraise()
        self.graph_page(self.origin_airport.get(), self.dest_airport.get())

    def graph_page(self, origin, dest):
        text = f'Origin Airport: {origin}, Destination Airport: {dest}'
        label = tk.Label(self.frame2,text=text)
        label.pack()
        x = np.arange(0.0, 2.0, 0.01)
        y = 1 + np.sin(2 * np.pi * x)
        # fig, self.ax = plt.subplots(2, 2, figsize=(3, 5))
        # self.canvas = FigureCanvasTkAgg(fig, master=second_frame)
        # self.canvas.get_tk_widget().pack(padx=30, pady=10, anchor=tk.CENTER,fill=tk.BOTH, expand=True)
        # fig, self.ax = plt.subplots(1, 4, figsize=(20, 3))
        fig, self.ax = plt.subplots(1,2,figsize=(13, 3))
        fig.subplots_adjust(wspace=1)
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame2)
        self.canvas.get_tk_widget().pack(padx=30, pady=10, anchor=tk.CENTER, fill=tk.BOTH, expand=True)

        fig2,self.ax2 = plt.subplots(1,2, figsize=(13, 3))
        fig.subplots_adjust(wspace=1)
        self.canvas2 = FigureCanvasTkAgg(fig2, master=self.frame2)
        self.canvas2.get_tk_widget().pack(padx=30, pady=10, anchor=tk.CENTER, fill=tk.BOTH, expand=True)
        if origin and dest:
            self.controller.filter_origin_and_dest(origin, dest)
            self.draw_stacked()
            self.draw_scatter()
            self.draw_hist()
            self.draw_line()

        # self.ax[0, 0].plot(x, y,color='#8E388E')
        # self.ax[0, 1].plot(x, y,color='#8E388E')
        # self.ax[1, 0].plot(x, y,color='#8E388E')
        # self.ax[1, 1].plot(x, y,color='#8E388E')

    def init_components2(self):
        # self.menubar()
        # print(22323)
        # self.notebook2 = ttk.Notebook(self)
        #, width=1200, height=600
        # self.geometry('900x800')
        top_frame = tk.Frame(self, bg='green', width=900, height=800)
        second_frame = tk.Frame(self, bg='black')
        # frame1 = tk.Frame(self.notebook2, bg='#A4D3EE', width=900, height=800)
        # self.notebook2.add(top_frame, text='Test mode')
        # self.notebook2.pack()
        # top_frame.pack(side=tk.TOP,expand=True)

        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        Label = tk.Label(top_frame, text='Flight\'s arrival delay data analysis', font=('Helvatic', 40))
        Label.grid(row=0, column=0)

        top_sub = tk.Frame(top_frame, bg='blue')
        top_sub.grid(row=1, column=0, pady=10)
        text_label = ['Airport:', 'Origin airport:', 'Destination airport:']

        for row in range(0, len(text_label)):
            label = tk.Label(top_sub, text=text_label[row])
            label.grid(row=row, column=0)

        # airport combobox
        self.airlines = tk.StringVar()
        self.pick_airline = ttk.Combobox(top_sub, textvariable=self.airlines)
        self.pick_airline.grid(row=0, column=2)
        self.pick_airline['values'] = self.controller.get_all_airlines()
        self.pick_airline.bind("<<ComboboxSelected>>",
                               lambda event: self.controller.get_airline_data(self.pick_airline.get(),2))  # set values
        # origin combobox
        self.origin_airport = tk.StringVar()
        self.pick_origin = ttk.Combobox(top_sub, textvariable=self.origin_airport)

        self.pick_origin.bind("<<ComboboxSelected>>",
                              lambda x: self.controller.get_origin_data(self.airlines.get(),self.origin_airport.get(),ui_num=2)) # set values
        self.pick_origin['state'] = 'readonly'
        self.pick_origin.grid(row=1, column=2)

        # dest combobox
        self.dest_airport = tk.StringVar()
        self.pick_dest = ttk.Combobox(top_sub, textvariable=self.dest_airport)
        self.pick_dest.grid(row=2, column=2, padx=5)
        self.pick_dest.bind("<<ComboboxSelected>>", lambda event: self.controller.get_dest_data(self.pick_dest.get(),2))



        second_frame.pack(expand=True, fill=tk.BOTH)
        Label2 = tk.Label(second_frame, text='TESTT', font=('Helvatic', 40))
        Label2.pack()

        button = tk.Button(top_frame, text='Generate', width=10,
                           command=lambda: self.draw_dist())
        button.grid(row=2,column=0,pady=35, ipady=10)

        Reset_btn = tk.Button(top_frame, text='Reset', width=10, command=self.reset)
        Reset_btn.grid(row=3,column=0,ipady=10)

        fig, self.ax = plt.subplots(1, 4, figsize=(9, 6))
        fig.subplots_adjust(wspace=0.5)
        self.canvas = FigureCanvasTkAgg(fig, master=second_frame)
        self.canvas.get_tk_widget().pack(padx=30, pady=10, anchor=tk.CENTER,fill=tk.BOTH, expand=True)


    # def menubar(self):
    #     self.menu = tk.Menu(self)
    #     self.config(menu=self.menu)
    #
    #     # create a menu
    #     file_menu = tk.Menu(self.menu)
    #
    #     file_menu.add_command(
    #         label='Data exploring',
    #         command=lambda: self.switch_mode('Explore'),
    #     )
    #     file_menu.add_command(
    #         label='Storytelling',
    #         command=lambda: self.switch_mode('Story'),
    #     )
    #
    #     # add a menu item to the menu
    #     file_menu.add_command(
    #         label='Exit',
    #         command=self.destroy
    #     )
    #     # add the File menu to the menubar
    #     self.menu.add_cascade(
    #         label="Menu",
    #         menu=file_menu
    #     )
    #
    # def switch_mode(self, mode):
    #     if mode == 'Explore':
    #         self.init_components()
    #     else:
    #         self.notebook.destroy()
    #         self.init_components2()

    def run(self):
        self.mainloop()



class UI1(UI):
    # def __init__(self, controller, data):
    #     super().__init__()
    #     # self.geometry('700x600')
    #     self.controller = controller
    #     self.data = data
    #     self.title('SkyVista')
    #     # self.geometry('1000x600')
    #     self.temp_data = None
    #     self.customFont = Font(family='GungsuhChe', size=24)
    #     # self.init_components2()
    #     self.init_components()

        # self.configure(bg='#A4D3EE')
    def __init__(self, controller, data):
        super().__init__(controller, data)
        self.title('SkyVistaEx')




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
        self.pick_airline.bind("<<ComboboxSelected>>", lambda event: self.controller.get_airline_data(self.pick_airline.get())) # set values
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

        button = tk.Button(left_window, text='Generate', width=10, command=lambda : self.draw_dist(self.temp_data, self.attributes.get()))
        button.pack(pady=35,ipady=10)

        Reset_btn = tk.Button(left_window, text='Reset', width=10, command=self.reset)
        Reset_btn.pack(ipady=10)
    #idk
    # def distribution_tab(self, frame1_2, left_window):
    #     text_label = ['Origin airport:', 'Destination airport:', 'Attribute:']
    #     Label = tk.Label(frame1_2, text='Distribution graph:', bg='#7171C6')
    #     Label.grid(row=0, column=0, sticky='w', pady=10)
    #     Label = tk.Label(frame1_2, text='Airlines:', bg='#7171C6')
    #     Label.grid(row=1, column=0, sticky='w')
    #     i = 0
    #     for row in range(3, 9, 2):
    #         Label = tk.Label(frame1_2, text=text_label[i], bg='#7171C6')
    #         Label.grid(row=row, column=0, sticky='w')
    #         i += 1
    #
    #     self.airlines = tk.StringVar()
    #     self.pick_airline = ttk.Combobox(frame1_2, textvariable=self.airlines)
    #     self.pick_airline['state'] = 'readonly'
    #     self.pick_airline.grid(row=2, column=0, pady=5)
    #     self.pick_airline['values'] = self.controller.get_all_airlines()
    #
    #     self.origin_airport = tk.StringVar()
    #     self.pick_origin = ttk.Combobox(frame1_2, textvariable=self.origin_airport)
    #     # self.pick_airline.bind("<<ComboboxSelected>>",
    #     #                        lambda x: self.controller.get_airline_data(self.airlines.get()))  # set values
    #     self.pick_airline.bind("<<ComboboxSelected>>",
    #                            lambda event: self.controller.get_airline_data(self.pick_airline.get()))
    #
    #     self.pick_origin['state'] = 'readonly'
    #     self.pick_origin.grid(row=4, column=0, pady=5)
    #
    #     self.dest_airport = tk.StringVar()
    #     self.pick_dest = ttk.Combobox(frame1_2, textvariable=self.dest_airport)
    #     self.pick_origin.bind("<<ComboboxSelected>>",
    #                           lambda x: self.controller.get_origin_data(self.airlines.get(), self.origin_airport.get()))
    #     self.pick_dest['state'] = 'readonly'
    #     self.pick_dest.grid(row=6, column=0, pady=5)
    #     self.pick_dest.bind("<<ComboboxSelected>>", lambda x: self.controller.get_dest_data(self.dest_airport.get()))
    #
    #     self.attributes = tk.StringVar()  # pick attribute
    #     self.pick_atr = ttk.Combobox(frame1_2, textvariable=self.attributes)
    #     self.pick_atr['state'] = 'readonly'
    #     self.pick_atr['values'] = self.controller.get_all_attributes()
    #     self.pick_atr.grid(row=8, column=0, pady=5)
    #
    #     # self.type = tk.StringVar() # pick graph type: histogram, boxplot
    #     # pick_type = ttk.Combobox(left_window,textvariable=self.type)
    #     # pick_type['values'] = ['Histogram','Boxplot']
    #     # pick_type['state'] = 'readonly'
    #     # pick_type.place(x=210,y=390,width=100)
    #
    #     # frame1_3 = tk.Frame(frame1_2,bg='purple')
    #
    #     button = tk.Button(left_window, text='Generate', width=10,
    #                        command=lambda: self.draw_dist(self.temp_data, self.attributes.get()))
    #     button.pack(pady=35, ipady=10)
    #
    #     Reset_btn = tk.Button(left_window, text='Reset', width=10, command=self.reset)
    #     Reset_btn.pack(ipady=10)
    #
    #     # frame1_3.grid(row=9,column=0)

    def draw_dist(self, data, attribute, type=None):
        self.ax.clear()
        self.canvas.draw()
        if attribute != '':
            self.ax.hist(data[attribute],color='#8E388E')
            # print(self.temp_data.loc[:,['ORIGIN_AIRPORT','DESTINATION_AIRPORT','AIRLINE']])
            self.ax.set_title(
                f'Distribution of airline {self.airlines.get()} on {attribute} from {self.origin_airport.get()} to {self.dest_airport.get()} airport')
            self.ax.set_ylabel('Frequency', fontsize=8)
            self.ax.set_xlabel(attribute.lower().upper(), fontsize=8)
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

    def update_dest(self, pick_dest):
        pick_dest['values'] = self.controller.get_all_dest(self.origin_airport.get())

    # def menubar(self):
    #     self.menu = tk.Menu(self)
    #     self.config(menu=self.menu)
    #
    #     # create a menu
    #     file_menu = tk.Menu(self.menu)
    #
    #     file_menu.add_command(
    #         label='Data exploring',
    #         command=lambda: self.switch_mode('Explore'),
    #     )
    #     file_menu.add_command(
    #         label='Storytelling',
    #         command=lambda: self.switch_mode('Story'),
    #     )
    #
    #     # add a menu item to the menu
    #     file_menu.add_command(
    #         label='Exit',
    #         command=self.destroy
    #     )
    #     # add the File menu to the menubar
    #     self.menu.add_cascade(
    #         label="Menu",
    #         menu=file_menu
    #     )

    # def init_components2(self):
    #     # self.menubar()
    #     # print(22323)
    #     # self.notebook2 = ttk.Notebook(self,width=900,height=500)
    #     #, width=1200, height=600
    #     self.geometry('900x800')
    #     top_frame = tk.Frame(self, bg='green', width=900, height=800)
    #     second_frame = tk.Frame(self, bg='black')
    #     # frame1 = tk.Frame(self.notebook2, bg='#A4D3EE', width=900, height=800)
    #     # self.notebook2.add(frame1, text='Test mode')
    #     # self.notebook2.pack()
    #     # top_frame.pack(side=tk.TOP,expand=True)
    #     top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    #     Label = tk.Label(top_frame, text='Flight\'s arrival delay data analysis', font=('Helvatic', 40))
    #     Label.grid(row=0, column=0)
    #
    #     top_sub = tk.Frame(top_frame, bg='blue')
    #     top_sub.grid(row=1, column=0, pady=10)
    #     text_label = ['Airport:', 'Origin airport:', 'Destination airport:']
    #
    #     for row in range(0, len(text_label)):
    #         label = tk.Label(top_sub, text=text_label[row])
    #         label.grid(row=row, column=0)
    #
    #     # airport combobox
    #     pick_airport = tk.StringVar()
    #     airport = ttk.Combobox(top_sub, textvariable=pick_airport)
    #     airport.grid(row=0, column=2)
    #     airport['values'] = self.controller.get_all_airlines()
    #
    #     # origin combobox
    #     pick_origin = tk.StringVar()
    #     self.pick_origin2 = ttk.Combobox(top_sub, textvariable=pick_origin)
    #     self.pick_origin2.grid(row=1, column=2)
    #     self.pick_origin2.bind("<<ComboboxSelected>>",
    #                            lambda x: self.controller.get_airline_data(pick_airport.get()))  # set values
    #
    #     # dest combobox
    #     pick_dest = tk.StringVar()
    #     dest = ttk.Combobox(top_sub, textvariable=pick_dest)
    #     dest.grid(row=2, column=2, padx=5)
    #     dest.bind("<<ComboboxSelected>>", lambda x: self.controller.get_dest_data(pick_dest.get()))
    #
    #     second_frame.pack(expand=True, fill=tk.BOTH)
    #     Label2 = tk.Label(second_frame, text='TESTT', font=('Helvatic', 40))
    #     Label2.pack()
    #
    #     x = np.arange(0.0, 2.0, 0.01)
    #     y = 1 + np.sin(2 * np.pi * x)
    #     fig, self.ax = plt.subplots(2, 2, figsize=(8, 5))
    #     self.canvas2 = FigureCanvasTkAgg(fig, master=second_frame)
    #     self.canvas2.get_tk_widget().pack(padx=30, pady=10, anchor=tk.CENTER)
    #     self.ax[0, 0].plot(x, y)
    #     self.ax[0, 1].plot(x, y)
    #     self.ax[1, 0].plot(x, y)
    #     self.ax[1, 1].plot(x, y)

    # def switch_mode(self, mode):
    #     if mode == 'Explore':
    #         self.init_components()
    #     else:
    #         self.notebook.destroy()
    #         self.init_components2()
        # selected_mode = event.widget['label']
        # print(selected_mode)

        # print(event.cget())

    def init_components(self):
        self.configure(bg='red')
        self.menubar()
        self.notebook = ttk.Notebook(self, width=900, height=500, style="Custom.TNotebook")  #width=1200,height=800
        self.notebook.pack(pady=10, expand=True, fill="both")

        # create frames
        frame1 = tk.Frame(self.notebook, bg='#A4D3EE', width=900, height=800)
        frame2 = tk.Frame(self.notebook, width=700, height=600)
        frame3 = ttk.Frame(self.notebook, width=700, height=600)
        frame4 = ttk.Frame(self.notebook, width=700, height=600)

        # frame1.pack()
        frame1.pack(fill='both', expand=True)

        left_window = tk.Frame(frame1)  #,width=400, height=800
        # left_window = tk.Frame(frame1, width=400, height=600)
        left_window.configure(bg='#A4D3EE')
        # left_window.grid(row=0,column=0, columnspan=3,sticky='ns')

        right_window = tk.Frame(frame1, width=800, height=1200)  #,width=800, height=1200
        right_window.configure(bg='#6CA6CD')  #
        # right_window.grid(row=0,column=3,columnspan=2) #sticky='e'

        # frame2.pack(fill='both', expand=True)

        # self.generate_btn = Image.open('Generate.png').resize((100,30))
        # self.generate_btn_tk = ImageTk.PhotoImage(self.generate_btn)
        # Label = tk.Label(left_window,text='Select criteria:',font=('Helvatic',30))
        # Label.place(x=40,y=0)

        frame1_2 = tk.Frame(left_window, background='#7171C6')
        frame1_2.pack(ipady=10, fill="both")
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
        self.canvas = FigureCanvasTkAgg(fig, master=right_window)
        self.canvas.get_tk_widget().pack(padx=30, pady=10, anchor=tk.CENTER)

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

        self.notebook.columnconfigure((0, 1), weight=1)
        left_window.pack(side=tk.LEFT, fill="both", expand=True, anchor=tk.SW)
        right_window.pack(side=tk.RIGHT, fill="both", expand=True)
        left_window.configure(bg='blue')
        # left_window.grid(row=0,column=0, columnspan=3,sticky='w')
        # right_window.grid(row=0,column=3,columnspan=2) #sticky='e'

    def run(self):
        self.mainloop()

if __name__ == '__main__':

    app = UI2()
    app.run()
