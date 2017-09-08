from tkinter import *

class SetupTableLayout:

    frame = None
    skip_first_line = False
    separatorEntry = None

    def __init__(self, master):
        self.master = master
        self.frame = Frame(master, width = 600, height=400, padx=20, pady=30)
        self.frame.pack()

        promptText = Label(
            self.frame, text="Define Settings labels!"
        ).pack(pady=30)

        self.separatorEntry = Entry(
            self.frame
        )

        continueButton = Button(
            self.frame, text="Proceed", command=self.proceed
        ).pack(pady=5)

        firstLineCheckbox = Checkbutton(
            self.frame, text="First line is description", command=self.should_skip_line
        ).pack(pady=10)

        separatorLabel = Label(
            self.frame, text="Set row separator!"
        ).pack()

        self.separatorEntry.pack()

    def should_skip_line(self):
        self.skip_first_line = self.skip_first_line != True

    def proceed(self):

        self.master.prepare_labeling(self.skip_first_line, self.separatorEntry.get())

class SetupJsonLayout:

    frame = None

    properties = None

    def __init__(self, master, jsonProps):
        self.master = master

        self.frame = Frame(master, width = 600, height=400, padx=20, pady=30)
        self.frame.pack()

        self.properties = []

        promptText = Label(
            self.frame, text="Choose properties!"
        ).pack(pady=30)

        continueButton = Button(
            self.frame, text="Proceed", command=self.proceed
        ).pack(pady=5)

        for prop in jsonProps:
            if type(jsonProps[prop]) in [str, int, bool]:
                self.add_property(prop)

    def add_property(self, propertyName):
        outlook = Frame(self.frame, height=1, width=400)
        outlook.pack(pady=5)

        formated = "{:20s}".format(propertyName)

        propertyCheckbox = Checkbutton(
            outlook, text=formated, command=lambda: self.change_state(propertyName)
        ).pack(side=RIGHT)

    def change_state(self, propertyName):
        if propertyName in self.properties:
            self.properties.remove(propertyName)
        else:
            self.properties.append(propertyName)

    def proceed(self):

        self.master.prepare_labeling(properties=self.properties)
