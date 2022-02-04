from pages import *
from PIL import Image, ImageTk


class app(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry('950x500')
        # on top of each other, then the one we want visible
        # will be raised above the others

        self.title('RoboEndo')
        self.iconbitmap('./resources/roboendo.ico')
        self.curr_frame = StartPage
        self.container = Frame(self)
        self.bind("<Configure>", self.resize)

        # handles the background of the main frame

        bg_image = Image.open("./resources/background.png")
        bg_image = bg_image.resize((1000, 1000), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(bg_image)
        background_label = Label(self.container, image=bg_image)
        background_label.image = bg_image

        self.container.configure(background="purple")

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
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=1, sticky="nsew")

        button_container = Frame(self.container, height=200, width=1000)
        button_container.configure(background='green')

        self.button1 = Button(button_container, text="Next",
                              command=lambda: self.next_frame())
        self.button2 = Button(button_container, text="Previous",
                              command=lambda: self.previous_frame())

        button_container.grid(row=2, column=1, sticky="nsew")
        background_label.place(x=-10, y=-10)

        self.container.pack(fill=BOTH, expand=TRUE)

        self.show_frame("StartPage")
        self.update()

    def next_frame(self):
        """this is really ugly but we can refactor it later"""
        for i in range(len(self.frames)):
            if self.curr_frame == list(self.frames.values())[i]:
                return self.show_frame(list(self.frames.values())[i + 1].get_name())
        self.update()

    def previous_frame(self):
        """this is really ugly but we can refactor it later"""
        for i in range(len(self.frames)):
            if self.curr_frame == list(self.frames.values())[i]:
                return self.show_frame(list(self.frames.values())[i - 1].get_name())
        self.update()

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        self.curr_frame = frame
        frame.tkraise()

        self.update()

    def resize(self, event):
        if event.widget == self:
            if self.curr_frame.get_name() in [ChartTwo.get_name(), ChartOne.get_name()]:
                self.frames[ChartOne.get_name()].canvas.get_tk_widget().pack_forget()
                self.frames[ChartTwo.get_name()].canvas.get_tk_widget().pack_forget()
                self.frames[ChartTwo.get_name()].canvas.figure.tight_layout()
                self.frames[ChartTwo.get_name()].canvas.figure.tight_layout()
                self.frames[ChartOne.get_name()].canvas.get_tk_widget().pack()
                self.frames[ChartTwo.get_name()].canvas.get_tk_widget().pack()

                print(f"Resize: {self.curr_frame.get_name()}")

    def update(self):
        self.button1.pack(side=RIGHT)
        self.button2.pack(side=LEFT)

        if self.curr_frame.get_name() in [PageThree.get_name(), loading_page.get_name(), ChartFour.get_name()]:
            self.button1.pack_forget()
        if self.curr_frame.get_name() in [StartPage.get_name(), loading_page.get_name(), ChartOne.get_name()]:
            self.button2.pack_forget()
        if self.curr_frame.get_name() in [loading_page.get_name()]:
            # ChartOne.show_graph(self.frames[ChartOne.get_name()])

            # this line is ugly, send help
            # TODO: Refactor this line
            self.frames[ChartOne.get_name()].canvas, \
            self.frames[ChartTwo.get_name()].canvas, \
            self.frames[ChartThree.get_name()].canvas, \
            self.frames[ChartFour.get_name()].canvas = plot(
                self.filename,
                self.frames[ChartOne.get_name()].graph,
                self.frames[ChartTwo.get_name()].graph,
                self.frames[ChartThree.get_name()].graph,
                self.frames[ChartFour.get_name()].graph)

            self.next_frame()


if __name__ == '__main__':
    app = app()
    app.mainloop()
