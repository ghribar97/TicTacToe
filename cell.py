import Common.functions as functions
from Common.variables import CellStatus
from Graphics.gui import ShapeDrawer


class Cell:
    """
    x1,y1--------
         |      |
         |      |
         --------x2,y2
    """
    def __init__(self, x1, y1, x2, y2, cell_id, x, y):
        if functions.are_numbers([x1, x2, y1, y2, x, y]):
            self.x1 = x1
            self.x2 = x2
            self.y1 = y1
            self.y2 = y2
            self.cell_id = cell_id
            self.x = x
            self.y = y
            self.status = None

    def is_click_inside(self, x, y):
        if functions.are_numbers([x, y]):
            return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def change_cell_type(self, new_cell_type):
        self.status = new_cell_type
        return self.status


class CrossCell(Cell):
    def __init__(self, x1, y1, x2, y2, cell_id, x, y):
        super().__init__(x1, y1, x2, y2, cell_id, x, y)
        self.status = CellStatus.Cross

    def draw(self, parent):
        ShapeDrawer.draw_cross(parent, self.x1, self.y1, self.x2, self.y2)


class CircleCell(Cell):
    def __init__(self, x1, y1, x2, y2, cell_id, x, y):
        super().__init__(x1, y1, x2, y2, cell_id, x, y)
        self.status = CellStatus.Circle

    def draw(self, parent):
        ShapeDrawer.draw_circle(parent, self.x1, self.y1, self.x2, self.y2)


class EmptyCell(Cell):
    def __init__(self, x1, y1, x2, y2, cell_id, x, y):
        super().__init__(x1, y1, x2, y2, cell_id, x, y)
        self.status = CellStatus.Empty

