import Common.functions as functions
import Graphics.messenger as messenger
import random
import tkinter
import menu

MAX_VALUE = 100
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
GAME_TITLE = "GUESSING GAME"
TITLE_COLOR = "green"


class Gui(tkinter.Tk):
    """
    ----------------------------
    |       GUESSING GAME       |
    |                           |
    |     ENTER THE NUMBER:     |
    |           _____           |
    |          |_____|          |
    |         RESPONSE          |
    |           BACK            |
    -----------------------------
    """
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.entry_text = tkinter.StringVar()
        self._setup_window_settings()
        self.elements = self._add_elements()
        self.bind('<Return>', self.logic.process_enter)
        self.protocol("WM_DELETE_WINDOW", self._on_destroy)

    def _on_destroy(self):
        self.destroy()
        exit(0)

    def change_response_text(self, text):
        if functions.is_string(text):
            self.elements[3].config(text=text)
            return text
        raise ValueError(str(text) + " is not a string!")

    def _add_elements(self):
        frame = tkinter.Frame(master=self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        frame.place(x=0)
        title = tkinter.Label(frame, text=GAME_TITLE, fg=TITLE_COLOR, font=("Helvetica", 25))
        title.grid(row=0, columnspan=3, pady=10)
        info = tkinter.Label(frame, text="Enter the number between 0 and " + str(MAX_VALUE) + " here:", font=("Helvetica", 10))
        info.grid(row=1, padx=70)
        entry = tkinter.Entry(frame, text=self.entry_text, justify="center", width=15)
        entry.grid(row=2, pady=5)
        resp = tkinter.Label(frame, text="After insertion press enter", font=("Helvetica", 10), fg="red")
        resp.grid(row=3)
        tkinter.Label(frame).grid(row=4)
        button = tkinter.Button(frame, text="BACK", command=self._go_back, bg="white")
        button.grid(row=5)
        return [title, info, entry, resp, button]

    def get_text(self):
        return self.entry_text.get()

    def _setup_window_settings(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position = self._calculate_center_of_the_screen(screen_width, screen_height)
        self.geometry("+{}+{}".format(position[0], position[1]))
        self.geometry(str(self.width) + "x" + str(self.height))  # dimensions
        self.resizable(0, 0)  # Don't allow resizing in the x or y direction
        self.title(GAME_TITLE)

    def _calculate_center_of_the_screen(self, width, height):
        if functions.is_number(width) and functions.is_number(height):
            position_right = int(width / 2 - self.width / 2)
            position_down = int(height / 2 - self.height / 2 - 50)
            return [position_right, position_down]
        return False

    def _go_back(self):
        self.destroy()
        menu.Menu()


class GuessingGame:
    def __init__(self, player_name):
        self.player_name = player_name
        self.number = self._set_number()
        self.number_of_guesses = 0
        self.gui = Gui(self)

    def _set_number(self):
        self.number = random.randint(1, MAX_VALUE)
        self.number_of_guesses = 0
        return self.number

    def process_enter(self, event):
        text = self.gui.get_text()
        try:
            text = int(text)
        except ValueError:
            messenger.SendToUser.error("Input should be number between 0 and " + str(MAX_VALUE))
            return
        except TypeError:
            messenger.SendToUser.error("Input should be number between 0 and " + str(MAX_VALUE))
            return
        if text > self.number:
            self.gui.change_response_text("Your guess is to high.")
        elif text < self.number:
            self.gui.change_response_text("Your guess is to low.")
        else:
            self._process_the_end()
        self.number_of_guesses += 1
        self.gui.entry_text.set("")

    def _process_the_end(self):
        text = "You guessed the number in " + str(self.number_of_guesses) + " tries."
        again = messenger.SendToUser.ask_for_new_game(text)
        if again:
            self._set_number()
            self.gui.change_response_text("After insertion press enter")
        else:
            exit(0)


def play(name):
    if functions.is_string(name):
        GuessingGame(name).gui.mainloop()
    else:
        raise ValueError(str(name) + " is not a string!")
