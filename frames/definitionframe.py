from tkinter import *

class DefinitionLayout:

    frame = None

    entries = None

    def __init__(self, master):
        self.master = master
        self.frame = Frame(master, width = 600, height=400, padx=20, pady=30)
        self.frame.pack()
        self.entries = []

        promptText = Label(
            self.frame, text="Define Possible labels!"
        ).pack(pady=30)

        continueButton = Button(
            self.frame, text="Proceed", command=self.set_labels
        ).pack(pady=5)

        addMoreEntriesButton = Button(
            self.frame, text="Add entry", command=self.add_entry
        ).pack(pady=20)

        self.add_entry()
        self.add_entry()

    def add_entry(self):
        if len(self.entries) == 6:
            return

        outlook = Frame(self.frame, height=1, width=400)
        outlook.pack(pady=5)

        label_entry = Text(
            outlook, height=1, width=25
        ).pack(side=LEFT, expand=True, fill='y')

        del_button = Button(
            outlook, text="X", height=1, command= lambda: self.remove_entry(outlook)
        ).pack(side=LEFT, expand=True, fill='y')

        self.entries.append(outlook)

    def remove_entry(self, frame):
        if len(self.entries) == 2:
            return

        self.entries.remove(frame)
        frame.destroy()

    def set_labels(self):
        labels = []

        for fr in self.entries:
            entry = fr.winfo_children()[0]
            label = entry.get("1.0",'end-1c')
            if len(label) == 0:
                continue

            labels.append(label)

        self.master.setup_labeling(labels)
