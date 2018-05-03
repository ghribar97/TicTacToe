import Common.functions as functions
from Common.variables import CellStatus
from player import MultiPlayerOpponent


class ClickManager:
    def __init__(self, board, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.playing_field = board.playing_field  # playing field logic
        board.gui.playing_field.bind("<Button-1>", self._detect_click)  # right click

    def _detect_click(self, event):
        if functions.are_numbers([event.x, event.y]) and not isinstance(self._get_playing_player(), MultiPlayerOpponent):
            return self.process_click(event.x, event.y)

    def _get_playing_player(self):
        if self.player1.turn_to_play:
            return self.player1
        return self.player2

    def process_click(self, x, y):
        if functions.are_numbers([x, y]):
            clicked_cell = self.playing_field.get_clicked_cell(x, y)
            if clicked_cell.status == CellStatus.Empty:
                playing_player = self._get_playing_player()
                clicked_cell = self.playing_field.change_cell_type(clicked_cell.cell_id, playing_player.shape)
                playing_player.play(clicked_cell)
                return clicked_cell
            return None

    def click(self, x, y):
        return self.process_click(x, y)
