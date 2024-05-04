# view
import tkinter as tk
import matplotlib.pyplot as plt
import tkinter.messagebox as messagebox
import matplotlib
# import seaborn as sns
from tkinter import ttk
from PIL import ImageTk, Image
from abc import ABC, abstractmethod
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # allow to dig canvas and put it on app
from matplotlib.figure import Figure
from threading import Thread
import calendar

matplotlib.use("TkAgg")  # tells that u want to use tkinter backend


# from pandas.plotting import scatter_matrix


class UI(tk.Tk):
    def __init__(self, controller, data):
        super().__init__()
        # self.geometry('700x600')
        self.controller = controller
        self.data = data
        # self.geometry('1000x600')
        self.temp_data = None
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

    @abstractmethod
    def init_components(self):
        pass


class UI2(UI):
    def __init__(self, controller, data):
        super().__init__(controller, data)
        self.title('SkyVista Storytelling')

    def reset_combo(self):
        self.pick_origin.set('')
        self.pick_dest.set('')

    def reset(self):
        self.ax.clear()
        self.canvas.draw()
        self.pick_origin.set('')
        self.pick_dest.set('')
        self.temp_data = None

    def draw_stacked(self):
        # print('s',self.temp_data)
        self.temp_data.reset_index()
        # print(self.temp_data.loc[:, ['ARRIVAL_DELAY', 'ORIGIN_AIRPORT', 'AIRLINE', 'DESTINATION_AIRPORT']])
        # get total flights by airlines from filtered data
        total_flights = self.controller.total_flights_count(self.temp_data)
        # get delayed flights by airlines
        delayed_flights = self.controller.arrival_delay_counts(self.temp_data, total_flights)
        # print(total_flights, delayed_flights)
        base = total_flights - delayed_flights
        self.color_arr = ['#CD6889', '#6495ED', '#FFAEB9', '#872657', '#ADD8E6', '#FFA07A', '#87CEFA', '#8B1C62']

        # print(base)
        # print(self.temp_data.loc[:,['ORIGIN_AIRPORT','DESTINATION_AIRPORT','DISTANCE','ARRIVAL_DELAY','MONTH']])

        airlines_arr = self.temp_data.AIRLINE.unique()

        # # Plotting total flights
        self.ax3.bar(airlines_arr, base, color=self.color_arr[1], label='Total Flights')
        #
        # Plotting delayed flights on top of total flights
        self.ax3.bar(airlines_arr, delayed_flights, bottom=base, color=self.color_arr[0], label='Delayed Flights')

        self.ax3.set_xlabel('Airlines')
        self.ax3.set_ylabel('Number of flights')
        self.ax3.set_title('Number of delayed flights out of total flights')
        self.ax3.legend()

    def draw_scatter(self):
        # print('scatter', self.temp_data.loc[:,["ORIGIN_AIRPORT",'DISTANCE', 'ARRIVAL_DELAY']])
        self.ax4.scatter(x=self.data['DISTANCE'], y=self.data['ARRIVAL_DELAY'], c=self.color_arr[0])
        self.ax4.set_ylabel('Arrival delay')
        self.ax4.set_xlabel('Distance')
        self.ax4.set_title('Relationship between distance and arrival delay')

    def draw_hist(self):
        airline_choices = self.controller.get_unique_airlines(self.temp_data)
        for index, airline in enumerate(airline_choices):
            self.ax2.hist(self.temp_data[self.temp_data.AIRLINE == airline].ARRIVAL_DELAY, alpha=0.8, label=airline,
                          histtype='bar', color=self.color_arr[index])

        self.ax2.legend()
        self.ax2.set_title('Histogram of arrival delay by airlines')
        self.ax2.set_ylabel('Frequency')
        self.ax2.set_xlabel('Arrival delay (minutes)')

    def draw_line(self):
        abbre_month = [calendar.month_abbr[x] for x in range(1, 13)]
        month_int = [x for x in range(1, 13)]
        mean_delay_by_month_df = self.controller.df_groupby('MONTH', 'ARRIVAL_DELAY', self.temp_data)  # dataframe
        line_df = self.controller.data.merge_df_blank(mean_delay_by_month_df)
        self.color_arr = ['#CD6889', '#6495ED', '#FFAEB9', '#872657', '#ADD8E6', '#FFA07A', '#87CEFA', '#8B1C62']
        self.ax.plot(month_int, line_df['ARRIVAL_DELAY'], color=self.color_arr[2])
        self.ax.set_xlim(1, 13)
        self.ax.set_xticks(month_int, abbre_month)
        self.ax.set_title('Monthly trends of arrival delay')
        self.ax.set_ylabel('Arrival delay ( Minutes)')
        self.ax.set_xlabel('Month')

    def on_origin_select(self, event):
        selected_origin = self.origin_airport.get()
        # Thread(target=self.controller.get_all_dest,args=(selected_origin,)).start()
        all_dest = self.controller.get_all_dest(selected_origin)
        self.pick_dest['values'] = all_dest

    # def resize(self, e):
    #     self.bg = Image.open('bg.png').resize((e.width,e.height))
    #     self.bg_tk = ImageTk.PhotoImage(self.bg)
    #     self.bg_canvas.create_image(0,0,image=self.bg_tk,anchor='nw')



    # def slow_process(self, selected_origin):
    #     all_dest = Thread(target=self.controller.get_all_dest,args=(selected_origin,)).start()
    #     self.pick_dest['values'] = all_dest


    def init_components(self):
        # self.bind("<Configure>", self.resize)
        # self.configure(bg='red')
        self.my_font_big = ('Georgia', 40)
        self.my_font_small = ('Georgia', 30)
        self.menubar()

        self.frame = tk.Frame(self, bg='#87CEFA')
        self.frame.pack(fill=tk.BOTH, expand=True, anchor='nw')
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        # self.bg = Image.open('bg.png')
        # self.bg_tk = ImageTk.PhotoImage(self.bg)
        # self.bg_canvas = tk.Canvas(self.frame)
        # self.bg_canvas.grid(row=0,column=0)
        # # self.bg_canvas.pack(fill=tk.BOTH,expand=True,anchor='nw')
        # self.bg_canvas.create_image(0,0,image=self.bg_tk,anchor='nw')
        # self.bg_canvas.create_text(250,20,text='Where do you want to go?',font=self.my_font_big, fill='white')

        header = tk.Label(self.frame, text='Where would you like to go?', font=self.my_font_big, bg='#87CEFA',
                          fg='white', border=0)
        header.grid(row=1, column=0)
        self.logo = Image.open('airplane_logo.png').resize((100, 80))
        self.logo_tk = ImageTk.PhotoImage(self.logo)
        logo = tk.Label(self.frame, image=self.logo_tk, bg='#87CEFA')
        logo.grid(row=0, column=0, columnspan=2)
        frame_small = tk.Frame(self.frame)
        frame_small.grid(row=2, column=0, pady=50, padx=50, sticky='n')

        text_label = ['Origin airport:', 'Destination airport:']

        label = tk.Label(frame_small, text=text_label[0], font=self.my_font_small)
        label.grid(row=1, column=0, pady=30, sticky='e')

        label2 = tk.Label(frame_small, text=text_label[1], font=self.my_font_small)
        label2.grid(row=2, column=0, pady=30, sticky='e')


        # origin combobox
        self.origin_airport = tk.StringVar()
        self.pick_origin = ttk.Combobox(frame_small, textvariable=self.origin_airport, width=5, font=('Georgia', 20))
        self.pick_origin['values'] = self.controller.get_all_origin()
        self.pick_origin['state'] = 'readonly'
        self.pick_origin.grid(row=1, column=1)
        self.pick_origin.bind("<<ComboboxSelected>>", self.on_origin_select)
        #
        # # dest combobox
        self.dest_airport = tk.StringVar()
        self.pick_dest = ttk.Combobox(frame_small, textvariable=self.dest_airport, width=5, font=('Georgia', 20))
        self.pick_dest.grid(row=2, column=1)
        self.pick_dest['state'] = 'readonly'

        button_frame = tk.Frame(self.frame, bg='#87CEFA')
        button_frame.grid(row=3, column=0)

        button = tk.Button(button_frame, text='Generate', width=10,
                           command=lambda: self.change_page(), font=self.my_font_small, border=0)
        button.grid(row=0, column=0, pady=35, ipady=10)
        reset_btn = tk.Button(button_frame, text='Reset', width=10, command=self.reset_combo, font=self.my_font_small,
                              border=0)
        reset_btn.grid(row=0, column=1, ipady=10, padx=4)

    def change_page(self):
        if self.origin_airport.get() and self.dest_airport.get():
            # self.frame2.tkraise()
            # self.bg_canvas.forget()
            self.frame.pack_forget()
            self.frame2 = tk.Frame(self, bg='white')
            self.frame2.pack(fill=tk.BOTH, expand=True, anchor='nw')
            self.frame2.columnconfigure(0, weight=1)
            self.frame2.columnconfigure(1, weight=1)
            self.frame2.rowconfigure(0, weight=0)
            self.frame2.rowconfigure(1, weight=1)
            # self.graph_page()

            self.graph_page(self.origin_airport.get(), self.dest_airport.get())
        else:
            messagebox.showinfo(title='Warning', message='Please select all options from the dropdown menu ')

    def clear(self):
        # for widget in self.frame2.winfo_children():
        #     widget.destroy()
        self.frame2.pack_forget()
        # self.bg_canvas.pack(fill=tk.BOTH,expand=True,anchor='nw')
        #TODO

        self.thread()
        # self.init_components()
        # self.frame.pack(fill=tk.BOTH,expand=True,anchor='nw')
        # self.frame.tkraise()

    def check_thread(self):
        if self.t.is_alive():
            print('thread')


    def thread(self):
        # self.t = Thread(target=self.init_components)
        # self.t.start()
        Thread(target=self.init_components).start()
        # self.after(3,self.check_thread)

    def stat(self):
        new_window = tk.Toplevel(self)
        new_window.title('Descriptive Statistic')
        # ARRIVAL_DELAY, AIR_TIME, DISTANCE, ELAPSED_TIME
        # mean std min 25,50,75 max
        columns, descriptive, label = self.controller.stat_columns()

        tree = ttk.Treeview(new_window, columns=columns, show='headings')
        for i, l in zip(columns, label):
            tree.heading(i, text=l)
        tree_view_data = self.controller.tree_view_data(descriptive, self.temp_data.loc[:, columns[1:]])
        for row in tree_view_data:
            tree.insert('', tk.END, values=row)

        tree.pack(expand=True, fill=tk.BOTH)

    def graph_page(self, origin, dest):

        for widget in self.frame2.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.frame2, bg='#87CEFA')
        frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

        #TODO
        button = tk.Button(frame, text='Back', font=self.my_font_small, command=self.clear, bg='#B0C4DE', border=0)
        button.pack(side=tk.LEFT, anchor=tk.CENTER, pady=2)

        stat = tk.Button(frame, text='Stats', font=self.my_font_small, command=self.stat, border=0)
        stat.pack(side=tk.LEFT, anchor=tk.CENTER, pady=2, padx=2)

        text = f'Origin Airport: {origin}, Destination Airport: {dest}'
        label = tk.Label(frame, text=text, pady=20, font=self.my_font_small, bg='#87CEFA', fg='white')
        label.pack(anchor=tk.CENTER)
        # label.grid(row=0,column=0)

        fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame2)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=30, pady=5, ipady=3)

        # fig2, self.ax2 = plt.subplots(1,2,figsize=(13, 3))
        fig2, self.ax2 = plt.subplots(figsize=(6, 4))
        self.canvas2 = FigureCanvasTkAgg(fig2, master=self.frame2)
        self.canvas2.get_tk_widget().grid(row=1, column=1, padx=30, pady=20)

        fig3, self.ax3 = plt.subplots(figsize=(6, 4))
        self.canvas3 = FigureCanvasTkAgg(fig3, master=self.frame2)
        self.canvas3.get_tk_widget().grid(row=2, column=0, padx=30)

        fig4, self.ax4 = plt.subplots(figsize=(6, 4))
        self.canvas4 = FigureCanvasTkAgg(fig4, master=self.frame2)
        self.canvas4.get_tk_widget().grid(row=2, column=1, padx=30, ipady=5)

        # df.corr('spearman').style.background_gradient(cmap="Blues")

        if origin and dest:
            # Thread(target=self.plot,args=(origin, dest)).start()
            self.controller.filter_origin_and_dest(origin, dest)  # self.temp.data
            self.draw_line()
            self.draw_hist()
            self.draw_stacked()
            self.draw_scatter()
        # print(9999,self.temp_data)
        # print(8888, self.controller.data.get_correlation(self.data, 'DISTANCE', 'ARRIVAL_DELAY'))
        correlation = self.controller.data.get_correlation(self.data, 'DISTANCE', 'ARRIVAL_DELAY')
        corre = tk.Label(self.frame2, text=f'Correlation: {correlation}', font=('Georgia', 15), border=0, bg='white')
        corre.grid(row=2, column=1, sticky='nw', padx=30, pady=2)

        plt.close(fig)
        plt.close(fig2)
        plt.close(fig3)
        plt.close(fig4)

    # def plot(self,origin,dest):
    #     self.controller.filter_origin_and_dest(origin, dest)
    #     self.draw_line()
    #     self.draw_hist()
    #     self.draw_stacked()
    #     self.draw_scatter()

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

    def correlation_tab(self, frame):
        pass

    def other_graphs_tab(self, frame):
        left_window = tk.Frame(frame, bg='#DDA0DD')
        left_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_window = tk.Frame(frame, bg='red')
        right_window.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        label = tk.Label(left_window, text='Create Visualization')
        label.grid(row=0, column=0, sticky='w', pady=10)
        label2 = tk.Label(left_window, text='Type of graph:')
        label2.grid(row=1, column=0, sticky='w')

        self.type = tk.StringVar()
        self.pick_type = ttk.Combobox(left_window, textvariable=self.type)
        self.pick_type['state'] = 'readonly'
        self.pick_type.grid(row=2, column=0, pady=5)
        self.pick_type['values'] = self.controller.get_all_airlines()

    def distribution_tab(self, frame1_2, left_window):
        text_label = ['Origin airport:', 'Destination airport:', 'Attribute:']
        self.my_font_big = ('Georgia', 20)
        self.my_font_small = ('Georgia', 16)
        Label = tk.Label(frame1_2, text='Distribution graph:', bg='#B0C4DE', font=self.my_font_big)
        Label.grid(row=0, column=0, sticky='w', pady=30)
        Label = tk.Label(frame1_2, text='Airlines:', bg='#B0C4DE', font=self.my_font_small)
        Label.grid(row=1, column=0, sticky='w')
        i = 0
        for row in range(3, 9, 2):
            Label = tk.Label(frame1_2, text=text_label[i], bg='#B0C4DE', font=self.my_font_small)
            Label.grid(row=row, column=0, sticky='w')
            i += 1

        self.airlines = tk.StringVar()
        self.pick_airline = ttk.Combobox(frame1_2, textvariable=self.airlines, font=self.my_font_small)
        self.pick_airline['state'] = 'readonly'
        self.pick_airline.grid(row=2, column=0, pady=5)
        self.pick_airline['values'] = self.controller.get_all_airlines()

        self.origin_airport = tk.StringVar()
        self.pick_origin = ttk.Combobox(frame1_2, textvariable=self.origin_airport, font=self.my_font_small)
        self.pick_airline.bind("<<ComboboxSelected>>",
                               lambda event: self.controller.get_airline_data(self.pick_airline.get()))  # set values
        self.pick_origin['state'] = 'readonly'
        self.pick_origin.grid(row=4, column=0, pady=5)

        self.dest_airport = tk.StringVar()
        self.pick_dest = ttk.Combobox(frame1_2, textvariable=self.dest_airport, font=self.my_font_small)
        self.pick_origin.bind("<<ComboboxSelected>>",
                              lambda x: self.controller.get_origin_data(self.airlines.get(), self.origin_airport.get()))
        self.pick_dest['state'] = 'readonly'
        self.pick_dest.grid(row=6, column=0, pady=5)
        self.pick_dest.bind("<<ComboboxSelected>>", lambda x: self.controller.get_dest_data(self.dest_airport.get()))

        self.attributes = tk.StringVar()  # pick attribute
        self.pick_atr = ttk.Combobox(frame1_2, textvariable=self.attributes, font=self.my_font_small)
        self.pick_atr['state'] = 'readonly'
        self.pick_atr['values'] = self.controller.get_all_attributes()
        self.pick_atr.grid(row=8, column=0, pady=5)

        button = tk.Button(left_window, text='Generate', width=10,
                           command=lambda: self.draw_dist(self.temp_data, self.attributes.get()),
                           font=self.my_font_small)
        button.pack(pady=35, ipady=10)

        Reset_btn = tk.Button(left_window, text='Reset', width=10, command=self.reset, font=self.my_font_small)
        Reset_btn.pack(ipady=10)

    def draw_dist(self, data, attribute, type=None):
        self.ax.clear()
        self.canvas.draw()
        if attribute != '' and self.airlines.get() != '' and self.dest_airport.get() != '' and self.origin_airport.get() != '':
            self.ax.hist(data[attribute], color='#8E388E')
            # print(self.temp_data.loc[:,['ORIGIN_AIRPORT','DESTINATION_AIRPORT','AIRLINE']])
            self.ax.set_title(
                f'Distribution of airline {self.airlines.get()} on {attribute} from {self.origin_airport.get()} to {self.dest_airport.get()} airport')
            self.ax.set_ylabel('Frequency', fontsize=8)
            self.ax.set_xlabel(attribute.lower().upper(), fontsize=8)
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

    def init_components(self):
        # self.configure(bg='red')
        self.menubar()
        self.notebook = ttk.Notebook(self, width=900, height=500, style="Custom.TNotebook")  # width=1200,height=800
        self.notebook.pack(pady=10, expand=True, fill="both")

        # create frames
        frame1 = tk.Frame(self.notebook, bg='#A4D3EE', width=900, height=800)
        frame2 = tk.Frame(self.notebook, width=700, height=600)
        frame3 = ttk.Frame(self.notebook, width=700, height=600)
        frame4 = ttk.Frame(self.notebook, width=700, height=600)

        frame1.pack(fill='both', expand=True)
        frame3.pack(fill='both', expand=True)

        left_window = tk.Frame(frame1)  #,width=400, height=800
        # left_window = tk.Frame(frame1, width=400, height=600)
        # left_window.configure(bg='#B0C4DE')
        # left_window.grid(row=0,column=0, columnspan=3,sticky='ns')

        right_window = tk.Frame(frame1, width=800, height=1200)  # ,width=800, height=1200
        right_window.configure(bg='#6CA6CD')  #
        # right_window.grid(row=0,column=3,columnspan=2) #sticky='e'

        # frame2.pack(fill='both', expand=True)

        # self.generate_btn = Image.open('Generate.png').resize((100,30))
        # self.generate_btn_tk = ImageTk.PhotoImage(self.generate_btn)
        # Label = tk.Label(left_window,text='Select criteria:',font=('Helvatic',30))
        # Label.place(x=40,y=0)

        frame1_2 = tk.Frame(left_window, background='#B0C4DE')
        frame1_2.pack(ipady=10, fill="both")

        # add frames to notebook

        self.notebook.add(frame1, text='Distribution')
        self.notebook.add(frame2, text='Correlation')
        self.notebook.add(frame3, text='Graphs')
        self.notebook.add(frame4, text='Descriptive Statistic')

        fig = Figure()
        self.ax = fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(fig, master=right_window)
        self.canvas.get_tk_widget().pack(padx=30, pady=30, ipadx=50, ipady=50, anchor=tk.CENTER)

        # # , image = self.generate_btn self.bg = Image.open('page1.png') self.page1_tk = ImageTk.PhotoImage(self.bg)
        # self.canvas2 = tk.Canvas(left_window,bg='grey',width=400,height=600,bd= 0, highlightthickness= 0,
        # relief= 'ridge') self.canvas2.pack(fill='both',expand=True)
        #
        # # # Place the image on the Canvas
        # self.canvas2.create_image(0,0,image=self.page1_tk,anchor='nw')

        # button = ttk.Button(self.canvas2, text='Generate', command=self.draw_graph)
        # button.place(x=70,y=500)
        # Reset_btn = tk.Button(self.canvas2,text='Reset',command=self.reset,bg='red')
        # Reset_btn.place(x=230,y=500)

        self.distribution_tab(frame1_2, left_window)
        self.other_graphs_tab(frame3)
        # self.correlation_tab(frame2)

        self.notebook.columnconfigure((0, 1), weight=1)
        left_window.pack(side=tk.LEFT, fill="both", expand=True, anchor=tk.SW)
        right_window.pack(side=tk.RIGHT, fill="both", expand=True)
        left_window.configure(bg='#6E7B8B')
        # left_window.grid(row=0,column=0, columnspan=3,sticky='w')
        # right_window.grid(row=0,column=3,columnspan=2) #sticky='e'

    def run(self):
        self.mainloop()
