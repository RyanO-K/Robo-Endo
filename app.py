from pages import *
from GetData import *
from PIL import Image, ImageTk
import os

debug = False


class app(Tk):

    def __init__(self, *args, **kwargs):
        self.recommendation_list = []
        self.data = {}
        self.debug = debug
        Tk.__init__(self, *args, **kwargs)
        self.geometry('950x500')
        # on top of each other, then the one we want visible
        # will be raised above the others

        self.title('RoboEndo')
        self.iconbitmap('./resources/roboendo.ico')
        self.curr_frame = StartPage
        self.container = Frame(self)

        # handles the background of the main frame

        bg_image = Image.open("./resources/background.png")
        bg_image = bg_image.resize((2000, 1000), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(bg_image)
        background_label = Label(self.container, image=bg_image)
        background_label.image = bg_image

        # configures the main frame rows and columns
        # weight is the share of the screen they get, allegedly
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=17)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=18)
        self.container.grid_columnconfigure(2, weight=1)

        self.frames = {}
        for F in page_set:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            # self.frames[page_name] = frame
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=1, sticky="nsew")

        button_container = Frame(self.container, height=200, width=1000)

        button_container.configure(background='#01384C')
        self.container.configure(background="#01384C")

        self.button1 = Button(button_container, text="Next",
                              command=lambda: self.next_frame())
        self.button2 = Button(button_container, text="Previous",
                              command=lambda: self.previous_frame())

        button_container.grid(row=2, column=1, sticky="nsew")
        background_label.place(x=-10, y=-10)

        self.container.pack(fill=BOTH, expand=TRUE)

        self.show_frame("StartPage")
        self.container.update()

    def next_frame(self):
        """this is really ugly but we can refactor it later"""
        for i in range(len(self.frames)):
            if self.curr_frame == list(self.frames.values())[i]:
                return self.show_frame(list(self.frames.values())[i + 1].get_name())
        self.update_page()

    def previous_frame(self):
        """this is really ugly but we can refactor it later"""
        for i in range(len(self.frames)):
            if self.curr_frame == list(self.frames.values())[i]:
                return self.show_frame(list(self.frames.values())[i - 1].get_name())
        self.update_page()

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        self.curr_frame = frame
        frame.tkraise()

        self.update_page()

    def update_page(self):
        self.button1.pack(side=RIGHT)
        self.button2.pack(side=LEFT)

        if self.curr_frame.get_name() in (
                PageFour.get_name(), loading_page.get_name(), MainMenu.get_name(), ChartPage.get_name(), RecPage.get_name()):
            self.button1.pack_forget()
        if self.curr_frame.get_name() in (StartPage.get_name(), loading_page.get_name(), MainMenu.get_name()):
            self.button2.pack_forget()
        if self.curr_frame.get_name() in [ChartPage.get_name(), RecPage.get_name()]:
            self.button2.pack_forget()
            self.button2.configure(text="Back to main menu")
            self.button2.configure(command=lambda: self.show_frame("MainMenu"))
            self.button2.pack(side=LEFT)
        if self.curr_frame.get_name() is loading_page.get_name():
            # ChartPage.show_graph(self.frames[ChartPage.get_name()])
            self.container.update()
            self.frames = {}
            for F in chart_set:
                page_name = F.get_name()
                frame = F(parent=self.container, controller=self)
                self.frames[page_name] = frame

                # put all of the pages in the same location;
                # the one on the top of the stacking order
                # will be the one that is visible.
                frame.grid(row=1, column=1, sticky="nsew")

            temp = plot(self.filename)
            i = 0
            for key in ['IOB', 'ID', 'skipsI', 'carb', 'CGM', 'skipsC', 'anC', 'peaks']:
                self.data[key] = temp[i]
                i += 1
       #     self.recommendation_list = get_recommendations(self.filename)
            self.show_frame(MainMenu.get_name())
        self.container.update()

    def display_chart(self, chart_num):
        try:
            del self.frames[ChartPage.get_name()].canvas

            for widget in self.frames[ChartPage.get_name()].graph.winfo_children():
                widget.destroy()
        except AttributeError:
            pass
        if chart_num is PageNum.CHARTONE:
            self.frames[ChartPage.get_name()].canvas = plotAnIOB(self.filename,
                                                                 self.data['IOB'],
                                                                 self.data['ID'],
                                                                 self.data['skipsI'],
                                                                 self.data['carb'],
                                                                 self.frames[ChartPage.get_name()].graph)
            self.frames[ChartPage.get_name()].graph_info.set(
                "IOB Anomaly Graph")
        if chart_num is PageNum.CHARTTWO:
            self.frames[ChartPage.get_name()].canvas = plotAnCGM(self.filename,
                                                                 self.data['CGM'],
                                                                 self.data['skipsC'],
                                                                 self.data['anC'],
                                                                 self.data['peaks'],
                                                                 self.data['carb'],
                                                                 self.frames[ChartPage.get_name()].graph)
            self.frames[ChartPage.get_name()].graph_info.set(
                "CGM Anomaly Graph")
        if chart_num is PageNum.CHARTTHREE:
            self.frames[ChartPage.get_name()].canvas = plotIOB(self.filename,
                                                               self.data['IOB'],
                                                               self.data['ID'],
                                                               self.data['skipsI'],
                                                               self.data['carb'],
                                                               self.frames[ChartPage.get_name()].graph)
            self.frames[ChartPage.get_name()].graph_info.set("IOB Graph")
        if chart_num is PageNum.CHARTFOUR:
            self.frames[ChartPage.get_name()].canvas = plotCGM(self.filename,
                                                               self.data['CGM'],
                                                               self.data['skipsC'],
                                                               self.data['anC'],
                                                               self.data['carb'],
                                                               self.frames[ChartPage.get_name()].graph)
            self.frames[ChartPage.get_name()].graph_info.set("CGM Graph")
        self.show_frame(ChartPage.get_name())

    def recommend(self):
        # self.recommendation_list += "Have Better Blood Sugar", "Eat Better", "Inject before eating", "Adjust basal"

        self.frames[RecPage.get_name()].recommendations_frame.grid_rowconfigure(
            0, weight=1)
        self.frames[RecPage.get_name()].recommendations_frame.grid_columnconfigure(
            0, weight=1)
        self.frames[RecPage.get_name()].recommendations_frame.grid_columnconfigure(
            1, weight=2)
        self.frames[RecPage.get_name()].recommendations_frame.grid_columnconfigure(
            2, weight=1)

        list_canvas = Listbox(self.frames[RecPage.get_name(
        )].recommendations_frame, bg='#303030', fg='white')
        list_canvas.grid(row=0, column=1, sticky="nsew")
        list_canvas.configure(font=('Times', 25))
        if len(self.recommendation_list) > 13:
            w = Scrollbar(
                self.frames[RecPage.get_name()].recommendations_frame)
            w.grid(row=0, column=2, sticky="nsw")
            w.config(command=list_canvas.yview)
            list_canvas.configure(yscrollcommand=w.set)

        index = 1

        for entry in self.recommendation_list:
            list_canvas.insert(END, str(index) + ": " + entry)
            # emplace sub widgets

            index += 1

        self.show_frame(RecPage.get_name())


if __name__ == '__main__':
    if os.environ.get("DEBUG"):
        debug = True
    app = app()
    app.mainloop()
