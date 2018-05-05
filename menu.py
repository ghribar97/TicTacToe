import enum
import abc
import tkinter
from tkinter import font
from tkinter import messagebox
import ticTacToe
import guessingGame

MENU_WIDTH = 500
MENU_HEIGHT = 330
FRAME_SEPARATOR = 130


class Menu(tkinter.Tk):
    """
    |---------------------|
    |      TOP_FRAME      |
    |---------------------|
    |      MID_FRAME      |
    |---------------------|
    |      BOT_FRAME      |
    |---------------------|
    """
    def __init__(self):
        super().__init__()
        self.title("First Step")
        self.player_name = tkinter.StringVar(value="Player One")

        self.top_frame = self._create_frame(0, 0)
        self.mid_frame = self._create_frame(0, FRAME_SEPARATOR)
        self.bot_frame = self._create_frame(0, FRAME_SEPARATOR*2)
        self.list_of_games = List(self.mid_frame, self)
        self.list_of_games.pack()

        self._configure_top_frame()
        self._configure_bot_frame()
        self._initialize_settings()

        self.mainloop()

    def _process_click(self):
        try:
            index = self.list_of_games.curselection()[0]
            game = self.list_of_games.get_game(index)
            game.start_game()
        except IndexError:
            messagebox.showinfo("Error", "You must first choose the game!")
            print("Choose the game first!")

    def _configure_top_frame(self):
        tkinter.Label(self.top_frame, text="CHOOSE GAME", font=("Helvetica", 35), fg="green").grid(row=0, padx=70)
        tkinter.Label(self.top_frame, text="Enter your name:", font=("Helvetica", 15)).grid(row=1)
        tkinter.Entry(self.top_frame, text=self.player_name, justify="center", width=50).grid(row=2)

    def _configure_bot_frame(self):
        button = tkinter.Button(self.bot_frame, text="PLAY", command=self._process_click, padx=20, height=2,
                                activebackground="green", bg="white")
        button.pack(padx=200)

    def _initialize_settings(self):
        self.geometry(str(MENU_WIDTH) + "x" + str(MENU_HEIGHT))  # dimensions
        self.resizable(0, 0)  # Don't allow resizing in the x or y direction
        position = self._calculate_center()  # "middle of the screen"
        self.geometry("+{}+{}".format(position[0], position[1]))

    def _calculate_center(self):
        position_right = int(self.winfo_screenwidth() / 2 - MENU_WIDTH / 2)
        position_down = int(self.winfo_screenheight() / 2 - MENU_HEIGHT / 2 - 50)
        return [position_right, position_down]

    def _create_frame(self, x, y):
        frame = tkinter.Frame(self, width=MENU_WIDTH, height=FRAME_SEPARATOR)
        frame.place(x=x, y=y)
        return frame

    def get_player_name(self):
        return self.player_name.get()


class List(tkinter.Listbox):

    def __init__(self, parent, tk):
        super().__init__(parent, width=MENU_WIDTH, height=3, font=tkinter.font.Font(size=16))
        self.items = self._create_items()
        self.parent = tk
        self._initialize()

    def destroy_window(self):
        self.parent.withdraw()
        self.parent.destroy()

    def _create_items(self):
        guess_game = GuessingGame(self)
        ttt_singl = TicTacToeSinglePlayer(self)
        ttt_mult = TicTacToeDoublePlayer(self)
        return {guess_game.index: guess_game, ttt_singl.index: ttt_singl, ttt_mult.index: ttt_mult}

    def _initialize(self):
        for game in self.items.values():
            self.insert(game.index, game.game_name)

    def get_game(self, index):
        if index in self.items:
            return self.items[index]
        raise Exception("Game name does not exist!")


class ListItem(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, parent, game_type, game_name):
        self.parent = parent
        self.game_type = game_type
        self.game_name = "{:^70}".format(game_name)  # entire field is approx 70 chars long, it can be in the center
        self.index = self.game_type.value

    def start_game(self):
        print(str(self.game_type)[7:] + " is starting")
        self.parent.destroy_window()


class GuessingGame(ListItem):
    def __init__(self, parent):
        super().__init__(parent, GameOf.Guessing_Game, "Guessing Game")

    def start_game(self):
        super().start_game()
        guessingGame.play(self.parent.parent.get_player_name())


class TicTacToeSinglePlayer(ListItem):
    def __init__(self, parent):
        super().__init__(parent, GameOf.Tic_Tac_Toe_Single, "Tic-Tac-Toe Single Player")

    def start_game(self):
        super().start_game()
        ticTacToe.TicTacToe.play_single_player(self.parent.parent.get_player_name())


class TicTacToeDoublePlayer(ListItem):
    def __init__(self, parent):
        super().__init__(parent, GameOf.Tic_Tac_Toe_Double, "Tic-Tac-Toe Double Player")

    def start_game(self):
        super().start_game()
        ticTacToe.TicTacToe.play_double_player(self.parent.parent.get_player_name())


class GameOf(enum.Enum):
    Guessing_Game = 0
    Tic_Tac_Toe_Single = 1
    Tic_Tac_Toe_Double = 2


if __name__ == "__main__":
    Menu()
