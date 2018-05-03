import Common.functions as functions
import Common.variables as variables
from endValidator import EndValidator
from Graphics.drawer import ShapeDrawer
from Communication.client import Client
import random


class Player:
    def __init__(self, name, shape, board, start):
        if functions.is_string(name) and functions.is_string(shape):
            self.shape = variables.Iam[shape].value
            self.name = name
            self.board = board
            self.turn_to_play = start
            self.opponent = None

    def set_opponent(self, opponent):
        self.opponent = opponent

    def _change_turns(self):
        if self.opponent is None:
            raise ValueError("Opponent is not set!")
        self.turn_to_play = False
        self.opponent.turn_to_play = True
        self.board.gui.update_info_canvas(self.opponent.shape)

    def react(self):
        empty_cells = self.board.playing_field.get_empty_cells()
        if len(empty_cells) == 0:  # it is draw
            return self.board.handle_the_end()

    def play(self, cell):
        if self.turn_to_play:
            cell.draw(self.board.gui.playing_field)
            end = EndValidator.check_for_the_end(self.board.playing_field, cell)
            self._change_turns()
            if self.handle_possible_the_end(end):
                if not isinstance(self, Bot):  # bot must do the first move next game
                    self.opponent.react()
            else:
                self.opponent.react()

    def back_to_menu(self):
        self.board.gui.bottom_frame.go_back()

    def handle_possible_the_end(self, end, send_to_server=False):
        if end is not None:  # it is over
            ShapeDrawer.draw_winning_line(self.board.gui.playing_field, end)
            return self.board.handle_the_end(self.name + " won!", send_to_server)
        return False


class MultiPlayer(Player):
    def __init__(self, name, board, start=False):
        super().__init__(name, "Cross", board, start)
        self.client = Client(self)

    def play(self, cell):
        if self.turn_to_play:
            cell.draw(self.board.gui.playing_field)
            self.client.send_clicked_cell(cell.cell_id)
            end = EndValidator.check_for_the_end(self.board.playing_field, cell)
            self._change_turns()
            if self.handle_possible_the_end(end, send_to_server=True):
                self.client.send_leave_request()
                exit(0)

    def initialize(self, start, opponent):
        shape = "Circle"
        if start:  # player who will start will always be cross
            shape = "Cross"
        self.shape = variables.Iam[shape].value
        self.turn_to_play = start
        self.set_opponent(opponent)
        self.opponent.set_opponent(self)
        if shape == "Circle":
            self.board.gui.bottom_frame.set_player_names(self.opponent.name, self.name)
            self.opponent.shape = variables.Iam["Cross"].value
        elif shape == "Cross":
            self.board.gui.bottom_frame.set_player_names(self.name, self.opponent.name)
            self.opponent.shape = variables.Iam["Circle"].value
        if start:
            self.board.gui.update_info_canvas(shape)
            self.opponent.turn_to_play = False
        else:
            self.board.gui.update_info_canvas(self.opponent.shape)
            self.opponent.turn_to_play = True


class Bot(Player):
    def __init__(self, name, shape, board, start):
        self.click_manager = None
        super().__init__(name, shape, board, start)

    def add_click_manager(self, manager):
        self.click_manager = manager

    def _respond(self, cell):
        self.click_manager.click(cell.x1 + 5, cell.y1 + 5)  # + 5 is to avoid borders

    def react(self):
        if self.click_manager is not None and self.turn_to_play:
            empty_cells = self.board.playing_field.get_empty_cells()
            if len(empty_cells) == 0:  # it is draw
                return self.board.handle_the_end()
            cell = empty_cells[random.randint(0, len(empty_cells) - 1)]
            if not len(empty_cells) == self.board.playing_field.get_number_of_cells():
                self.board.gui.after(500, lambda: self._respond(cell))  # to create an illusion that the bot is thinking
            else:  # first cell will be drawn immediately
                self._respond(cell)
        else:
            raise ValueError("Click manager is not set!")


class MultiPlayerOpponent(Bot):
    def __init__(self, name, shape, board, start):
        self.click_manager = None
        super().__init__(name, shape, board, start)

    def play(self, cell):
        if self.turn_to_play:
            cell.draw(self.board.gui.playing_field)
            end = EndValidator.check_for_the_end(self.board.playing_field, cell)
            self._change_turns()
            self.handle_possible_the_end(end)

    def click(self, cell_id):
        if functions.is_number(cell_id) and self.click_manager is not None:
            cell = self.board.playing_field.get_cell_by_id(cell_id)
            self.click_manager.click(cell.x1 + 5, cell.y1 + 5)

