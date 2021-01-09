import tkinter as tk
from tkinter import *
from tkinter import ttk

from Views.shared_view import center_window


class UserTrainingsView(ttk.Frame):
    def __init__(self, master, shared_view, user):
        ttk.Frame.__init__(self, master)
        self.shared_view = shared_view
        self.user = user

        self._create_main_frame()

        self._create_trainings_list_container()
        self._fill_container_with_trainings()
        self._create_buttons()

    def _create_main_frame(self):
        self.frame_main = Frame(self.master)
        self.frame_main.pack(fill='both', padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

    def _create_trainings_list_container(self):
        self.frame_container = Frame(self.frame_main, relief="groove", bd=2)
        self.frame_container.pack(fill="both")

        self.canvas_trainings = Canvas(self.frame_container, bd=0, highlightthickness=0, height=200)
        self.scrollbar = Scrollbar(self.frame_container, orient=VERTICAL,
                                   command=self.canvas_trainings.yview)

        self.frame_scrollable = Frame(self.canvas_trainings)
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas_trainings.configure(
            scrollregion=self.canvas_trainings.bbox("all"))
                                   )

        self.canvas_trainings.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas_trainings.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_trainings.pack(side="left", fill="both", expand=1)
        self.scrollbar.pack(side="right", fill="y")

    def _fill_container_with_trainings(self):
        self.frame_trainings = Frame(self.frame_scrollable)
        self.frame_trainings.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_trainings, width=550)
        frame_sizer.pack()

        self.training_selected = tk.IntVar()
        training_id = 0
        for user_training in self.user['current_date_trainings']:
            frame_training = Frame(self.frame_trainings, relief="ridge", bd=2)
            frame_training.pack(fill="both", padx=self.shared_view.VERY_SMALL_PAD, pady=self.shared_view.VERY_SMALL_PAD)
            frame_training.focus()

            # Radio button
            frame_radio_button = Frame(frame_training)
            frame_radio_button.grid(row=0, column=0)

            radio_button = Radiobutton(frame_radio_button, variable=self.training_selected, value=training_id)
            radio_button.pack(fill="both", padx=(self.shared_view.SMALL_PAD, 0))

            # Name
            frame_name = Frame(frame_training, relief="ridge", bd=1)
            frame_name.grid(row=0, column=1, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_name = Label(frame_name, text=f"{user_training['training_name']}",
                               font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Duration
            frame_duration = Frame(frame_training, relief="ridge", bd=1)
            frame_duration.grid(row=0, column=2, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            duration_text = ""
            duration_text += f"{user_training['duration_hours']} h " if user_training['duration_hours'] > 0 else ""
            duration_text += f"{user_training['duration_minutes']} min" if user_training['duration_minutes'] > 0 else ""
            label_duration = Label(frame_duration, text=f"{duration_text}", font=self.shared_view.font_style_10)
            label_duration.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories burned
            frame_calories_burned = Frame(frame_training, relief="ridge", bd=1)
            frame_calories_burned.grid(row=0, column=3, padx=(0, self.shared_view.SMALL_PAD),
                                       pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories_burned)
            frame_center.pack()

            label_calories_burned = Label(frame_center, text=f"{user_training['burned_calories']} kcal",
                                          font=self.shared_view.font_style_10)
            label_calories_burned.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            training_id += 1

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_delete_training = tk.Button(self.frame_buttons, text="Usuń trening", width=self.shared_view.btn_size,
                                             font=self.shared_view.font_style_12)
        self.btn_delete_training.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD),
                                      pady=self.shared_view.NORMAL_PAD)

        self.btn_edit_training = tk.Button(self.frame_buttons, text="Edytuj trening", width=self.shared_view.btn_size,
                                           font=self.shared_view.font_style_12)
        self.btn_edit_training.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD),
                                    pady=self.shared_view.NORMAL_PAD)

        self.btn_add_training = tk.Button(self.frame_buttons, text="Dodaj trening", width=self.shared_view.btn_size,
                                          font=self.shared_view.font_style_12)
        self.btn_add_training.pack(side='left', pady=self.shared_view.NORMAL_PAD)

    def update_trainings(self):
        self.frame_trainings.pack_forget()
        self.frame_trainings.destroy()
        self._fill_container_with_trainings()


class DeleteTrainingWindow(tk.Toplevel):
    def __init__(self, master, shared_view, training):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.training = training
        self.withdraw()

        self.title('BeeFit - Usuń trening')
        self.resizable(False, False)

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        self.frame_label = ttk.Frame(self.frame_main)
        self.frame_label.pack()

        self.label = Label(self.frame_label,
                           text=f"Czy na pewno chcesz usunąć trening \n\'{self.training['training_name']}\'?",
                           font=self.shared_view.font_style_12)
        self.label.pack()

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Nie", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_delete_training = tk.Button(self.frame_buttons, text="Tak", width=self.shared_view.btn_size,
                                             font=self.shared_view.font_style_12)
        self.btn_delete_training.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class AddTrainingWindow(tk.Toplevel):
    def __init__(self, master, shared_view, training_types, default_radio=0, default_duration=30):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.training_types = training_types
        self.default_radio = default_radio
        self.default_duration = default_duration
        self.withdraw()

        self.title('BeeFit - Dodaj trening')
        self.resizable(False, False)

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_search_box()
        self._create_container()
        self._fill_container_with_training_types(self.training_types)
        self._create_duration_entry()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_search_box(self):
        self.label_frame_search = ttk.LabelFrame(self.frame_main, text="Wyszukaj trening:")
        self.label_frame_search.pack(fill=tk.BOTH, expand=1, pady=(0, self.shared_view.NORMAL_PAD))

        self.frame_search = ttk.Frame(self.label_frame_search)
        self.frame_search.pack(fill=tk.BOTH, padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

        self.entry_search = tk.Entry(self.frame_search, font=self.shared_view.font_style_12)
        self.entry_search.pack(fill=tk.BOTH, side='left', expand=1, padx=self.shared_view.NORMAL_PAD,
                               pady=self.shared_view.NORMAL_PAD)

        self.btn_search = tk.Button(self.frame_search, text="Szukaj", width=self.shared_view.btn_size,
                                    font=self.shared_view.font_style_12)
        self.btn_search.pack(side='right')

    def _create_container(self):
        self.frame_container = Frame(self.frame_main, relief="groove", bd=2)
        self.frame_container.pack(fill="both")

        self.canvas_training_types = Canvas(self.frame_container, bd=0, highlightthickness=0, height=230)
        self.scrollbar = Scrollbar(self.frame_container, orient=VERTICAL,
                                   command=self.canvas_training_types.yview)

        self.frame_scrollable = Frame(self.canvas_training_types)
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas_training_types.configure(
            scrollregion=self.canvas_training_types.bbox("all")))

        self.canvas_training_types.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas_training_types.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_training_types.pack(side="left", fill="both", expand=1)
        self.scrollbar.pack(side="right", fill="y")

    def _fill_container_with_training_types(self, training_types):
        self.frame_training_types = Frame(self.frame_scrollable)
        self.frame_training_types.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_training_types, width=377)
        frame_sizer.pack()

        self.training_type_selected = tk.IntVar(value=self.default_radio)
        index = 0
        for training_type in training_types:
            frame_training_type = Frame(self.frame_training_types, relief="ridge", bd=2)
            frame_training_type.pack(fill="both", padx=self.shared_view.VERY_SMALL_PAD,
                                     pady=self.shared_view.VERY_SMALL_PAD)
            frame_training_type.focus()

            # Radio button
            frame_radio_button = Frame(frame_training_type)
            frame_radio_button.grid(row=0, column=0)

            radio_button = Radiobutton(frame_radio_button, variable=self.training_type_selected, value=index)
            radio_button.pack(fill="both", padx=(self.shared_view.SMALL_PAD, 0))

            # Name
            frame_name = Frame(frame_training_type, relief="ridge", bd=1)
            frame_name.grid(row=0, column=1, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_name = Label(frame_name, text=f"{training_type['training_name']}",
                               font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories per min burned
            frame_calories_burned = Frame(frame_training_type, relief="ridge", bd=1)
            frame_calories_burned.grid(row=0, column=2, padx=(0, self.shared_view.SMALL_PAD),
                                       pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories_burned)
            frame_center.pack()

            label_calories_burned = Label(frame_center, text=f"{training_type['burned_calories_per_min']} kcal/min",
                                          font=self.shared_view.font_style_10)
            label_calories_burned.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            index += 1

    def _create_duration_entry(self):
        self.label_frame = ttk.LabelFrame(self.frame_main, text="Czas trwania treningu [min]:")
        self.label_frame.pack(fill=tk.BOTH, expand=1, pady=(self.shared_view.NORMAL_PAD, 0))

        self.frame_duration = ttk.Frame(self.label_frame)
        self.frame_duration.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.entry_duration = tk.Entry(self.frame_duration, font=self.shared_view.font_style_12)
        self.entry_duration.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_duration.insert(0, f'{self.default_duration}')

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_add_training = tk.Button(self.frame_buttons, text="Dodaj", width=self.shared_view.btn_size,
                                          font=self.shared_view.font_style_12)
        self.btn_add_training.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))

    def update_training_types_list(self, training_types):
        self.frame_training_types.pack_forget()
        self.frame_training_types.destroy()
        self._fill_container_with_training_types(training_types)
