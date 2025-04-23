import random  # importing necessary libraries

from collections import deque

from tkinter import *

from player import Player

BLACK = "#000000"

WHITE = "#FFFFFF"

GREEN = "#55FF55"

FONT_NAME = "Courier"

START_COLOR = '#FFD300'

END_COLOR = GREEN


# create an empty 2D array of cells with specified dimensions
def createEmptyMaze(rows, cols):
    global maze

    maze = []

    for r in range(rows):

        maze_row = []

        for c in range(cols):
            maze_row.append(Cell(r, c))

        maze.append(maze_row)

    return maze


class MazeGenerator(Canvas):  # creating the class maze generator
    north = 0
    south = 1
    east = 2
    west = 3

    def __init__(self, master):
        super().__init__(master=master, bg="black")
        # initialising variables
        self.loading_label = None
        self.l = None
        self.cell_processing_percentage = 0
        self.list_of_traps_and_buffs = None
        self.game_paused = False
        self.buff_one_location = None
        self.buff_two_location = None
        self.buff_three_location = None
        self.trap_one_location = None
        self.trap_two_location = None
        self.trap_three_location = None
        self.game_running = False
        self.wall_coords = None
        self._start_x = 0
        self._start_y = 0
        self._maze_width = 0
        self._maze_height = 0
        self._cell_size = 0
        self.rectangle = None
        self.game_start = False
        self.label = None
        self.no_of_cells_processed = 0

    # update all variables used in rendering the maze
    def updateGraphicVars(self, rows, cols):
        self._cell_size = min(self.winfo_width() / cols, self.winfo_height() / rows)
        self._maze_width = self._cell_size * cols
        self._maze_height = self._cell_size * rows
        self._start_x = (self.winfo_width() - self._maze_width) / 2
        self._start_y = (self.winfo_height() - self._maze_height) / 2

    # create a randomly generated maze with specified dimensions from any starting point within the maze

    def generateMaze(self,
                     wall_color,
                     pointer_color,
                     rows,
                     cols,
                     player_size,
                     player_step_count,
                     no_of_trap_instances,
                     no_of_buff_instances,
                     solution_pos,
                     starting_pos,
                     game_mode,
                     window,
                     start_row=0,
                     start_col=0
                     ):

        self.player_size = player_size
        self.player_step_count = player_step_count
        self.no_of_trap_instances = no_of_trap_instances
        self.no_of_buff_instances = no_of_buff_instances
        self.starting_pos = starting_pos
        self.solution_pos = solution_pos
        self.game_mode = game_mode
        self.rows = rows
        self.cols = cols
        self.window = window
        self.updateGraphicVars(self.rows, self.cols)
        self.pointer_colour = pointer_color

        # maze creation variables
        global visited_cell_count

        maze = createEmptyMaze(self.rows, self.cols)
        cell_stack = deque()
        curr_cell = maze[start_row][start_col]
        curr_cell.setVisited(True)
        visited_cell_count = 1

        # continue generating the maze while cells haven't been visited

        self.game_running = True

        while visited_cell_count <= rows * cols:
            # update graphics
            self.update()
            self.delete("all")
            self.fillCell((0, 0), color=START_COLOR)
            self.fillCell(self.solution_pos, color=END_COLOR)

            self.drawMaze(maze, wall_color=wall_color)  # redraws the updated maze
            self.loading_screen()
            neighbors_and_indices = self.getUnvisitedNeighbors(maze, curr_cell.getPos())

            neighbor_cells = neighbors_and_indices[0]

            neighbor_indices = neighbors_and_indices[1]

            if len(neighbor_indices) > 0:
                # add the current cell to the stack
                cell_stack.append(curr_cell)
                # choose a random neighbor to set as the current cell
                direction = neighbor_indices[random.randrange(0, len(neighbor_indices))]
                curr_cell = neighbor_cells[direction]
                # update maze
                self.removeWalls(cell_stack[-1], curr_cell, direction)
                curr_cell.setVisited(True)
                visited_cell_count += 1
                self.process_cells()

            else:
                # backtrack if there are no available cells
                if cell_stack:
                    curr_cell = cell_stack.pop()
                else:
                    self.show_maze()
                    return

    # update the list of neighbors of the current cell

    def getUnvisitedNeighbors(self, maze, curr_pos):
        neighbor_cells = [None] * 4
        neighbor_indices = []

        # check for north neighbor
        if curr_pos[0] > 0:
            north_neighbor = maze[curr_pos[0] - 1][curr_pos[1]]
            if not north_neighbor.isVisited():
                neighbor_cells[MazeGenerator.north] = north_neighbor
                neighbor_indices.append(MazeGenerator.north)

        # check for south neighbor

        if curr_pos[0] < len(maze) - 1:

            south_neighbor = maze[curr_pos[0] + 1][curr_pos[1]]

            if not south_neighbor.isVisited():
                neighbor_cells[MazeGenerator.south] = south_neighbor

                neighbor_indices.append(MazeGenerator.south)

        # check for east neighbor

        if curr_pos[1] < len(maze[0]) - 1:

            east_neighbor = maze[curr_pos[0]][curr_pos[1] + 1]

            if not east_neighbor.isVisited():
                neighbor_cells[MazeGenerator.east] = east_neighbor

                neighbor_indices.append(MazeGenerator.east)

        # check for west neighbor

        if curr_pos[1] > 0:

            west_neighbor = maze[curr_pos[0]][curr_pos[1] - 1]

            if not west_neighbor.isVisited():
                neighbor_cells[MazeGenerator.west] = west_neighbor

                neighbor_indices.append(MazeGenerator.west)

        return neighbor_cells, neighbor_indices

    # remove wall from appropriate cell based on direction moved

    def removeWalls(self, prev_cell, curr_cell, direction):

        if direction == MazeGenerator.north:  # north
            prev_cell.set_north_wall(False)  # Remove the north wall of the previous cell
            curr_cell.set_south_wall(False)  # Remove the south wall of the current cell

        elif direction == MazeGenerator.south:  # south
            prev_cell.set_south_wall(False)  # Remove the south wall of the previous cell
            curr_cell.set_north_wall(False)  # Remove the north wall of the current cell

        elif direction == MazeGenerator.east:  # east
            prev_cell.set_east_wall(False)  # Remove the east wall of the previous cell
            curr_cell.set_west_wall(False)  # Remove the west wall of the current cell

        elif direction == MazeGenerator.west:  # west
            prev_cell.set_west_wall(False)  # Remove the west wall of the previous cell
            curr_cell.set_east_wall(False)  # Remove the east wall of the current cell

    # draw the walls around a cell
    def drawWalls(self, cell, color):
        rows = 10
        cols = 10
        global visited_cell_count
        cell_pos = cell.getPos()
        cell_x = self._start_x + (cell_pos[1] * self._cell_size)
        cell_y = self._start_y + (cell_pos[0] * self._cell_size)

        if cell.get_north_wall():
            line = (cell_x, cell_y, cell_x + self._cell_size, cell_y)
            self.create_line(*line, fill=color)
            if visited_cell_count >= (rows * cols) - rows and line not in self.wall_coords:
                self.wall_coords.append(line)

        if cell.get_south_wall():
            line = (cell_x, cell_y + self._cell_size, cell_x + self._cell_size, cell_y + self._cell_size)
            self.create_line(*line, fill=color)
            if visited_cell_count >= (rows * cols) - rows and line not in self.wall_coords:
                self.wall_coords.append(line)

        if cell.get_east_wall():
            line = (cell_x + self._cell_size, cell_y, cell_x + self._cell_size, cell_y + self._cell_size)
            self.create_line(*line, fill=color)
            if visited_cell_count >= (rows * cols) - rows and line not in self.wall_coords:
                self.wall_coords.append(line)

        if cell.get_west_wall():
            line = (cell_x, cell_y, cell_x, cell_y + self._cell_size)
            self.create_line(*line, fill=color)
            if visited_cell_count >= (rows * cols) - rows and line not in self.wall_coords:
                self.wall_coords.append(line)

    def fillCell(self, cell_pos, color):
        cell_x = self._start_x + (cell_pos[1] * self._cell_size)
        cell_y = self._start_y + (cell_pos[0] * self._cell_size)
        self.create_rectangle(cell_x, cell_y, cell_x + self._cell_size, cell_y + self._cell_size, fill=color)

    def drawMaze(self, maze, wall_color):

        # list of wall coords contains a list of all the lines present at the end

        # of the maze, tells the program when there is a wall present to make sure

        # the player cant move through walls

        self.wall_coords = []

        # draw north and west walls

        self.create_line(self._start_x, self._start_y, self._maze_width, self._start_y, fill=wall_color)

        self.create_line(self._start_x, self._start_y, self._start_x, self._maze_height, fill=wall_color)

        for row in range(len(maze)):

            for col in range(len(maze[0])):
                cell = maze[row][col]

                self.drawWalls(cell, color=wall_color)

    def loading_screen(self):  # to make sure the player can't try to solve the maze whilst its being created
        self.rectangle = self.create_rectangle(0, 0, 1600, 1600, fill=BLACK)
        if self.game_mode == "easy":
            if self.cell_processing_percentage % 2 == 0 or self.cell_processing_percentage > 95:
                if self.loading_label is not None:
                    self.loading_label.destroy()
                self.loading_label = Label(self, text=f"Loading {self.cell_processing_percentage}%...",
                                           font=(FONT_NAME, 40),
                                           bg=BLACK,
                                           fg=GREEN)
                self.loading_label.place(x=550, y=280)
        else:
            if self.loading_label is not None:
                self.loading_label.destroy()
            self.loading_label = Label(self, text=f"Loading {self.cell_processing_percentage}%...",
                                       font=(FONT_NAME, 40),
                                       bg=BLACK,
                                       fg=GREEN)
            self.loading_label.place(x=550, y=280)

        if self.label is None:
            self.label = Label(self, text="Generating Maze", bg=BLACK, fg=GREEN, font=(FONT_NAME, 50))
            self.label.place(x=490, y=200)

    def show_maze(self):
        global player
        global maze

        self.delete(self.rectangle)
        self.loading_label.destroy()

        self.label.destroy()

        # terminates the loading screen and creates a player which can iterate through the maze

        self.game_start = True
        self.set_traps_and_buffs()
        self.set_buffs()
        self.set_traps_locations()
        print('done')
        global player
        player = Player(self,
                        self.player_size,
                        self.starting_pos[0],
                        self.starting_pos[1],
                        self.wall_coords,
                        self.trap_one_location,
                        self.trap_two_location,
                        self.trap_three_location,
                        self.buff_one_location,
                        self.buff_two_location,
                        self.buff_three_location,
                        self.solution_pos,
                        self.player_step_count,
                        maze,
                        self.window,
                        self._cell_size
                        )

        self.bind('<Up>', lambda event: player.move_player(1))
        self.bind('<Down>', lambda event: player.move_player(2))
        self.bind('<Left>', lambda event: player.move_player(3))
        self.bind('<Right>', lambda event: player.move_player(4))

        self.focus_set()

    def set_traps_locations(self):
        # there will be 3 traps the player may face:
        # 1: trap will send the player to a random square in the map (at least 2 steps away from the solution)
        # 2: trap will decrease points from the point counter
        # 3: trap will send the player to starting pos: at square (0,0)
        # since in some game modes there are multiple traps and buffs in each maze
        # the attributes data type will be a list of tuples

        self.trap_one_location = []  # defining the locations of the traps
        self.trap_two_location = []
        self.trap_three_location = []
        for i in range(len(self.list_of_traps_and_buffs)):
            self.trap_one_location.append(self.list_of_traps_and_buffs[i][0])  # defining the locations of the traps
            self.trap_two_location.append(self.list_of_traps_and_buffs[i][1])
            self.trap_three_location.append(self.list_of_traps_and_buffs[i][2])

        '''
        self.fillCell((self.trap_one_location[1], self.trap_one_location[0]),

                      color='pink')  # for testing reasons, to be deleted once finished

        self.fillCell((self.trap_two_location[1], self.trap_two_location[0]),

                      color='green')  # for testing reasons, to be deleted once finished

        self.fillCell((self.trap_three_location[1], self.trap_three_location[0]),

                      color='purple')  # for testing reasons, to be deleted once finished
        '''

    def set_buffs(self):
        #   there will be 3 buffs the player may face:
        #   buff 1 - adding points to the users overall points
        #   buff 2 - adding more time
        #   buff 3 - performing A* pathfinder to show the player the quickest route to the exit
        # the attributes data type will be a list of tuples
        self.buff_one_location = []  # defining the locations of the traps
        self.buff_two_location = []
        self.buff_three_location = []

        for i in range(len(self.list_of_traps_and_buffs)):
            self.buff_one_location.append(self.list_of_traps_and_buffs[i][3])  # defining the locations of the traps
            self.buff_two_location.append(self.list_of_traps_and_buffs[i][4])
            self.buff_three_location.append(self.list_of_traps_and_buffs[i][5])

        '''
        self.fillCell((self.buff_one_location[1], self.buff_one_location[0]),

                      color='red')  # for testing reasons, to be deleted once finished

        self.fillCell((self.buff_two_location[1], self.buff_two_location[0]),

                      color='blue')  # for testing reasons, to be deleted once finished

        self.fillCell((self.buff_three_location[1], self.buff_three_location[0]),

                      color='grey')  # for testing reasons, to be deleted once finished
        '''

    def set_traps_and_buffs(self):
        # this method will generate the locations of traps and buffs
        # as some difficulty levels will have multiple traps and buffs
        # hence it will return a 2d array of coordinates rather than a 1d array
        self.list_of_traps_and_buffs = []

        number_of_traps_and_buffs_per_level = None
        if self.game_mode == 'easy':
            number_of_traps_and_buffs_per_level = 1
        elif self.game_mode == 'medium':
            number_of_traps_and_buffs_per_level = 3
        elif self.game_mode == 'hard':
            number_of_traps_and_buffs_per_level = 10
        elif self.game_mode == 'madness':
            number_of_traps_and_buffs_per_level = 15

        for i in range(number_of_traps_and_buffs_per_level):
            l = []
            for x in range(6):  # 6 different types of traps and buffs
                random_location = (
                    random.randint(0, self.solution_pos[0] - 1), random.randint(0, self.solution_pos[0] - 1))
                while random_location in self.list_of_traps_and_buffs:
                    random_location = (
                        random.randint(0, self.solution_pos[0] - 1), random.randint(0, self.solution_pos[0] - 1))
                l.append(random_location)
            self.list_of_traps_and_buffs.append(l)
        print('buff and trap locations:')
        print(self.list_of_traps_and_buffs)

    def game_is_paused(self):
        global player
        print('game is paused')
        self.game_paused = True
        player.game_is_paused()

    def game_is_resumed(self):
        global player
        print('game is resumed')
        self.game_paused = False
        player.game_resumes()

    def process_cells(self):
        self.no_of_cells_processed += 1
        self.cell_processing_percentage = round((self.no_of_cells_processed / (self.rows * self.cols)) * 100)


class Cell:

    def __init__(self, row, col):
        self._pos = (row, col)
        self._visited = False
        self._vertical_wall = True
        self._horizontal_wall = True
        # cell starts of with all 4 walls being present- and is generated
        # by the walls being erased as they are visited via procedural DFS
        self.north_wall = True
        self.south_wall = True
        self.east_wall = True
        self.west_wall = True

    # Setters
    def setVisited(self, visited):
        self._visited = visited

    def set_vertical_wall(self, v_wall):
        self._vertical_wall = v_wall

    def set_horizontal_wall(self, h_wall):
        self._horizontal_wall = h_wall

    def set_north_wall(self, n_wall):
        self.north_wall = n_wall

    def set_south_wall(self, s_wall):
        self.south_wall = s_wall

    def set_east_wall(self, e_wall):
        self.east_wall = e_wall

    def set_west_wall(self, w_wall):
        self.west_wall = w_wall

    # Getters
    def get_x(self):
        return self._pos[0]

    def get_y(self):
        return self._pos[1]

    def getPos(self):
        return self._pos

    def isVisited(self):
        return self._visited

    def has_vertical_wall(self):
        return self._vertical_wall

    def has_horizontal_wall(self):
        return self._horizontal_wall

    def get_north_wall(self):
        return self.north_wall

    def get_south_wall(self):
        return self.south_wall

    def get_east_wall(self):
        return self.east_wall

    def get_west_wall(self):
        return self.west_wall

    def __str__(self):
        return self._pos
