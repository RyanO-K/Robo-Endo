
from pages import *


class app(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry('950x500')
        # on top of each other, then the one we want visible
        # will be raised above the others

        self.title('RoboEndo')
        self.iconbitmap('roboendo.ico')
        self.curr_frame = StartPage
        container = Frame(self)

        container.configure(background='purple')
        container.grid_rowconfigure(0, weight=9)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, loading_page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        button_container = Frame(container, height=200, width=1000)
        button_container.configure(background='green')

        self.button1 = Button(button_container, text="Next",
                              command=lambda: self.next_frame())
        self.button2 = Button(button_container, text="Previous",
                              command=lambda: self.previous_frame())
        button_container.grid(row=1, column=0, sticky="nsew")

        container.pack(fill=BOTH, expand=TRUE)

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
        if self.curr_frame.get_name() == loading_page.get_name(loading_page):
            # call the analytics
            for line in self.file:
                print(line)

        self.update()

    def update(self):
        self.button1.pack(side=RIGHT)
        self.button2.pack(side=LEFT)

        if self.curr_frame.get_name() == "PageThree":
            self.button1.pack_forget()
        elif self.curr_frame.get_name() == "StartPage":
            self.button2.pack_forget()


if __name__ == '__main__':
    app = app()
    app.mainloop()
