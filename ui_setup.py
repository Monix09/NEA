# import modules

import tkinter
from abc import abstractmethod

from tkinter import *

from player import check_if_solution_is_found

import pymysql.cursors

import mysql.connector

import time

import random

import smtplib

from tkinter import Tk, Frame, Button

from MazeGenerator import MazeGenerator

global g_username

global g_password

global game_ended_s  # success

global game_ended_f  # fail

global no_of_times_time_incremented

global points_less_than_zero

no_of_times_time_incremented = 0

game_ended_s = None

game_ended_f = None

points_less_than_zero = None

# connecting to the database


db = mysql.connector.connect(host="localhost", user="root", passwd="Bella72006!", port="3306",

                             database="maze_of_madness_data_base")
my_cur = db.cursor()

remaining_time = 0

remaining_milliseconds = 0

EASY_MIN = 0.5

MED_MIN = 2

HARD_MIN = 5

MADNESS_MIN = 7

EASY_TIME_STAMPS = [10, 20, 30]

MED_TIME_STAMPS = [40, 80, 120]

HARD_TIME_STAMPS = [100, 200, 300]

MADNESS_TIME_STAMPS = [140, 280, 420]

P_B_CATEGORIES = ['time', 'accuracy', 'points']

BLACK = "#000000"

WHITE = "#FFFFFF"

GREEN = "#55FF55"

FONT_NAME = "Courier"

INSTRUCTIONS = "•Use the ⬆,⬇,⬅,➡ buttons to move through the maze" \
 \
               "\n•reach the exit as quick as possible to gain points" \
 \
               "\n•retracing your steps will result in a deduction of points" \
 \
               "\n•falling into a trap the game will send you back to the starting position " \
 \
               "\n•game is over when you reach the exit or if the timer runs out"


class GamePlay_ui(Tk):

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        self.total_points = None
        self.username = None
        self.fetch_user_info()

        #   creating screen + widgets

        self.title('Main Menu')

        Button(self, text='end game', highlightthickness=0, command=self.destroy).place(x=0, y=0)

        self.config(padx=300, pady=300, bg=BLACK)

        Label(self, text=f'total points:{self.total_points}', bg=BLACK, fg=GREEN, font=(FONT_NAME, 20, 'bold')).grid(
            row=0, column=1)
        #   username label

        Label(self, text=f'welcome back user: {self.username}', bg=BLACK, fg=GREEN, font=(FONT_NAME, 40, 'bold')).grid(

            row=1, column=0)

        #   click to play button

        Button(self, text='Click To Play', width=70, height=2, highlightthickness=0,

               command=self.Select_difficulty).grid(row=2, column=0, pady=10)

        #   how to play button

        button1 = Button(self, text='How To Play', highlightthickness=0, width=70, height=2, command=self.How_to_play)

        button1.grid(row=3, column=0, pady=10)

        # Leader Board Button

        button3 = Button(self, text='Leader Board', highlightthickness=0, width=70, height=2,
                         command=self.open_leaderboard)

        button3.grid(row=4, column=0, pady=10)

    def open_leaderboard(self):
        from leaderboard import Leaderboard
        leaderboard = Leaderboard(self.get_user_id())

    def get_user_id(self):
        return self.user_id

    def fetch_user_info(self):  # fetches user info from database

        print('user id:', self.user_id)
        sql = "select username , total_points from users where user_id = %s"
        my_cur.execute(sql, self.user_id)
        result = my_cur.fetchall()
        self.username = result[0][0]
        self.total_points = result[0][1]

    class Select_difficulty(tkinter.Toplevel):

        def __init__(self):
            super().__init__()
            self.list_of_game_mode_stars = []
            self.list_of_texts = []
            self.madness_accessibility = None
            self.hard_accessibility = None
            self.medium_accessibility = None
            global app
            self.user_id = app.get_user_id()
            self.get_user_accessibility()

            self.title("Select_difficulty")

            self.config(padx=300, pady=300, bg=BLACK)

            Label(self, text='select difficulty:', bg=BLACK, fg=GREEN, font=(FONT_NAME, 40, 'bold')).grid(

                row=0, column=0)

            easy = Button(self, text='easy', command=self.start_easy_gameplay, width=70, height=2)

            easy.grid(row=1, column=0, pady=10)

            Label(self, text=self.list_of_texts[0], bg=BLACK, fg=GREEN, font=(FONT_NAME, 35)).grid(row=1, column=1)
            Label(self, text=self.list_of_texts[1], bg=BLACK, fg=GREEN, font=(FONT_NAME, 35)).grid(row=2, column=1)
            Label(self, text=self.list_of_texts[2], bg=BLACK, fg=GREEN, font=(FONT_NAME, 35)).grid(row=3, column=1)
            Label(self, text=self.list_of_texts[3], bg=BLACK, fg=GREEN, font=(FONT_NAME, 35)).grid(row=4, column=1)

            medium = Button(self, text='medium', command=self.start_medium_gameplay, width=70, height=2)

            medium.grid(row=2, column=0, pady=10)

            hard = Button(self, text='hard', command=self.start_hard_gameplay, width=70, height=2)

            hard.grid(row=3, column=0, pady=10)

            madness = Button(self, text='madness', command=self.start_madness_gameplay, width=70, height=2)

            madness.grid(row=4, column=0, pady=10)

        def get_user_accessibility(self):
            print('user id:', self.user_id)
            sql = "select medium_accessibility, hard_accessibility, madness_accessibility from users where user_id = %s"
            my_cur.execute(sql, self.user_id)
            result = my_cur.fetchall()
            self.medium_accessibility = result[0][0]
            self.hard_accessibility = result[0][1]
            self.madness_accessibility = result[0][2]

            game_modes = ['medium', 'hard', 'madness']
            self.get_stars('easy')
            print('len of game modes:', len(game_modes))
            for i in range(len(game_modes)):
                print(self.list_of_texts)
                print(i)
                print(result[0][i])
                print('for loop', game_modes[i])
                if result[0][i] == 1:
                    print('meathod')
                    self.get_stars(game_modes[i])
                elif result[0][i] == 0:
                    print('not')
                    self.list_of_texts.append('🔒')

            print(self.list_of_game_mode_stars)
            print(self.list_of_texts)

        def get_stars(self, difficulty):
            print('difficulty:', difficulty)
            # Define the SQL query to get max stars for the specific difficulty
            query = """
            SELECT MAX(stars_earned) AS max_stars
            FROM personal_best
            WHERE user_id = %s
            AND difficulty = %s;
            """

            # Execute the query with user_id and difficulty as parameters
            my_cur.execute(query, (self.user_id[0], difficulty))

            # Fetch the result
            result = my_cur.fetchone()

            if result[0] == 1:
                self.list_of_texts.append('★☆☆')

            elif result[0] == 2:
                self.list_of_texts.append('★★☆')

            elif result[0] == 3:
                self.list_of_texts.append('★★★')
            else:
                self.list_of_texts.append('☆☆☆')

        def start_easy_gameplay(self):
            global app
            global easy
            # app.destroy()

            easy = Easy()

            # easy.mainloop()

        def start_medium_gameplay(self):
            global app
            if self.list_of_texts[1] == '🔒':
                return
            medium = Medium()

        def start_hard_gameplay(self):
            global app

            if self.list_of_texts[2] == '🔒':
                return
            hard = Hard()

        def start_madness_gameplay(self):
            global app

            # app.destroy()
            if self.list_of_texts[3] == '🔒':
                return
            madness = Madness()

    class How_to_play(tkinter.Toplevel):

        def __init__(self):
            super().__init__()

            self.title("How To Play")

            self.config(padx=50, pady=50, bg=BLACK)

            Label(self, text='Game Instructions:', bg=BLACK, fg=GREEN, font=(FONT_NAME, 30, 'bold')).grid(row=0,

                                                                                                          column=1,

                                                                                                          pady=(0, 20))

            Label(self, text=INSTRUCTIONS, bg=BLACK, fg=WHITE, font=(FONT_NAME, 20)).grid(row=1, column=1)

            # Back Button

            button3 = Button(self, text='Back', highlightthickness=0, command=self.destroy)

            button3.config(width=6, height=2)

            button3.grid(row=0, column=0, pady=20)

    class Game_ended:

        def __init__(self,
                     game_ended_success,
                     game_ended_fail,
                     point_checker,
                     minutes,
                     seconds,
                     milliseconds,
                     game_mode,
                     all_times_logged,
                     all_points_logged,
                     all_inaccuracy_points_logged):
            self.accessibility_result = None
            self.user_id = None
            self.total_time_done_in_s = 0
            self.minutes = minutes
            self.seconds = seconds
            self.milliseconds = milliseconds
            self.point_checker = point_checker
            self.game_mode = game_mode
            self.total_min_done_in = 0
            self.total_seconds_done_in = 0
            self.total_milli_sec_done_in = 0
            self.end_time = 0
            self.points_earned = 0
            self.inaccuracy_points = 0
            self.tt_points = 0
            self.number_of_stars = 0
            self.stars_earned = 0
            self.all_times_logged = all_times_logged
            self.all_points_logged = all_points_logged
            self.all_inaccuracy_points_logged = all_inaccuracy_points_logged
            global app
            self.user_id = app.get_user_id()

            if self.game_mode == 'easy':
                print('1')
                self.start_time = EASY_MIN * 60

            elif self.game_mode == 'medium':
                print('2')
                self.start_time = MED_MIN * 60

            elif self.game_mode == 'hard':
                print('3')
                self.start_time = HARD_MIN * 60

            elif self.game_mode == 'madness':
                print('4')
                self.start_time = MADNESS_MIN * 60
            print('start time:', self.start_time)

            self.game_ended_window = Tk()
            self.game_ended_window.config(bg=BLACK)
            self.game_ended_window.grid_rowconfigure(0, weight=1)
            self.game_ended_window.grid_rowconfigure(1, weight=1)
            self.game_ended_window.grid_rowconfigure(2, weight=1)
            self.game_ended_window.grid_rowconfigure(3, weight=1)
            self.game_ended_window.grid_rowconfigure(4, weight=1)
            self.game_ended_window.grid_columnconfigure(0, weight=1)
            self.game_ended_window.grid_columnconfigure(1, weight=1)
            self.game_ended_window.grid_columnconfigure(2, weight=1)
            self.game_ended_window.grid_columnconfigure(3, weight=1)
            self.game_ended_window.grid_columnconfigure(4, weight=1)
            self.game_ended_window.grid_columnconfigure(5, weight=1)
            self.game_ended_window.grid_columnconfigure(6, weight=1)

            self.game_ended_window.attributes("-fullscreen", True)

            self.success = game_ended_success
            self.fail = game_ended_fail

            self.time = time
            print(game_ended_s)
            print(game_ended_f)
            print(self.point_checker)
            if self.success is True and self.fail is False and self.point_checker is False:
                self.successful()
            else:
                if self.point_checker is True:
                    self.failed(1)
                else:
                    self.failed(2)

        def successful(self):
            self.calculate_time()
            self.calculate_total_points()
            self.calculate_stars_earned()
            self.check_if_personal_best()
            self.update_total_points()

            Label(self.game_ended_window, text="Level Complete!", font=(FONT_NAME, 60), bg=BLACK, fg=GREEN).place(x=650,
                                                                                                                  y=25)
            Label(self.game_ended_window,
                  text=f"time: {self.total_min_done_in:02d}:{self.total_seconds_done_in:02d}:{self.total_milli_sec_done_in}",
                  font=(FONT_NAME, 48), bg=BLACK, fg=GREEN).place(x=550, y=160)

            Label(self.game_ended_window, text="Level Complete!", font=(FONT_NAME, 60), bg=BLACK, fg=GREEN).place(x=650,
                                                                                                                  y=15)
            Label(self.game_ended_window,
                  text=f"time taken: {self.total_min_done_in:02d}:{self.total_seconds_done_in:02d}:{self.total_milli_sec_done_in}",
                  font=(FONT_NAME, 48), bg=BLACK, fg=GREEN).place(x=550, y=160)

            if self.number_of_stars == 1:
                print('1')
                Label(self.game_ended_window, text='★☆☆', font=(FONT_NAME, 48),
                      bg=BLACK,
                      fg=WHITE, ).place(x=850, y=500)

            elif self.number_of_stars == 2:
                print('2')
                Label(self.game_ended_window, text='★★☆', font=(FONT_NAME, 48),
                      bg=BLACK,
                      fg=WHITE, ).place(x=850, y=500)

            elif self.number_of_stars == 3:
                print('3')
                Label(self.game_ended_window, text='★★★', font=(FONT_NAME, 48),
                      bg=BLACK,
                      fg=WHITE, ).place(x=850, y=500)
                self.adjust_accessibility_by_game_mode()
            else:
                print('0')
                Label(self.game_ended_window, text='☆☆☆', font=(FONT_NAME, 48),
                      bg=BLACK,
                      fg=WHITE, ).place(x=850, y=500)

            Label(self.game_ended_window,
                  text=f"total points= {self.points_earned}+{int(self.end_time - self.total_seconds_done_in)}= {int(self.tt_points)}",
                  font=(FONT_NAME, 48), bg=BLACK, fg=GREEN, ).place(x=550, y=250)

            Label(self.game_ended_window, text=f'inaccuracy points:{self.inaccuracy_points}', font=(FONT_NAME, 48),
                  bg=BLACK,
                  fg=GREEN, ).place(x=550, y=340)

            Button(self.game_ended_window, text="play again", command=refresh_gameplay, width=70, height=2).place(x=700,
                                                                                                                  y=430)

        def update_total_points(self):
            sql = "select total_points from users where user_id = %s"
            my_cur.execute(sql, self.user_id)
            result = my_cur.fetchall()
            total_points = result[0][0]

            total_points += self.tt_points

            sql_update = """UPDATE users 
                            SET total_points = %s 
                            WHERE user_id = %s"""

            values = (total_points, self.user_id[0])
            my_cur.execute(sql_update, values)

        def failed(self, mode):
            button = Button(self.game_ended_window, text="play again", command=refresh_gameplay, width=70, height=2)
            button.place(x=700, y=250)
            Label(self.game_ended_window, text="Game Over...", font=(FONT_NAME, 60), bg=BLACK, fg=GREEN, ).place(x=700,
                                                                                                                 y=15)
            if mode == 1:
                Label(self.game_ended_window, text="Be careful not to let your score drop below zero!",
                      font=(FONT_NAME, 35), bg=BLACK, fg="red", ).place(x=300, y=160)
            else:
                Label(self.game_ended_window, text="Make sure you don't run out of time!",
                      font=(FONT_NAME, 35), bg=BLACK, fg="red", ).place(x=530, y=160)

        def calculate_time(self):

            print('time incremented:')
            print(no_of_times_time_incremented)
            self.end_time = self.start_time + (10 * no_of_times_time_incremented)

            self.total_seconds_done_in = int(
                self.end_time - (self.minutes * 60 + self.seconds))

            self.total_milli_sec_done_in = 10 - self.milliseconds

            if self.total_seconds_done_in >= 60:
                self.total_min_done_in = self.total_seconds_done_in // 60
                self.total_seconds_done_in = self.total_seconds_done_in % 60

            print(
                f"Minutes: {self.total_min_done_in}, Seconds: {self.total_seconds_done_in}, Milliseconds: {self.total_milli_sec_done_in}")

        def calculate_total_points(self):
            from player import get_point_counter
            self.points_earned = get_point_counter()

            self.tt_points = self.points_earned + (self.end_time - self.total_seconds_done_in)

        def get_user_accessibility(self):
            sql1 = """
            SELECT medium_accessibility, hard_accessibility, madness_accessibility 
            FROM users 
            WHERE user_id = %s
            """
            print('user id:', self.user_id)
            my_cur.execute(sql1, self.user_id)
            self.accessibility_result = my_cur.fetchall()
            print('result1', self.accessibility_result)

        def adjust_accessibility_by_game_mode(self):
            self.get_user_accessibility()
            if self.game_mode != 'madness':
                if self.game_mode == 'easy' and self.accessibility_result[0][0] == 0:
                    self.change_user_accessibility([1, 0, 0])
                elif self.game_mode == 'medium' and self.accessibility_result[0][1] == 0:
                    self.change_user_accessibility([1, 1, 0])
                elif self.game_mode == 'hard' and self.accessibility_result[0][2] == 0:
                    self.change_user_accessibility([1, 1, 1])

        def change_user_accessibility(self, game_modes_to_change):
            sql_update = """
                UPDATE users 
                SET medium_accessibility = %s, 
                    hard_accessibility = %s, 
                    madness_accessibility = %s
                WHERE user_id = %s
            """
            values = (game_modes_to_change[0], game_modes_to_change[1], game_modes_to_change[2], self.user_id[0])
            print('values:', values)
            my_cur.execute(sql_update, values)

            db.commit()

        def check_if_personal_best(self):

            sql2 = "SELECT * FROM personal_best WHERE user_id = %s AND difficulty = %s"

            my_cur.execute(sql2, (self.user_id[0], self.game_mode.upper()))

            personal_bests_results = my_cur.fetchall()

            print('Personal Bests Results:', personal_bests_results)

            if personal_bests_results:  # if there is a personal best under that user id - check if it has been beaten
                for i in range(len(personal_bests_results)):
                    self.check_if_personal_best_is_beaten('time')
                    self.check_if_personal_best_is_beaten('points')
                    self.check_if_personal_best_is_beaten('inaccuracy_points')
            else:  # if there is no personal bests under that user id - add this score under all categories
                self.add_personal_best_record('time')
                self.add_personal_best_record('inaccuracy_points')
                self.add_personal_best_record('points')

        def add_personal_best_record(self, category):
            sql_get_last_id = "SELECT MAX(p_b_id) FROM personal_best"

            my_cur.execute(sql_get_last_id)

            personal_best_id = my_cur.fetchone()
            personal_best_id = personal_best_id[0]
            personal_best_id += 1
            sql_insert = """INSERT INTO personal_best (p_b_id, user_id, category, points, time_taken, inaccuracy_points, 
            difficulty, stars_earned, total_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (
                personal_best_id, self.user_id[0], category, self.tt_points, self.total_time_done_in_s,
                self.inaccuracy_points, self.game_mode, self.number_of_stars, int(self.end_time))

            print('values:', values)
            my_cur.execute(sql_insert, values)

            db.commit()

            print(f"Successfully inserted record into personal_best for user_id {self.user_id}")
            self.update_and_add_time_stamps(personal_best_id)

        def remove_existing_time_stamps(self, personal_best_id):
            print('personal best id:', personal_best_id)
            sql_delete = """
            DELETE FROM time_stamps 
            WHERE p_b_id = %s
            """
            values = (personal_best_id,)
            my_cur.execute(sql_delete, values)

            db.commit()

            if my_cur.rowcount > 0:
                print(f"Successfully deleted record for personal bests {personal_best_id}")

        def update_and_add_time_stamps(self, personal_best_id):
            # self.get_user_accessibility_and_points()
            print('final data:')
            if self.total_time_done_in_s not in self.all_times_logged:  # basically appends final values before user won
                self.all_times_logged.append(self.total_time_done_in_s)
                self.all_points_logged.append(self.tt_points)
                self.all_inaccuracy_points_logged.append(self.inaccuracy_points)
            print(self.all_times_logged)
            print(self.all_points_logged)
            print(self.all_inaccuracy_points_logged)

            for i in range(len(self.all_times_logged)):
                sql_get_last_id = "SELECT MAX(t_s_id) FROM time_stamps"
                my_cur.execute(sql_get_last_id)
                time_stamp_id = my_cur.fetchone()
                time_stamp_id = time_stamp_id[0]
                time_stamp_id += 1
                sql_insert = """INSERT INTO time_stamps (t_s_id, p_b_id, time_taken, points, 
                inaccuracy_points) VALUES (%s, %s, %s, %s, %s)"""

                values = (
                    time_stamp_id, personal_best_id, self.all_times_logged[i],
                    self.all_points_logged[i],
                    self.all_inaccuracy_points_logged[i])

                print('values:', values)
                my_cur.execute(sql_insert, values)

                db.commit()

                print(f"Successfully inserted record into personal_best for user_id {self.user_id}")

        def remove_personal_best_record(self, category, personal_best_id):
            self.remove_existing_time_stamps(personal_best_id)
            print('personal best id:', personal_best_id)
            print('category:', category)

            sql_delete = """
            DELETE FROM personal_best 
            WHERE user_id = %s AND category = %s AND difficulty = %s
            """
            values = (self.user_id[0], category, self.game_mode)
            my_cur.execute(sql_delete, values)

            db.commit()

            if my_cur.rowcount > 0:
                print(f"Successfully deleted record for user_id {self.user_id} in category '{category}'")

        def check_if_personal_best_is_beaten(self, category):
            # SQL query to retrieve the user's current personal best record for the specified category
            sql_query = "SELECT * FROM personal_best WHERE user_id = %s AND category = %s AND difficulty =%s"
            print('time time time', self.total_time_done_in_s)
            # Execute the query, passing parameters as a tuple
            my_cur.execute(sql_query, (self.user_id[0], category, self.game_mode))
            personal_bests_results = my_cur.fetchall()
            print('if beaten results:', personal_bests_results)

            # Check if the personal best record exists for this user and category
            if not personal_bests_results:
                # No personal best record found, so just add the new record
                self.add_personal_best_record(category)
                return

            # Compare the current performance to the personal best and update if the new performance is better
            if category == 'time':
                if self.total_time_done_in_s < personal_bests_results[0][4]:  # Assuming column 4 is for 'time'
                    self.remove_existing_time_stamps(personal_bests_results[0][0])
                    self.remove_personal_best_record('time', personal_bests_results[0][0])
                    self.add_personal_best_record('time')

            elif category == 'points':
                if self.tt_points > personal_bests_results[0][3]:  # Assuming column 3 is for 'points'
                    self.remove_existing_time_stamps(personal_bests_results[0][0])
                    self.remove_personal_best_record('points', personal_bests_results[0][0])
                    self.add_personal_best_record('points')

            elif category == 'inaccuracy_points':

                if self.inaccuracy_points < personal_bests_results[0][5]:  # Assuming column 5 is for inaccuracy_points
                    self.remove_existing_time_stamps(personal_bests_results[0][0])
                    self.remove_personal_best_record('inaccuracy_points', personal_bests_results[0][0])
                    self.add_personal_best_record('inaccuracy_points')

        def calculate_stars_earned(self):

            from player import inaccuracy_points
            print('inaccuracy points:', inaccuracy_points)
            print('end time', self.end_time)
            self.inaccuracy_points = inaccuracy_points
            self.total_time_done_in_s = (self.total_min_done_in * 60) + self.total_seconds_done_in
            self.stars_earned = Star_rating(self.total_time_done_in_s, self.inaccuracy_points, self.tt_points)

            if self.game_mode == 'easy':
                self.stars_earned.calculate_star_rating(15, 10, 50)

            elif self.game_mode == 'medium':
                self.stars_earned.calculate_star_rating(45, 20, 75)

            elif self.game_mode == 'hard':
                self.stars_earned.calculate_star_rating(150, 35, 250)

            else:
                self.stars_earned.calculate_star_rating(300, 50, 350)

            self.number_of_stars = self.stars_earned.get_stars_earned()
            print('stars earned:', self.number_of_stars)


class Difficulty:
    def __init__(self,
                 rows,
                 cols,
                 player_size,
                 player_step_count,
                 no_of_trap_instances,
                 no_of_buff_instances,
                 starting_pos,
                 solution_pos,
                 game_mode):
        #   declaring and initialising attributes

        self.rows = rows
        self.cols = cols
        self.player_size = player_size
        self.player_step_count = player_step_count
        self.no_of_trap_instances = no_of_trap_instances
        self.no_of_buff_instances = no_of_buff_instances
        self.starting_pos = starting_pos
        self.solution_pos = solution_pos
        self.game_mode = game_mode
        global no_of_times_time_incremented
        no_of_times_time_incremented = 0

        # initialize window
        global window
        global current_pos
        global solution
        global maze_gen
        current_pos = 1
        solution = 0
        self.ui_set_up()

    def ui_set_up(self):
        self.window = Tk()

        self.window.attributes("-fullscreen", True)

        self.window.grid_rowconfigure(0, weight=1)

        self.window.grid_columnconfigure(0, weight=1)

        self.window.grid_columnconfigure(1, weight=5)

        # initialize components

        self.buttonFrame = Frame(self.window, bg="grey")

        self.buttonFrame.grid(row=0, column=0, sticky="NSEW")

        self.generate_maze()

        self.maze_gen.grid(row=0, column=1, sticky="NSEW")

        self.gen_maze_button.pack()

        self.window.mainloop()

    def generate_maze(self):
        global maze_gen
        self.maze_gen = MazeGenerator(self.window)
        self.gen_maze_button = Button(self.buttonFrame, text="Generate Maze",

                                      command=lambda: [

                                          self.destroy_button(),

                                          self.maze_gen.generateMaze(wall_color="white",
                                                                     pointer_color="white",
                                                                     rows=self.rows,
                                                                     cols=self.cols,
                                                                     player_size=self.player_size,
                                                                     player_step_count=self.player_step_count,
                                                                     no_of_trap_instances=self.no_of_trap_instances,
                                                                     no_of_buff_instances=self.no_of_buff_instances,
                                                                     game_mode=self.game_mode,
                                                                     starting_pos=self.starting_pos,
                                                                     solution_pos=self.solution_pos,
                                                                     window=self.window
                                                                     ),

                                          self.start_timer()])

    @abstractmethod
    def start_timer(self):
        pass

    def destroy_button(self):
        self.gen_maze_button.destroy()


class Easy(Difficulty):
    def __init__(self):
        super().__init__(rows=10,
                         cols=10,
                         player_size=55,
                         player_step_count=110,
                         no_of_trap_instances=1,
                         no_of_buff_instances=1,
                         starting_pos=(283, 23),
                         solution_pos=(9, 9),
                         game_mode='easy'
                         )

    def start_timer(self):
        global app
        timer = TimeAndScoreTracker(0, 30, self.window, app, self.maze_gen, 'easy', EASY_TIME_STAMPS)


class Medium(Difficulty):
    def __init__(self):
        super().__init__(rows=20,
                         cols=20,
                         player_size=25,
                         player_step_count=54,
                         no_of_trap_instances=1,
                         no_of_buff_instances=1,
                         starting_pos=(273, 18),
                         solution_pos=(19, 19),
                         game_mode='medium')

    def start_timer(self):
        global app
        timer = TimeAndScoreTracker(MED_MIN, 0, self.window, app, self.maze_gen, 'medium', MED_TIME_STAMPS)


class Hard(Difficulty):
    def __init__(self):
        super().__init__(rows=25,
                         cols=25,
                         player_size=20,
                         player_step_count=43,
                         no_of_trap_instances=1,
                         no_of_buff_instances=1,
                         starting_pos=(263, 12),
                         solution_pos=(24, 24),
                         game_mode='hard')

    def start_timer(self):
        global app
        timer = TimeAndScoreTracker(HARD_MIN, 0, self.window, app, self.maze_gen, 'hard', HARD_TIME_STAMPS)


class Madness(Difficulty):
    def __init__(self):
        super().__init__(rows=30,
                         cols=30,
                         player_size=23,
                         player_step_count=36,
                         no_of_trap_instances=1,
                         no_of_buff_instances=1,
                         starting_pos=(260, 10),
                         solution_pos=(29, 29),
                         game_mode='madness')

    def start_timer(self):
        global app
        timer = TimeAndScoreTracker(MADNESS_MIN, 0, self.window, app, self.maze_gen, 'madness',
                                    MADNESS_TIME_STAMPS)


class TimeAndScoreTracker:
    def __init__(self, minutes,
                 seconds,
                 window_object,
                 app_object,
                 maze_gen_object,
                 game_mode,
                 time_stamp_mode):

        self.time_stamp_mode = time_stamp_mode
        self.remaining_time = None
        self.milliseconds = 0
        self.remaining_milliseconds = None
        self.minutes = minutes
        self.seconds = seconds
        self.game_ended_s = None
        self.game_ended_f = None
        self.points_less_than_zero = None
        self.game_paused = False
        self.maze_gen = maze_gen_object
        self.no_of_times_time_incremented = 0
        self.window = window_object
        self.app = app_object
        self.game_mode = game_mode
        self.log_time_stamp = Log_time_stamp()

        self.timer_label = Label(self.window, text="00:00:00", font=("Helvetica", 48))
        self.timer_label.grid(row=0, column=0, sticky="NSEW")

        self.points_label = Label(self.window, text="points:0", font=("Helvetica", 48))
        self.points_label.place(x=0, y=100)

        self.inaccuracy_points_label = Label(self.window, text="inaccuracy points:0", font=("Helvetica", 30))
        self.inaccuracy_points_label.place(x=0, y=200)

        pause_button = Button(self.window, text="▐▐",
                              command=lambda: [pause_button.place_forget(), self.pause_gameplay()])
        pause_button.place(x=0, y=0)

        minutes = self.minutes
        seconds = self.seconds

        self.remaining_time = (minutes * 60) + seconds
        print('remaining time', self.remaining_time)
        self.remaining_milliseconds = self.milliseconds

        self.update_timer()

    # Function to update the timer
    def update_timer(self):

        from player import time_increase
        from player import get_point_counter
        from player import check_if_point_is_below_0
        from player import get_inaccuracy_points
        global check_if_solution_is_found
        global points_label
        global no_of_times_time_incremented

        self.minutes = 0
        self.seconds = 0
        self.milliseconds = 0
        if self.remaining_time > 0 and self.game_paused is False or self.remaining_milliseconds > 0 and self.game_paused is False:
            if self.remaining_milliseconds > 0:
                self.remaining_milliseconds -= 100
            else:
                self.remaining_milliseconds = 900
                self.remaining_time -= 1

            print('remaining time', self.remaining_time)

            if self.remaining_time in self.time_stamp_mode and self.remaining_time not in self.log_time_stamp.get_all_times_logged():
                print()
                print(self.time_stamp_mode)
                self.log_time_stamp.log_new_time(self.remaining_time)
                self.log_time_stamp.log_new_points(get_point_counter())
                self.log_time_stamp.log_new_inaccuracy_points(get_inaccuracy_points())

            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            milliseconds = self.remaining_milliseconds // 100

            if time_increase is True:
                no_of_times_time_incremented += 1
                seconds += 10
                self.remaining_time += 10
                from player import set_time_increase
                set_time_increase(False)
            try:
                self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}:{milliseconds}")
                self.points_label.config(text=f"points:{get_point_counter()}")
                self.inaccuracy_points_label.config(text=f"inaccuracy points:{get_inaccuracy_points()}")

            except tkinter.TclError:
                pass

            from player import check_if_solution_is_found
            if check_if_solution_is_found() is True:
                print('solution found')
                self.game_ended_s = True
                self.game_ended_f = False
                self.points_less_than_zero = False
                self.app.Game_ended(self.game_ended_s, self.game_ended_f, self.points_less_than_zero, minutes, seconds,
                                    milliseconds, self.game_mode, self.log_time_stamp.get_all_times_logged(),
                                    self.log_time_stamp.get_all_points_logged(),
                                    self.log_time_stamp.get_all_inaccuracy_points_logged())
                self.window.destroy()
                return
            elif check_if_point_is_below_0() is True:
                self.points_less_than_zero = True
                self.game_ended_s = True
                self.game_ended_f = False
                self.app.Game_ended(self.game_ended_s, self.game_ended_f, self.points_less_than_zero, minutes, seconds,
                                    milliseconds, self.game_mode, self.log_time_stamp.get_all_times_logged(),
                                    self.log_time_stamp.get_all_points_logged(),
                                    self.log_time_stamp.get_all_inaccuracy_points_logged())
                self.window.destroy()
                return

            elif minutes == 0 and seconds == 0 and milliseconds == 0:
                print('2')
                self.game_ended_s = False
                self.game_ended_f = True
                self.points_less_than_zero = False
                self.app.Game_ended(self.game_ended_s, self.game_ended_f, self.points_less_than_zero, minutes, seconds,
                                    milliseconds, self.game_mode, self.log_time_stamp.get_all_times_logged(),
                                    self.log_time_stamp.get_all_points_logged(),
                                    self.log_time_stamp.get_all_inaccuracy_points_logged())
                self.window.destroy()
                return

            self.window.after(100, self.update_timer)

        else:
            if self.game_paused is True:
                return
            else:
                print('3')
                game_ended_s = False
                game_ended_f = True
                points_less_than_zero = False
                self.app.Game_ended(game_ended_s, game_ended_f, points_less_than_zero, self.minutes, self.seconds,
                                    self.milliseconds, self.game_mode, self.log_time_stamp)
                return

    def pause_gameplay(self):
        self.maze_gen.game_is_paused()
        self.game_paused = True
        # timer_label.grid_forget()
        global canvas
        canvas = Canvas(self.window, width=550, height=820, bg="black")
        canvas.grid(row=0, column=1, sticky="NSEW")
        Label(canvas, text='Game Play Paused', bg="black", fg=GREEN, font=(FONT_NAME, 50, 'bold')).place(x=300, y=10)
        Button(canvas, text="play again", command=refresh_gameplay).place(x=450, y=300)
        Button(canvas, text="resume game play", command=self.resume).place(x=450, y=400)

    def resume(self):
        global canvas
        global window
        self.maze_gen.game_is_resumed()
        self.game_paused = False
        canvas.destroy()
        self.update_timer()
        pause_button = Button(self.window, text="▐▐",
                              command=lambda: [pause_button.place_forget(), self.pause_gameplay()])
        pause_button.place(x=0, y=0)


class Star_rating:
    def __init__(self,
                 time_taken,  # (in seconds)
                 inaccuracy,
                 points
                 ):
        # attributes set to private - star calculation process is kept secure from accidental or incorrect modification
        self.__time_taken = time_taken
        print('time:', time_taken)
        print('inaccuracy:', inaccuracy)
        print('points:', points)
        self.__inaccuracy = inaccuracy
        self.__points_earned = points
        self.__stars_earned = 0

    def calculate_star_rating(self, max_time_taken, max_inaccuracy, min_points):
        if self.__points_earned >= min_points:
            self.__stars_earned += 1
            print('points')

        if self.__time_taken <= max_time_taken:
            self.__stars_earned += 1
            print('time')

        if self.__inaccuracy <= max_inaccuracy:
            self.__stars_earned += 1
            print('inaccuracy')

    def get_stars_earned(self):
        return self.__stars_earned


class Log_time_stamp:  # used to create statistics in leaderboard
    def __init__(self):
        self.all_times_logged = []
        self.all_points_logged = []
        self.all_inaccuracy_points_logged = []

    def log_new_time(self, new_time):  # new_time will be logged in seconds
        self.all_times_logged.append(new_time)

    def log_new_points(self, new_points):
        self.all_points_logged.append(new_points)

    def log_new_inaccuracy_points(self, new_inaccuracy_points):
        self.all_inaccuracy_points_logged.append(new_inaccuracy_points)

    def get_all_times_logged(self):
        print('retrieving time...')
        print(self.all_times_logged)
        return self.all_times_logged

    def get_all_points_logged(self):
        print('points...')
        print(self.all_points_logged)
        return self.all_points_logged

    def get_all_inaccuracy_points_logged(self):
        print('retrieving inaccuracy points...')
        print(self.all_inaccuracy_points_logged)
        return self.all_inaccuracy_points_logged


def refresh_gameplay():
    global app
    if app:
        user_id = app.get_user_id()
        app.iconify()
        app.destroy()
    start_game_play(user_id)
    return app


def start_game_play(user_id):
    global app
    app = GamePlay_ui(user_id)
    app.mainloop()



