from tkinter import *

class Slider(Frame):
    """
    Class for controlling Slider Widget
    """
    # Function when initiate Counter
    def __init__(self, master=None, from_=0, to=100, default=0, text=None):
        # Create background frame element
        super().__init__(master)
        # Create value variable
        self.value = StringVar(master, value=default)
        # Create Entry Widget
        self.display = Entry(self, textvariable=self.value, width=2, font="terminal 10")
        self.display.pack(side=LEFT, ipadx=3, ipady=1, padx=5, pady=5)
        # Create Scale Widget
        self.slider = Scale(self, from_=from_, to=to, orient=HORIZONTAL, showvalue=False, variable=self.value)
        self.slider.pack(side=LEFT, padx=2, pady=1)

    def set_value(self, value):
        self.value.set(value)

    def get_value(self):
        return self.value.get()

    def disable(self):
        self.slider.config(state=DISABLED)
        self.display.config(state=DISABLED)
    
    def enable(self):
        self.slider.config(state=NORMAL)
        self.display.config(state=NORMAL)
    
    def toggle(self):
        if self.slider['state'] == DISABLED:
            self.enable()
        else:
            self.disable()