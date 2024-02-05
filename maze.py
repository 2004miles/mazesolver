from cell import Cell
import time
import random


class Maze():

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y,
                 win=None, seed=None):

        self.root = self
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()
        self.seed = seed if seed is not None else random.randint(0, 10000)  # Generate a seed if not provided
        random.seed(self.seed)  # Initialize the RNG with the seed 
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)
        self._animate()

    def _get_adjacent_cells(self, i, j):
        adjacent_indices = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self._num_cols and 0 <= nj < self._num_rows:
                adjacent_indices.append((ni, nj))
        return adjacent_indices

    def _solve_astar(self, i, j):
        # Each cell represents a node

        self._cells[i][j].visited = True
        if i == (self._num_cols -1) and j == (self._num_rows - 1):
            return True
        start = self._cells[0][0]
        end = self._cells[self._num_cols-1][self._num_rows-1]
        start.g = start.f = start.h = 0
        end.g = end.f = end.h = 0

        open_list = [start]
        closed_list = []

        while open_list:

            current_cell = min(open_list, key=lambda cell: cell.f)
            open_list.remove(current_cell)
            # Update and visualize estimated path at each step

            if current_cell == end:
                # Found the goal, reconstruct and visualize the final path
                return self.reconstruct_and_visualize_path(current_cell, None)
            closed_list.append(current_cell)
            successors = []
            for ni, nj in self._get_adjacent_cells(current_cell._location[0], current_cell._location[1]):
                if not self._cells[ni][nj].visited or self._cells[ni][nj] in closed_list:

                    if ni == current_cell._location[0] + 1 and not self._cells[current_cell._location[0]][current_cell._location[1]].has_right_wall and not self._cells[current_cell._location[0]+1][current_cell._location[1]].has_left_wall:
                        successors.append(self._cells[ni][nj])
                    if ni == current_cell._location[0] - 1 and not self._cells[current_cell._location[0]][current_cell._location[1]].has_left_wall and not self._cells[current_cell._location[0]-1][current_cell._location[1]].has_right_wall:
                        successors.append(self._cells[ni][nj])
                    if nj == current_cell._location[1] + 1 and not self._cells[current_cell._location[0]][current_cell._location[1]].has_bottom_wall and not self._cells[current_cell._location[0]][current_cell._location[1]+1].has_top_wall:
                        successors.append(self._cells[ni][nj])
                    if nj == current_cell._location[1] - 1 and not self._cells[current_cell._location[0]][current_cell._location[1]].has_top_wall and not self._cells[current_cell._location[0]][current_cell._location[1]-1].has_bottom_wall:
                        successors.append(self._cells[ni][nj])

            # Loop through successors
            for successor in successors:

                if successor.visited:
                    continue

                # Create the f, g, and h values
                successor.g = current_cell.g + 1
                successor.h = abs(successor._position[0] - end._position[0]) + abs(successor._position[1] - end._position[1])
                successor.f = successor.g + successor.h
                successor.parent = current_cell
                successor.visited = True

                # Add the child to the open list
                if self.add_to_open(open_list, successor):
                    open_list.append(successor)
                    self._animate()
                    successor.draw_move(successor.parent, 'search')
           

    def add_to_open(self, open_list, successor):
        for node in open_list:
            if successor == node and successor.f >= node.f:
                return False
        return True

    def reconstruct_and_visualize_path(self, end_cell, style):
        path = []
        current = end_cell
        while current is not None:
            path.insert(0, current)
            current = current.parent

        # Visualize the path
        for i in range(len(path) - 1):
            self._animate()
            path[i].draw_move(path[i+1], style)

        return path
 
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == (self._num_cols -1) and j == (self._num_rows - 1):
            return True

        for ni, nj in self._get_adjacent_cells(i, j):
            if self._cells[ni][nj] is not None and not self._cells[ni][nj].visited:

                if ni == i + 1 and not self._cells[i][j].has_right_wall and not self._cells[i+1][j].has_left_wall:
                    self._animate()
                    self._cells[i][j].draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    self._animate()
                    self._cells[i][j].draw_move(self._cells[ni][nj], 'undo')

                if ni == i - 1 and not self._cells[i][j].has_left_wall and not self._cells[i-1][j].has_right_wall:
                    self._animate()
                    self._cells[i][j].draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    self._animate()
                    self._cells[i][j].draw_move(self._cells[ni][nj], 'undo')

                if nj == j + 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].has_top_wall:
                    self._animate()
                    self._cells[i][j].draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    self._animate()
                    self._cells[i][j].draw_move(self._cells[ni][nj], 'undo')

                if nj == j - 1 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].has_bottom_wall:
                    self._animate()
                    self._cells[i][j].draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    self._animate()
                    self._cells[i][j].draw_move(self._cells[ni][nj], 'undo')

        return False

    def solve(self):
        return self._solve_astar(0, 0)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            possible_directions = []
            for ni, nj in self._get_adjacent_cells(i, j):
                if not self._cells[ni][nj].visited:
                    possible_directions.append((ni, nj))

            if not possible_directions:
                self._draw_cell(i, j)
                break

            next_i, next_j = random.choice(possible_directions)

            # right
            if next_i == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_i == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_j == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_j == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._draw_cell(next_i, next_j)
            self._draw_cell(i, j)
            self._break_walls_r(next_i, next_j)
  
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
                self._create_cell_location(i, j)

    def _create_cell_location(self, i, j):
        # creates cell location
        self._cells[i][j]._x1 = self._x1 + i * self._cell_size_x
        self._cells[i][j]._y1 = self._y1 + j * self._cell_size_y
        self._cells[i][j]._x2 = self._cells[i][j]._x1 + self._cell_size_x
        self._cells[i][j]._y2 = self._cells[i][j]._y1 + self._cell_size_y

        x1 = (self._cells[i][j]._x1 + self._cells[i][j]._x2)/2
        y1 = (self._cells[i][j]._y1 + self._cells[i][j]._y2)/2
        
        self._cells[i][j]._position.append(x1)
        self._cells[i][j]._position.append(y1)
        self._cells[i][j]._location.append(i)
        self._cells[i][j]._location.append(j)


    def _draw_cell(self, i, j, color="black"):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2, color)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.02)
