import Common.functions as functions
import Common.variables as variables
from Common.variables import CellStatus
import tkinter


class ShapeDrawer:
    @staticmethod
    def draw_cross(canvas, x1, y1, x2, y2):
        if functions.are_numbers([x1, y1, x2, y2]):
            x1 += variables.CELL_PADDING
            y1 += variables.CELL_PADDING
            x2 -= variables.CELL_PADDING
            y2 -= variables.CELL_PADDING
            canvas.create_line(x1, y1, x2, y2, fill=variables.CROSS_COLOR, width=variables.SHAPE_LINE_WIDTH)  # LT to RB
            canvas.create_line(x1, y2, x2, y1, fill=variables.CROSS_COLOR, width=variables.SHAPE_LINE_WIDTH)  # LB to RT
            return True

    @staticmethod
    def draw_circle(canvas, x1, y1, x2, y2):
        if functions.are_numbers([x1, y1, x2, y2]):
            x1 += variables.CELL_PADDING
            y1 += variables.CELL_PADDING
            x2 -= variables.CELL_PADDING
            y2 -= variables.CELL_PADDING
            canvas.create_oval(x1, y1, x2, y2, fill=variables.FRAMES_BACKGROUND,
                             outline=variables.CIRCLE_COLOR, width=variables.SHAPE_LINE_WIDTH)
            return True

    @staticmethod
    def draw_info_circle(canvas, parent, shrink=0):
        if functions.is_number(shrink):
            tkinter.Tk.update(parent)
            width = height = canvas.winfo_reqheight()
            canvas.delete(["all"])
            ShapeDrawer.draw_circle(canvas, shrink, shrink, width - shrink, height - shrink)
            return True

    @staticmethod
    def draw_info_cross(canvas, parent, shrink=0):
        if functions.is_number(shrink):
            tkinter.Tk.update(parent)
            width = height = canvas.winfo_reqheight()
            canvas.delete(["all"])
            ShapeDrawer.draw_cross(canvas, shrink, shrink, width - shrink, height - shrink)
            return True

    @staticmethod
    def _color_green(cell, canvas):
        canvas.create_rectangle(cell.x1, cell.y1, cell.x2, cell.y2, fill=variables.WINNING_LINE_COLOR)
        if cell.status == CellStatus.Circle:
            ShapeDrawer.draw_circle(canvas, cell.x1, cell.y1, cell.x2, cell.y2)
        else:
            ShapeDrawer.draw_cross(canvas, cell.x1, cell.y1, cell.x2, cell.y2)
        return True

    @staticmethod
    def draw_winning_line(canvas, cells):
        for cell in cells:
            ShapeDrawer._color_green(cell, canvas)
