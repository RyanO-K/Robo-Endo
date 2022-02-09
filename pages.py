from tkinter import *
from tkinter.filedialog import askopenfilename
from GetData import plot
from PIL import Image, ImageTk


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize StartPage's row and col
        self.grid_columnconfigure(0, weight=4, minsize=200)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        info = Frame(self)
        main = Frame(self)
        self.sub_main = Frame(main)

        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=17)
        main.grid_rowconfigure(2, weight=1)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=17)
        main.grid_columnconfigure(2, weight=1)

        # colors
        main.configure(background='#303030')
        info.configure(background='#01384C')
        self.configure(background='#01384C')

        # create sub widgets
        welcome = Label(info, text="Welcome to Robo-Endo")
        nav = Label(info, text="Please navigate to:\nhttps://tconnect.tandemdiabetes.com/login.aspx")
        self.sub_main.grid(row=1, column=1, sticky="")

        self.welcome_image = Image.open("./resources/welcome.png")
        self.welcome_image = self.welcome_image.resize((500, 400), Image.ANTIALIAS)
        temp_image = ImageTk.PhotoImage(self.welcome_image)
        self.welcome_label = Label(self.sub_main, image=temp_image, borderwidth=0)
        self.welcome_label.image = temp_image

        # emplace sub widgets
        welcome.place(relx=.5, rely=.2, anchor="center")
        nav.place(relx=.5, rely=.7, anchor="center")
        self.welcome_label.pack(fill=BOTH)

        # emplace sub frames
        main.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")
        self.sub_main.grid(row=1, column=1, sticky="")

    def resize_image(self):
        self.welcome_image.resize((self.sub_main.winfo_width(), self.sub_main.winfo_height()))
        temp_image = ImageTk.PhotoImage(self.welcome_image)
        self.welcome_label.grid_remove()
        self.welcome_label = Label(self.sub_main, image=temp_image, borderwidth=0)
        self.welcome_label.image = temp_image
        self.welcome_label.grid(row=0, column=0, sticky="nsew")

        return self.sub_main.winfo_width(), self.sub_main.winfo_height()

    @staticmethod
    def get_name():
        return "StartPage"


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize PageOne's row and col
        self.grid_columnconfigure(0, weight=4, minsize=200)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        info = Frame(self)
        main = Frame(self)
        sub_main = Frame(main)

        # organize main's row and col
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=17)
        main.grid_rowconfigure(2, weight=1)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=17)
        main.grid_columnconfigure(2, weight=1)

        # colors
        main.configure(background='#303030')
        info.configure(background='#01384C')
        self.configure(background='#01384C')

        # create sub widgets
        nav = Label(info, text="After your data is uploaded click\n“Custom” and select a time\nperiod of 3 or more months")

        dashboard_image = Image.open("./resources/dashboard.png")
        dashboard_image = ImageTk.PhotoImage(dashboard_image)
        dashboard_label = Label(sub_main, image=dashboard_image, borderwidth=0)
        dashboard_label.image = dashboard_image

        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")
        dashboard_label.grid(row=0, column=0, sticky="")

        # emplace sub frames
        main.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")
        sub_main.grid(row=1, column=1, sticky="")

    @staticmethod
    def get_name():
        return "PageOne"


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize PageTwo's row and col
        self.grid_columnconfigure(0, weight=4, minsize=200)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        info = Frame(self)
        main = Frame(self)
        sub_main = Frame(main)

        # organize main's row and col
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=17)
        main.grid_rowconfigure(2, weight=1)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=17)
        main.grid_columnconfigure(2, weight=1)

        # colors
        main.configure(background='#303030')
        info.configure(background='#01384C')
        self.configure(background='#01384C')

        # create sub widgets
        nav = Label(info, text="Now click\n“Reports”")

        report_image = Image.open("./resources/report.png")
        report_image = report_image.resize((500, 60), Image.ANTIALIAS)
        report_image = ImageTk.PhotoImage(report_image)
        report_label = Label(sub_main, image=report_image, borderwidth=0)
        report_label.image = report_image

        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")
        report_label.grid(row=0, column=0, sticky="")

        # emplace sub frames
        main.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")
        sub_main.grid(row=1, column=1, sticky="")

    @staticmethod
    def get_name():
        return "PageTwo"


class PageThree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize PageTwo's row and col
        self.grid_columnconfigure(0, weight=4, minsize=200)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        info = Frame(self)
        main = Frame(self)
        sub_main = Frame(main)

        # organize main's row and col
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=17)
        main.grid_rowconfigure(2, weight=1)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=17)
        main.grid_columnconfigure(2, weight=1)

        # colors
        main.configure(background='#303030')
        info.configure(background='#01384C')
        self.configure(background='#01384C')

        # create sub widgets
        nav = Label(info, text='Under “Save & Print Report” \nchoose “Export Data"')

        export_image = Image.open("./resources/export.png")
        export_image = ImageTk.PhotoImage(export_image)
        export_label = Label(sub_main, image=export_image, borderwidth=0)
        export_label.image = export_image

        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")
        export_label.grid(row=0, column=0, sticky="")

        # emplace sub frames
        main.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")
        sub_main.grid(row=1, column=1, sticky="")

    @staticmethod
    def get_name():
        return "PageThree"


class PageFour(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize PageFour's row and col
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(background='#01384C')

        # create subframes under StartPage
        main = Frame(self)

        # colors
        main.configure(background='#303030')

        # create sub widgets
        nav = Label(main, text="Now choose that file here")
        choose_file = Button(main, text="Choose File",
                             command=self.select_file)

        # emplace sub widgets
        nav.place(relx=.5, rely=.3, anchor="center")
        choose_file.place(relx=.5, rely=.7, anchor="center")

        # emplace sub frames
        main.grid(row=0, column=0, sticky="nsew")

    def select_file(self):

        filetypes = (
            ('Excel files', '*.xlsx *.xls *.csv'),
        )
        try:
            filename = askopenfilename(filetypes=filetypes)
            self.controller.filename = filename
        except FileNotFoundError:
            return

        self.controller.next_frame()

    @staticmethod
    def get_name():
        return "PageFour"


class ChartOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        info = Frame(self)
        self.graph = Frame(self)
        self.configure(background='#01384C')
        self.graph.configure(background='#303030')

        info.configure(background='#01384C')

        # create sub widgets
        nav = Label(info, text="This graph is 1")
        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        self.graph.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "ChartOne"


class ChartTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        info = Frame(self)
        self.graph = Frame(self)

        info.configure(background='#01384C')
        self.configure(background='#01384C')
        self.graph.configure(background='#303030')

        # create sub widgets
        nav = Label(info, text="This graph is 2")
        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        self.graph.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "ChartTwo"


class ChartThree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        info = Frame(self)
        self.graph = Frame(self)

        info.configure(background='#01384C')
        self.graph.configure(background='#303030')

        # create sub widgets
        nav = Label(info, text="This graph is 3")
        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        self.graph.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "ChartThree"


class ChartFour(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        info = Frame(self)
        main = Frame(self)
        self.graph = Frame(main)

        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=17)
        main.grid_rowconfigure(2, weight=1)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=17)
        main.grid_columnconfigure(2, weight=1)

        info.configure(background='#01384C')
        self.graph.configure(background='#303030')
        main.configure(background='#303030')

        # create sub widgets
        nav = Label(info, text="This graph is 4")
        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        self.graph.grid(row=1, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")
        main.grid(row=0, column=1, sticky="nsew")

    @staticmethod
    def get_name():
        return "ChartFour"


class loading_page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        main = Frame(self)

        # colors
        main.configure(background='#303030')

        # create sub widgets
        nav = Label(main, text="Loading")

        # emplace sub widgets
        nav.place(relx=.5, rely=.3, anchor="center")

        # emplace sub frames
        main.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "loading_page"


class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create subframes under StartPage
        top_left = Frame(self)
        top_right = Frame(self)
        bottom_left = Frame(self)
        bottom_right = Frame(self)

        # create sub widgets
        chart_one_btn = Button(top_left, text="IOB Anomalies", command=lambda: self.controller.show_frame(ChartOne.get_name()))
        chart_two_btn = Button(top_right, text="CGM Anomalies", command=lambda: self.controller.show_frame(ChartTwo.get_name()))
        chart_three_btn = Button(bottom_left, text="IOB over time", command=lambda: self.controller.show_frame(ChartThree.get_name()))
        chart_four_btn = Button(bottom_right, text="CGM over time", command=lambda: self.controller.show_frame(ChartFour.get_name()))

        # emplace sub widgets
        chart_one_btn.place(relx=.5, rely=.5, anchor="center")
        chart_two_btn.place(relx=.5, rely=.5, anchor="center")
        chart_three_btn.place(relx=.5, rely=.5, anchor="center")
        chart_four_btn.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        top_left.grid(row=0, column=0, sticky="nsew")
        top_right.grid(row=0, column=1, sticky="nsew")
        bottom_left.grid(row=1, column=0, sticky="nsew")
        bottom_right.grid(row=1, column=1, sticky="nsew")

    @staticmethod
    def get_name():
        return "MainMenu"


page_set = (StartPage, PageOne, PageTwo, PageThree, PageFour, loading_page, MainMenu, ChartOne, ChartTwo, ChartThree, ChartFour)
chart_names = (ChartOne.get_name(), ChartTwo.get_name(), ChartThree.get_name(), ChartFour.get_name())
