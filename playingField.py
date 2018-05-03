import Common.variables as variables
import Common.functions as functions
import cell


class PlayingField:
    """
    This class is carrying all the data about the field.
    """
    def __init__(self, parent):
        self.parent = parent
        self.field_cells = {}
        self.initialize_field(variables.DEFAULT_FIELD_SIZE)

    def get_empty_cells(self):
        cells = []
        for cell in self.field_cells.values():
            if cell.status == variables.CellStatus.Empty:
                cells.append(cell)
        return cells

    def get_number_of_cells(self):
        return len(self.field_cells)

    def get_cell_by_id(self, id):
        if functions.is_number(id):
            return self.field_cells[id]
        return None

    def get_cell_by_x_y(self, x, y):
        for cell in self.field_cells.values():
            if cell.x == x and cell.y == y:
                return cell
        return None

    def get_clicked_cell(self, x, y):
        for one_cell in self.field_cells.values():
            if one_cell.is_click_inside(x, y):
                return one_cell
        return None

    @staticmethod
    def _correct_input(x):
        return x == variables.Iam.Cross.value or x == variables.Iam.Circle.value

    def change_cell_type(self, previous_id, new_type):
        if functions.is_number(previous_id) and PlayingField._correct_input(new_type):
            old_cell = self.field_cells[previous_id]
            x = old_cell.x
            y = old_cell.y
            # we are not interested if new_type is typeof EmptyCell
            new_cell = cell.CrossCell(old_cell.x1, old_cell.y1, old_cell.x2, old_cell.y2, previous_id, x, y)
            if new_type == variables.CellStatus.Circle.value:
                new_cell = cell.CircleCell(old_cell.x1, old_cell.y1, old_cell.x2, old_cell.y2, previous_id, x, y)
            self.field_cells[previous_id] = new_cell
            return new_cell
        return False

    def initialize_field(self, num):
        """
        Initialize/reset the playing field.
        :param num: number of columns/lines (default 3)
        :return:
        """
        if functions.is_number(num):
            self.field_cells = {}
            id_counter = 0
            padding = (variables.PLAYING_FIELD_WIDTH / num)
            for y in range(num):
                for x in range(num):
                    # height and width are the same
                    x1 = x * padding
                    y1 = y * padding
                    x2 = x1 + padding
                    y2 = y1 + padding
                    self.field_cells[id_counter] = cell.EmptyCell(x1, y1, x2, y2, id_counter, x, y)  # cells are empty
                    id_counter += 1
