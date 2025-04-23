import random

from tkinter import Canvas

from collections import deque

from tkinter import *

import heapq

FONT_NAME = "Courier"
WHITE = "#FFFFFF"
TRAP_COLOR = "#8B0000"
BUFF_COLOR = "#06402b"
global time_increase
global current_pos
global solution
global point_counter
global inaccuracy_points
point_counter = 0
time_increase = False
current_pos = 0
solution = 1
inaccuracy_points = 0  # each time a player backtracks points decrease and inaccuracy points increase


class Player:

    def __init__(self, canvas, square_size, start_x, start_y, list_of_line_coordinates, trap_one_location,

                 trap_two_location, trap_three_location, buff_one_location, buff_two_location, buff_three_location,
                 solution_pos, step_count, maze, window, cell_size):

        self.visited_set = None
        self.trap_or_buff_alert = None
        self.list_of_filled_cells = []
        global solution
        global current_pos
        global point_counter
        global inaccuracy_points
        solution = 1
        current_pos = 0
        self.cell_size = cell_size
        self.path = None
        point_counter = 0
        inaccuracy_points = 0
        self.window = window
        self.solution_found = None

        self.step_count = step_count

        self.player_pos_in_maze = (0, 0)

        solution_found = False

        self.maze = maze

        center_x = start_x + square_size / 2

        center_y = start_y + square_size / 2

        radius = square_size / 2

        self.current_cell = None

        self.positions_explored = []

        self.list_of_line_coordinates = list_of_line_coordinates

        self.canvas = canvas

        self.player = self.canvas.create_oval(center_x - radius,

                                              center_y - radius,

                                              center_x + radius,

                                              center_y + radius,

                                              outline=WHITE,

                                              width=2,

                                              fill=WHITE)

        canvas.tag_raise(self.player)
        self.current_x_pos = start_x

        self.current_y_pos = start_y

        self.starting_x = start_x

        self.starting_y = start_y

        self.pos = (self.current_x_pos, self.current_y_pos)

        self.solution = solution_pos

        self.trap_one_location = trap_one_location

        self.trap_two_location = trap_two_location

        self.trap_three_location = trap_three_location

        self.buff_one_location = buff_one_location

        self.buff_two_location = buff_two_location

        self.buff_three_location = buff_three_location

        self.game_paused = False

        self.array_2_graph()
        print(self.graph)

    def move_player(self, direction):  # direction 1-up,2-down,3-left,4-right

        if self.current_cell is None:
            self.current_cell = self.maze[0][0]

            self.pos = (0, 0)

        # Calculate new potential position

        print('new pos:', self.pos)

        new_x_pos = self.current_x_pos

        new_y_pos = self.current_y_pos
        if direction == 1 and self.game_paused is False:  # up

            new_y_pos -= self.step_count

        elif direction == 2 and self.game_paused is False:  # down

            new_y_pos += self.step_count

        elif direction == 3 and self.game_paused is False:  # left

            new_x_pos -= self.step_count

        elif direction == 4 and self.game_paused is False:  # right

            new_x_pos += self.step_count

        # Check if the new position crosses any lines

        if not self.crosses_line(self.current_x_pos, self.current_y_pos, new_x_pos, new_y_pos):
            self.canvas.move(self.player, new_x_pos - self.current_x_pos, new_y_pos - self.current_y_pos)

            print()

            self.current_x_pos = new_x_pos

            self.current_y_pos = new_y_pos

            print('x:', self.current_x_pos)

            print('y:', self.current_y_pos)

            print((self.current_x_pos - self.starting_x) // self.step_count,

                  (self.current_y_pos - self.starting_y) // self.step_count)

            self.current_cell = self.maze[(self.current_x_pos - self.starting_x) // self.step_count][

                (self.current_y_pos - self.starting_y) // self.step_count]

            self.pos = (self.current_x_pos, self.current_y_pos)

            print('new pos:', self.pos)

            print('new pos: (before checking if in trap)', self.pos)

            self.check_if_stepped_on_trap()
            self.check_if_stepped_on_buff()

        global point_counter
        global current_pos
        global solution
        global inaccuracy_points

        print('self.pos', self.pos)
        print('actual current pos:', self.current_cell.getPos())

        current_pos = self.current_cell.getPos()
        solution = self.solution

        if self.current_cell.getPos() in self.positions_explored and self.game_paused is False:
            inaccuracy_points += 1
            point_counter -= 1

        elif self.current_cell.getPos() not in self.positions_explored and self.game_paused is False:  # add a checker if points are greater than - 1
            point_counter += 1

            self.positions_explored.append(self.current_cell.getPos())

        if self.path:
            print('removing square')
            print(self.path)
            print(self.current_cell.getPos())
            print(type(self.current_cell.getPos()), self.current_cell.getPos())
            print(type(self.path[0]), self.path)
            if self.current_cell.getPos() in self.path:
                print(self.path)
                pos = self.path.index(self.current_cell.getPos())
                self.canvas.delete(self.list_of_filled_cells[pos])

    def crosses_line(self, x1, y1, x2, y2):
        print(
            f"Checking path from ({(x1 // self.step_count) - self.starting_x}, {(y1 // self.step_count) - self.starting_y}) to ({(x2 // self.step_count) - self.starting_x}, {(y2 // self.step_count) - self.starting_y})")
        for line in self.list_of_line_coordinates:
            x1_line, y1_line, x2_line, y2_line = line

            # Check for intersection
            if self.lines_intersect(x1, y1, x2, y2, x1_line, y1_line, x2_line, y2_line):
                print(f"Intersection detected with wall line: ({x1_line}, {y1_line}) -> ({x2_line}, {y2_line})")
                return True

        return False

    @staticmethod
    def lines_intersect(x1, y1, x2, y2, x3, y3, x4, y4):

        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        return ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and \
 \
            ccw((x1, y1), (x2, y2), (x3, y3)) != ccw((x1, y1), (x2, y2), (x4, y4))

    def get_player_pos(self):

        return self.pos

    def get_player_pos_in_maze(self):

        return self.player_pos_in_maze

    def set_player_pos_in_maze(self, x, y):

        self.player_pos_in_maze = (x, y)

    def check_if_stepped_on_trap(self):  # returns location of the trap if the player steps on it
        print('new pos:', self.pos)

        print('trap 1 locations', self.trap_one_location)
        print('trap 2 locations', self.trap_two_location)
        print('trap 3 locations', self.trap_three_location)

        if self.current_cell.getPos() in self.trap_one_location:
            self.stepped_in_trap_one()

        if self.current_cell.getPos() in self.trap_two_location:
            self.stepped_in_trap_two()

        if self.current_cell.getPos() in self.trap_three_location:
            self.stepped_in_trap_three()

    def stepped_in_trap_three(self):
        global point_counter
        if point_counter >= 5:
            point_counter -= 6
        self.trap_three_location.remove(self.current_cell.getPos())
        self.trap_three_location.append(generate_random_location(self.solution, self.trap_one_location,
                                                                 self.trap_two_location, self.trap_three_location,
                                                                 self.buff_one_location, self.buff_two_location,
                                                                 self.buff_three_location))
        self.stepped_in_trap_or_buff_indicator("You've triggered a trap!\n -5 points", color=TRAP_COLOR)

    def stepped_in_trap_two(self):
        self.trap_two_location.remove(self.current_cell.getPos())
        if self.path:
            print('existing path found')
            for pos in range(len(self.path)):
                self.canvas.delete(self.list_of_filled_cells[pos])
            self.list_of_filled_cells = []
            self.path = None

        dx = ((0 * self.step_count) - self.current_x_pos) + self.starting_x

        dy = ((0 * self.step_count) - self.current_y_pos) + self.starting_y

        self.canvas.move(self.player, dx, dy)

        self.current_x_pos = self.starting_x

        self.current_y_pos = self.starting_y

        self.current_cell = self.maze[0][0]

        self.pos = (self.current_x_pos, self.current_y_pos)

        self.trap_two_location.append(generate_random_location(self.solution, self.trap_one_location,
                                                               self.trap_two_location, self.trap_three_location,
                                                               self.buff_one_location, self.buff_two_location,
                                                               self.buff_three_location))

        self.positions_explored = []  # resetting positions explored
        self.stepped_in_trap_or_buff_indicator("You've triggered a trap!\nTransporting you back\nto the starting "
                                               "point...", color=TRAP_COLOR)

    def check_if_stepped_on_buff(self):  # returns location of the trap if the player steps on it

        print('new pos:', self.pos)
        print('buff 1 location', self.buff_one_location)
        print('buff 2 location', self.buff_two_location)
        print('buff 3 location', self.buff_three_location)

        if self.current_cell.getPos() in self.buff_one_location:
            self.stepped_in_buff_one()

        if self.current_cell.getPos() in self.buff_two_location:
            self.stepped_in_buff_two()

        if self.current_cell.getPos() in self.buff_three_location:
            self.stepped_in_buff_three()

    def stepped_in_trap_one(self):
        # trap one sends the player to a random location in the maze
        # this can be a trap or a buff as this random location can be near the
        # solution (ask if that is ok or if I should add a limit as to the
        # randomness of the location (at least 2 squares away from the solution?)
        # however there are some squares that cannot lead to the final destination
        # (hence leading the player to be trapped)
        # we can solve this problem by... (working on that)
        # using a DFS to check if there is a solution available: problem self.maze is a 2d array not a graph...
        # create a while loop and a visited set and each loop a new random player
        # location is generated and loop until the visited set contains the solution
        # from the random location
        self.trap_one_location.remove(self.current_cell.getPos())
        if self.path:
            print('existing path found')
            for pos in range(len(self.path)):
                self.canvas.delete(self.list_of_filled_cells[pos])
                print('yes')
            self.list_of_filled_cells = []
            self.path = None

        self.solution_found = False
        while self.solution_found is False:
            # each time solution found is false - generate a new value and call dfs again
            new_random_location = generate_random_location(self.solution, self.trap_one_location,
                                                           self.trap_two_location, self.trap_three_location,
                                                           self.buff_one_location, self.buff_two_location,
                                                           self.buff_three_location)
            print(new_random_location)
            new_r_l_x = new_random_location[0]  # generating random location
            new_r_l_y = new_random_location[1]

            self.visited_set = set()
            new_potential_pos = (new_r_l_x, new_r_l_y)
            self.dfs(new_potential_pos)  # dfs only there to check if solution is findable
            if self.solution_found is False:
                print('dfs was not efficient')
                back_up_checker = self.shortest_path(self.current_cell.getPos())
                if self.solution in back_up_checker:
                    self.solution_found = True

        current_coords = self.canvas.coords(self.player)
        current_x = int(current_coords[0])

        current_y = int(current_coords[1])

        print('current x, current y')

        print(current_x, current_y)

        dx = ((new_r_l_x * self.step_count) - current_x) + self.starting_x

        dy = ((new_r_l_y * self.step_count) - current_y) + self.starting_y

        self.canvas.move(self.player, dx, dy)  # the cell is going to the right pos

        self.current_x_pos = current_x + dx

        self.current_y_pos = current_y + dy

        self.current_cell = self.maze[new_r_l_x][new_r_l_y]  # but it's going through walls

        self.pos = (self.current_x_pos, self.current_y_pos)

        # 20/08/2024: added the trap BUT DFS is needed bc there is a chance that the player
        # may land on a random spot that is unsolvable from that position: which breaks the game
        # hence dfs is needed to check IF random location is solvable: move to that spot
        # while location isn't solvable generate another random location and keep looping and

        # calling dfs until it is solvable
        self.trap_one_location.append(generate_random_location(self.solution, self.trap_one_location,
                                                               self.trap_two_location, self.trap_three_location,
                                                               self.buff_one_location, self.buff_two_location,
                                                               self.buff_three_location))
        self.positions_explored = []  # resetting positions explored
        self.stepped_in_trap_or_buff_indicator("You've triggered a trap!\n Transporting you to a\n random location...",
                                               color=TRAP_COLOR)

    def dfs(self, current_pos_dfs):

        # Check if we have reached the solution
        if current_pos_dfs == self.solution:
            self.solution_found = True
            return

        # if the current position has not been visited, add it to the visited set
        if current_pos_dfs not in self.visited_set:
            self.visited_set.add(current_pos_dfs)

            # Recursively visit all neighboring nodes
            for neighbouring_node in self.graph[current_pos_dfs]:
                if neighbouring_node not in self.visited_set:
                    self.dfs(neighbouring_node)

    def stepped_in_buff_one(self):
        #   if a player steps in buff one the easiest route to the destination should be shown on screen
        #   this would be calculated via using A star pathfinder to find the shortest path in the 2D array
        #   when the player steps on this buff all trap locations will be set to NONE

        '''  # this was when A star was implemented
        path = self.astar_search((self.buff_one_location[1], self.buff_one_location[0]))
        if path:
            print("Path found:", path)
            print()
            for i in range(len(path)):
                self.fillCell(path[i], 'red', 104.0, 0.0, 80.0)

        else:
            print("No path found")
        '''
        print('path:', self.path)
        if self.path:
            print('existing path found')
            for pos in range(len(self.path)):
                self.canvas.delete(self.list_of_filled_cells[pos])
                print('yes')
            self.list_of_filled_cells = []
            self.path = None

        self.path = self.shortest_path(self.current_cell.getPos())

        for i in range(len(self.path)):
            self.fillCell((self.path[i][1], self.path[i][0]), 'red', 255.0, 0.0, self.cell_size, 'l')

        self.buff_one_location.remove(self.current_cell.getPos())
        self.buff_one_location.append(generate_random_location(self.solution, self.trap_one_location,
                                                               self.trap_two_location, self.trap_three_location,
                                                               self.buff_one_location, self.buff_two_location,
                                                               self.buff_three_location))
        self.stepped_in_trap_or_buff_indicator(
            "You've activated a buff!\n The shortest path to the\n end of the maze is now\n revealed.",
            color=BUFF_COLOR)

    def stepped_in_buff_two(self):
        global point_counter
        point_counter += 5
        self.buff_two_location.remove(self.current_cell.getPos())
        self.buff_two_location.append(generate_random_location(self.solution, self.trap_one_location,
                                                               self.trap_two_location, self.trap_three_location,
                                                               self.buff_one_location, self.buff_two_location,
                                                               self.buff_three_location))
        self.stepped_in_trap_or_buff_indicator("You've activated a buff!\n +5 points",
                                               color=BUFF_COLOR)


    def stepped_in_buff_three(self):
        time_increase_indicator()
        self.buff_three_location.remove(self.current_cell.getPos())
        self.buff_three_location.append(generate_random_location(self.solution, self.trap_one_location,
                                                                 self.trap_two_location, self.trap_three_location,
                                                                 self.buff_one_location, self.buff_two_location,
                                                                 self.buff_three_location))
        self.stepped_in_trap_or_buff_indicator("You've activated a buff!\n +10 seconds",
                                               color=BUFF_COLOR)

    def array_2_graph(self):  # creates a graph version of the maze - called when a player is created in constructor
        # checks if there is a wall
        delta = [[self.step_count * -1, 0],  # go up
                 [0, self.step_count * -1],  # go left
                 [self.step_count, 0],  # go down
                 [0, self.step_count]]  # go right

        self.graph = {}

        for x in range(len(self.maze[0])):  # creating a graph with keys of all the coordinates within the maze
            for y in range(len(self.maze[1])):  # i.e a 10x10 maze would have 100 keys
                self.graph[(x, y)] = []

        for x in range(len(self.maze[0])):
            x1 = (x * self.step_count) + self.starting_x
            for y in range(len(self.maze[1])):
                y1 = (y * self.step_count) + self.starting_y
                for directions in range(len(delta)):
                    x2 = x1 + delta[directions][0]  # in tkinter format
                    y2 = y1 + delta[directions][1]
                    x_coordinate = (x2 - self.starting_x) // self.step_count
                    y_coordinate = (y2 - self.starting_y) // self.step_count
                    if 0 <= x_coordinate < (len(self.maze[0])) and 0 <= y_coordinate < (len(self.maze[0])):
                        if not self.crosses_line(x1, y1, x2, y2):
                            self.graph[(x, y)].append((x_coordinate, y_coordinate))

    def shortest_path(self, start):
        distances = self.dijkstra(self.solution)
        print(distances)
        path = []
        current_node = start
        path.append(current_node)
        distance_of_current_node = distances[current_node]
        while distance_of_current_node != 0:
            potential_next_nodes = []
            potential_next_distance = []
            for neighbour in self.graph[current_node]:
                if distances[neighbour] < distance_of_current_node:
                    potential_next_nodes.append(neighbour)
                    potential_next_distance.append(distances[neighbour])

            min_distance_index = potential_next_distance.index(min(potential_next_distance))
            current_node = potential_next_nodes[min_distance_index]

            path.append(current_node)
            distance_of_current_node = distances[current_node]
        return path

    def astar_search(self, start):
        open_set = []
        closed_set = set()

        start_node = Node(start, 0, heuristic(start, self.solution))
        heapq.heappush(open_set, start_node)

        g_score = {start: 0}

        while open_set:
            current_node = heapq.heappop(open_set)

            if current_node.position == self.solution:
                # Path found, reconstruct and return it
                path = []
                while current_node:
                    path.insert(0, current_node.position)
                    current_node = current_node.parent
                return path

            closed_set.add(current_node.position)

            for neighbor_idx in range(len(self.graph[current_node.position])):
                neighbor = self.graph[current_node.position][neighbor_idx]
                if neighbor in closed_set:
                    continue

                # Calculate the tentative cost
                tentative_g_score = g_score[current_node.position] + 3  # Assuming a constant step cost of 3

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g_score
                    heuristic_val = heuristic(neighbor, self.solution)
                    new_node = Node(neighbor, tentative_g_score, heuristic_val)
                    new_node.parent = current_node

                    heapq.heappush(open_set, new_node)
        return None  # No path found

    def fillCell(self, cell_pos, color, start_x, start_y, cell_size, pos):
        cell_x = start_x + (cell_pos[1] * cell_size)

        cell_y = start_y + (cell_pos[0] * cell_size)
        r = self.canvas.create_rectangle(cell_x, cell_y, cell_x + cell_size, cell_y + cell_size, fill=color)
        self.list_of_filled_cells.append(r)
        print('r', r)
        if pos == 'l':
            self.canvas.tag_lower(r)
        if pos == 'h':
            self.canvas.lift()

    def dijkstra(self, start):
        # Create a dictionary to store the distance from the start node to other nodes
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        # Create a priority queue to store the nodes to be processed
        heap = [(0, start)]

        while heap:
            # Extract the node with the smallest distance
            (current_distance, current_node) = heapq.heappop(heap)

            # If the current distance is greater than the recorded distance, skip this node
            if current_distance > distances[current_node]:
                continue

            # Update the distances for the neighbors of the current node
            for neighbor in self.graph[current_node]:
                weight = self.calc_weight(current_node, neighbor)
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))

        return distances

    def calc_weight(self, current_node, next_node):
        x1 = (current_node[0] * self.step_count) + self.starting_x
        y1 = (current_node[1] * self.step_count) + self.starting_y
        x2 = (next_node[0] * self.step_count) + self.starting_x
        y2 = (next_node[1] * self.step_count) + self.starting_y
        if not self.crosses_line(x1, y1, x2, y2):
            return 1
        else:
            return float('inf')

    def game_is_paused(self):
        self.game_paused = True
        if self.trap_or_buff_alert:
            self.trap_or_buff_alert.place_forget()

    def game_resumes(self):
        self.game_paused = False

    def stepped_in_trap_or_buff_indicator(self, display_text, color):
        if self.trap_or_buff_alert:
            self.trap_or_buff_alert.destroy()
        self.trap_or_buff_alert = Label(self.window, text=display_text, font=(FONT_NAME, 20, "bold"), anchor='w',
                                        justify='left')
        self.trap_or_buff_alert.place(x=0, y=300)
        self.trap_or_buff_alert.config(fg=color)


def generate_random_location(solution, trap_one_location, trap_two_location, trap_three_location, buff_one_location,
                             buff_two_location, buff_three_location):
    print('solution')
    print(solution)
    new_random_location = (random.randint(0, solution[0] - 1), random.randint(0, solution[0] - 1))
    print(new_random_location)

    while (new_random_location == solution or
           new_random_location == (0, 0) or
           new_random_location in trap_one_location or
           new_random_location in trap_two_location or
           new_random_location in trap_three_location or
           new_random_location in buff_one_location or
           new_random_location in buff_two_location or
           new_random_location in buff_three_location):
        print('solution')
        print(solution)
        new_random_location = (random.randint(0, solution[0] - 1), random.randint(0, solution[0] - 1))
        print(new_random_location)

    print('new random location:', new_random_location)
    return new_random_location


class Node:
    def __init__(self, position, cost, heuristic):
        self.position = position
        self.cost = cost
        self.heuristic = heuristic
        self.parent = None  # Add a parent attribute to track the path

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def heuristic(node, goal):
    # Simple Manhattan distance as the heuristic
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def get_inaccuracy_points():
    global inaccuracy_points
    return inaccuracy_points


def get_point_counter():
    global point_counter
    return point_counter


def check_if_solution_is_found():
    global current_pos
    global solution
    if current_pos == solution:
        print('current pos:', current_pos)
        print('solution', solution)
        return True
    else:
        return False


def check_if_point_is_below_0():
    global point_counter
    if point_counter < 0:
        return True
    return False


def time_increase_indicator():  # if called within player: returns true, if called within ui set up returns false
    global time_increase
    time_increase = True


def set_time_increase(input):
    global time_increase
    time_increase = input
