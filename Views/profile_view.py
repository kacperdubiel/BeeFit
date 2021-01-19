import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

from Misc.config import IMG_PATH_PENCIL_ICON, IMG_PATH_PLUS_ICON, ACTIVITY_OPTIONS, GOAL_OPTIONS, GENDER_MALE, \
    GENDER_FEMALE
from Views.shared_view import center_window


class ProfileView(ttk.Frame):
    def __init__(self, master, shared_view, user):
        ttk.Frame.__init__(self, master)
        self.shared_view = shared_view
        self.user = user

        self._create_frames()

        # Icons
        self.image_pencil = Image.open(IMG_PATH_PENCIL_ICON).resize((self.shared_view.ICON_SIZE,
                                                                     self.shared_view.ICON_SIZE), Image.ANTIALIAS)
        self.icon_pencil = ImageTk.PhotoImage(self.image_pencil)

        self.image_plus = Image.open(IMG_PATH_PLUS_ICON).resize((self.shared_view.ICON_SIZE,
                                                                 self.shared_view.ICON_SIZE), Image.ANTIALIAS)
        self.icon_plus = ImageTk.PhotoImage(self.image_plus)

        self._create_left_block()
        self._create_right_block()

    def _create_frames(self):
        # Frames
        self.frame_profile_view = Frame(self.master)
        self.frame_profile_view.pack(fill='both')

        # Left frame
        self.label_frame_left_block = LabelFrame(self.frame_profile_view, text="Dane osobowe",
                                                 font=self.shared_view.font_style_10_bold, relief="raised", bd=2)
        self.label_frame_left_block.pack(fill='both', side="left", padx=self.shared_view.NORMAL_PAD,
                                         pady=self.shared_view.NORMAL_PAD)

        self.frame_left_block = Frame(self.label_frame_left_block)
        self.frame_left_block.pack(side="left", padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

        self.frame_sizer_left = Frame(self.frame_left_block, width=195)
        self.frame_sizer_left.pack()

        # Right frame
        self.label_frame_right_block = LabelFrame(self.frame_profile_view, text="Dieta",
                                                  font=self.shared_view.font_style_10_bold, relief="raised", bd=2,
                                                  width=350)
        self.label_frame_right_block.pack(fill='both', side="right", padx=(0, self.shared_view.NORMAL_PAD),
                                          pady=self.shared_view.NORMAL_PAD)
        self.label_frame_right_block.pack_propagate(0)

        self.frame_right_block = Frame(self.label_frame_right_block)
        self.frame_right_block.pack(side="left", padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

        self.frame_sizer_right = Frame(self.frame_right_block, width=340)
        self.frame_sizer_right.pack()

    def _create_left_block(self):
        # --- LEFT BLOCK ---
        # Gender
        self.frame_gender = ttk.Frame(self.frame_left_block)
        self.frame_gender.pack(fill='both', pady=(0, self.shared_view.SMALL_PAD))

        self.label_gender = Label(self.frame_gender, text=f"Płeć: ", font=self.shared_view.font_style_12_bold)
        self.label_gender.pack(side="left")

        self.label_gender_value = Label(self.frame_gender, text=f"{self.user['gender']}",
                                        font=self.shared_view.font_style_12)
        self.label_gender_value.pack(side="left", padx=(0, self.shared_view.VERY_SMALL_PAD))

        self.btn_set_gender = tk.Button(self.frame_gender, image=self.icon_pencil)
        self.btn_set_gender.pack(side="left")

        # Weight
        self.frame_weight = ttk.Frame(self.frame_left_block)
        self.frame_weight.pack(fill='both', pady=(0, self.shared_view.SMALL_PAD))

        self.label_weight = Label(self.frame_weight, text=f"Waga [kg]: ", font=self.shared_view.font_style_12_bold)
        self.label_weight.pack(side="left")

        self.label_weight_value = Label(self.frame_weight, text=f"{self.user['current_date_weight']['weight_value']}",
                                        font=self.shared_view.font_style_12)
        self.label_weight_value.pack(side="left", padx=(0, self.shared_view.VERY_SMALL_PAD))

        self.btn_set_weight = tk.Button(self.frame_weight, image=self.icon_plus)
        self.btn_set_weight.pack(side="left")

        # Height
        self.frame_height = ttk.Frame(self.frame_left_block)
        self.frame_height.pack(fill='both', pady=(0, self.shared_view.SMALL_PAD))

        self.label_height = Label(self.frame_height, text=f"Wzrost [cm]: ", font=self.shared_view.font_style_12_bold)
        self.label_height.pack(side="left")

        self.label_height_value = Label(self.frame_height, text=f"{self.user['height']}",
                                        font=self.shared_view.font_style_12)
        self.label_height_value.pack(side="left", padx=(0, self.shared_view.VERY_SMALL_PAD))

        self.btn_set_height = tk.Button(self.frame_height, image=self.icon_pencil)
        self.btn_set_height.pack(side="left")

        # Age
        self.frame_age = ttk.Frame(self.frame_left_block)
        self.frame_age.pack(fill='both')

        self.label_age = Label(self.frame_age, text=f"Wiek: ", font=self.shared_view.font_style_12_bold)
        self.label_age.pack(side="left")

        self.label_age_value = Label(self.frame_age, text=f"{self.user['age']}", font=self.shared_view.font_style_12)
        self.label_age_value.pack(side="left", padx=(0, self.shared_view.VERY_SMALL_PAD))

        self.btn_set_age = tk.Button(self.frame_age, image=self.icon_pencil)
        self.btn_set_age.pack(side="left")

    def _create_right_block(self):
        # --- RIGHT BLOCK ---
        # Physical activity
        self.frame_activity = ttk.Frame(self.frame_right_block)
        self.frame_activity.pack(fill='both', pady=(0, self.shared_view.SMALL_PAD))

        self.label_activity = Label(self.frame_activity, text=f"Aktywność fizyczna: ",
                                    font=self.shared_view.font_style_12_bold)
        self.label_activity.pack(side="left")

        activity_id = self.user['physical_activity']
        self.label_activity_value = Label(self.frame_activity, text=f"{ACTIVITY_OPTIONS[int(activity_id) - 1]}",
                                          font=self.shared_view.font_style_12)
        self.label_activity_value.pack(side="left", padx=(0, self.shared_view.VERY_SMALL_PAD))

        self.btn_set_activity = tk.Button(self.frame_activity, image=self.icon_pencil)
        self.btn_set_activity.pack(side="left")

        # Goal
        self.frame_goal = ttk.Frame(self.frame_right_block)
        self.frame_goal.pack(fill='both', pady=(0, self.shared_view.SMALL_PAD))

        self.label_goal = Label(self.frame_goal, text=f"Cel: ", font=self.shared_view.font_style_12_bold)
        self.label_goal.pack(side="left")

        goal_id = self.user['goal']
        self.label_goal_value = Label(self.frame_goal, text=f"{GOAL_OPTIONS[int(goal_id) - 1]}",
                                      font=self.shared_view.font_style_12)
        self.label_goal_value.pack(side="left", padx=(0, self.shared_view.VERY_SMALL_PAD))

        self.btn_set_goal = tk.Button(self.frame_goal, image=self.icon_pencil)
        self.btn_set_goal.pack(side="left")

        # GDA
        self.frame_gda = ttk.Frame(self.frame_right_block)
        self.frame_gda.pack(fill='both', pady=(0, self.shared_view.SMALL_PAD))

        self.label_gda = Label(self.frame_gda, text=f"Dzienne zapotrzebowanie: ",
                               font=self.shared_view.font_style_12_bold)
        self.label_gda.pack(side="left")

        self.label_gda_value = Label(self.frame_gda, text=f"{self.user['current_date_gda']['gda_value']} kcal",
                                     font=self.shared_view.font_style_12)
        self.label_gda_value.pack(side="left")

        # GDA Button
        self.frame_gda_button = ttk.Frame(self.frame_right_block)
        self.frame_gda_button.pack()

        self.btn_eval_gda = tk.Button(self.frame_gda_button, text="Wylicz ponownie",
                                      font=self.shared_view.font_style_12)
        self.btn_eval_gda.pack()

    def update_gender(self):
        self.label_gender_value.configure(text=f"{self.user['gender']}")

    def update_weight(self):
        self.label_weight_value.configure(text=f"{self.user['current_date_weight']['weight_value']}")

    def update_height(self):
        self.label_height_value.configure(text=f"{self.user['height']}")

    def update_age(self):
        self.label_age_value.configure(text=f"{self.user['age']}")

    def update_physical_activity(self):
        activity_id = self.user['physical_activity']
        self.label_activity_value.configure(text=f"{ACTIVITY_OPTIONS[int(activity_id) - 1]}")

    def update_goal(self):
        goal_id = self.user['goal']
        self.label_goal_value.configure(text=f"{GOAL_OPTIONS[int(goal_id) - 1]}")

    def update_gda(self):
        self.label_gda_value.configure(text=f"{self.user['current_date_gda']['gda_value']} kcal")


class SetGenderWindow(tk.Toplevel):
    def __init__(self, master, shared_view, current_gender):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.current_gender = current_gender
        self.withdraw()

        self.title('BeeFit - Ustaw płeć')
        self.resizable(False, False)

        self.frame_set_gender = ttk.Frame(self)
        self.frame_set_gender.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        # Gender radio buttons
        self.label_frame = ttk.LabelFrame(self.frame_set_gender, text="Wybierz płeć:")
        self.label_frame.pack(fill=tk.BOTH, expand=1)

        self.frame_gender = ttk.Frame(self.label_frame)
        self.frame_gender.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.gender_value = tk.StringVar(value=self.current_gender)
        self.gender_radio_btn1 = Radiobutton(self.frame_gender, text="Mężczyzna", variable=self.gender_value,
                                             value=GENDER_MALE, font=self.shared_view.font_style_12)
        self.gender_radio_btn1.pack(side='left')

        self.gender_radio_btn2 = Radiobutton(self.frame_gender, text="Kobieta", variable=self.gender_value,
                                             value=GENDER_FEMALE, font=self.shared_view.font_style_12)
        self.gender_radio_btn2.pack(side='left')

    def _create_buttons(self):
        self.btn_back = tk.Button(self.frame_set_gender, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_set_gender = tk.Button(self.frame_set_gender, text="Aktualizuj", width=self.shared_view.btn_size,
                                        font=self.shared_view.font_style_12)
        self.btn_set_gender.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class SetWeightWindow(tk.Toplevel):
    def __init__(self, master, shared_view, current_weight):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.current_weight = current_weight
        self.withdraw()

        self.title('BeeFit - Dodaj wagę')
        self.resizable(False, False)

        self.frame_set_weight = ttk.Frame(self)
        self.frame_set_weight.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        self.label_frame = ttk.LabelFrame(self.frame_set_weight, text="Podaj wagę:")
        self.label_frame.pack(fill=tk.BOTH, expand=1)

        self.frame_weight = ttk.Frame(self.label_frame)
        self.frame_weight.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.entry_weight = tk.Entry(self.frame_weight, font=self.shared_view.font_style_12)
        self.entry_weight.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_weight.insert(0, f'{self.current_weight}')

    def _create_buttons(self):
        self.btn_back = tk.Button(self.frame_set_weight, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_set_weight = tk.Button(self.frame_set_weight, text="Aktualizuj", width=self.shared_view.btn_size,
                                        font=self.shared_view.font_style_12)
        self.btn_set_weight.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class SetHeightWindow(tk.Toplevel):
    def __init__(self, master, shared_view, current_height):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.current_height = current_height
        self.withdraw()

        self.title('BeeFit - Ustaw wzrost')
        self.resizable(False, False)

        self.frame_set_height = ttk.Frame(self)
        self.frame_set_height.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        self.label_frame = ttk.LabelFrame(self.frame_set_height, text="Podaj wzrost:")
        self.label_frame.pack(fill=tk.BOTH, expand=1)

        self.frame_height = ttk.Frame(self.label_frame)
        self.frame_height.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.entry_height = tk.Entry(self.frame_height, font=self.shared_view.font_style_12)
        self.entry_height.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_height.insert(0, f'{self.current_height}')

    def _create_buttons(self):
        self.btn_back = tk.Button(self.frame_set_height, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_set_height = tk.Button(self.frame_set_height, text="Aktualizuj", width=self.shared_view.btn_size,
                                        font=self.shared_view.font_style_12)
        self.btn_set_height.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class SetAgeWindow(tk.Toplevel):
    def __init__(self, master, shared_view, current_age):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.current_age = current_age
        self.withdraw()

        self.title('BeeFit - Ustaw wiek')
        self.resizable(False, False)

        self.frame_set_age = ttk.Frame(self)
        self.frame_set_age.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        self.label_frame = ttk.LabelFrame(self.frame_set_age, text="Podaj wiek:")
        self.label_frame.pack(fill=tk.BOTH, expand=1)

        self.frame_age = ttk.Frame(self.label_frame)
        self.frame_age.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.entry_age = tk.Entry(self.frame_age, font=self.shared_view.font_style_12)
        self.entry_age.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_age.insert(0, f'{self.current_age}')

    def _create_buttons(self):
        self.btn_back = tk.Button(self.frame_set_age, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_set_age = tk.Button(self.frame_set_age, text="Aktualizuj", width=self.shared_view.btn_size,
                                     font=self.shared_view.font_style_12)
        self.btn_set_age.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class SetActivityWindow(tk.Toplevel):
    def __init__(self, master, shared_view, current_activity):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.current_activity = current_activity
        self.withdraw()

        self.title('BeeFit - Ustaw aktywność fizyczną')
        self.resizable(False, False)

        self.frame_set_activity = ttk.Frame(self)
        self.frame_set_activity.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        self.label_frame = ttk.LabelFrame(self.frame_set_activity, text="Wybierz aktywność fizyczną w ciągu dnia:")
        self.label_frame.pack(fill=tk.BOTH, expand=1)

        self.frame_activity = ttk.Frame(self.label_frame)
        self.frame_activity.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        activity_options_list = ACTIVITY_OPTIONS
        self.activity_value = tk.StringVar(value=activity_options_list[self.current_activity - 1])
        activity_option_menu = tk.OptionMenu(self.frame_activity, self.activity_value, *activity_options_list)
        activity_option_menu.config(font=self.shared_view.font_style_12)
        activity_option_menu.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD,
                                  pady=(self.shared_view.SMALL_PAD, self.shared_view.SMALL_PAD))

    def _create_buttons(self):
        self.btn_back = tk.Button(self.frame_set_activity, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_set_activity = tk.Button(self.frame_set_activity, text="Aktualizuj", width=self.shared_view.btn_size,
                                          font=self.shared_view.font_style_12)
        self.btn_set_activity.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class SetGoalWindow(tk.Toplevel):
    def __init__(self, master, shared_view, current_goal):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.current_goal = current_goal
        self.withdraw()

        self.title('BeeFit - Ustaw cel')
        self.resizable(False, False)

        self.frame_set_goal = ttk.Frame(self)
        self.frame_set_goal.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        self.label_frame = ttk.LabelFrame(self.frame_set_goal, text="Wybierz cel:")
        self.label_frame.pack(fill=tk.BOTH, expand=1)

        self.frame_goal = ttk.Frame(self.label_frame)
        self.frame_goal.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        goal_options_list = GOAL_OPTIONS
        self.goal_value = tk.StringVar(value=goal_options_list[self.current_goal - 1])
        goal_option_menu = tk.OptionMenu(self.frame_goal, self.goal_value, *goal_options_list)
        goal_option_menu.config(font=self.shared_view.font_style_12)
        goal_option_menu.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD,
                              pady=(self.shared_view.SMALL_PAD, self.shared_view.NORMAL_PAD))

    def _create_buttons(self):
        self.btn_back = tk.Button(self.frame_set_goal, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_set_goal = tk.Button(self.frame_set_goal, text="Aktualizuj", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_set_goal.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class EvaluateGDAWindow(tk.Toplevel):
    def __init__(self, master, shared_view):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.withdraw()

        self.title('BeeFit - Zapotrzebowanie kaloryczne')
        self.resizable(False, False)

        self.frame_eval_gda = ttk.Frame(self)
        self.frame_eval_gda.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        self.frame_label_gda = ttk.Frame(self.frame_eval_gda)
        self.frame_label_gda.pack()

        self.label_gda = Label(self.frame_label_gda,
                               text="Czy na pewno chcesz ponownie wyliczyć swoje \ndzienne zapotrzebowanie kaloryczne?",
                               font=self.shared_view.font_style_12)
        self.label_gda.pack()

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_eval_gda)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Nie", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_eval_gda = tk.Button(self.frame_buttons, text="Tak", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_eval_gda.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))
