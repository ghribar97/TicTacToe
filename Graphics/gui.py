import Common.variables as variables
import Common.functions as functions
from Graphics.drawer import ShapeDrawer
#from menu import Menu
import tkinter


class Board(tkinter.Tk):
    """
    -------------------------------
    | |--------------| |---------| |
    | |              | |         | |
    | |   Playing    | |  Right  | |
    | |    Field     | |  Frame  | |
    | |              | |         | |
    | |--------------| |---------| |
    | |--------------------------| |
    | |        Bottom Frame      | |
    | |--------------------------| |
    --------------------------------
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._setup_board_settings()
        self.playing_field = PlayingField(self)
        self.right_frame = RightFrame(self)
        self.bottom_frame = BottomFrame(self)
        self.protocol("WM_DELETE_WINDOW", self._on_destroy)

        ShapeDrawer.draw_info_cross(self.right_frame.info_canvas, self, variables.CELL_PADDING)

    def _on_destroy(self):
        self.destroy()
        exit(0)

    def update_info_canvas(self, shape):
        if shape == variables.Iam.Circle.value:
            ShapeDrawer.draw_info_circle(self.right_frame.info_canvas, self, variables.CELL_PADDING)
        else:
            ShapeDrawer.draw_info_cross(self.right_frame.info_canvas, self, variables.CELL_PADDING)

    def _setup_board_settings(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position = Board.calculate_center_of_the_screen(screen_width, screen_height)
        self.geometry("+{}+{}".format(position[0], position[1]))
        self.geometry(str(variables.BOARD_WIDTH) + "x" + str(variables.BOARD_HEIGHT))  # dimensions
        self.resizable(0, 0)  # Don't allow resizing in the x or y direction
        self.title(variables.GAME_TITLE)

    def get_field_size(self):
        return int(self.right_frame.field_size.get())

    def set_field_size(self, val):
        if functions.is_number(val):
            self.right_frame.field_size.set(str(val))
            return val

    @staticmethod
    def calculate_center_of_the_screen(width, height):
        if functions.is_number(width) and functions.is_number(height):
            position_right = int(width / 2 - variables.BOARD_WIDTH / 2)
            position_down = int(height / 2 - variables.BOARD_HEIGHT / 2 - 50)
            return [position_right, position_down]
        return False


class Frame(tkinter.Frame):
    def __init__(self, master, x=0, y=0, width=100, height=100):
        if functions.are_numbers([x, y, width, height]):
            super().__init__(master=master, width=width, height=height)
            self.place(x=x, y=y)

    def _add_editbox(self, text, width=5):
        if functions.is_number(width) and functions.is_string(text.get()):
            return tkinter.Entry(self, text=text, justify="center", width=width)

    def _add_label(self, text, color="black", font=0):
        if functions.is_number(font) and functions.is_string(text) and functions.is_string(color):
            return tkinter.Label(self, text=text, font=(variables.TEXT_FONT, variables.LABEL_TEXT_SIZE + font), fg=color)

    def _add_button(self, text, funct):
        if functions.is_string(text):
            return tkinter.Button(self, text=text, padx=20, bg="white", bd=1, command=funct)

    def _create_info_canvas(self, parent):
        tkinter.Tk.update(parent)
        width = height = self.winfo_reqheight()
        return tkinter.Canvas(master=self, width=width, height=height)


class BottomFrame(Frame):
    def __init__(self, parent):
        self.parent = parent
        x_left = variables.EDGE
        y_top = variables.BOARD_HEIGHT * variables.FIELD_Y_RATIO + variables.EDGE
        width = variables.BOARD_WIDTH - 2 * variables.EDGE
        height = variables.BOARD_HEIGHT - y_top - variables.EDGE

        super().__init__(parent, x_left, y_top, width, height)

        self.elements = self._add_elements()

    def set_player_names(self, player_one, player_two):
        self.elements[2].config(text="- {}  ".format(player_one))
        self.elements[4].config(text="- {}".format(player_two))

    def go_back(self):
        self.parent.destroy()
        #Menu()

    def _add_elements(self):
        temp = variables.SHAPE_LINE_WIDTH
        variables.SHAPE_LINE_WIDTH = 2
        but = self._add_button("BACK", self.go_back)
        but.grid(column=0, row=2)
        lab1 = self._add_label("X ", color=variables.CROSS_COLOR)
        lab1.grid(column=1, row=0)
        lab2 = self._add_label("- {}  ".format("Player One"), font=-1)
        lab2.grid(column=2, row=0)
        lab3 = self._add_label("O ", color=variables.CIRCLE_COLOR)
        lab3.grid(column=3, row=0)
        lab4 = self._add_label("- {}".format("Player Two"), font=-1)
        lab4.grid(column=4, row=0)
        lab5 = self._add_label("")
        lab5.grid(row=1)  # so that the button can be in row 3
        variables.SHAPE_LINE_WIDTH = temp
        return [but, lab1, lab2, lab3, lab4, lab5]


class RightFrame(Frame):
    def __init__(self, parent):
        self.parent = parent
        x_left = variables.BOARD_WIDTH * variables.FIELD_X_RATIO + variables.EDGE
        y_top = variables.EDGE
        width = variables.BOARD_WIDTH - (2 * variables.EDGE) - (variables.BOARD_WIDTH * variables.FIELD_X_RATIO)
        height = (variables.BOARD_HEIGHT * variables.FIELD_Y_RATIO) - y_top

        super().__init__(self.parent, x_left, y_top, width, height)
        self.field_size = tkinter.StringVar(value=str(variables.DEFAULT_FIELD_SIZE))
        self.info_canvas = self._initialize_info_canvas()
        self._add_elements()

    def _initialize_info_canvas(self):
        width = variables.BOARD_WIDTH - variables.PLAYING_FIELD_WIDTH - 3 * variables.EDGE
        canvas = self._create_info_canvas(self.parent)
        canvas.config(width=width, height=width)
        canvas.grid(row=5, columnspan=2)
        return canvas

    def get_field_size_input(self):
        return self.field_size.get()

    def _add_elements(self):
        self._add_title()
        self._add_label(variables.FIELD_SIZE_TEXT, font=-1).grid(pady=20, row=2, column=0, columnspan=1)
        self._add_editbox(self.field_size).grid(row=2, column=1)
        self._add_button("RESET", self.parent.parent.reset).grid(row=3, pady=15, columnspan=2)
        self._add_label("Next Player's turn: ", font=-5).grid(row=4, pady=5, columnspan=2)

    def _add_title(self):
        self._add_label("Game of", color="purple", font=5).grid(row=0, columnspan=2)
        self._add_label(variables.GAME_TITLE, color="green", font=10).grid(row=1, columnspan=2)


class MainFrame(Frame):
    def __init__(self, parent):
        x_left = variables.EDGE
        y_top = variables.EDGE
        width = variables.PLAYING_FIELD_WIDTH
        height = variables.PLAYING_FIELD_HEIGHT
        if height != width:  # not a square
            raise ValueError("Height and Width of the playing field are not the same!")
        super().__init__(parent, x_left, y_top, width, height)


class PlayingField(tkinter.Canvas):
    def __init__(self, parent):
        self.parent = parent
        self.height = variables.PLAYING_FIELD_HEIGHT
        self.width = variables.PLAYING_FIELD_HEIGHT
        super().__init__(master=MainFrame(parent), height=self.height, width=self.width, bg=variables.FRAMES_BACKGROUND)

        self._draw_grid(variables.DEFAULT_FIELD_SIZE)
        self.pack(fill=tkinter.BOTH, expand=1)

    def restart(self):
        try:
            num = int(self.parent.right_frame.field_size.get())
            if functions.is_number(num) and 3 <= num <= 5:
                self._draw_grid(num)
                return num
        except ValueError:
            self.parent.parent.handle_wrong_input()
            self.parent.right_frame.field_size.set(variables.DEFAULT_FIELD_SIZE)
            return self.restart()

    def _draw_grid(self, num):
        self.delete("all")  # clear canvas
        if functions.is_number(num):
            #  we already know that height and width of the field is the same
            self._draw_outer_lines()
            for x in range(num):
                padding = x * (self.height / num)
                self.create_line(padding, 0, padding, self.height, fill=variables.BACKGROUND_COLOR)  # vertical line
                self.create_line(0, padding, self.width, padding, fill=variables.BACKGROUND_COLOR)  # horizontal line

    def _draw_outer_lines(self):
        self.create_rectangle(2, 2, self.width, self.height, outline=variables.BACKGROUND_COLOR)
