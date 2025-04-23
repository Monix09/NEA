import tkinter

from tkinter import *

import mysql.connector

import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BLACK = "#000000"

WHITE = "#FFFFFF"

GREEN = "#55FF55"
GOLD = '#FFD700'

FONT_NAME = "Courier"

db = mysql.connector.connect(host="localhost", user="root", passwd="Bella72006!", port="3306",

                             database="maze_of_madness_data_base")
my_cur = db.cursor()


class Leaderboard:
    def __init__(self, user_id):

        self.name_plate = None
        self.x_axis_label = None
        self.y_value_label = None
        self.donut_graph = None
        self.line_graph = None
        self.all_user_data = []
        self.canvas3 = None
        self.canvas1 = None
        self.canvas2 = None

        self.user_id = user_id

        self.list_of_ids = []
        self.list_of_user_data = []
        self.game_mode_sorting_criteria = 'points'
        self.active_difficulty_mode = 'easy'
        self.y_axis_value = 'points'

        self.get_user_ids(self.active_difficulty_mode, self.game_mode_sorting_criteria)

        if self.game_mode_sorting_criteria == 'time':
            n = self.sort_based_on_time_or_inaccuracy_points(self.list_of_user_data, self.list_of_ids)
            print('answer', n)

        elif self.game_mode_sorting_criteria == 'inaccuracy_points':
            n = self.sort_based_on_time_or_inaccuracy_points(self.list_of_user_data, self.list_of_ids)
            print('answer', n)

        elif self.game_mode_sorting_criteria == 'points':
            print('points:', self.list_of_user_data)
            n = self.sort_based_on_points(self.list_of_user_data, self.list_of_ids)
            print('answer', n)

        self.list_of_ids = []
        for i in range(len(n[1])):
            self.list_of_ids.append(n[1][i])

        self.process_user_summary()
        self.leaderboard_window = Tk()
        self.leaderboard_window.config(bg=BLACK)
        self.leaderboard_window.attributes("-fullscreen", True)
        Label(self.leaderboard_window, text="Leaderboard", font=(FONT_NAME, 60, 'bold'), bg=BLACK, fg=GREEN).place(
            x=200,
            y=15)

        self.create_label('rank', 25, 95, 15, WHITE)
        self.create_label('username', 140, 95, 15, WHITE)
        self.create_label('difficulty', 320, 95, 15, WHITE)
        self.create_label('time', 520, 95, 15, WHITE)
        self.create_label('accuracy', 640, 95, 15, WHITE)
        self.create_label('pts', 800, 95, 15, WHITE)

        Button(self.leaderboard_window, text='Back', highlightthickness=0, command=self.destroy_window).place(x=0, y=0)

        self.create_label('sort by:', 40, 0, 15, WHITE)

        self.create_button('time', 0, 30, command_=lambda: self.sort_by_category('time'))
        self.create_button('accuracy', 50, 30, command_=lambda: self.sort_by_category('inaccuracy_points'))
        self.create_button('pts', 130, 30, command_=lambda: self.sort_by_category('points'))

        self.create_button('easy', 760, 0, command_=lambda: self.change_difficulty('easy'))
        self.create_button('medium', 810, 0, command_=lambda: self.change_difficulty('medium'))
        self.create_button('hard', 760, 30, command_=lambda: self.change_difficulty('hard'))
        self.create_button('madness', 760, 60, command_=lambda: self.change_difficulty('madness'))

        self.top_10_side()
        self.user_details_side()
        self.your_personal_best()

    def destroy_window(self):
        self.leaderboard_window.destroy()

    def user_details_side(self):  # right
        self.canvas1 = Canvas(self.leaderboard_window, width=1200, height=1200)
        self.canvas1.place(x=900, y=125)
        self.canvas1.create_rectangle(0, 0, 1200, 1200, fill=BLACK)

    def top_10_side(self):  # left
        self.canvas2 = Canvas(self.leaderboard_window, width=1200, height=1200)
        self.canvas2.place(x=-250, y=125)

        self.canvas2.create_rectangle(0, 0, 1200, 1200, fill=BLACK)

        self.canvas2.create_rectangle(0, 0, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 75, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 175, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 275, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 375, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 475, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 575, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 675, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 775, 1200, 75, fill='', outline=WHITE)
        self.canvas2.create_rectangle(0, 875, 1200, 75, fill='', outline=WHITE)

        # top 10 ranking numbers
        self.create_label('#1', 25, 135, 35, GREEN)
        self.create_label('#2', 25, 235, 35, GREEN)
        self.create_label('#3', 25, 335, 35, GREEN)
        self.create_label('#4', 25, 435, 35, GREEN)
        self.create_label('#5', 25, 535, 35, GREEN)
        self.create_label('#6', 25, 635, 35, GREEN)
        self.create_label('#7', 25, 735, 35, GREEN)
        self.create_label('#8', 25, 835, 35, GREEN)
        self.create_label('#9', 25, 935, 35, GREEN)
        self.create_label('#10', 25, 1020, 35, GREEN)

        # top 10 ranking numbers' buttons
        self.create_button('i', 886, 125, command_=lambda: self.get_time_stamps(0))
        self.create_button('i', 886, 200, command_=lambda: self.get_time_stamps(1))
        self.create_button('i', 886, 300, command_=lambda: self.get_time_stamps(2))
        self.create_button('i', 886, 400, command_=lambda: self.get_time_stamps(3))
        self.create_button('i', 886, 500, command_=lambda: self.get_time_stamps(4))
        self.create_button('i', 886, 600, command_=lambda: self.get_time_stamps(5))
        self.create_button('i', 886, 700, command_=lambda: self.get_time_stamps(6))
        self.create_button('i', 886, 800, command_=lambda: self.get_time_stamps(7))
        self.create_button('i', 886, 900, command_=lambda: self.get_time_stamps(8))
        self.create_button('i', 886, 1000, command_=lambda: self.get_time_stamps(9))

        # top 10 ranking numbers' names
        self.create_label(self.get_parts_of_user_summery(0, 'username'), 90, 145, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(1, 'username'), 90, 245, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(2, 'username'), 90, 345, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(3, 'username'), 90, 445, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(4, 'username'), 90, 545, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(5, 'username'), 90, 645, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(6, 'username'), 90, 745, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(7, 'username'), 90, 845, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(8, 'username'), 90, 945, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(9, 'username'), 115, 1030, 25, WHITE)

        # difficulty

        self.create_label(self.get_parts_of_user_summery(0, 'difficulty'), 320, 145, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(1, 'difficulty'), 320, 245, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(2, 'difficulty'), 320, 345, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(3, 'difficulty'), 320, 445, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(4, 'difficulty'), 320, 545, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(5, 'difficulty'), 320, 645, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(6, 'difficulty'), 320, 745, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(7, 'difficulty'), 320, 845, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(8, 'difficulty'), 320, 945, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(9, 'difficulty'), 345, 1030, 25, WHITE)

        # time

        self.create_label(self.get_parts_of_user_summery(0, 'time_taken'), 500, 145, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(1, 'time_taken'), 500, 245, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(2, 'time_taken'), 500, 345, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(3, 'time_taken'), 500, 445, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(4, 'time_taken'), 500, 545, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(5, 'time_taken'), 500, 645, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(6, 'time_taken'), 500, 745, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(7, 'time_taken'), 500, 845, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(8, 'time_taken'), 500, 945, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(9, 'time_taken'), 525, 1030, 25, WHITE)

        # accuracy

        self.create_label(self.get_parts_of_user_summery(0, 'inaccuracy_points'), 640, 145, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(1, 'inaccuracy_points'), 640, 245, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(2, 'inaccuracy_points'), 640, 345, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(3, 'inaccuracy_points'), 640, 445, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(4, 'inaccuracy_points'), 640, 545, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(5, 'inaccuracy_points'), 640, 645, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(6, 'inaccuracy_points'), 640, 745, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(7, 'inaccuracy_points'), 640, 845, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(8, 'inaccuracy_points'), 640, 945, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(9, 'inaccuracy_points'), 660, 1030, 25, WHITE)

        # points

        self.create_label(self.get_parts_of_user_summery(0, 'points'), 780, 145, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(1, 'points'), 780, 245, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(2, 'points'), 780, 345, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(3, 'points'), 780, 445, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(4, 'points'), 780, 545, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(5, 'points'), 780, 645, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(6, 'points'), 780, 745, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(7, 'points'), 780, 845, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(8, 'points'), 780, 945, 25, WHITE)
        self.create_label(self.get_parts_of_user_summery(9, 'points'), 780, 1030, 25, WHITE)

        # stars

        self.create_label(self.get_parts_of_user_summery(0, 'stars_earned'), 850, 175, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(1, 'stars_earned'), 850, 275, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(2, 'stars_earned'), 850, 375, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(3, 'stars_earned'), 850, 475, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(4, 'stars_earned'), 850, 575, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(5, 'stars_earned'), 850, 675, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(6, 'stars_earned'), 850, 775, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(7, 'stars_earned'), 850, 875, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(8, 'stars_earned'), 850, 975, 10, GOLD)
        self.create_label(self.get_parts_of_user_summery(9, 'stars_earned'), 850, 1060, 10, GOLD)

    def your_personal_best(self):
        self.canvas3 = Canvas(self.leaderboard_window, width=1000, height=75)
        self.canvas3.place(x=900, y=25)
        self.canvas3.create_rectangle(0, 0, 10000, 10000, fill=BLACK, outline=WHITE)

        self.create_label('rank', 900, -5, 15, WHITE)
        self.create_label('username', 1050, -5, 15, WHITE)
        self.create_label('difficulty', 1250, -5, 15, WHITE)
        self.create_label('time', 1440, -5, 15, WHITE)
        self.create_label('accuracy', 1620, -5, 15, WHITE)
        self.create_label('pts', 1800, -5, 15, WHITE)

        i = self.get_your_personal_best_index()

        if i is None:
            self.create_label('not attempted', 1250, 40, 30, GREEN)
        else:
            self.create_label(f'#{i + 1}', 905, 35, 40, GREEN)
            self.create_label(self.get_parts_of_user_summery(i, 'username'), 1050, 45, 25, WHITE)
            self.create_label(self.get_parts_of_user_summery(i, 'difficulty'), 1250, 45, 25, WHITE)
            self.create_label(self.get_parts_of_user_summery(i, 'time_taken'), 1440, 45, 25, WHITE)
            self.create_label(self.get_parts_of_user_summery(i, 'inaccuracy_points'), 1650, 45, 25, WHITE)
            self.create_label(self.get_parts_of_user_summery(i, 'points'), 1800, 45, 25, WHITE)
            self.create_label(self.get_parts_of_user_summery(i, 'stars_earned'), 1850, 80, 10, GOLD)
            self.create_button('i', 1890, 25, command_=lambda: self.get_time_stamps(i))

    def get_your_personal_best_index(self):
        for i in range(len(self.all_user_data)):
            print(self.all_user_data[i][0])
            print(self.user_id)
            if self.all_user_data[i][0] == self.user_id[0]:
                return i
        return None

    def get_user_name(self, user_id):

        query1 = """
        SELECT username
        FROM users
        WHERE user_id = %s
        """
        my_cur.execute(query1, (user_id,))
        result1 = my_cur.fetchone()
        return result1

    def get_time(self, user_id):
        if user_id is None:
            return '00:00'
        print('user id:', user_id)
        query = """
        SELECT time_taken FROM personal_best WHERE user_id = %s AND category = 'time' AND difficulty=%s
        """
        my_cur.execute(query, (user_id, self.active_difficulty_mode))

        results = my_cur.fetchall()

        for i in range(len(results)):
            self.list_of_user_data.append(results[i][0])
        print('times', self.list_of_user_data)

    def get_accuracy(self, user_id):
        if user_id is None:
            return '100%'
        print('user id: we', user_id)
        print(self.game_mode_sorting_criteria)
        query = """
         SELECT inaccuracy_points FROM personal_best WHERE user_id = %s AND category = 'inaccuracy_points' AND difficulty=%s
         """
        my_cur.execute(query, (user_id, self.active_difficulty_mode))

        results = my_cur.fetchall()

        for i in range(len(results)):
            self.list_of_user_data.append(results[i][0])
        print('inaccuracy points', self.list_of_user_data)

    def get_points(self, user_id):
        if user_id is None:
            return '9999'
        print('user id: we', user_id)
        print(self.game_mode_sorting_criteria)
        query = """
         SELECT points FROM personal_best WHERE user_id = %s AND category = 'points' AND difficulty=%s
         """
        my_cur.execute(query, (user_id, self.active_difficulty_mode))

        results = my_cur.fetchall()

        for i in range(len(results)):
            self.list_of_user_data.append(results[i][0])
        print('points', self.list_of_user_data)

    def create_label(self, text_, x_, y_, text_size, color):
        Label(self.leaderboard_window, text=text_, bg=BLACK, fg=color, font=(FONT_NAME, text_size, 'bold')).place(x=x_,
                                                                                                                  y=y_)

    def create_button(self, text_, x_, y_, command_):
        Button(self.leaderboard_window, text=text_, bg=WHITE, fg=BLACK, command=command_, font='bold',
               borderwidth=0).place(x=x_, y=y_)

    def get_user_ids(self, difficulty_level, category):

        query = """
        SELECT user_id FROM personal_best WHERE difficulty = %s AND category= %s
        """
        my_cur.execute(query, (difficulty_level, category))

        results = my_cur.fetchall()
        print('results', results)
        if results:
            print(f"Personal Bests for {difficulty_level.capitalize()} Difficulty:")
            for i in range(len(results)):
                self.list_of_ids.append(results[i][0])
                print(results[i][0])
                self.get_data(results[i][0])

    def get_data(self, user_id):
        print(user_id)
        if self.game_mode_sorting_criteria == 'time':
            self.get_time(user_id)
        elif self.game_mode_sorting_criteria == 'inaccuracy_points':
            self.get_accuracy(user_id)

        elif self.game_mode_sorting_criteria == 'points':
            self.get_points(user_id)

    def sort_based_on_time_or_inaccuracy_points(self, arr, arr_of_ids):
        elements = len(arr)

        if elements < 2:
            return arr, arr_of_ids

        current_position = 0

        for i in range(1, elements):
            if arr[i] <= arr[0]:
                current_position += 1
                arr[i], arr[current_position] = arr[current_position], arr[i]
                arr_of_ids[i], arr_of_ids[current_position] = arr_of_ids[current_position], arr_of_ids[i]

        arr[0], arr[current_position] = arr[current_position], arr[0]
        arr_of_ids[0], arr_of_ids[current_position] = arr_of_ids[current_position], arr_of_ids[0]

        left_arr, left_ids = self.sort_based_on_time_or_inaccuracy_points(arr[0:current_position],
                                                                          arr_of_ids[0:current_position])
        right_arr, right_ids = self.sort_based_on_time_or_inaccuracy_points(arr[current_position + 1:],
                                                                            arr_of_ids[current_position + 1:])

        sorted_arr = left_arr + [arr[current_position]] + right_arr
        sorted_ids = left_ids + [arr_of_ids[current_position]] + right_ids

        return sorted_arr, sorted_ids
        # returned in the format i.e: ([5, 9, 15], [1, 2, 3])- ascending order - quickest/ most accurate first

    def sort_based_on_points(self, arr, arr_of_ids):
        elements = len(arr)

        if elements < 2:
            return arr, arr_of_ids

        current_position = 0

        for i in range(1, elements):
            if arr[i] >= arr[0]:
                current_position += 1
                arr[i], arr[current_position] = arr[current_position], arr[i]
                arr_of_ids[i], arr_of_ids[current_position] = arr_of_ids[current_position], arr_of_ids[i]

        arr[0], arr[current_position] = arr[current_position], arr[0]
        arr_of_ids[0], arr_of_ids[current_position] = arr_of_ids[current_position], arr_of_ids[0]

        left_arr, left_ids = self.sort_based_on_points(arr[0:current_position], arr_of_ids[0:current_position])
        right_arr, right_ids = self.sort_based_on_points(arr[current_position + 1:], arr_of_ids[current_position + 1:])

        sorted_arr = left_arr + [arr[current_position]] + right_arr
        sorted_ids = left_ids + [arr_of_ids[current_position]] + right_ids

        return sorted_arr, sorted_ids
        # returned in the format i.e: ([215, 114, 78], [1, 2, 3])- descending order - most amount of points first

    def process_user_summary(self):
        print(self.list_of_ids)
        for user_id in self.list_of_ids:
            cur = db.cursor(buffered=True)
            print(user_id)
            result1 = self.get_user_name(user_id)

            query2 = """
              SELECT time_taken, inaccuracy_points, points, stars_earned, p_b_id
              FROM personal_best
              WHERE user_id = %s AND difficulty = %s AND category = %s
              """
            cur.execute(query2, (user_id, self.active_difficulty_mode, self.game_mode_sorting_criteria))
            result2 = cur.fetchone()
            cur.close()

            self.all_user_data.append([user_id, result1[0], result2])
            print(self.all_user_data)  # Check to see all the user data added

    def get_stars(self):
        return '★★★'

    def get_parts_of_user_summery(self, place, category):

        if place < len(self.all_user_data):
            print('lanth', len(self.all_user_data))
            if category == 'username':
                return self.all_user_data[place][1]
            elif category == 'time_taken':
                return self.convert_into_time_format(self.all_user_data[place][2][0])
            elif category == 'inaccuracy_points':
                return self.convert_into_accuracy_formatt(self.all_user_data[place][2][1],
                                                          self.all_user_data[place][2][2])
            elif category == 'points':
                return self.all_user_data[place][2][2]
            elif category == 'stars_earned':
                return self.convert_into_stars_formatt(self.all_user_data[place][2][3])
            elif category == 'difficulty':
                return self.active_difficulty_mode
        else:
            return ''

    def convert_into_time_format(self, time_in_seconds):
        minutes = time_in_seconds // 60
        seconds = time_in_seconds % 60

        return f"{minutes:02}:{seconds:02}"

    def convert_into_accuracy_formatt(self, inaccuracy_points, points):
        return f"{int(points / (points + inaccuracy_points) * 100)}%"

    def convert_into_stars_formatt(self, no_of_stars):
        if no_of_stars == 1:
            return '★☆☆'

        elif no_of_stars == 2:
            return '★★☆'

        elif no_of_stars == 3:
            return '★★★'
        else:
            return '☆☆☆'

    def sort_by_category(self, category):
        self.game_mode_sorting_criteria = category
        self.refresh_screen()

    def change_difficulty(self, difficulty):
        self.active_difficulty_mode = difficulty
        self.refresh_screen()

    def refresh_screen(self):
        self.list_of_ids = []
        self.list_of_user_data = []
        self.all_user_data = []
        self.canvas2.delete('all')
        self.get_user_ids(self.active_difficulty_mode, self.game_mode_sorting_criteria)

        if self.line_graph:
            self.line_graph.delete_line_graph()
            self.y_value_label.destroy()
            self.x_axis_label.destroy()
        if self.name_plate:
            self.name_plate.destroy()
            self.name_plate = None

        if self.donut_graph:
            self.donut_graph.delete_graph()

        if self.game_mode_sorting_criteria == 'time':
            sorted_values = self.sort_based_on_time_or_inaccuracy_points(self.list_of_user_data, self.list_of_ids)
            print('answer', sorted_values)

        elif self.game_mode_sorting_criteria == 'inaccuracy_points':
            sorted_values = self.sort_based_on_time_or_inaccuracy_points(self.list_of_user_data, self.list_of_ids)
            print('answer', sorted_values)

        elif self.game_mode_sorting_criteria == 'points':
            sorted_values = self.sort_based_on_points(self.list_of_user_data, self.list_of_ids)
            print('answer', sorted_values)

        self.list_of_ids = []
        for i in range(len(sorted_values[1])):
            self.list_of_ids.append(sorted_values[1][i])

        self.process_user_summary()
        self.top_10_side()
        self.your_personal_best()

    def get_time_stamps(self, place):
        # Sample data points (x, y)
        if place > len(self.all_user_data) - 1:
            return
        personal_best_id = self.all_user_data[place][2][4]
        print(personal_best_id)

        total_time = self.get_total_time(personal_best_id)
        total_time = total_time[0]
        print(total_time)

        cur = db.cursor(buffered=True)
        query2 = """
          SELECT time_taken, points,inaccuracy_points
          FROM time_stamps
          WHERE p_b_id = %s
          """
        cur.execute(query2, (personal_best_id,))
        result2 = cur.fetchall()
        cur.close()

        print('results:')
        print(result2)

        data_points = [(0, 0)]
        for i in range(len(result2) - 1):
            if result2[i][0] % 10 == 0:
                t = total_time - result2[i][0]
            if self.y_axis_value == 'points':
                data_tuple = (t, result2[i][1])

            else:
                data_tuple = (t, result2[i][2])
            data_points.append(data_tuple)
            print(data_tuple)
        if self.y_axis_value == 'points':
            data_tuple = (self.all_user_data[place][2][0], self.all_user_data[place][2][2])
        else:
            data_tuple = (self.all_user_data[place][2][0], self.all_user_data[place][2][1])

        print(data_tuple)
        if data_tuple[0] not in data_points:
            data_points.append(data_tuple)
        data_points.sort(key=lambda x: x[0])
        print(data_points)
        self.draw_graphs(data_points, place)

    def draw_graphs(self, data_points, place):
        self.create_label('sort by:', 1750, 130, 15, WHITE)
        self.create_button('points', 1750, 160, lambda: self.change_y_value('points', place))
        self.create_button('inaccuracy points', 1750, 190, lambda: self.change_y_value('inaccuracy points', place))

        self.line_graph = LineGraphApp(self.leaderboard_window, data_points, self.y_axis_value)
        self.donut_graph = Donut(self.leaderboard_window, [self.all_user_data[place][2][1],
                                                           self.all_user_data[place][2][2]])

        if self.name_plate is not None:
            self.name_plate.destroy()

        if self.y_value_label is not None:
            self.y_value_label.destroy()
            self.y_value_label = None
        self.x_axis_label = Label(self.leaderboard_window, text='time', bg=BLACK, fg=WHITE,
                                  font=(FONT_NAME, 20, 'bold'))
        self.x_axis_label.place(x=1300, y=500)

        self.name_plate = Label(self.leaderboard_window, text=f"{self.all_user_data[place][1]}'s gameplay performance",
                                bg=BLACK, fg=WHITE,
                                font=(FONT_NAME, 30, 'bold'))
        self.name_plate.place(x=960, y=130)

        if self.y_axis_value == 'points':

            self.y_value_label = Label(self.leaderboard_window, text=self.y_axis_value, bg=BLACK, fg=WHITE,
                                       wraplength=1,
                                       font=(FONT_NAME, 20, 'bold'))
            self.y_value_label.place(x=1130, y=270)

        else:
            self.y_value_label = Label(self.leaderboard_window, text='inaccuracy \npoints', bg=BLACK, fg=WHITE,
                                       wraplength=1,
                                       font=(FONT_NAME, 10, 'bold'))
            self.y_value_label.place(x=1130, y=230)

    def change_y_value(self, variable, place):
        self.y_axis_value = variable
        self.get_time_stamps(place)

    def get_total_time(self, personal_best_id):
        cur = db.cursor(buffered=True)
        query2 = """
          SELECT total_time
          FROM personal_best
          WHERE p_b_id = %s
          """
        cur.execute(query2, (personal_best_id,))
        result = cur.fetchall()
        cur.close()
        return result[0]


class LineGraphApp:
    def __init__(self, root, data, type):
        self.root = root
        self.root.title("Line Graph")

        self.type = type

        self.canvas = Canvas(root, width=600, height=300, bg=BLACK, highlightthickness=0)
        self.canvas.place(x=1150, y=245)

        self.data = data

        self.draw_line_graph()

    def draw_line_graph(self):

        if self.type == 'points':
            x_scale = 4
            y_scale = 0.5
            x_offset = 20
            y_offset = 250
        else:
            x_scale = 4
            y_scale = 6
            x_offset = 30
            y_offset = 250

        # Draw x and y axes
        self.canvas.create_line(x_offset, y_offset, x_offset + 360, y_offset, width=2, fill='WHITE')
        self.canvas.create_line(x_offset, y_offset, x_offset, y_offset - 250, width=2, fill='WHITE')

        # Draw data points and lines
        for i in range(len(self.data) - 1):
            x1, y1 = self.data[i]
            x2, y2 = self.data[i + 1]
            x1_scaled, y1_scaled = x1 * x_scale + x_offset, y_offset - y1 * y_scale
            x2_scaled, y2_scaled = x2 * x_scale + x_offset, y_offset - y2 * y_scale
            self.canvas.create_oval(x1_scaled - 3, y1_scaled - 3, x1_scaled + 3, y1_scaled + 3, fill=GREEN)
            self.canvas.create_line(x1_scaled, y1_scaled, x2_scaled, y2_scaled, fill=GREEN, width=3)

    def delete_line_graph(self):
        self.canvas.delete('all')


class Donut:
    def __init__(self, root, data):
        self.root = root
        self.root.title("Line Graph")

        fig = matplotlib.figure.Figure(figsize=(5, 5))
        fig.patch.set_facecolor('black')

        ax = fig.add_subplot(111)
        ax.set_facecolor('black')

        wedges, texts = ax.pie(data, textprops={'color': 'white'})

        labels = [f'inaccuracy points: {data[0]}', f'points: {data[1]}']
        ax.legend(labels, loc="best", fontsize="small", labelcolor="white", frameon=False)

        circle = matplotlib.patches.Circle((0, 0), 0.7, color='black')
        ax.add_artist(circle)

        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.get_tk_widget().place(x=1100, y=500)

        self.canvas.draw()

    def delete_graph(self):
        self.canvas.get_tk_widget().delete('all')
        self.canvas.get_tk_widget().create_rectangle(0, 0, 1200, 1200, fill=BLACK)
