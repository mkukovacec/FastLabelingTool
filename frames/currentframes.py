import tkinter as tk

class CurrentFrames(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.all_instances = []

    def add(self, frame):
        self.all_instances.append(frame)

    def remove(self):
        # don't allow the user to destroy the last item
        if len(self.all_instances) > 0:
            subframe = self.all_instances.pop(0)
            subframe.frame.destroy()
