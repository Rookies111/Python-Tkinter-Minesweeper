from tkinter import *

class Counter(Frame):
    """
    Class for controlling Counter widget
    """
    # Function when initiate Counter
    def __init__(self, master=None, icon=None, default: int=0):
        # Create number variable
        self.total = abs(default)
        # Create background frame element
        super().__init__(master)
        # Create Counter icon
        Label(self, image=icon).pack(pady=5)
        # Create Counter display
        txt = str(self.total).zfill(2)
        self.display = Label(self, text=txt, bg="#000", font="terminal 16 bold", fg="#FFF")
        self.display.pack(ipadx=5, ipady=5)

    # Function to set Counter number
    def set(self, number: int):
        self.total = number
        self.display.config(text=str(self.total).zfill(2))
    
    # Function to reset Counter number
    def reset(self):
        self.total = 0
        self.display.config(text=str(self.total).zfill(2))

    # Function to increment Counter number
    def increse(self):
        self.total += 1
        self.display.config(text=str(self.total).zfill(2))

    # Function to decrement Counter number
    def decrese(self):
        self.total -= 1
        self.display.config(text=str(self.total).zfill(2))