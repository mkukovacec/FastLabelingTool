from frames.entryframe import EntryLayout
from frames.definitionframe import DefinitionLayout
from frames.setupframe import SetupTableLayout
from frames.setupframe import SetupJsonLayout
from frames.currentframes import CurrentFrames
from frames.framelabel import FrameGroup
from frames.framelabel import FrameLabel

from labelnode import LabelNode

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *

import pickle
import re
import json

class GUI(tk.Tk):

    CURRENT_LAYOUT = None
    CURRENT_LABELS = None
    CURRENT_FILE = None
    LABELING_MODE = None
    ROW_SEPARATOR = None
    SKIP_FIRST_LINE = False
    FIRST_ROW = False

    file_menu = False
    frame_group = None

    def __init__(self):
        tk.Tk.__init__(self)
        self.master_frame = tk.Frame(self)
        self.all_instances = CurrentFrames(self.master_frame)
        self.setup_menu()

        # create the first frame
        self.all_instances.add(EntryLayout(self))

    def setup_menu(self):
        menubar = Menu(self)
        self.file_menu = Menu(menubar, tearoff=0)
        self.file_menu.add_command(label="Save", command = self.save, state=DISABLED)
        self.file_menu.add_command(label="Reset", command = self.reset)

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=self.file_menu)

        self.config(menu=menubar)

    def get_excel_file(self):
        filename=askopenfilename(filetypes = (("Table Files", "*.?sv"),("Excel Files", "*.xl*")))

        if not filename:
            return

        if self.file_check(["[A-Za-z0-9]*..sv","[A-Za-z0-9]*.xl[a-z]+"], False, filename):

            self.CURRENT_FILE=filename
            self.LABELING_MODE = "TABLE"

            self.setup_defitinion()
        else:
            messagebox.showinfo("Error", "Chosen file is not appropriate")


    def get_JSON_file(self):
        filename=askopenfilename(filetypes = (("JSON Files", "*.json"),("All Files", "*.*")))

        if not filename:
            return

        if self.file_check(["[A-Za-z0-9]*.json"], False, filename):
            self.CURRENT_FILE=filename
            self.LABELING_MODE="JSON"
            self.setup_defitinion()
        else:
            messagebox.showinfo("Error", "Chosen file is not JSON")

    def load_xcel(self, filename):
        return open(filename).readlines()

    def load_json(self, filename):
        return json.load(open(filename))

    def file_check(self, regex_list, directory, filename):

        if directory:
            if os.path.isdir(filename):
                return True
            else:
                return False

        filename = filename.split('/')[-1]

        for reg in regex_list:
            if re.match(reg, filename):
                return True

        return False

    def setup_defitinion(self):
        self.all_instances.remove()
        self.all_instances.add(DefinitionLayout(self))

    def setup_labeling(self, labels):

        self.CURRENT_LABELS = labels
        self.all_instances.remove()

        if self.LABELING_MODE=="TABLE":
            self.all_instances.add(SetupTableLayout(self))
        else:
            self.all_instances.add(SetupJsonLayout(self, self.load_json(self.CURRENT_FILE)[0]))

    def prepare_labeling(self, skip_first_line = False, separator = '', properties = []):

        self.SKIP_FIRST_LINE = skip_first_line
        self.ROW_SEPARATOR = separator

        self.all_instances.remove()

        start = 0
        label_nodes = []

        if self.LABELING_MODE=="TABLE":
            lines = self.load_xcel(self.CURRENT_FILE)

            if skip_first_line:
                self.FIRST_ROW = lines[start]
                start += 1

            for i in range(start, len(lines)):
                note_info = '\n'.join(lines[i].split(separator))
                label_nodes.append(LabelNode(note_info))

            self.frame_group = FrameGroup(self, label_nodes, self.LABELING_MODE, self.CURRENT_LABELS)
            self.all_instances.add(FrameLabel(self, label_nodes[0], self.CURRENT_LABELS))

        else:
            data = self.load_json(self.CURRENT_FILE)

            for i in range(start, len(data)):
                note_info = ''
                for prop in properties:
                    if prop in data[i]:
                        note_info += "{0} : {1}\n".format(prop, str(data[i][prop]))
                label_nodes.append(LabelNode(note_info.strip()))

            self.frame_group = FrameGroup(self, label_nodes, self.LABELING_MODE, self.CURRENT_LABELS)
            self.all_instances.add(FrameLabel(self, label_nodes[0], self.CURRENT_LABELS))


    def save(self):
        file_name = asksaveasfilename()
        with open(file_name, 'w') as target:
            if self.LABELING_MODE=='TABLE':
                if self.SKIP_FIRST_LINE:
                    outputline = self.FIRST_ROW + self.ROW_SEPARATOR + "label\n"
                    target.write(outputline)
                for node in self.frame_group.label_nodes:
                    outputline = self.ROW_SEPARATOR.join(node.node_info.split('\n')) + node.label_out + "\n"
                    target.write(outputline)
            else:
                data = self.load_json(self.CURRENT_FILE)
                for i in range(0, len(data)):
                    data[i]["label"] = self.frame_group.label_nodes[i].label_out

                    target.write(json.dumps(data, indent=4, sort_keys=True))

    def reset(self):
        self.all_instances.remove()
        self.file_menu.entryconfigure(0, state=DISABLED)
        self.all_instances.add(EntryLayout(self))
