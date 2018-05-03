import Graphics.gui as gui
import clickManager
import player
import playingField
import Graphics.messenger as messenger


class TicTacToe:
    @staticmethod
    def play_single_player(player_one_name):
        bot_name = "Bot Player"
        board = Board(player_one_name, bot_name)
        player1 = player.Player(player_one_name, "Cross", board, start=True)
        player2 = player.Bot(bot_name, "Circle", board, start=False)
        player1.set_opponent(player2)
        player2.set_opponent(player1)
        cm = clickManager.ClickManager(board, player1, player2)
        player2.add_click_manager(cm)

        board.gui.mainloop()

    @staticmethod
    def play_double_player(player_name):
        board = Board(player_name, "Waiting for opponent")
        play = player.MultiPlayer(player_name, board)
        board.add_multi_player(play)

        board.gui.mainloop()


class Board:
    def __init__(self, name1, name2):
        self.playing_field = playingField.PlayingField(self)
        self.gui = gui.Board(self)
        self.gui.bottom_frame.set_player_names(name1, name2)
        self.multi_player = None

    def add_multi_player(self, player):
        self.multi_player = player

    def reset(self, rematch=False):
        if self.multi_player is not None and not rematch:
            self.multi_player.client.send_change_field_request()
        else:
            num = self.gui.playing_field.restart()
            self.playing_field.initialize_field(num)

    def handle_the_end(self, text="It is draw!", send_to_server=False):
        if messenger.SendToUser.ask_for_new_game(text):
            self.reset(rematch=True)
            return False
        else:
            if send_to_server:
                return True
            exit(0)

    @staticmethod
    def handle_wrong_input():
        messenger.SendToUser.error("Wrong input! Number should be a number between 3 and 5")


if __name__ == "__main__":
    TicTacToe.play_single_player("lolek")
