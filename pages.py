from tkinter import *
from tkinter.filedialog import askopenfilename
from GetData import plot


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize StartPage's row and col
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        info = Frame(self)
        main = Frame(self)

        # organize main's row and col
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # colors
        main.configure(background='#303030')
        info.configure(background='#01384C')
        self.configure(background='red')

        # create sub widgets
        welcome = Label(info, text="Welcome to Robo-Endo")
        nav = Label(info, text="Please navigate to:\nhttps://tconnect.tandemdiabetes.com/login.aspx")

        button1 = Button(main, text="Go to Page One",
                         command=lambda: controller.show_frame("PageOne"))
        button2 = Button(main, text="Go to Page Two",
                         command=lambda: controller.show_frame("PageTwo"))

        # emplace sub widgets
        welcome.place(relx=.5, rely=.2, anchor="center")
        nav.place(relx=.5, rely=.7, anchor="center")
        button1.grid(row=0, column=0, sticky="")
        button2.grid(row=0, column=1, sticky="")

        # emplace sub frames
        main.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "StartPage"


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize PageOne's row and col
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        info = Frame(self)
        main = Frame(self)

        # organize main's row and col
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # colors
        main.configure(background='#303030')
        info.configure(background='#01384C')

        # create sub widgets
        nav = Label(info, text="After your data is uploaded click\n“Custom” and select a time\nperiod of 3 or more months")

        button1 = Button(main, text="Go to Page One",
                         command=lambda: controller.show_frame("PageOne"))
        button2 = Button(main, text="Go to Page Two",
                         command=lambda: controller.show_frame("PageTwo"))

        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")
        button1.grid(row=0, column=0, sticky="")
        button2.grid(row=0, column=1, sticky="")

        # emplace sub frames
        main.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "PageOne"


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize PageTwo's row and col
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        info = Frame(self)
        main = Frame(self)

        # organize main's row and col
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # colors
        main.configure(background='#303030')
        info.configure(background='#01384C')

        # create sub widgets
        nav = Label(info, text="Now click\n“Reports”")

        button1 = Button(main, text="Go to Page One",
                         command=lambda: controller.show_frame("PageOne"))
        button2 = Button(main, text="Go to Page Two",
                         command=lambda: controller.show_frame("PageTwo"))

        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")
        button1.grid(row=0, column=0, sticky="")
        button2.grid(row=0, column=1, sticky="")

        # emplace sub frames
        main.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "PageTwo"


class PageThree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # organize PageThree's row and col
        # why is col 1 bigger on this one????
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

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
        return "PageThree"


class ChartOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        info = Frame(self)
        self.graph = Frame(self)

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

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        info = Frame(self)
        self.graph = Frame(self)

        info.configure(background='#01384C')

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
        self.graph = Frame(self)

        info.configure(background='#01384C')

        # create sub widgets
        nav = Label(info, text="This graph is 4")
        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        self.graph.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")

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


page_set = (StartPage, PageOne, PageTwo, PageThree, loading_page, ChartOne, ChartTwo, ChartThree,ChartFour)
