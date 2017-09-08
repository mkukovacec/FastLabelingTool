from tkinter import *

class EntryLayout:

    frame = None

    def __init__(self, master):

        self.master = master
        self.frame = Frame(master, width = 600, height=400, padx=20, pady=30)

        self.frame.pack()

        promptText = Label(
            self.frame, text="Choose input method!"
        ).pack(pady=70)

        self.excel = Button(
            self.frame, text="Data table", height=2, width=60, command= lambda: self.master.get_excel_file()
        ).pack(pady=15)

        self.json = Button(
            self.frame, text="JSON format", height=2, width=60, command= lambda: self.master.get_JSON_file()
        ).pack(pady=15)
