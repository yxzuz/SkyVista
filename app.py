# view
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg") # tells that u want to use tkinter backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # allow to dig canvas and put it on app
from matplotlib.figure import Figure
from PIL import ImageTk, Image
import seaborn as sns
from pandas.plotting import scatter_matrix

class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.geometry('700x600')
        self.title('SkyVista')
        self.init_components()



    # def distribution_tab(self):
    #

    def draw_graph(self):
        self.ax.clear()
        x = np.arange(100)
        self.ax.plot(x, x ** 2)
        self.canvas.draw()

    def reset(self):
        self.ax.clear()
    def init_components(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        # create frames
        frame1 = tk.Frame(self.notebook,bg='grey', width=700, height=600)
        frame2 = tk.Frame(self.notebook, width=700, height=600)
        frame3 = ttk.Frame(self.notebook, width=700, height=600)
        frame4 = ttk.Frame(self.notebook, width=700, height=600)

        frame1.pack()
        left_window = tk.Frame(frame1, width=300, height=600)
        left_window.configure(bg='pink')
        left_window.grid(row=0, columnspan=3)
        right_window = tk.Frame(frame1, width=700, height=600)
        right_window.configure(bg='grey')
        right_window.grid(row=0,column=3)

        # frame1.pack(fill='both', expand=True)
        # frame2.pack(fill='both', expand=True)

        self.generate_btn = Image.open('Generate.png').resize((100,30))
        self.generate_btn_tk = ImageTk.PhotoImage(self.generate_btn)
        # Label = tk.Label(left_window,text='Select criteria:',font=('Helvatic',30))
        # Label.place(x=40,y=0)



        # Label2 = tk.Label(left_window,text='Origin:')
        # Label2.place(x=80,y=100)
        # Label3 = tk.Label(left_window, text='Destination:')
        # Label3.place(x=50, y=150)
        #
        # Label4 = tk.Label(left_window,text='Attribute:')
        # Label4.place(x=65,y=200)
        #
        # Reset_btn = tk.Button(left_window,text='Reset')
        # Reset_btn.place(x=65,y=300)
        # add frames to notebook
        self.notebook.add(frame1, text='Distribution')
        self.notebook.add(frame2, text='Correlation')
        self.notebook.add(frame3, text='Graphs')
        self.notebook.add(frame4, text='Descriptive Statistic')



        fig = Figure()
        self.ax = fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(fig,master=right_window)
        self.canvas.get_tk_widget().pack()

        # , image = self.generate_btn
        self.bg = Image.open('page1.png')
        self.page1_tk = ImageTk.PhotoImage(self.bg)
        self.canvas2 = tk.Canvas(left_window,bg='grey',width=400,height=600,bd= 0, highlightthickness= 0, relief= 'ridge')
        self.canvas2.pack(fill='both',expand=True)

        # # Place the image on the Canvas
        self.canvas2.create_image(0,0,image=self.page1_tk,anchor='nw')

        button = ttk.Button(self.canvas2, text='Generate', command=self.draw_graph)
        button.place(x=70,y=500)
        Reset_btn = tk.Button(self.canvas2,text='Reset',command=self.reset,bg='red')
        Reset_btn.place(x=230,y=500)


    def run(self):
        self.mainloop()


# if __name__ == '__main__':
#     app = UI()
#     app.run()