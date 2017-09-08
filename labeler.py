from userinterface import GUI

if __name__ == '__main__':

    root = GUI()
    root.title('Fast Labeling Tool')
    root.geometry('{}x{}+{}+{}'.format(640, 480, 200, 200))
    root.bind_all('<Control-Key-s>', GUI.save)
    root.mainloop()
    # root.destroy() not needed
