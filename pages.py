from tkinter import *
from tkinter.filedialog import askopenfilename
from GetData import plot
from PIL import Image, ImageTk
from enum import IntEnum


class PageNum(IntEnum):
    CHARTONE = 0
    CHARTTWO = 1
    CHARTTHREE = 2
    CHARTFOUR = 3
    CHARTFIVE = 4


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
        main.configure(background='#D9D9D9') #right; for img
        info.configure(background='#049CB8') #left; for text
        self.configure(background='#D9D9D9') #far right col

        # create sub widgets
        welcome = Label(info, text="\n\n Welcome to \n Robo-Endo",
            fg="#EFEFEF", bg="#049CB8", font= ('Helvetica 15 bold', 45))
        nav = Label(info, text=" Please navigate to:\n https://tconnect.tandem\n diabetes.com/login.aspx",
            fg="#EFEFEF", bg="#049CB8", font= ('Helvetica 15 bold', 24))
        self.sub_main.grid(row=1, column=1, sticky="")

        self.welcome_image = Image.open("./resources/welcome2.png")
        self.welcome_image = self.welcome_image.resize(
            (500, 412), Image.ANTIALIAS)
        temp_image = ImageTk.PhotoImage(self.welcome_image)
        self.welcome_label = Label(
            self.sub_main, image=temp_image, borderwidth=0)
        self.welcome_label.image = temp_image

        # emplace sub widgets
        welcome.place(relx=.5, rely=.2, anchor="center")
        nav.place(relx=.5, rely=.6, anchor="center")
        self.welcome_label.pack(fill=BOTH)

        # emplace sub frames
        main.grid(row=0, column=1, sticky="nsew")
        info.grid(row=0, column=0, sticky="nsew")
        self.sub_main.grid(row=1, column=1, sticky="")

    def resize_image(self):
        self.welcome_image.resize(
            (self.sub_main.winfo_width(), self.sub_main.winfo_height()))
        temp_image = ImageTk.PhotoImage(self.welcome_image)
        self.welcome_label.grid_remove()
        self.welcome_label = Label(
            self.sub_main, image=temp_image, borderwidth=0)
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
        main.configure(background='#D9D9D9')
        info.configure(background='#D9D9D9')
        self.configure(background='#D9D9D9')

        # create sub widgets
        nav = Label(info, text="After your data\nis uploaded\nclick “Custom” \nand select \na time period\nof 3 or more months",
            fg="#333F50", bg="#D9D9D9", font= ('Helvetica 15 bold', 20))

        dashboard_image = Image.open("./resources/dashboard2.png")
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
        main.configure(background='#D9D9D9')
        info.configure(background='#D9D9D9')
        self.configure(background='#D9D9D9')

        # create sub widgets
        nav = Label(info, text="Now click\n“Reports”",
            fg="#333F50", bg="#D9D9D9", font= ('Helvetica 15 bold', 25))

        report_image = Image.open("./resources/report2.png")
        report_image = report_image.resize((585, 50), Image.ANTIALIAS)
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
        main.configure(background='#D9D9D9')
        info.configure(background='#D9D9D9')
        self.configure(background='#D9D9D9')

        # create sub widgets
        nav = Label(info, text='Under “Save & Print Report” \nchoose “Export Data"',
            fg="#333F50", bg="#D9D9D9", font= ('Helvetica 15 bold', 21))

        export_image = Image.open("./resources/Export2.png")
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
        self.configure(background='#333F50')

        # create subframes under StartPage
        main = Frame(self)

        # colors
        main.configure(background='#D9D9D9')

        # create sub widgets
        nav = Label(main, text="Now choose that file here",
            fg="#333F50", bg="#D9D9D9", font= ('Helvetica 15 bold', 35))
        global choose
        choose = PhotoImage(file = "./resources/next2.png")
        choose_file = Button(main, text="Choose File",
            font= ('Helvetica 15 bold', 30), fg="#EAEAEA", image=choose, compound=CENTER, borderwidth=2, height=80, width=250,
            command=self.select_file)

        # emplace sub widgets
        nav.place(relx=.5, rely=.3, anchor="center")
        choose_file.place(relx=.5, rely=.6, anchor="center")

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
            self.controller.previous_frame()

        self.controller.next_frame()
        self.controller.update_page()

    @staticmethod
    def get_name():
        return "PageFour"


class ChartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.info = Frame(self)
        self.graph = Frame(self)
        self.configure(background='#333F50') #far right
        self.graph.configure(background='#333F50') #behind graph

        self.info.configure(background='#333F50', width=33) #left; behind buttons
        self.graph_info = StringVar()
        # create sub widgets
        self.nav = Label(self.info, textvariable=self.graph_info, font=('Helvetica 15 bold', 25), foreground="white", background='#333F50')
        # emplace sub widgets
        self.nav.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        self.graph.grid(row=0, column=1, sticky="nsew")
        self.info.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "ChartPage"


class RecPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=4)
        self.grid_rowconfigure(0, weight=1, minsize=20)
        self.grid_rowconfigure(1, weight=4)

        title = Frame(self)
        self.recommendations_frame = Frame(self)
        self.configure(background='#D9D9D9')
        self.recommendations_frame.configure(background='#D9D9D9')

        title.configure(background='#333F50') #title; top page
        # create sub widgets
        nav = Label(title, text="Potential Recommendations",
            fg="white", bg="#333F50", font=('Helvetica 15 bold', 33))

        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        self.recommendations_frame.grid(row=1, column=0, sticky="nsew")
        title.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "Recommendation"


class loading_page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        main = Frame(self)

        # colors
        main.configure(background='#333F50')

        # create sub widgets
        nav = Label(main, text="Loading", font=('Helvetica 15 bold', 45), fg="white", bg="#333F50")

        # emplace sub widgets
        nav.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        main.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "loading_page"


class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        # create subframes under StartPage
        left = Frame(self, bg='#D9D9D9')
        left.grid_rowconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)
        left.grid_columnconfigure(1, weight=1)

        right = Frame(self, bg='#D9D9D9')
        right.grid_columnconfigure(0,weight=1)
        right.grid_rowconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        top_right = Frame(right, bg='#D9D9D9')
        bottom_right = Frame(right, bg='#D9D9D9')
        top_left = Frame(left, bg='#D9D9D9')
        top_mid = Frame(left, bg='#D9D9D9')
        bottom_left = Frame(left, bg='#D9D9D9')
        bottom_mid = Frame(left, bg='#D9D9D9')

        # create sub widgets
        global iobanon, cgmanon, avgiob, avgcgm, meal, recom
        iobanon= PhotoImage(file = "./resources/iobanon.png")
        cgmanon= PhotoImage(file = "./resources/cgmanon.png")
        avgiob= PhotoImage(file = "./resources/avgiob.png")
        avgcgm= PhotoImage(file = "./resources/avgcgm.png")
        meal= PhotoImage(file = "./resources/meal.png")
        recom= PhotoImage(file = "./resources/recom.png")
        chart_one_btn = Button(top_left, image=iobanon, width=250, height=120, borderwidth=3, command=lambda: self.controller.display_chart(PageNum.CHARTONE))
        chart_two_btn = Button(top_mid, image=cgmanon, width=250, height=120, borderwidth=3, command=lambda: self.controller.display_chart(PageNum.CHARTTWO))
        chart_three_btn = Button(bottom_left, image=avgiob, width=250, height=120, borderwidth=3, command=lambda: self.controller.display_chart(PageNum.CHARTTHREE))
        chart_four_btn = Button(bottom_mid, image=avgcgm, width=250, height=120, borderwidth=3, command=lambda: self.controller.display_chart(PageNum.CHARTFOUR))
        chart_five_btn = Button(top_right, image=meal, width=250, height=120, borderwidth=3, command=lambda: self.controller.display_chart(PageNum.CHARTFIVE))
        recommendation_btn = Button(bottom_right, image=recom, width=250, height=120, borderwidth=3, command=lambda: self.controller.recommend())


        # emplace sub widgets
        chart_one_btn.place(relx=.5, rely=.5, anchor="center")
        chart_two_btn.place(relx=.5, rely=.5, anchor="center")
        chart_three_btn.place(relx=.5, rely=.5, anchor="center")
        chart_four_btn.place(relx=.5, rely=.5, anchor="center")
        chart_five_btn.place(relx=.5, rely=.5, anchor="center")
        recommendation_btn.place(relx=.5, rely=.5, anchor="center")

        # emplace sub frames
        top_left.grid(row=0, column=0, sticky="nsew")
        top_mid.grid(row=0, column=1, sticky="nsew")
        bottom_left.grid(row=1, column=0, sticky="nsew")
        bottom_mid.grid(row=1, column=1, sticky="nsew")
        bottom_right.grid(row=1, column=0, sticky="nsew")
        top_right.grid(row=0, column=0, sticky="nsew")

        right.grid(row=0, column=1, sticky="nsew")
        left.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def get_name():
        return "MainMenu"


page_set = (StartPage, PageOne, PageTwo, PageThree, PageFour, loading_page)
chart_set = (MainMenu, ChartPage, RecPage)
