from tkinter import *

class Timer:
    """
    Class for control Timer widget
    """
    # Function when initiate Timer
    def __init__(self, master=None):
        # Set default time and timer state
        self.time = 0
        self.state = False
        # Create timer display
        self.display = Label(
            master, bg="#000", font="terminal 20 bold", fg="#FFF")
        self.display.pack(pady=10, ipadx=10, ipady=10)
        # Start timer clock loop
        self.clock()

    # Function to calculate time to minutes and seconds, then display it to Label
    def clock(self):
        # Add 1 to time variable
        self.time += 1 if self.state else 0
        # Calculate minutes and seconds from time
        if self.time >= 3600: self.time = 0
        minutes = str(self.time // 60).zfill(2)
        seconds = str(self.time % 60).zfill(2)
        # Display minutes and seconds to timer
        self.display.config(text=f"{minutes}:{seconds}")
        # Loop everything again
        self.display.after(1000, self.clock)

    # Function to start timer
    def start(self):
        self.state = True

    # Function to stop timer
    def stop(self):
        self.state = False

    # Function to reset timer
    def reset(self):
        self.time = 0