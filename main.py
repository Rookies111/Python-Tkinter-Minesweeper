######################################################
#                    Import library                  #
######################################################
import os
from random import choices, randint
from tkinter import *
from tkinter import messagebox
######################################################
#                       Variable                     #
######################################################
DIMENSION = 10
TOTAL_BOMB = 15
######################################################
#                       Function                     #
######################################################
class Page:
    """
    Class to control all GUI window
    """
    def __init__(self):
        self._mainpage()

    def _mainpage(self):
        # Create root window
        self.root = Tk()
        # Setting title, icon, and size
        self.root.title("Minesweeper")
        self.root.iconbitmap("icon.ico")
        self.root.geometry("-150+50")
        # self.root.geometry("500x400-10+10")
        self.root.resizable(False, False)
        # Create and configure menu bar
        toolbar = Menu(self.root)
        self.root.config(menu = toolbar)
        # Adding main menu bar
        # toolbar.add_command(label = "Config", command = self._config)
        # toolbar.add_command(label = "Statistic", command = self._statistic)
        # Create header Frame
        self.header = Frame(self.root)
        self.header.pack(fill=BOTH, padx=20, pady=5)
        # Create body Frame
        self.body = Frame(self.root, bg="#666", name="body")
        self.body.pack(padx=15, pady=15)

    def _subpage(self):
        # Create branch window
        self._branch = Tk()
        # Setting icon, and size
        self._branch.iconbitmap("icon.ico")
        self._branch.geometry("250x300-400+75")
        # Create subpage footer section
        self.footer = Frame(self._branch)
        self.footer.pack(side=BOTTOM, anchor=S, fill=BOTH, padx=5, pady=5, ipady=5)

    def _config(self):
        # Action when click confirm button
        def confirm_action():
            global DIMENSION, TOTAL_BOMB
            DIMENSION = int(dimension_setting.get_value())
            if do_random:
                TOTAL_BOMB = randint(DIMENSION**2//10, DIMENSION**2-1)
            else:
                TOTAL_BOMB = int(total_bomb_setting.get_value())
            action.onReset()
            self._branch.destroy()
        # Check whether the subpage is already open
        try:
            for widget in self._branch.winfo_children():
                widget.destroy()
        except:
            self._subpage()
        # Set the subpage title
        self._branch.title("Configure")
        # Create mode variable
        do_random = BooleanVar(self._branch)
        mode = IntVar(self._branch, 0)
        # Create confirm and cancel button in the subpage footer
        cancel = Button(self.footer, text="Cancel", font="terminal 10", command=self._branch.destroy)
        cancel.pack(side=RIGHT, ipadx=3, ipady=5, padx=3)
        confirm = Button(self.footer, text="Confirm", font="terminal 10", command=confirm_action)
        confirm.pack(side=RIGHT, ipadx=3, ipady=5, padx=3)
        # Dimension setting section
        dimension_section = LabelFrame(self._branch, text="Board Dimension", font="terminal 10 bold")
        dimension_section.pack(fill=X, padx=5, pady=5)
        dimension_setting = Slider(dimension_section, from_=9, to=15, default=DIMENSION)
        dimension_setting.pack(pady=5)
        # Total bomb setting section
        total_bomb_section = LabelFrame(self._branch, text="Total Bomb", font="terminal 10 bold")
        total_bomb_section.pack(fill=X, padx=5, pady=5)
        rng_btn = Checkbutton(total_bomb_section, text="Random", font="terminal 9", variable=do_random, offvalue=False, onvalue=True)
        rng_btn.pack()
        total_bomb_setting = Slider(total_bomb_section, from_=DIMENSION**2//10, to=DIMENSION**2-1, default=TOTAL_BOMB)
        total_bomb_setting.pack(pady=5)
        rng_btn.config(command=total_bomb_setting.toggle)
        # Mode setting section
        mode_section = LabelFrame(self._branch, text="Mode", font="terminal 10 bold")
        mode_section.pack(fill=X, padx=5, pady=5)
        selection = Frame(mode_section)
        selection.pack()
        casual = Radiobutton(selection, text="Casual", font="terminal 9", variable=mode, value=0)
        casual.pack(side=LEFT)
        challenge = Radiobutton(selection, text="Challenge", font="terminal 9", variable=mode, value=1)
        challenge.pack(side=RIGHT)
        mode_setting = Slider(mode_section, from_=300, to=600, default=300)
        mode_setting.pack()

    def _statistic(self):
        # Check whether the subpage is already open
        try:
            for widget in self._branch.winfo_children():
                widget.destroy()
        except:
            self._subpage()
        # Set the subpage title
        self._branch.title("Statistic")
        self.footer.config(bg="#000")

class Game:
    """
    Class for control Game board widget
    """
    def __init__(self):
        # Create bomb and flag picture
        self.BOMB = PhotoImage(file="bomb.png")
        self.FLAG = PhotoImage(file="flag.png")
        # Initiate flag Counter
        self.flag_counter = Counter(page.header, self.FLAG)
        self.flag_counter.pack(side=LEFT, padx=5)
        # Initiate bomb Counter
        self.bomb_counter = Counter(page.header, self.BOMB)
        self.bomb_counter.pack(side=RIGHT)
        # Initiate Timer
        self.clock = Timer(page.header)
        # Setup the game board
        self._setup(DIMENSION, TOTAL_BOMB)

    def _setup(self, d: int=10, total: int=25):
        # Set default parameter
        self.dimension = d
        self.total = total
        self.map = {
            "current": [ [1]*self.dimension for i in range(self.dimension) ],
            "answer": [ [0]*self.dimension for i in range(self.dimension) ],
            "mask": [ [0]*self.dimension for i in range(self.dimension) ]
        }
        # Set bomb counter and flag counter
        self.bomb_counter.set(self.total)
        self.flag_counter.set(self.total)
        # Create and Distribute Bomb
        _map = self.map["answer"] = self._distributeBomb(self.map["answer"])
        # Add mask layer data from answer data 
        mask = self.map["mask"]
        for i in range(self.dimension**2):
            x = i % self.dimension
            y = i // self.dimension
            if _map[y][x] == 1:
                mask[y][x] = "*"

        # Add number indicate every bomb in proximity
        for i in range(self.dimension**2):
            x = i % self.dimension
            y = i // self.dimension
            # Check whether that coordinate has a bomb
            if mask[y][x] != "*":
                continue
            # If it is a bomb
            for j in range(9):
                a = x + (j % 3) - 1
                b = y + (j // 3) - 1
                # Check whether that coordinate has a bomb
                if 0 <= b < self.dimension and 0 <= a < self.dimension and mask[b][a] != "*":
                    # Add add number indicate surrounding bomb
                    mask[b][a] += 1

        self._printBoard(mask)

        # Create button in the body Frame
        for i in range(self.dimension**2):
            x = i % self.dimension
            y = i // self.dimension
            Button(page.body, name=f"{y}{x}", width=2).grid(column=x, row=y, ipadx=1)
        
        # Start the timer
        self.clock.start()

    def _distributeBomb(self, _map:list):
        # Set default bomb(1) and empty(0) probability
        prob_1 = self.total / self.dimension
        prob_0 = prob_1 * 2
        # Distribute
        while self.total > 0:
            for i in range(self.dimension**2):
                # Calculate x and y coordinates
                x = i % self.dimension
                y = i // self.dimension
                # Check whether there already is bomb in that position
                if _map[y][x] == 1:
                    continue
                # Get random for bomb or blank
                status = choices([1,0], weights=[prob_1, prob_0])[0]
                # Add to current row
                _map[y][x] = status
                # Adjust bomb and blank probabilities base on status
                if status == 1:
                    self.total -= 1
                    prob_0 += 25
                elif status == 0:
                    prob_1 += 1
                # Set bomb probability to 0 if total amount of bomb is 0
                prob_1 = 0 if self.total == 0 else prob_1
        return _map

    def _printBoard(self, _map:list):
        for i in range(self.dimension**2):
            x = i % self.dimension
            y = i // self.dimension
            print(_map[y][x], end=" ")
            if (i+1) % DIMENSION == 0: print()

class Activity:
    """
    Class for control clicking event
    """
    def __init__(self):
        # Create bomb and flag picture
        self.BOMB = PhotoImage(file="bomb.png")
        self.FLAG = PhotoImage(file="flag.png")
        # Bind left mouse button to coord function
        page.root.bind("<Button-1>", self.onClick)
        # Bind right mouse button to flag function
        page.root.bind("<Button-3>", self.onFlag)
        # Bind Enter button to restart function
        page.root.bind("<Return>", self.onReset)

    def onClick(self, event):
        """
        Action when clicked on the tile
        """
        d = board.dimension
        current, answer, mask = board.map["current"], board.map["answer"], board.map["mask"]
        # Get widget and x, y grid coordinate
        if self._get_coord(event) == None:
            return
        widget, x, y = self._get_coord(event)
        print(widget, x, y)
        # Remove clicked button from that grid coordinate
        if widget["image"] != "":
            return
        widget.grid_remove()
        if mask[y][x] == "*":
            # Get all bomb coordinate
            all_bomb_coord = [(i%d, i//d) for i in range(d**2) if mask[i//d][i%d]=="*"]
            # Display all the bomb
            for coord in all_bomb_coord:
                # Get coordinate
                x, y = coord
                # Get new widget
                new_id = f".body.{y}{x}"
                new_widget = page.root.nametowidget(new_id)
                # Remove Button widget
                new_widget.grid_remove()
                # Create Label and put it to the grid coordinate
                Label(page.body, image=self.BOMB).grid(column=x, row=y, padx=1, pady=1)
            # Stop the timer
            board.clock.stop()
            # Unbind clicked and flagged function
            page.root.unbind("<Button-1>")
            page.root.unbind("<Button-3>")
            # Show game over messagebox
            # messagebox.showerror(title="Game Over", message="Game Over")
        elif mask[y][x] == 0:
            for x, y in self._all_safe_position(mask, x, y):
                new_id = f".body.{y}{x}"
                new_widget = page.root.nametowidget(new_id)
                # Check if already flagged, if not remove
                if new_widget["image"] == "":
                    new_widget.grid_remove()
                # Update scoreboard
                current[y][x] = 0
                # Create Label and put it to the grid coordinate
                Label(page.body, text=mask[y][x], width=2, font="terminal 16", borderwidth=1).grid(
                    column=x, row=y, ipady=1, padx=1, pady=1)
        else:
            current[y][x] = 0
            # Create Label and put it to the grid coordinate
            Label(page.body, text=mask[y][x], width=2, font="terminal 16", borderwidth=1).grid(
                column=x, row=y, ipady=1, padx=1, pady=1)
        # Check if all non-tile have been clicked
        if current == answer:
            # Stop the timer
            board.clock.stop()
            # Unbind clicked and flagged function
            page.root.unbind("<Button-1>")
            page.root.unbind("<Button-3>")
            # Show game over messagebox
            messagebox.showinfo(title="Congratulations", message="Congratulations, You WIN.")

    def onFlag(self, event):
        """
        Action when flag the tile
        """
        # Get widget and x, y grid coordinate
        if self._get_coord(event) == None:
            return
        widget, x, y = self._get_coord(event)
        # Check if widget already flagged, and flag or remove flag
        if widget["image"] != "":
            board.flag_counter.increse()
            widget.config(image="", width=2)
        elif board.flag_counter.total > 0:
            board.flag_counter.decrese()
            widget.config(image=board.FLAG, width=18)

    def onReset(self, event=None):
        # Clear the board
        for widget in page.body.winfo_children():
            widget.destroy()
        # Reset the timer and board
        board.clock.reset()
        board._setup(DIMENSION, TOTAL_BOMB)
        # Bind left mouse button to coord function
        page.root.bind("<Button-1>", self.onClick)
        # Bind right mouse button to flag function
        page.root.bind("<Button-3>", self.onFlag)

    def _get_coord(self, event: Event):
        # Get x and y location
        x = event.x_root - page.body.winfo_rootx()
        y = event.y_root - page.body.winfo_rooty()
        # Get widget from x and y location
        for child in page.body.children.values():
            x1 = child.winfo_rootx()-page.body.winfo_rootx()
            y1 = child.winfo_rooty()-page.body.winfo_rooty()
            x2 = x1 + child.winfo_width()
            y2 = y1 + child.winfo_height()
            if x1 <= x <= x2 and y1 <= y <= y2:
                widget = child
                break
        else:
            return
        # Get grid coordinate from x and y location
        x, y = page.body.grid_location(x, y)
        # Return output value
        return widget, x, y
    
    def _all_safe_position(self, ref, x0, y0):
        # Create initial analyze list and checked list
        all_0, surround = [(x0, y0)], []
        checked = all_0.copy()
        # Analyze surrounding coordinate to get all connected empty tile
        while len(all_0) > 0:
            # Get first coordinate from analyze list
            x0, y0 = all_0[0]
            # Check surrounding coordinate
            for i in range(9):
                x = x0 + (i % 3) - 1
                y = y0 + (i // 3) - 1
                # Add to analyze list if it is empty and not already analyze
                if 0 <= x < DIMENSION and 0 <= y < DIMENSION and (x, y) not in checked and ref[y][x] == 0:
                    all_0.append((x, y))
            # Remove first coordinate from analyze list
            all_0.remove((x0, y0))
            # Add new coordinate to checked list
            checked.extend([i for i in all_0 if i not in checked])
        # Get empty tile surrounding coordinate
        for x0, y0 in checked:
            # Check surrounding coordinate
            for i in range(9):
                x = x0 + (i % 3) - 1
                y = y0 + (i // 3) - 1
                # Add to analyze list if it is empty and not already analyze
                if 0 <= x < DIMENSION and 0 <= y < DIMENSION and (x, y) not in checked and (x, y) not in surround:
                    surround.append((x, y))
        # Add surrounding coordinate to checked list
        checked.extend(surround)
        return checked

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
        page.root.after(1000, self.clock)

    # Function to start timer
    def start(self):
        self.state = True

    # Function to stop timer
    def stop(self):
        self.state = False

    # Function to reset timer
    def reset(self):
        self.time = 0

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

######################################################
#                         GUI                        #
######################################################
def main():
    global page, board, action
    # Set file directory to asset folder
    os.chdir(os.path.abspath(os.getcwd()) + "/asset")
    # Initialize main game page
    page = Page()
    # Initialize game board
    board = Game()
    # Initialize game event action
    action = Activity()
    # Initiate GUI window
    mainloop()

######################################################
#                        Start                       #
######################################################
main()