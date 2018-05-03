import enum

GAME_TITLE = "Tic-Tac-Toe"
BOARD_WIDTH = 600
BOARD_HEIGHT = 500
FIELD_Y_RATIO = 4 / 5  # How much of the board is the field (Y axis ratio)
FIELD_X_RATIO = 2 / 3  # How much of the board is the field (x axis ratio)
EDGE = 10  # Edge from the corner of the window
PLAYING_FIELD_HEIGHT = BOARD_HEIGHT * FIELD_Y_RATIO - EDGE
PLAYING_FIELD_WIDTH = BOARD_WIDTH * FIELD_X_RATIO - EDGE
CELL_PADDING = 20
SHAPE_LINE_WIDTH = 10

LABEL_TEXT_SIZE = 15
FIELD_SIZE_TEXT = "Field size (3-5): "
TEXT_FONT = "Helvetica"

FRAMES_BACKGROUND = "white"
BACKGROUND_COLOR = "grey"
CIRCLE_COLOR = "blue"
CROSS_COLOR = "red"
WINNING_LINE_COLOR = "OliveDrab1"

DEFAULT_FIELD_SIZE = 3  # number of columns/rows

SERVER_NAME = "localhost"
HEADER_DATA = "!HH"
PORT_NUMBER = 10000
HEADER_LENGTH = 4  # number of bytes


class CellStatus(enum.Enum):
    Empty = "Empty"
    Circle = "Circle"
    Cross = "Cross"


class Iam(enum.Enum):
    Circle = "Circle"
    Cross = "Cross"


class Headers(enum.Enum):
    Request_click = 0
    Request_join = 1
    Request_leave = 2
    Request_change_size = 3
    Request_change_shapes = 4

    Response_change_shapes = 5
    Response_change_size = 6
    Response_leave = 7
    Response_join = 8
    Response_click = 9


class ResponseCode(enum.Enum):
    Ok = 0
    Not_Ok = 1
