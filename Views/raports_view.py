from tkinter import *
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class RaportsView(ttk.Frame):
    def __init__(self, master, shared_view, user):
        ttk.Frame.__init__(self, master)
        self.shared_view = shared_view
        self.user = user

        self._create_main_frame()

        self.tab_control = ttk.Notebook(self.frame_meal_plan_view)

        self.tab_weight_raport = ttk.Frame(self.tab_control)
        self.tab_calories_raport = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_weight_raport, text='Waga')
        self.tab_control.add(self.tab_calories_raport, text='Kalorie')

        self.tab_control.pack(expand=1, fill="both")

        month_labels, weight_values = self.get_weight_labels_and_values()
        self._create_weight_raport(month_labels, weight_values)

        week_labels, calories_consumed, calories_burned = self.get_calories_labels_and_values()
        self._create_calories_raport(week_labels, calories_consumed, calories_burned)

    def _create_main_frame(self):
        self.frame_meal_plan_view = Frame(self.master)
        self.frame_meal_plan_view.pack(fill='both', padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

    def _create_weight_raport(self, month_labels, weight_values):
        month_values = np.arange(1, len(month_labels) + 1)
        self.frame_weight_raport = Frame(self.tab_weight_raport)
        self.frame_weight_raport.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

        fig = Figure(figsize=(6, 4), dpi=90)

        a = fig.add_subplot(111)
        a.plot(month_values, weight_values, color="orange", linewidth=2)

        a.set_ylabel("Waga [kg]", fontsize=10)
        a.set_xlabel("Dni", fontsize=10)
        a.set_xticks(month_values[::3])
        a.set_xticklabels(month_labels[::3], rotation=30, fontsize=10)

        min_weight = min(weight_values)
        max_weight = max(weight_values)
        margin = (max_weight - min_weight) * 0.34
        if margin > 0.3:
            a.set_ylim(bottom=min_weight - margin, top=max_weight + margin)
        a.yaxis.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_weight_raport)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def _create_calories_raport(self, week_labels, calories_consumed, calories_burned):
        week_values = np.arange(1, len(week_labels) + 1)

        self.frame_calories_raport = Frame(self.tab_calories_raport)
        self.frame_calories_raport.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

        fig = Figure(figsize=(6, 4), dpi=90)
        a = fig.add_subplot(111)
        a.plot(week_values, calories_consumed, color="green", linewidth=2, markersize=6, marker='o', label="Spożyte")
        a.plot(week_values, calories_burned, color="darkred", linewidth=2, markersize=6, marker='o', label="Spalone")

        a.set_ylabel("Kalorie [kcal]", fontsize=10)
        a.set_xlabel("Dni", fontsize=10)
        a.legend()

        a.set_xticks(week_values)
        a.set_xticklabels(week_labels, rotation=30, fontsize=10)

        min_cal = min(min(calories_consumed), min(calories_burned))
        max_cal = max(max(calories_consumed), max(calories_burned))
        margin = (max_cal - min_cal) * 0.34
        if margin > 0.3:
            a.set_ylim(bottom=min_cal - margin, top=max_cal + margin)
        a.yaxis.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_calories_raport)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def update_raports(self):
        month_labels, weight_values = self.get_weight_labels_and_values()
        self.frame_weight_raport.pack_forget()
        self.frame_weight_raport.destroy()
        self._create_weight_raport(month_labels, weight_values)

        week_labels, calories_consumed, calories_burned = self.get_calories_labels_and_values()
        self.frame_calories_raport.pack_forget()
        self.frame_calories_raport.destroy()
        self._create_calories_raport(week_labels, calories_consumed, calories_burned)

    def get_weight_labels_and_values(self):
        month_labels = []
        weight_values = []
        for weight in self.user['current_month_weights']:
            month_labels.append(f"{weight['day']}/{weight['month']}")
            weight_values.append(weight['weight_value'])

        return month_labels, weight_values

    def get_calories_labels_and_values(self):
        week_labels = []
        calories_consumed = []
        calories_burned = []
        for cal_data in self.user['current_week_calories_data']:
            week_labels.append(f"{cal_data['day']}/{cal_data['month']}")
            calories_consumed.append(cal_data['calories_consumed'])
            calories_burned.append(cal_data['calories_burned'])

        return week_labels, calories_consumed, calories_burned
