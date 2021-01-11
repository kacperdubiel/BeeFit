import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk

from Misc.config import IMG_PATH_NO_IMAGE, GI_RATING_OPTIONS, GI_RATING_OPTIONS_LIST
from Models.main_model import convert_to_binary_data, get_image_from_bytes
from Models.user_model import scale_image
from Views.shared_view import center_window


class UserDishesView(ttk.Frame):
    def __init__(self, master, shared_view, user):
        ttk.Frame.__init__(self, master)
        self.shared_view = shared_view
        self.user = user

        self._create_main_frame()
        self._create_search_entry()
        self._create_dishes_list_container()
        self._fill_container_with_dishes()
        self._create_dishes_buttons()

    def _create_main_frame(self):
        self.frame_main = Frame(self.master)
        self.frame_main.pack(fill='both', padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

    def _create_search_entry(self):
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

    def _create_dishes_list_container(self):
        self.frame_container_dishes = Frame(self.frame_main, relief="groove", bd=2)
        self.frame_container_dishes.pack(fill="both")

        self.canvas_dishes = Canvas(self.frame_container_dishes, bd=0, highlightthickness=0, height=200)
        self.scrollbar_dishes = Scrollbar(self.frame_container_dishes, orient=VERTICAL,
                                          command=self.canvas_dishes.yview)

        self.frame_scrollable = Frame(self.canvas_dishes)
        self.frame_scrollable.bind("<Configure>", lambda e: self.canvas_dishes.configure(
            scrollregion=self.canvas_dishes.bbox("all"))
                                   )

        self.canvas_dishes.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas_dishes.configure(yscrollcommand=self.scrollbar_dishes.set)

        self.canvas_dishes.pack(side="left", fill="both", expand=1)
        self.scrollbar_dishes.pack(side="right", fill="y")

    def _fill_container_with_dishes(self):
        self.frame_dishes = Frame(self.frame_scrollable)
        self.frame_dishes.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_dishes, width=550)
        frame_sizer.pack()

        self.dishes_images = []
        self.dishes_img_renders = []

        self.dish_selected = tk.IntVar()
        index = 0
        for dish_id in self.user['selected_dishes_ids']:
            dish = self.user['dishes'][f'{dish_id}']
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

            self.dishes_images.append(dish['image'])
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

            label_name = Label(frame_name, text=f"{dish['dish_name']}", font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # GI rating
            frame_gi_rating = Frame(frame_dish, relief="ridge", bd=1)
            frame_gi_rating.grid(row=0, column=3, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            gi_rating_index = dish['glycemic_index_rating']
            label_gi_rating = Label(frame_gi_rating, text=f"{GI_RATING_OPTIONS[gi_rating_index]}",
                                    font=self.shared_view.font_style_10)
            label_gi_rating.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Grammage
            frame_grammage = Frame(frame_dish, relief="ridge", bd=1)
            frame_grammage.grid(row=0, column=4, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_grammage)
            frame_center.pack()

            label_grammage = Label(frame_center, text=f"{dish['grammage']} g",
                                   font=self.shared_view.font_style_10)
            label_grammage.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories
            frame_calories = Frame(frame_dish, relief="ridge", bd=1)
            frame_calories.grid(row=0, column=5, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center,
                                   text=f"{dish['calories']} kcal ({dish['calories_per_100g']} kcal/100g)",
                                   font=self.shared_view.font_style_10)
            label_calories.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            index += 1

    def _create_dishes_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
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

    def update_dishes(self):
        self.frame_dishes.pack_forget()
        self.frame_dishes.destroy()
        self._fill_container_with_dishes()


class DeleteDishWindow(tk.Toplevel):
    def __init__(self, master, shared_view, dish):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.dish = dish
        self.withdraw()

        self.title('BeeFit - Usuń danie')
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


class AddDishWindow(tk.Toplevel):
    def __init__(self, master, shared_view, user_products, products_ids_list=None, products_grammage_list=None,
                 default_name="Nazwa dania", default_ig_rating=0, default_image=None):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.user_products = user_products
        self.products_ids_list = products_ids_list
        self.products_grammage_list = products_grammage_list
        self.default_name = default_name
        self.default_ig_rating = default_ig_rating
        self.default_image = default_image
        self.new_image = False
        self.withdraw()

        self.title('BeeFit - Dodaj danie')
        self.resizable(False, False)

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()
        self._fill_container_with_products()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        # Name
        label_frame = LabelFrame(self.frame_main, text="Nazwa nowego dania:", font=self.shared_view.font_style_10_bold)
        label_frame.pack(fill=tk.BOTH, expand=1, pady=0)

        frame_name = ttk.Frame(label_frame)
        frame_name.pack(fill=tk.BOTH, padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

        self.entry_name = tk.Entry(frame_name, font=self.shared_view.font_style_12)
        self.entry_name.pack(fill=tk.BOTH, padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_name.insert(0, f'{self.default_name}')

        # GI rating
        label_frame = LabelFrame(self.frame_main, text="Stopień indeksu glikemicznego:",
                                 font=self.shared_view.font_style_10_bold)
        label_frame.pack(fill=tk.BOTH, expand=1, pady=(self.shared_view.SMALL_PAD, 0))

        frame_gi_rating = ttk.Frame(label_frame)
        frame_gi_rating.pack(fill=tk.BOTH, padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

        gi_rating_options_list = GI_RATING_OPTIONS_LIST
        self.gi_rating_value = tk.StringVar(value=gi_rating_options_list[self.default_ig_rating])
        gi_option_menu = tk.OptionMenu(frame_gi_rating, self.gi_rating_value, *gi_rating_options_list)
        gi_option_menu.config(font=self.shared_view.font_style_12)
        gi_option_menu.pack(fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                            pady=(self.shared_view.SMALL_PAD, self.shared_view.SMALL_PAD))

        # Products
        self.frame_container_products = LabelFrame(self.frame_main, text="Produkty:",
                                                   font=self.shared_view.font_style_10_bold)
        self.frame_container_products.pack(fill="both", pady=(self.shared_view.SMALL_PAD, 0))

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

        # Products buttons
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_delete_prod = tk.Button(self.frame_buttons, text="Usuń produkt", width=self.shared_view.btn_size,
                                         font=self.shared_view.font_style_12)
        self.btn_delete_prod.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=self.shared_view.SMALL_PAD)

        self.btn_edit_prod = tk.Button(self.frame_buttons, text="Edytuj produkt", width=self.shared_view.btn_size,
                                       font=self.shared_view.font_style_12)
        self.btn_edit_prod.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=self.shared_view.SMALL_PAD)

        self.btn_add_prod = tk.Button(self.frame_buttons, text="Dodaj produkt", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_add_prod.pack(side='left', pady=self.shared_view.SMALL_PAD)

        # Image
        label_frame = LabelFrame(self.frame_main, text="Zdjęcie dania:", font=self.shared_view.font_style_10_bold)
        label_frame.pack(fill=tk.BOTH, pady=(self.shared_view.SMALL_PAD, 0))

        frame_image = ttk.Frame(label_frame)
        frame_image.pack(fill=tk.BOTH, padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

        if self.default_image is None:
            self.default_image = convert_to_binary_data(IMG_PATH_NO_IMAGE)
            self.dish_image = get_image_from_bytes(self.default_image)
        else:
            self.dish_image = self.default_image

        img_width, img_height = scale_image(self.dish_image, self.shared_view.ADD_ITEM_IMG_SIZE)
        self.dish_image = self.dish_image.resize((img_width, img_height))

        self.canvas_avatar = tk.Canvas(frame_image, width=self.shared_view.ADD_ITEM_IMG_SIZE,
                                       height=self.shared_view.ADD_ITEM_IMG_SIZE)

        self.avatar_render = ImageTk.PhotoImage(self.dish_image)
        self.canvas_image_avatar = self.canvas_avatar.create_image((self.shared_view.ADD_ITEM_IMG_SIZE / 2) + 1,
                                                                   (self.shared_view.ADD_ITEM_IMG_SIZE / 2) + 1,
                                                                   image=self.avatar_render)

        self.canvas_avatar.pack()

        self.btn_add_img = tk.Button(frame_image, text="Ustaw zdjęcie", width=self.shared_view.btn_size,
                                     font=self.shared_view.font_style_12)
        self.btn_add_img.pack(pady=(self.shared_view.SMALL_PAD, 0))

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_add_dish = tk.Button(self.frame_buttons, text="Dodaj danie", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_add_dish.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))

    def set_dish_image(self, image):
        self.default_image = image
        self.dish_image = get_image_from_bytes(self.default_image)
        img_width, img_height = scale_image(self.dish_image, self.shared_view.ADD_ITEM_IMG_SIZE)
        self.dish_image = self.dish_image.resize((img_width, img_height))
        self.avatar_render = ImageTk.PhotoImage(self.dish_image)
        self.canvas_avatar.itemconfig(self.canvas_image_avatar, image=self.avatar_render)
        self.new_image = True

    def _fill_container_with_products(self):
        self.frame_products = Frame(self.frame_scrollable)
        self.frame_products.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_products, width=550)
        frame_sizer.pack()

        self.prods_images = list()
        self.prods_img_renders = list()

        self.product_selected = tk.IntVar()
        prod_id = 0
        size = len(self.products_ids_list) if self.products_ids_list is not None else 0
        for i in range(0, size):
            dish_prod = self.user_products[f'{self.products_ids_list[i]}']
            frame_product = Frame(self.frame_products, relief="ridge", bd=2)
            frame_product.pack(fill="both", padx=self.shared_view.VERY_SMALL_PAD, pady=self.shared_view.VERY_SMALL_PAD)
            frame_product.focus()

            # Radio button
            frame_radio_button = Frame(frame_product)
            frame_radio_button.grid(row=0, column=0)

            product_radio_button = Radiobutton(frame_radio_button, variable=self.product_selected, value=prod_id)
            product_radio_button.pack(fill="both", padx=(self.shared_view.SMALL_PAD, 0))

            # Img
            frame_image = Frame(frame_product, relief="groove", bd=1)
            frame_image.grid(row=0, column=1, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            self.prods_images.append(dish_prod['image'])
            img_width, img_height = scale_image(self.prods_images[prod_id], self.shared_view.LIST_IMG_SIZE)

            self.prods_images[prod_id] = self.prods_images[prod_id].resize((img_width, img_height))
            self.prods_img_renders.append(ImageTk.PhotoImage(self.prods_images[prod_id]))

            canvas_avatar = tk.Canvas(frame_image, width=self.shared_view.LIST_IMG_SIZE,
                                      height=self.shared_view.LIST_IMG_SIZE)
            canvas_avatar.create_image((self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       (self.shared_view.LIST_IMG_SIZE // 2) + 1,
                                       image=self.prods_img_renders[prod_id])
            canvas_avatar.pack(fill="both")

            # Name
            frame_name = Frame(frame_product, relief="ridge", bd=1)
            frame_name.grid(row=0, column=2, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_name = Label(frame_name, text=f"{dish_prod['product_name']}",
                               font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # GI rating
            frame_gi_rating = Frame(frame_product, relief="ridge", bd=1)
            frame_gi_rating.grid(row=0, column=3, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            gi_rating_index = dish_prod['glycemic_index_rating']
            label_gi_rating = Label(frame_gi_rating, text=f"{GI_RATING_OPTIONS[gi_rating_index]}",
                                    font=self.shared_view.font_style_10)
            label_gi_rating.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Grammage
            frame_grammage = Frame(frame_product, relief="ridge", bd=1)
            frame_grammage.grid(row=0, column=4, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            label_grammage = Label(frame_grammage, text=f"{self.products_grammage_list[i]} g",
                                   font=self.shared_view.font_style_10)
            label_grammage.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories
            frame_calories = Frame(frame_product, relief="ridge", bd=1)
            frame_calories.grid(row=0, column=5, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories)
            frame_center.pack()
            calories = int((dish_prod['calories'] * int(self.products_grammage_list[i])) / 100)
            label_calories = Label(frame_center, text=f"{calories} kcal",
                                   font=self.shared_view.font_style_10)
            label_calories.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            prod_id += 1

    def update_products_list(self, products_ids_list, products_grammage_list):
        self.frame_products.pack_forget()
        self.frame_products.destroy()
        self.products_ids_list = products_ids_list
        self.products_grammage_list = products_grammage_list
        self._fill_container_with_products()


class DeleteDishProductWindow(tk.Toplevel):
    def __init__(self, master, shared_view, product):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.product = product
        self.withdraw()

        self.title('BeeFit - Usuń produkt')
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
                           text=f"Czy na pewno chcesz usunąć z tego dania produkt\n\'{self.product['product_name']}\'?",
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


class AddDishProductWindow(tk.Toplevel):
    def __init__(self, master, shared_view, user_prods, user_prods_ids, default_radio=0, default_grammage=100):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.user_prods = user_prods
        self.user_prods_ids = user_prods_ids
        self.default_radio = default_radio
        self.default_grammage = default_grammage
        self.withdraw()

        self.title('BeeFit - Dodaj produkt')
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
