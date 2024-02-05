from graphics import Line, Point


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        #win location
        self._position = []
        #2d array location
        self._location = []
        self._win = win
        self.visited = False

        # A*
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def draw(self, x1, y1, x2, y2, color="black"):
        if self._win is None:
            return

        # Define the points for the corners of the cell
        top_left = Point(x1, y1)
        bottom_left = Point(x1, y2)
        top_right = Point(x2, y1)
        bottom_right = Point(x2, y2)

        # A list of tuples containing the condition for drawing a wall,
        # the start and end points of that wall, and the default color
        walls = [
            (self.has_left_wall, top_left, bottom_left, color),
            (self.has_top_wall, top_left, top_right, color),
            (self.has_right_wall, top_right, bottom_right, color),
            (self.has_bottom_wall, bottom_left, bottom_right, color)
        ]

        # Iterate through each wall and draw it if the condition is True
        for has_wall, start, end, color in walls:
            line_color = "white" if not has_wall else color
            line = Line(start, end)
            self._win.draw_line(line, line_color)

    def draw_move(self, to_cell, style=None):
        if self._win is None:
            return
        x_mid = (self._x1 + self._x2) / 2
        y_mid = (self._y1 + self._y2) / 2

        to_x_mid = (to_cell._x1 + to_cell._x2) / 2
        to_y_mid = (to_cell._y1 + to_cell._y2) / 2

        fill_color = "red"
        if style == 'undo':
            fill_color = "gray"
        if style == 'search':
            fill_color = 'blue' 

        # moving left
        if self._x1 > to_cell._x1:
            line = Line(Point(self._x1, y_mid), Point(x_mid, y_mid))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_y_mid), Point(to_cell._x2, to_y_mid))
            self._win.draw_line(line, fill_color)

        # moving right
        elif self._x1 < to_cell._x1:
            line = Line(Point(x_mid, y_mid), Point(self._x2, y_mid))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_cell._x1, to_y_mid), Point(to_x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)

        # moving up
        elif self._y1 > to_cell._y1:
            line = Line(Point(x_mid, y_mid), Point(x_mid, self._y1))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_cell._y2), Point(to_x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)

        # moving down
        elif self._y1 < to_cell._y1:
            line = Line(Point(x_mid, y_mid), Point(x_mid, self._y2))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_y_mid), Point(to_x_mid, to_cell._y1))
            self._win.draw_line(line, fill_color)
