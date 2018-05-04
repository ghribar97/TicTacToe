import math
import Common.functions as functions
from Common.variables import CellStatus


class EndValidator:
    @staticmethod
    def _check_decreasing_diagonal(playing_field, columns):
        if functions.is_number(columns):
            cells = []
            first_cell = playing_field.get_cell_by_id(0)
            for x in range(int(columns)):
                cell = playing_field.get_cell_by_x_y(x, x)
                if cell.status != first_cell.status or cell.status == CellStatus.Empty:
                    return []
                cells.append(cell)
            return cells

    @staticmethod
    def _check_increasing_diagonal(playing_field, columns):
        if functions.is_number(columns):
            cells = []
            first_cell = playing_field.get_cell_by_id(columns * 2)
            for x in range(int(columns)):
                id = (x + 1) * (columns - 1)
                cell = playing_field.get_cell_by_id(id)
                if cell.status != first_cell.status or cell.status == CellStatus.Empty:
                    return []
                cells.append(cell)
            return cells

    @staticmethod
    def _check_line(playing_field, columns, line):
        if functions.are_numbers([columns, line]):
            cells = []
            first_cell = playing_field.get_cell_by_x_y(0, line)
            for x in range(int(columns)):
                cell = playing_field.get_cell_by_x_y(x, line)
                if cell.status != first_cell.status or cell.status == CellStatus.Empty:
                    return []
                cells.append(cell)
            return cells

    @staticmethod
    def _check_column(playing_field, columns, column):
        if functions.are_numbers([columns, column]):
            cells = []
            first_cell = playing_field.get_cell_by_x_y(column, 0)
            for y in range(int(columns)):
                cell = playing_field.get_cell_by_x_y(column, y)
                if cell.status != first_cell.status or cell.status == CellStatus.Empty:
                    return []
                cells.append(cell)
            return cells

    @staticmethod
    def _win(cells, columns):
        if isinstance(cells, list) and functions.is_number(columns):
            if len(cells) > 0:
                first_one = cells[0]
                for one_cell in cells:
                    if one_cell.status != first_one.status or one_cell.status == CellStatus.Empty:
                        return False
            return len(cells) == columns
        raise ValueError(str(cells) + " is not a list!")

    @staticmethod
    def check_for_the_end(playing_field, cell):
        number_of_cells = playing_field.get_number_of_cells()
        columns = math.sqrt(number_of_cells)
        dec_d = EndValidator._check_decreasing_diagonal(playing_field, columns)
        inc_d = EndValidator._check_increasing_diagonal(playing_field, columns)
        line = EndValidator._check_line(playing_field, columns, cell.y)
        column = EndValidator._check_column(playing_field, columns, cell.x)
        if EndValidator._win(dec_d, columns):
            return dec_d
        elif EndValidator._win(inc_d, columns):
            return inc_d
        elif EndValidator._win(line, columns):
            return line
        elif EndValidator._win(column, columns):
            return column
        else:
            return None
