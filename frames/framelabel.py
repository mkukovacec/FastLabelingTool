import tkinter as tk
from tkinter import *
from tkinter import Frame
from tkinter import Radiobutton
from tkinter import Button
from tkinter import Label

class FrameLabel:

    def __init__(self, master, labelNode, possible_labels):

        self.master = master
        self.group = master.frame_group
        self.possible_labels = possible_labels

        self.frame = Frame(master, width = 600, height=400, padx=20, pady=30)
        self.frame.pack()
        self.selected = StringVar()

        self.labelNode = labelNode

        infoText = Message(self.frame, width=400, text=labelNode.node_info).pack(pady=50)

        for label in possible_labels:
            b = Radiobutton(self.frame, text=label, variable=self.selected, value=label, height=1, width=15, indicatoron=0, command = lambda: self.set_label())
            b.pack(side = TOP, pady=5)
            if label == labelNode.label_out:
                b.select()

        self.back = Button(
            self.frame, text="<", command=lambda: self.group.back()
        ).pack(side=LEFT,pady=50)

        self.next = Button(
            self.frame, text=">", command=lambda: self.group.next()
        ).pack(side=RIGHT, pady=50)


    def set_label(self):
        self.master.frame_group.label_nodes[self.group.current].label_out= self.selected.get()
        self.group.next()


class FrameGroup:

    label_nodes = None
    labelingMode = None
    possible_labels = None
    master = None
    current = None

    def __init__(self, master, label_nodes, labelingMode, possibleLabels):

        self.label_nodes = label_nodes
        self.labelingMode = labelingMode
        self.master = master
        self.possible_labels = possibleLabels
        self.current = 0


    def next(self):
        if self.current + 1 == len(self.label_nodes):
            self.master.file_menu.entryconfigure(0, state=NORMAL)
            return

        self.current += 1

        self.master.all_instances.remove()
        self.master.all_instances.add(FrameLabel(self.master, self.label_nodes[self.current], self.possible_labels))

    def back(self):
        if self.current == 0:
            return

        self.current -= 1

        self.master.all_instances.remove()
        self.master.all_instances.add(FrameLabel(self.master, self.label_nodes[self.current], self.possible_labels))
