import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk

from Misc.config import GI_RATING_OPTIONS
from Models.user_model import scale_image
from Views.shared_view import center_window


class MealPlanView(ttk.Frame):
    def __init__(self, master, shared_view, user):
        ttk.Frame.__init__(self, master)
        self.shared_view = shared_view
        self.user = user

        self._create_main_frame()

        self.tab_control = ttk.Notebook(self.frame_meal_plan_view)

        self.tab_consumed_products = ttk.Frame(self.tab_control)
        self.tab_consumed_dishes = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_consumed_products, text='Spożyte produkty')
        self.tab_control.add(self.tab_consumed_dishes, text='Spożyte dania')

        self.tab_control.pack(expand=1, fill="both")

        self._create_c_products_list_container()
        self._fill_container_with_c_products()
        self._create_consumed_products_buttons()

        self._create_c_dishes_list_container()
        self._fill_container_with_c_dishes()
        self._create_consumed_dishes_buttons()

    def _create_main_frame(self):
        self.frame_meal_plan_view = Frame(self.master)
        self.frame_meal_plan_view.pack(fill='both', padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

    def _create_c_products_list_container(self):
        # Consumed products tab
        self.frame_container_products = Frame(self.tab_consumed_products, relief="groove", bd=2)
        self.frame_container_products.pack(fill="both")

        self.canvas_products = Canvas(self.frame_container_products, bd=0, highlightthickness=0, height=200)
        self.scrollbar_products = Scrollbar(self.frame_container_products, orient=VERTICAL,
                                            command=self.canvas_products.yview)

        self.frame_scrollable = Frame(self.canvas_products)
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas_products.configure(
            scrollregion=self.canvas_products.bbox("all"))
                                   )

        self.canvas_products.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas_products.configure(yscrollcommand=self.scrollbar_products.set)

        self.canvas_products.pack(side="left", fill="both", expand=1)
        self.scrollbar_products.pack(side="right", fill="y")

    def _fill_container_with_c_products(self):
        self.frame_products = Frame(self.frame_scrollable)
        self.frame_products.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_products, width=550)
        frame_sizer.pack()

        self.prods_images = []
        self.prods_img_renders = []

        self.product_selected = tk.IntVar()
        c_prod_id = 0
        for c_prod in self.user['consumed_products']:
            frame_product = Frame(self.frame_products, relief="ridge", bd=2)
            frame_product.pack(fill="both", padx=self.shared_view.VERY_SMALL_PAD, pady=self.shared_view.VERY_SMALL_PAD)
            frame_product.focus()

            # Radio button
            frame_radio_button = Frame(frame_product)
            frame_radio_button.grid(row=0, column=0)

            product_radio_button = Radiobutton(frame_radio_button, variable=self.product_selected, value=c_prod_id)
            product_radio_button.pack(fill="both", padx=(self.shared_view.SMALL_PAD, 0))

            # Img
            frame_image = Frame(frame_product, relief="groove", bd=1)
            frame_image.grid(row=0, column=1, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            self.prods_images.append(c_prod['image'])
            img_width, img_height = scale_image(self.prods_images[c_prod_id], self.shared_view.LIST_IMG_SIZE)

            self.prods_images[c_prod_id] = self.prods_images[c_prod_id].resize((img_width, img_height))
            self.prods_img_renders.append(ImageTk.PhotoImage(self.prods_images[c_prod_id]))

            canvas_avatar = tk.Canvas(frame_image, width=self.shared_view.LIST_IMG_SIZE,
                                      height=self.shared_view.LIST_IMG_SIZE)
            canvas_avatar.create_image((self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       (self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       image=self.prods_img_renders[c_prod_id])
            canvas_avatar.pack(fill="both")

            # Name
            frame_name = Frame(frame_product, relief="ridge", bd=1)
            frame_name.grid(row=0, column=2, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_name = Label(frame_name, text=f"{c_prod['product_name']}", font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # GI rating
            frame_gi_rating = Frame(frame_product, relief="ridge", bd=1)
            frame_gi_rating.grid(row=0, column=3, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            gi_rating_index = c_prod['glycemic_index_rating']
            label_gi_rating = Label(frame_gi_rating, text=f"{GI_RATING_OPTIONS[gi_rating_index]}",
                                    font=self.shared_view.font_style_10)
            label_gi_rating.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Grammage
            frame_grammage = Frame(frame_product, relief="ridge", bd=1)
            frame_grammage.grid(row=0, column=4, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_grammage = Label(frame_grammage, text=f"{c_prod['product_grammage']} g",
                                   font=self.shared_view.font_style_10)
            label_grammage.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories
            frame_calories = Frame(frame_product, relief="ridge", bd=1)
            frame_calories.grid(row=0, column=5, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center, text=f"{c_prod['calories']} kcal", font=self.shared_view.font_style_10)
            label_calories.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            c_prod_id += 1

    def _create_consumed_products_buttons(self):
        # Consumed products buttons
        self.frame_buttons = ttk.Frame(self.tab_consumed_products)
        self.frame_buttons.pack()

        # Add button
        self.btn_delete_prod = tk.Button(self.frame_buttons, text="Usuń produkt", width=self.shared_view.btn_size,
                                         font=self.shared_view.font_style_12)
        self.btn_delete_prod.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=self.shared_view.NORMAL_PAD)

        self.btn_edit_prod = tk.Button(self.frame_buttons, text="Edytuj produkt", width=self.shared_view.btn_size,
                                       font=self.shared_view.font_style_12)
        self.btn_edit_prod.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=self.shared_view.NORMAL_PAD)

        self.btn_add_prod = tk.Button(self.frame_buttons, text="Dodaj produkt", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_add_prod.pack(side='left', pady=self.shared_view.NORMAL_PAD)

    def update_consumed_products(self):
        self.frame_products.pack_forget()
        self.frame_products.destroy()
        self._fill_container_with_c_products()

    def _create_c_dishes_list_container(self):
        # Consumed dishes tab
        self.frame_container_dishes = Frame(self.tab_consumed_dishes, relief="groove", bd=2)
        self.frame_container_dishes.pack(fill="both")

        self.canvas_dishes = Canvas(self.frame_container_dishes, bd=0, highlightthickness=0, height=200)
        self.scrollbar_dishes = Scrollbar(self.frame_container_dishes, orient=VERTICAL,
                                          command=self.canvas_dishes.yview)

        self.frame_scrollable_dishes = Frame(self.canvas_dishes)
        self.frame_scrollable_dishes.bind("<Configure>", lambda e: self.canvas_dishes.configure(
            scrollregion=self.canvas_dishes.bbox("all"))
                                          )

        self.canvas_dishes.create_window((0, 0), window=self.frame_scrollable_dishes, anchor="nw")
        self.canvas_dishes.configure(yscrollcommand=self.scrollbar_dishes.set)

        self.canvas_dishes.pack(side="left", fill="both", expand=1)
        self.scrollbar_dishes.pack(side="right", fill="y")

    def _fill_container_with_c_dishes(self):
        self.frame_dishes = Frame(self.frame_scrollable_dishes)
        self.frame_dishes.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_dishes, width=550)
        frame_sizer.pack()

        self.dishes_images = []
        self.dishes_img_renders = []

        self.dish_selected = tk.IntVar()
        c_dish_id = 0
        for c_dish in self.user['consumed_dishes']:
            frame_dish = Frame(self.frame_dishes, relief="ridge", bd=2)
            frame_dish.pack(fill="both", padx=self.shared_view.VERY_SMALL_PAD, pady=self.shared_view.VERY_SMALL_PAD)
            frame_dish.focus()

            # Radio button
            frame_radio_button = Frame(frame_dish)
            frame_radio_button.grid(row=0, column=0)

            dish_radio_button = Radiobutton(frame_radio_button, variable=self.dish_selected, value=c_dish_id)
            dish_radio_button.pack(fill="both", padx=(self.shared_view.SMALL_PAD, 0))

            # Img
            frame_image = Frame(frame_dish, relief="groove", bd=1)
            frame_image.grid(row=0, column=1, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            self.dishes_images.append(c_dish['image'])
            img_width, img_height = scale_image(self.dishes_images[c_dish_id], self.shared_view.LIST_IMG_SIZE)

            self.dishes_images[c_dish_id] = self.dishes_images[c_dish_id].resize((img_width, img_height))
            self.dishes_img_renders.append(ImageTk.PhotoImage(self.dishes_images[c_dish_id]))

            canvas_avatar = tk.Canvas(frame_image, width=self.shared_view.LIST_IMG_SIZE,
                                      height=self.shared_view.LIST_IMG_SIZE)
            canvas_avatar.create_image((self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       (self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       image=self.dishes_img_renders[c_dish_id])
            canvas_avatar.pack(fill="both")

            # Name
            frame_name = Frame(frame_dish, relief="ridge", bd=1)
            frame_name.grid(row=0, column=2, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_name = Label(frame_name, text=f"{c_dish['dish_name']}", font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # GI rating
            frame_gi_rating = Frame(frame_dish, relief="ridge", bd=1)
            frame_gi_rating.grid(row=0, column=3, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            gi_rating_index = c_dish['glycemic_index_rating']
            label_gi_rating = Label(frame_gi_rating, text=f"{GI_RATING_OPTIONS[gi_rating_index]}",
                                    font=self.shared_view.font_style_10)
            label_gi_rating.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Grammage
            frame_grammage = Frame(frame_dish, relief="ridge", bd=1)
            frame_grammage.grid(row=0, column=4, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_grammage = Label(frame_grammage, text=f"{c_dish['dish_grammage']} g",
                                   font=self.shared_view.font_style_10)
            label_grammage.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories
            frame_calories = Frame(frame_dish, relief="ridge", bd=1)
            frame_calories.grid(row=0, column=5, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center, text=f"{c_dish['calories']} kcal",
                                   font=self.shared_view.font_style_10)
            label_calories.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            c_dish_id += 1

    def _create_consumed_dishes_buttons(self):
        # Consumed dishes buttons
        self.frame_buttons = ttk.Frame(self.tab_consumed_dishes)
        self.frame_buttons.pack()

        # Add button
        self.btn_delete_dish = tk.Button(self.frame_buttons, text="Usuń danie", width=self.shared_view.btn_size,
                                         font=self.shared_view.font_style_12)
        self.btn_delete_dish.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=self.shared_view.NORMAL_PAD)

        self.btn_edit_dish = tk.Button(self.frame_buttons, text="Edytuj danie", width=self.shared_view.btn_size,
                                       font=self.shared_view.font_style_12)
        self.btn_edit_dish.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=self.shared_view.NORMAL_PAD)

        self.btn_add_dish = tk.Button(self.frame_buttons, text="Dodaj danie", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_add_dish.pack(side='left', pady=self.shared_view.NORMAL_PAD)

    def update_consumed_dishes(self):
        self.frame_dishes.pack_forget()
        self.frame_dishes.destroy()
        self._fill_container_with_c_dishes()


class DeleteConsumedProductWindow(tk.Toplevel):
    def __init__(self, master, shared_view, product):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.product = product
        self.withdraw()

        self.title('BeeFit - Usuń skonsumowany produkt')
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
                           text=f"Czy na pewno chcesz usunąć produkt \n\'{self.product['product_name']}\'?",
                           font=self.shared_view.font_style_12)
        self.label.pack()

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Nie", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_delete_prod = tk.Button(self.frame_buttons, text="Tak", width=self.shared_view.btn_size,
                                         font=self.shared_view.font_style_12)
        self.btn_delete_prod.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class AddConsumedProductWindow(tk.Toplevel):
    def __init__(self, master, shared_view, user_prods, user_prods_ids, default_radio=0, default_grammage=100):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.user_prods = user_prods
        self.user_prods_ids = user_prods_ids
        self.default_radio = default_radio
        self.default_grammage = default_grammage
        self.withdraw()

        self.title('BeeFit - Dodaj skonsumowany produkt')
        self.resizable(False, False)

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_search_box()
        self._create_container()
        self._fill_container_with_products(self.user_prods_ids)
        self._create_grammage_entry()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_search_box(self):
        self.label_frame_search = ttk.LabelFrame(self.frame_main, text="Wyszukaj produkt:")
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
        self.frame_container_products = Frame(self.frame_main, relief="groove", bd=2)
        self.frame_container_products.pack(fill="both")

        self.canvas_products = Canvas(self.frame_container_products, bd=0, highlightthickness=0, height=200)
        self.scrollbar_products = Scrollbar(self.frame_container_products, orient=VERTICAL,
                                            command=self.canvas_products.yview)

        self.frame_scrollable = Frame(self.canvas_products)
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas_products.configure(
            scrollregion=self.canvas_products.bbox("all")))

        self.canvas_products.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas_products.configure(yscrollcommand=self.scrollbar_products.set)

        self.canvas_products.pack(side="left", fill="both", expand=1)
        self.scrollbar_products.pack(side="right", fill="y")

        frame_sizer = Frame(self.frame_main, width=540)
        frame_sizer.pack()

    def _fill_container_with_products(self, products_ids):
        self.frame_products = Frame(self.frame_scrollable)
        self.frame_products.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_products, width=517)
        frame_sizer.pack()

        self.prods_images = []
        self.prods_img_renders = []

        self.product_selected = tk.IntVar(value=self.default_radio)
        index = 0
        for product_id in products_ids:
            frame_product = Frame(self.frame_products, relief="ridge", bd=2)
            frame_product.pack(fill="both", padx=self.shared_view.VERY_SMALL_PAD, pady=self.shared_view.VERY_SMALL_PAD)
            frame_product.focus()

            # Radio button
            frame_radio_button = Frame(frame_product)
            frame_radio_button.grid(row=0, column=0)

            product_radio_button = Radiobutton(frame_radio_button, variable=self.product_selected, value=index)
            product_radio_button.pack(fill="both", padx=(self.shared_view.SMALL_PAD, 0))

            # Img
            frame_image = Frame(frame_product, relief="groove", bd=1)
            frame_image.grid(row=0, column=1, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            self.prods_images.append(self.user_prods[f'{product_id}']['image'])
            img_width, img_height = scale_image(self.prods_images[index], self.shared_view.LIST_IMG_SIZE)

            self.prods_images[index] = self.prods_images[index].resize((img_width, img_height))
            self.prods_img_renders.append(ImageTk.PhotoImage(self.prods_images[index]))

            canvas_avatar = tk.Canvas(frame_image, width=self.shared_view.LIST_IMG_SIZE,
                                      height=self.shared_view.LIST_IMG_SIZE)
            canvas_avatar.create_image((self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       (self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       image=self.prods_img_renders[index])
            canvas_avatar.pack(fill="both")

            # Name
            frame_name = Frame(frame_product, relief="ridge", bd=1)
            frame_name.grid(row=0, column=2, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_name = Label(frame_name, text=f"{self.user_prods[f'{product_id}']['product_name']}",
                               font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # GI rating
            frame_gi_rating = Frame(frame_product, relief="ridge", bd=1)
            frame_gi_rating.grid(row=0, column=3, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            gi_rating_index = self.user_prods[f'{product_id}']['glycemic_index_rating']
            label_gi_rating = Label(frame_gi_rating, text=f"{GI_RATING_OPTIONS[gi_rating_index]}",
                                    font=self.shared_view.font_style_10)
            label_gi_rating.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories
            frame_calories = Frame(frame_product, relief="ridge", bd=1)
            frame_calories.grid(row=0, column=4, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center, text=f"{self.user_prods[f'{product_id}']['calories']} kcal/100g",
                                   font=self.shared_view.font_style_10)
            label_calories.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            index += 1

    def _create_grammage_entry(self):
        self.label_frame = ttk.LabelFrame(self.frame_main, text="Waga produktu [g]:")
        self.label_frame.pack(fill=tk.BOTH, expand=1, pady=(self.shared_view.NORMAL_PAD, 0))

        self.frame_grammage = ttk.Frame(self.label_frame)
        self.frame_grammage.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.entry_grammage = tk.Entry(self.frame_grammage, font=self.shared_view.font_style_12)
        self.entry_grammage.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_grammage.insert(0, f'{self.default_grammage}')

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_add_prod = tk.Button(self.frame_buttons, text="Wybierz", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_add_prod.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))

    def update_products_list(self, products_ids):
        self.frame_products.pack_forget()
        self.frame_products.destroy()
        self._fill_container_with_products(products_ids)


class DeleteConsumedDishWindow(tk.Toplevel):
    def __init__(self, master, shared_view, dish):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.dish = dish
        self.withdraw()

        self.title('BeeFit - Usuń skonsumowane danie')
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
                           text=f"Czy na pewno chcesz usunąć danie \n\'{self.dish['dish_name']}\'?",
                           font=self.shared_view.font_style_12)
        self.label.pack()

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Nie", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_delete_dish = tk.Button(self.frame_buttons, text="Tak", width=self.shared_view.btn_size,
                                         font=self.shared_view.font_style_12)
        self.btn_delete_dish.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))


class AddConsumedDishWindow(tk.Toplevel):
    def __init__(self, master, shared_view, user_dishes, user_dishes_ids, default_radio=0, default_grammage=100):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.user_dishes = user_dishes
        self.user_dishes_ids = user_dishes_ids
        self.default_radio = default_radio
        self.default_grammage = default_grammage
        self.withdraw()

        self.title('BeeFit - Dodaj skonsumowane danie')
        self.resizable(False, False)

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_search_box()
        self._create_container()
        self._fill_container_with_dishes(self.user_dishes_ids)
        self._create_grammage_entry()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_search_box(self):
        self.label_frame_search = ttk.LabelFrame(self.frame_main, text="Wyszukaj danie:")
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
        self.frame_container_dishes = Frame(self.frame_main, relief="groove", bd=2)
        self.frame_container_dishes.pack(fill="both")

        self.canvas_dishes = Canvas(self.frame_container_dishes, bd=0, highlightthickness=0, height=200)
        self.scrollbar_dishes = Scrollbar(self.frame_container_dishes, orient=VERTICAL,
                                          command=self.canvas_dishes.yview)

        self.frame_scrollable = Frame(self.canvas_dishes)
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas_dishes.configure(
            scrollregion=self.canvas_dishes.bbox("all")))

        self.canvas_dishes.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas_dishes.configure(yscrollcommand=self.scrollbar_dishes.set)

        self.canvas_dishes.pack(side="left", fill="both", expand=1)
        self.scrollbar_dishes.pack(side="right", fill="y")

        frame_sizer = Frame(self.frame_main, width=580)
        frame_sizer.pack()

    def _fill_container_with_dishes(self, dishes_ids):
        self.frame_dishes = Frame(self.frame_scrollable)
        self.frame_dishes.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_dishes, width=557)
        frame_sizer.pack()

        self.dishes_images = []
        self.dishes_img_renders = []

        self.dish_selected = tk.IntVar(value=self.default_radio)
        index = 0
        for dish_id in dishes_ids:
            frame_dish = Frame(self.frame_dishes, relief="ridge", bd=2)
            frame_dish.pack(fill="both", padx=self.shared_view.VERY_SMALL_PAD, pady=self.shared_view.VERY_SMALL_PAD)
            frame_dish.focus()

            # Radio button
            frame_radio_button = Frame(frame_dish)
            frame_radio_button.grid(row=0, column=0)

            dish_radio_button = Radiobutton(frame_radio_button, variable=self.dish_selected, value=index)
            dish_radio_button.pack(fill="both", padx=(self.shared_view.SMALL_PAD, 0))

            # Img
            frame_image = Frame(frame_dish, relief="groove", bd=1)
            frame_image.grid(row=0, column=1, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            self.dishes_images.append(self.user_dishes[f'{dish_id}']['image'])
            img_width, img_height = scale_image(self.dishes_images[index], self.shared_view.LIST_IMG_SIZE)

            self.dishes_images[index] = self.dishes_images[index].resize((img_width, img_height))
            self.dishes_img_renders.append(ImageTk.PhotoImage(self.dishes_images[index]))

            canvas_avatar = tk.Canvas(frame_image, width=self.shared_view.LIST_IMG_SIZE,
                                      height=self.shared_view.LIST_IMG_SIZE)
            canvas_avatar.create_image((self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       (self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       image=self.dishes_img_renders[index])
            canvas_avatar.pack(fill="both")

            # Name
            frame_name = Frame(frame_dish, relief="ridge", bd=1)
            frame_name.grid(row=0, column=2, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_name = Label(frame_name, text=f"{self.user_dishes[f'{dish_id}']['dish_name']}",
                               font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # GI rating
            frame_gi_rating = Frame(frame_dish, relief="ridge", bd=1)
            frame_gi_rating.grid(row=0, column=3, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            gi_rating_index = self.user_dishes[f'{dish_id}']['glycemic_index_rating']
            label_gi_rating = Label(frame_gi_rating, text=f"{GI_RATING_OPTIONS[gi_rating_index]}",
                                    font=self.shared_view.font_style_10)
            label_gi_rating.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Grammage
            frame_grammage = Frame(frame_dish, relief="ridge", bd=1)
            frame_grammage.grid(row=0, column=4, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_grammage)
            frame_center.pack()

            label_grammage = Label(frame_center, text=f"{self.user_dishes[f'{dish_id}']['grammage']} g",
                                   font=self.shared_view.font_style_10)
            label_grammage.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories
            frame_calories = Frame(frame_dish, relief="ridge", bd=1)
            frame_calories.grid(row=0, column=5, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center,
                                   text=f"{self.user_dishes[f'{dish_id}']['calories']} kcal "
                                        f"({self.user_dishes[f'{dish_id}']['calories_per_100g']} kcal/100g)",
                                   font=self.shared_view.font_style_10)
            label_calories.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            index += 1

    def _create_grammage_entry(self):
        self.label_frame = ttk.LabelFrame(self.frame_main, text="Waga dania [g]:")
        self.label_frame.pack(fill=tk.BOTH, expand=1, pady=(self.shared_view.NORMAL_PAD, 0))

        self.frame_grammage = ttk.Frame(self.label_frame)
        self.frame_grammage.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.entry_grammage = tk.Entry(self.frame_grammage, font=self.shared_view.font_style_12)
        self.entry_grammage.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_grammage.insert(0, f'{self.default_grammage}')

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_add_dish = tk.Button(self.frame_buttons, text="Wybierz", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_add_dish.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))

    def update_dishes_list(self, dishes_ids):
        self.frame_dishes.pack_forget()
        self.frame_dishes.destroy()
        self._fill_container_with_dishes(dishes_ids)
