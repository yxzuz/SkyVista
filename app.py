"""view in MVC"""
import tkinter as tk
from abc import ABC, abstractmethod
import queue
import calendar
from threading import Thread
from tkinter import ttk
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
import matplotlib
# import seaborn as sns
from PIL import ImageTk, Image
# allow to dig canvas and put it on app
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
matplotlib.use("TkAgg")  # tells that u want to use tkinter backend



class UI(tk.Tk):
    """abstract class for concrete ui"""
    def __init__(self, controller, data):
        super().__init__()
        self.controller = controller
        self.data = data
        self.temp_data = None



    def menubar(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        # create a menu
        file_menu = tk.Menu(self.menu)
        file_menu.add_command(label='Data exploring',command=lambda: self.controller.switch_mode('Explore'))
        file_menu.add_command(label='Storytelling', command=lambda: self.controller.switch_mode('Story'),)
        file_menu.add_command(label='Exit', command=self.destroy)
        self.menu.add_cascade(label="Menu", menu=file_menu)

    def report_error(self):
        messagebox.showwarning('Warning', 'Please select all remaining field(s)')

    @abstractmethod
    def init_components(self):
        pass


class UI2(UI):
    """program mode: storytelling data"""
    def __init__(self, controller, data):
        super().__init__(controller, data)
        self.my_queue = queue.Queue()
        self.title('SkyVista Storytelling')
        self.color_arr = ['#CD6889', '#6495ED', '#FFAEB9',
                          '#872657', '#ADD8E6', '#FFA07A', '#87CEFA', '#8B1C62']
        self.init_components()

    def reset_combo(self):
        self.pick_origin.set('')
        self.pick_dest.set('')



    def draw_stacked(self):
        """draw stacked bar graph"""
        self.temp_data.reset_index()
        total_flights = self.controller.total_flights_count(self.temp_data)
        # get delayed flights by airlines
        delayed_flights = self.controller.arrival_delay_counts(self.temp_data, total_flights)
        base = total_flights - delayed_flights
        airlines_arr = self.temp_data.AIRLINE.unique()

        # Plotting total flights
        self.ax3.bar(airlines_arr, base, color=self.color_arr[1], label='Total Flights')
        # Plotting delayed flights on top of total flights
        self.ax3.bar(airlines_arr, delayed_flights, bottom=base,
                     color=self.color_arr[0], label='Delayed Flights')

        self.ax3.set_xlabel('Airlines')
        self.ax3.set_ylabel('Number of flights')
        self.ax3.set_title('Number of delayed flights out of total flights')
        self.ax3.legend()

    def draw_scatter(self):
        """draw scattered plot"""
        self.ax4.scatter(x=self.data['DISTANCE'], y=self.data['ARRIVAL_DELAY'], c=self.color_arr[0])
        self.ax4.set_ylabel('Arrival delay')
        self.ax4.set_xlabel('Distance')
        self.ax4.set_title('Relationship between distance and arrival delay')

    def draw_hist(self):
        """draw histogram"""
        airline_choices = self.controller.get_unique_airlines(self.temp_data)
        for index, airline in enumerate(airline_choices):
            self.ax2.hist(self.temp_data[self.temp_data.AIRLINE == airline].ARRIVAL_DELAY,
                          alpha=0.8, label=airline,
                          histtype='bar', color=self.color_arr[index])

        self.ax2.legend()
        self.ax2.set_title('Histogram of arrival delay by airlines')
        self.ax2.set_ylabel('Frequency')
        self.ax2.set_xlabel('Arrival delay (minutes)')

    def draw_line(self):
        """draw line graph"""
        abbre_month = [calendar.month_abbr[x] for x in range(1, 13)]
        month_int = list(range(1, 13))
        mean_delay_by_month_df = self.controller.df_groupby('MONTH', 'ARRIVAL_DELAY', self.temp_data)  # dataframe
        line_df = self.controller.data.merge_df_blank(mean_delay_by_month_df, 'ARRIVAL_DELAY')
        self.ax.plot(month_int, line_df['ARRIVAL_DELAY'], color=self.color_arr[2])
        self.ax.set_xlim(1, 13)
        self.ax.set_xticks(month_int, abbre_month)
        self.ax.set_title('Monthly trends of arrival delay')
        self.ax.set_ylabel('Arrival delay ( Minutes)')
        self.ax.set_xlabel('Month')

    def on_origin_select(self, event):
        selected_origin = self.origin_airport.get()
        # Thread(target=self.controller.get_all_dest,args=(selected_origin,)).start()
        # self.thread = Thread(target=self.long_task_2, args=(selected_origin,))
        # self.thread.start()
        all_dest = self.controller.get_all_dest(selected_origin)
        # self.set_value(self.pick_dest)
        self.pick_dest['values'] = all_dest

    # def long_task_2(self,selected_origin):
    #     result = self.controller.get_all_dest(selected_origin)
    #     self.my_queue.put(result)

    # def resize(self, e):
    #     self.bg = Image.open('bg.png').resize((e.width,e.height))
    #     self.bg_tk = ImageTk.PhotoImage(self.bg)
    #     self.bg_canvas.create_image(0,0,image=self.bg_tk,anchor='nw')

    def init_components(self):
        """set up UI and functional usage"""
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

        header = tk.Label(self.frame, text='Where would you like to go?',
                          font=self.my_font_big, bg='#87CEFA',
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

        self.small_frame(frame_small)

        button_frame = tk.Frame(self.frame, bg='#87CEFA')
        button_frame.grid(row=3, column=0)

        button = tk.Button(button_frame, text='Generate', width=10,
                           command=lambda: self.change_page(), font=self.my_font_small, border=0)
        button.grid(row=0, column=0, pady=35, ipady=10)
        reset_btn = tk.Button(button_frame, text='Reset', width=10,
                              command=self.reset_combo, font=self.my_font_small,
                              border=0)
        reset_btn.grid(row=0, column=1, ipady=10, padx=4)

    def long_running(self):
        """thread will do long task in the background"""
        result = self.controller.get_all_origin()
        self.my_queue.put(result)

    def set_value(self, combobox):
        """set combobox value"""
        if not self.thread.is_alive():
            combobox['values'] = self.my_queue.get()
        else:
            self.after(2, lambda: self.set_value(combobox))

    def small_frame(self, frame_small):
        """user interaction frame"""
        self.thread = Thread(target=self.long_running)
        self.thread.start()
        self.origin_airport = tk.StringVar()
        self.pick_origin = ttk.Combobox(frame_small, textvariable=self.origin_airport, width=5, font=('Georgia', 20))
        self.set_value(self.pick_origin)
        # self.set_value()
        # if not self.my_queue.empty():
        # self.pick_origin['values'] =
        #self.controller.get_all_origin()
        # self.my_queue.get(block=False)
        self.pick_origin['state'] = 'readonly'
        self.pick_origin.grid(row=1, column=1)
        self.pick_origin.bind("<<ComboboxSelected>>", self.on_origin_select)
        # # dest combobox
        self.dest_airport = tk.StringVar()
        self.pick_dest = ttk.Combobox(frame_small, textvariable=self.dest_airport, width=5, font=('Georgia', 20))
        self.pick_dest.grid(row=2, column=1)
        self.pick_dest['state'] = 'readonly'

    def change_page(self):
        """change page to page 2"""
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
            messagebox.showinfo(title='Warning',
                                message='Please select all options from the dropdown menu ')

    def clear(self):
        """clear the frame before changing page"""
        # for widget in self.frame2.winfo_children():
        #     widget.destroy()
        self.frame2.pack_forget()
        # self.bg_canvas.pack(fill=tk.BOTH,expand=True,anchor='nw')
        self.init_components()
        # self.frame.pack(fill=tk.BOTH,expand=True,anchor='nw')
        # self.frame.tkraise()

    def stat(self):
        """addinfg data to treeview"""
        new_window = tk.Toplevel(self)
        new_window.title('Descriptive Statistic')
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

        button = tk.Button(frame, text='Back', font=self.my_font_small, command=self.clear, bg='#B0C4DE', border=0)
        button.pack(side=tk.LEFT, anchor=tk.CENTER, pady=2)

        stat = tk.Button(frame, text='Stats', font=self.my_font_small, command=self.stat, border=0)
        stat.pack(side=tk.LEFT, anchor=tk.CENTER, pady=2, padx=2)

        text = f'Origin Airport: {origin}, Destination Airport: {dest}'
        label = tk.Label(frame, text=text, pady=20, font=self.my_font_small, bg='#87CEFA', fg='white')
        label.pack(anchor=tk.CENTER)


        fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame2)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=30, pady=5, ipady=3)
        fig2, self.ax2 = plt.subplots(figsize=(6, 4))
        self.canvas2 = FigureCanvasTkAgg(fig2, master=self.frame2)
        self.canvas2.get_tk_widget().grid(row=1, column=1, padx=30, pady=20)

        fig3, self.ax3 = plt.subplots(figsize=(6, 4))
        self.canvas3 = FigureCanvasTkAgg(fig3, master=self.frame2)
        self.canvas3.get_tk_widget().grid(row=2, column=0, padx=30)

        fig4, self.ax4 = plt.subplots(figsize=(6, 4))
        self.canvas4 = FigureCanvasTkAgg(fig4, master=self.frame2)
        self.canvas4.get_tk_widget().grid(row=2, column=1, padx=30, ipady=5)

        if origin and dest:
            # Thread(target=self.plot,args=(origin, dest)).start()
            self.controller.filter_origin_and_dest(origin, dest)  # self.temp.data
            self.draw_line()
            self.draw_hist()
            self.draw_stacked()
            self.draw_scatter()

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
        """run ui"""
        self.mainloop()


class UI1(UI):
    """program mode: exploring data"""
    def __init__(self, controller, data):
        super().__init__(controller, data)
        self.title('SkyVistaEx')
        print('init')
        self.my_font_big = ('Georgia', 20)
        self.my_font_small = ('Georgia', 16)
        self.color_arr = ['#CD6889', '#6495ED', '#FFAEB9', '#872657', '#ADD8E6', '#FFA07A', '#87CEFA', '#8B1C62']
        self.num_col = ['DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF',
                        'ELAPSED_TIME', 'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN',
                        'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME', 'ARRIVAL_DELAY', 'CANCELLED']
        self.init_components()

    def two_side_window(self, root, header: str):
        """generate two sides window"""
        l_frame = tk.Frame(root, bg='#B0C4DE')
        l_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        r_frame = tk.Frame(root, bg='#6CA6CD')
        r_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        sub_frame = tk.Frame(l_frame, bg='#B0C4DE')
        sub_frame.pack(anchor='nw')
        label = tk.Label(sub_frame, text=header, font=self.my_font_big, bg='#B0C4DE')  # Header
        label.grid(row=0, columnspan=1, sticky='n', pady=10)
        return l_frame, r_frame, sub_frame

    def draw_corr(self, x, y, ax):
        """draw scatterplot"""
        ax.clear()
        self.corr.draw()
        if x and y:
            print(x, y)
            ax.scatter(x=self.data[:1000][x], y=self.data[:1000][y], c=self.color_arr[1])
            ax.set_ylabel(f'{y}')
            ax.set_xlabel(f'{x}')
            ax.set_title(f'Relationship between {x} and {y}')
        self.corr.draw()

    def display_corr(self, x, y):
        """update correlation value"""
        if x and y:
            corre = self.controller.data.get_correlation(self.data, x, y)
            self.corr_label.configure(text=f'Correlation: {corre}')
        else:
            self.report_error()

    def draw_heat_map(self):
        """draw heat map for corrleation tab"""
        new_window = tk.Toplevel(self)

        frame = tk.Frame(new_window)
        frame.grid(row=0, column=0, sticky='nsew', ipady=2)

        frame2 = tk.Frame(new_window)
        frame2.grid(row=0, column=1, sticky='nsew')

        fig, ax = plt.subplots()
        self.corr = FigureCanvasTkAgg(fig, master=frame)
        self.corr.get_tk_widget().pack(side=tk.TOP)
        num_col = self.controller.data.num_attributes()
        temp_corr = self.data.loc[:, num_col[:4]]
        g1 = sns.heatmap(temp_corr.corr(),
                         square=True,
                         linewidths=0.25,
                         linecolor=(0, 0, 0),
                         cmap=sns.color_palette("coolwarm"),
                         annot=True)

        fig2, ax2 = plt.subplots()
        self.corr2 = FigureCanvasTkAgg(fig2, master=frame2)
        self.corr2.get_tk_widget().pack()
        temp_corr = self.data.loc[:, num_col[4:]]
        g2 = sns.heatmap(temp_corr.corr(),
                         square=True,
                         linewidths=0.25,
                         linecolor=(0, 0, 0),
                         cmap=sns.color_palette("coolwarm"),
                         annot=True)
        for graph in [g1, g2]:
            graph.set_yticklabels(graph.get_yticklabels(), rotation=-270, fontsize=8)
            graph.set_xticklabels(graph.get_xticklabels(), rotation=0, fontsize=8)

    def update_temp_data(self, orig, dest):
        """update temp data based on origin and destinaiton airport"""
        self.temp_data = self.controller.data.filtered_attributes_dist(orig, dest)

    def create_tree_view(self, tree, descriptive, columns, orig, dest):
        """add data to treeview"""
        if orig and dest:
            self.update_temp_data(orig, dest)
            tree_view_data = self.controller.tree_view_data(descriptive, self.temp_data.loc[:, columns[1:]])
            for row in tree_view_data:
                tree.insert('', tk.END, values=row)
        else:
            self.report_error()

    @staticmethod
    def reset_tree_view(tree):
        """reset descriptive tab, treeview and combobox"""
        for row in tree.get_children():
            tree.delete(row)

    def descriptive(self, frame):
        """descriptive tab components"""
        sub_frame = tk.Frame(frame, bg='#B0C4DE')
        sub_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(sub_frame, bg='#B0C4DE')
        header.pack(fill=tk.BOTH, expand=True)
        small_frame = tk.Frame(sub_frame, bg='#B0C4DE')
        small_frame.pack()
        label = tk.Label(header, text='Descriptive statistic', font=self.my_font_big, bg='#B0C4DE')
        label.pack(anchor=tk.CENTER, pady=10)
        label2 = tk.Label(small_frame, text='Origin airport:', font=self.my_font_small, bg='#B0C4DE')
        label2.grid(row=1, column=0, sticky='e')
        label3 = tk.Label(small_frame, text='Destination airport:', font=self.my_font_small, bg='#B0C4DE')
        label3.grid(row=2, column=0, sticky='e')

        # ARRIVAL_DELAY, AIR_TIME, DISTANCE, ELAPSED_TIME
        # mean std min 25,50,75 max
        # columns, descriptive, label = self.controller.stat_columns()
        columns = ['STATISTICS'] + self.num_col
        descriptive = ['mean', 'std', 'min', 'q1', 'q2', 'q3', 'max']
        label = ['Statistics'] + [x.lower().upper() for x in self.num_col]
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for i, l in zip(columns, label):
            tree.heading(i, text=l)
        tree.pack(expand=True, fill=tk.BOTH)
        #
        # treeXScroll = ttk.Scrollbar(frame, orient='horizontal')
        # treeXScroll.configure(command=tree.xview)
        # tree.configure(xscrollcommand=treeXScroll.set)
        #
        origin_airport = tk.StringVar()
        pick_origin = ttk.Combobox(small_frame, textvariable=origin_airport, font=self.my_font_small)
        pick_origin['values'] = self.controller.get_all_origin()
        pick_origin['state'] = 'readonly'
        pick_origin.grid(row=1, column=1, pady=5, padx=5)

        dest_airport = tk.StringVar()
        pick_dest = ttk.Combobox(small_frame, textvariable=dest_airport, font=self.my_font_small)
        pick_dest['state'] = 'readonly'
        pick_origin.bind("<<ComboboxSelected>>", lambda event: self.update_dest(pick_dest, origin_airport.get()))

        pick_dest.grid(row=2, column=1, pady=5, padx=5)

        button = tk.Button(small_frame, text='Generate', width=10,
                           command=lambda: self.create_tree_view(tree, descriptive,
                                                                 columns, origin_airport.get(),
                                                                 dest_airport.get()), font=self.my_font_small)
        button.grid(row=3, column=0, pady=20)
        reset_btn = tk.Button(small_frame, text='Reset', width=10, command=lambda: self.reset_all_combo(small_frame),
                              font=self.my_font_small)

        reset_btn.grid(row=3, column=1, )
        reset_btn.bind("<Button-1>", lambda e: UI1.reset_tree_view(tree))
        scrollbar = ttk.Scrollbar(
            frame,
            orient='horizontal',
            command=tree.xview
        )
        scrollbar.pack(side='bottom', fill='x')
        tree['xscrollcommand'] = scrollbar.set

    def clear_corr_header(self):
        """clear header text: correlation value"""
        self.corr_label.configure(text=f'Correlation: ')

    def correlation_tab(self, frame):
        """notebook tab: correlation and its components"""
        for i in range(2):
            frame.columnconfigure(i, weight=1)
        left_window, right_window, self.sub_frame = self.two_side_window(frame, 'Correlation')

        self.reset_all_combo(self.sub_frame)
        label = tk.Label(self.sub_frame, text='Attribute 1:', font=self.my_font_small, bg='#B0C4DE')
        label.grid(row=1, column=0, sticky='w')

        label2 = tk.Label(self.sub_frame, text='Attribute 2:', font=self.my_font_small, bg='#B0C4DE')
        label2.grid(row=3, column=0, sticky='w')

        self.x = tk.StringVar()  # pick x attribute
        self.pick_x = ttk.Combobox(self.sub_frame, textvariable=self.x, font=self.my_font_small, width=22)
        self.pick_x['state'] = 'readonly'
        self.pick_x['values'] = self.controller.data.num_attributes()
        self.pick_x.grid(row=2, column=0, pady=5, padx=5)
        self.y = tk.StringVar()  # pick y attribute
        self.pick_y = ttk.Combobox(self.sub_frame, textvariable=self.y, font=self.my_font_small, width=22)
        self.pick_y['state'] = 'readonly'
        self.pick_y['values'] = self.controller.data.num_attributes()
        self.pick_y.grid(row=4, column=0, pady=5, padx=5)

        button = tk.Button(left_window, text='Generate', width=10,
                           command=lambda: self.draw_corr(self.pick_x.get(), self.pick_y.get(), self.ax2),
                           font=self.my_font_small)
        button.pack(pady=10)

        button.bind("<Button-1>", lambda e: self.display_corr(self.pick_x.get(), self.pick_y.get()), add='+')
        reset_btn = tk.Button(left_window, text='Reset', width=10,
                              command=lambda: self.reset_all_combo(self.sub_frame, self.corr, self.ax2),
                              font=self.my_font_small)
        reset_btn.pack(pady=10)
        reset_btn.bind("<Button-1>", lambda e: self.clear_corr_header(), add='+')

        button2 = tk.Button(left_window, text='Heatmap', width=10, font=self.my_font_small, command=self.draw_heat_map)
        button2.pack(pady=10)

        self.corr_label = tk.Label(right_window, text='Correlation: ', font=self.my_font_big, bg='#6CA6CD')
        self.corr_label.pack()

        fig, self.ax2 = plt.subplots(figsize=(8, 5))
        self.corr = FigureCanvasTkAgg(fig, master=right_window)
        self.corr.get_tk_widget().pack(padx=30, pady=30, ipadx=50, ipady=50, anchor=tk.CENTER)

    def draw_line(self):
        """draw line graph"""
        self.graph.get_tk_widget().pack_forget()
        fig, self.ax3 = plt.subplots(figsize=(8, 5))
        self.graph = FigureCanvasTkAgg(fig, master=self.right_window3)
        self.graph.get_tk_widget().pack(padx=30, pady=30, ipadx=50, ipady=50, anchor=tk.CENTER)

        if self.pick_attr2.get():
            self.graph.draw()
            self.ax3.clear()
            abbre_month = [calendar.month_abbr[x] for x in range(1, 13)]
            month_int = [x for x in range(1, 13)]
            mean_attr_by_month_df = self.controller.df_groupby('MONTH', self.pick_attr2.get(),
                                                               self.temp_data)  # dataframe
            line_df = self.controller.data.merge_df_blank(mean_attr_by_month_df, self.pick_attr2.get())
            self.ax3.plot(month_int, line_df[self.pick_attr2.get()], color=self.color_arr[2])
            self.ax3.set_xlim(1, 13)
            self.ax3.set_xticks(month_int, abbre_month)
            self.ax3.set_title(f'Monthly trends of {self.pick_attr2.get().lower().replace("_", " ")}')
            if self.pick_attr2.get() == 'DISTANCE':
                self.ax3.set_ylabel(f'{self.pick_attr2.get()} (miles)')
            else:
                self.ax3.set_ylabel(f'{self.pick_attr2.get()} (minutes)')
            self.ax3.set_xlabel('Month')
            self.graph.draw()
        else:
            self.report_error()

    def delayed_pie(self):
        if self.dest_airport2.get() and not self.temp_data.empty:
            total_flights = len(self.temp_data)
            delayed = self.controller.delayed_counts(self.temp_data)
            normal_flights = total_flights - delayed

            temp = self.controller.data.create_series(col=['delayed', 'cancelled', 'normal flights'],
                                                      values=[delayed, normal_flights])
            self.ax3.clear()
            self.graph.draw()

            self.ax3.pie(temp, labels=temp.index, startangle=90, counterclock=False,
                         autopct='%1.1f%%', colors=self.color_arr)

            self.ax3.legend(bbox_to_anchor=(0.79, 1))

            self.ax3.set_title('Pie chart of Delayed and Normal Flights')
            self.graph.draw()
        else:
            self.report_error()

    def overall_pie(self):
        """draw overall pie graph of delayed, cancelled comparing to normal flights"""
        total_flights = len(self.temp_data)
        delayed = self.controller.delayed_counts(self.temp_data)

        cancelled = self.controller.cancelled_counts(self.temp_data)

        normal_flights = total_flights - (delayed + cancelled)

        temp = self.controller.data.create_series(col=['delayed', 'cancelled', 'normal flights'],
                                                  values=[delayed, cancelled, normal_flights])
        self.ax3.clear()
        self.graph.draw()

        self.ax3.pie(temp, labels=temp.index, startangle=90, counterclock=False,
                     autopct='%1.1f%%', colors=self.color_arr)

        self.ax3.legend(bbox_to_anchor=(0.79, 1))

        self.ax3.set_title('Pie chart of Delayed, Cancelled, and Normal Flights')
        self.graph.draw()

    def cancelled_pie(self):
        total_flights = len(self.temp_data)
        cancelled = self.controller.cancelled_counts(self.temp_data)
        normal_flights = total_flights - cancelled
        temp = self.controller.data.create_series(col=['cancelled', 'normal flights'],
                                                  values=[cancelled, normal_flights])
        self.ax3.pie(temp, labels=temp.index, startangle=90, counterclock=False,
                     autopct='%1.1f%%', colors=self.color_arr)

        self.ax3.legend(bbox_to_anchor=(0.79, 1))

        self.ax3.set_title('A pie chart comparing cancelled and non-cancelled flights')
        self.graph.draw()

    def draw_pie(self):
        """draw pie graph based on attribute"""
        atr = self.attribute2.get()
        self.ax3.clear()
        self.graph.draw()
        if atr == 'overall':
            self.overall_pie()
        elif atr == 'Cancelled vs not cancelled flights':
            self.cancelled_pie()
        else:
            self.delayed_pie()

    def on_click_atr(self, atr):
        """change pick_attr2 values based on type of graph user selected"""
        pie_attr = ['overall', 'Cancelled vs not cancelled flights',
                    'Delayed vs not delayed flights']
        self.attribute2.set('')
        self.pick_attr2['values'] = self.num_col if atr == 'line graph' else pie_attr

    def check_all_atr(self, widget):
        """check whether if all widget's combobox was selected"""
        for child in widget.winfo_children():
            if isinstance(child, ttk.Combobox) and child.cget('textvariable') == '':
                self.report_error()



    def other_graphs_tab(self, frame):
        """other graphs tab components"""
        left_window, self.right_window3, sub_frame = self.two_side_window(frame, 'Create Visualization')
        name = ['Graph Type:', 'Airline:', 'Origin airport:', 'Destination airport:', 'Attribute: ']
        t = 0
        for i in range(1, 10, 2):
            label = tk.Label(sub_frame, text=name[t], font=self.my_font_small, bg='#B0C4DE')
            label.grid(row=i, column=0, sticky='w')
            t += 1

        self.type = tk.StringVar()
        self.pick_type2 = ttk.Combobox(sub_frame, textvariable=self.type, font=self.my_font_small)
        self.pick_type2['state'] = 'readonly'
        self.pick_type2.grid(row=2, column=0, pady=5, padx=5)
        self.pick_type2['values'] = ['line graph', 'pie graph']
        self.pick_type2.bind("<<ComboboxSelected>>", lambda event: self.on_click_atr(self.type.get()))

        self.airlines2 = tk.StringVar()
        self.pick_airline2 = ttk.Combobox(sub_frame, textvariable=self.airlines2, font=self.my_font_small)
        self.pick_airline2['state'] = 'readonly'
        self.pick_airline2.grid(row=4, column=0, pady=5, padx=5)
        self.pick_airline2['values'] = self.controller.get_all_airlines()

        self.origin_airport2 = tk.StringVar()
        self.pick_origin2 = ttk.Combobox(sub_frame, textvariable=self.origin_airport2, font=self.my_font_small)
        self.pick_airline2.bind("<<ComboboxSelected>>",
                                lambda event: self.controller.get_airline_data(self.pick_airline2.get(),
                                                                               widget=2))  # set values
        self.pick_origin2['state'] = 'readonly'
        self.pick_origin2.grid(row=6, column=0, pady=5, padx=5)

        self.dest_airport2 = tk.StringVar()
        self.pick_dest2 = ttk.Combobox(sub_frame, textvariable=self.dest_airport2, font=self.my_font_small)
        self.pick_origin2.bind("<<ComboboxSelected>>",
                               lambda x: self.controller.get_origin_data(self.airlines2.get(),
                                                                         self.origin_airport2.get(), widget=2))
        self.pick_dest2['state'] = 'readonly'
        self.pick_dest2.grid(row=8, column=0, pady=5, padx=5)
        self.pick_dest2.bind("<<ComboboxSelected>>", lambda x: self.controller.get_dest_data(self.dest_airport2.get()))

        self.attribute2 = tk.StringVar()
        self.pick_attr2 = ttk.Combobox(sub_frame, textvariable=self.attribute2, font=self.my_font_small)
        self.pick_attr2.grid(row=10, column=0, pady=5, padx=5)
        self.pick_attr2['state'] = 'readonly'

        button = tk.Button(left_window, text='Generate', width=10,
                           font=self.my_font_small)
        button.pack(pady=10)
        button.bind('<Button-1>', lambda e: self.check_all_atr(sub_frame), add='+')
        button.bind('<Button-1>',
                    lambda e: self.draw_line() if self.pick_type2.get() == 'line graph' else self.draw_pie(), add='+')

        reset_btn = tk.Button(left_window, text='Reset', width=10,
                              command=lambda: self.reset_all_combo(sub_frame, self.graph),
                              font=self.my_font_small)
        reset_btn.pack(pady=10)

        reset_btn.bind("<Button-1>", lambda e: UI1.reset_canvas(self.ax3, self.graph), add='+')

        fig, self.ax3 = plt.subplots(figsize=(8, 5))
        self.graph = FigureCanvasTkAgg(fig, master=self.right_window3)
        self.graph.get_tk_widget().pack(padx=30, pady=30, ipadx=50, ipady=50, anchor=tk.CENTER)

    @staticmethod
    def reset_canvas(ax, canvas):
        """reset canvas and axes"""
        ax.clear()
        canvas.get_tk_widget().delete("all")

    def distribution_tab(self, left_window):
        """distribution tab components"""
        text_label = ['Origin airport:', 'Destination airport:', 'Attribute:']
        label = tk.Label(self.frame1_2, text='Distribution', bg='#B0C4DE', font=self.my_font_big)
        label.grid(row=0, columnspan=1, sticky='n', pady=10)
        label2 = tk.Label(self.frame1_2, text='Airlines:', bg='#B0C4DE', font=self.my_font_small)
        label2.grid(row=1, column=0, sticky='w')
        i = 0
        for row in range(3, 9, 2):
            temp = tk.Label(self.frame1_2, text=text_label[i],
                            bg='#B0C4DE', font=self.my_font_small)
            temp.grid(row=row, column=0, sticky='w')
            i += 1

        self.airlines = tk.StringVar()
        self.pick_airline = ttk.Combobox(self.frame1_2, textvariable=self.airlines, font=self.my_font_small)
        self.pick_airline['state'] = 'readonly'
        self.pick_airline.grid(row=2, column=0, pady=5, padx=5)
        self.pick_airline['values'] = self.controller.get_all_airlines()

        self.origin_airport = tk.StringVar()
        self.pick_origin = ttk.Combobox(self.frame1_2, textvariable=self.origin_airport, font=self.my_font_small)
        self.pick_airline.bind("<<ComboboxSelected>>",
                               lambda event: self.controller.get_airline_data(self.pick_airline.get()),
                               add='+')  # set values
        self.pick_origin['state'] = 'readonly'
        self.pick_origin.grid(row=4, column=0, pady=5, padx=5)

        self.dest_airport = tk.StringVar()
        self.pick_dest = ttk.Combobox(self.frame1_2, textvariable=self.dest_airport, font=self.my_font_small)
        self.pick_origin.bind("<<ComboboxSelected>>",
                              lambda x: self.controller.get_origin_data(self.airlines.get(), self.origin_airport.get()),
                              add='+')

        self.pick_dest['state'] = 'readonly'
        # self.pick_dest['state'] = 'readonly'
        self.pick_dest.grid(row=6, column=0, pady=5, padx=5)
        self.pick_dest.bind("<<ComboboxSelected>>", lambda x: self.controller.get_dest_data(self.dest_airport.get()))

        self.attributes = tk.StringVar()  # pick attribute
        self.pick_atr = ttk.Combobox(self.frame1_2, textvariable=self.attributes, font=self.my_font_small)
        self.pick_atr['state'] = 'readonly'
        self.pick_atr['values'] = self.controller.get_all_attributes()
        self.pick_atr.grid(row=8, column=0, pady=5, padx=5)

        button = tk.Button(left_window, text='Generate', width=10,
                           font=self.my_font_small)

        button.bind('<Button-1>', lambda e: self.check_all_atr(self.frame1_2), add='+')
        button.bind('<Button-1>', lambda e: self.draw_dist(self.temp_data, self.attributes.get()), add='+')
        button.pack(pady=10)

        reset_btn = tk.Button(left_window, text='Reset', width=10,
                              command=lambda: self.reset_all_combo(self.frame1_2, self.canvas, self.ax),
                              font=self.my_font_small)
        reset_btn.pack(pady=10)

    def draw_dist(self, data, attribute):
        """draw distribution graph"""
        self.ax.clear()
        self.canvas.draw()
        if (attribute != '' and self.airlines.get() != '' and
                self.dest_airport.get() != '' and self.origin_airport.get() != ''):
            self.ax.hist(data[attribute], color=self.color_arr[1])
            self.ax.set_title(
                f'Distribution of airline {self.airlines.get()} on {attribute} '
                f'from {self.origin_airport.get()} to {self.dest_airport.get()} airport',
                fontsize=11)
            self.ax.set_ylabel('Frequency', fontsize=8)
            self.ax.set_xlabel(attribute.lower().upper(), fontsize=8)
            self.canvas.draw()
        else:
            self.report_error()

    def reset_all_combo(self, widget, canvas=None, ax=None):
        """"reset all combobox of widget, reset canvas and axes"""
        if ax and canvas:
            ax.clear()
            canvas.draw()
        for child in widget.winfo_children():
            if isinstance(child, ttk.Combobox):
                child.set('')
        self.temp_data = None

    def update_dest(self, pick_dest, origin):
        """update pick destination combobox"""
        pick_dest['values'] = self.controller.data.all_destination(origin)

    def init_components(self):
        print('init')
        self.menubar()
        self.notebook = ttk.Notebook(self, width=900, height=500, style="Custom.TNotebook")
        self.notebook.pack(pady=10, expand=True, fill="both")

        # create frames
        frame1 = tk.Frame(self.notebook, bg='#A4D3EE', width=900, height=800)
        frame2 = tk.Frame(self.notebook, width=700, height=600)
        frame3 = ttk.Frame(self.notebook, width=700, height=600)
        frame4 = ttk.Frame(self.notebook, width=700, height=600)

        frame1.pack(fill='both', expand=True)
        frame2.pack(fill='both', expand=True)
        frame3.pack(fill='both', expand=True)
        frame4.pack(fill='both', expand=True)

        left_window = tk.Frame(frame1)

        right_window = tk.Frame(frame1, width=800, height=1200)
        right_window.configure(bg='#6CA6CD')
        self.frame1_2 = tk.Frame(left_window, background='#B0C4DE')
        self.frame1_2.pack(ipady=10, fill="both")

        # add frames to notebook

        self.notebook.add(frame1, text='Distribution')
        self.notebook.add(frame2, text='Correlation')
        self.notebook.add(frame3, text='Graphs')
        self.notebook.add(frame4, text='Descriptive Statistic')

        fig = Figure()
        self.ax = fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(fig, master=right_window)
        self.canvas.get_tk_widget().pack(padx=30, pady=30, ipadx=50, ipady=50, anchor=tk.CENTER)

        self.distribution_tab(left_window)
        self.other_graphs_tab(frame3)
        self.correlation_tab(frame2)
        self.descriptive(frame4)

        # self.notebook.columnconfigure((0, 1), weight=1)
        left_window.pack(side=tk.LEFT, fill="both", expand=True, anchor=tk.SW)
        right_window.pack(side=tk.RIGHT, fill="both", expand=True)
        left_window.configure(bg='#B0C4DE')

        # self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.reset_all_combo(self.frame1_2), add='+')
        # self.correlation_tab(frame)
        # left_window.grid(row=0,column=0, columnspan=3,sticky='w')
        # right_window.grid(row=0,column=3,columnspan=2) #sticky='e'

    def report_error(self):
        """report error when combobox value is missing"""
        messagebox.showwarning('Warning', 'Please select all remaining field(s)')

    def run(self):
        """run the ui"""
        self.mainloop()
