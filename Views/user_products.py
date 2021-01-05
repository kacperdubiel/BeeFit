import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk

from Misc.config import IMG_PATH_NO_IMAGE
from Models.main_model import convert_to_binary_data, get_image_from_bytes
from Models.user_model import scale_image
from Views.shared_view import center_window


class UserProductsView(ttk.Frame):
    def __init__(self, master, shared_view, user):
        ttk.Frame.__init__(self, master)
        self.shared_view = shared_view
        self.user = user

        self._create_main_frame()
        self._create_search_entry()
        self._create_products_list_container()
        self._fill_container_with_products()
        self._create_products_buttons()

    def _create_main_frame(self):
        self.frame_main = Frame(self.master)
        self.frame_main.pack(fill='both', padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

    def _create_search_entry(self):
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

    def _create_products_list_container(self):
        # Products tab
        self.frame_container_products = Frame(self.frame_main, relief="groove", bd=2)
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

    def _fill_container_with_products(self):
        self.frame_products = Frame(self.frame_scrollable)
        self.frame_products.pack(fill="both", expand=1)

        frame_sizer = Frame(self.frame_products, width=550)
        frame_sizer.pack()

        self.prods_images = []
        self.prods_img_renders = []

        self.product_selected = tk.IntVar()
        index = 0
        for prod_id in self.user['selected_products_ids']:
            product = self.user['products'][f'{prod_id}']
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

            self.prods_images.append(product['image'])
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

            label_name = Label(frame_name, text=f"{product['product_name']}", font=self.shared_view.font_style_10_bold)
            label_name.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            # Calories
            frame_calories = Frame(frame_product, relief="ridge", bd=1)
            frame_calories.grid(row=0, column=4, padx=(0, self.shared_view.SMALL_PAD), pady=self.shared_view.SMALL_PAD)

            frame_center = Frame(frame_calories)
            frame_center.pack()

            label_calories = Label(frame_center, text=f"{product['calories']} kcal/100g",
                                   font=self.shared_view.font_style_10)
            label_calories.pack(padx=self.shared_view.SMALL_PAD, pady=self.shared_view.SMALL_PAD)

            index += 1

    def _create_products_buttons(self):
        # Consumed products buttons
        self.frame_buttons = ttk.Frame(self.frame_main)
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

    def update_products(self):
        self.frame_products.pack_forget()
        self.frame_products.destroy()
        self._fill_container_with_products()


class DeleteProductWindow(tk.Toplevel):
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


class AddProductWindow(tk.Toplevel):
    def __init__(self, master, shared_view, default_name="Nazwa produktu", default_calories=100, default_image=None):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.default_name = default_name
        self.default_calories = default_calories
        self.default_image = default_image
        self.new_image = False
        self.withdraw()

        self.title('BeeFit - Dodaj produkt')
        self.resizable(False, False)

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_entries(self):
        label_frame = ttk.LabelFrame(self.frame_main, text="Nazwa nowego produktu:")
        label_frame.pack(fill=tk.BOTH, expand=1, pady=(self.shared_view.NORMAL_PAD, 0))

        frame_name = ttk.Frame(label_frame)
        frame_name.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.entry_name = tk.Entry(frame_name, font=self.shared_view.font_style_12)
        self.entry_name.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_name.insert(0, f'{self.default_name}')

        label_frame = ttk.LabelFrame(self.frame_main, text="Liczba kalorii na 100 gram:")
        label_frame.pack(fill=tk.BOTH, expand=1, pady=(self.shared_view.NORMAL_PAD, 0))

        frame_calories = ttk.Frame(label_frame)
        frame_calories.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.entry_calories = tk.Entry(frame_calories, font=self.shared_view.font_style_12)
        self.entry_calories.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.SMALL_PAD)
        self.entry_calories.insert(0, f'{self.default_calories}')

        label_frame = ttk.LabelFrame(self.frame_main, text="Zdjęcie produktu:")
        label_frame.pack(fill=tk.BOTH, pady=(self.shared_view.NORMAL_PAD, 0))

        frame_image = ttk.Frame(label_frame)
        frame_image.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        if self.default_image is None:
            self.default_image = convert_to_binary_data(IMG_PATH_NO_IMAGE)
            self.prod_image = get_image_from_bytes(self.default_image)
        else:
            self.prod_image = self.default_image

        img_width, img_height = scale_image(self.prod_image, self.shared_view.ADD_ITEM_IMG_SIZE)
        self.prod_image = self.prod_image.resize((img_width, img_height))

        self.canvas_avatar = tk.Canvas(frame_image, width=self.shared_view.ADD_ITEM_IMG_SIZE,
                                       height=self.shared_view.ADD_ITEM_IMG_SIZE)

        self.avatar_render = ImageTk.PhotoImage(self.prod_image)
        self.canvas_image_avatar = self.canvas_avatar.create_image((self.shared_view.ADD_ITEM_IMG_SIZE / 2) + 1,
                                                                   (self.shared_view.ADD_ITEM_IMG_SIZE / 2) + 1,
                                                                   image=self.avatar_render)

        self.canvas_avatar.pack()

        self.btn_add_img = tk.Button(frame_image, text="Ustaw zdjęcie", width=self.shared_view.btn_size,
                                     font=self.shared_view.font_style_12)
        self.btn_add_img.pack(pady=(self.shared_view.NORMAL_PAD, 0))

    def _create_buttons(self):
        self.frame_buttons = ttk.Frame(self.frame_main)
        self.frame_buttons.pack()

        self.btn_back = tk.Button(self.frame_buttons, text="Powrót", width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_add_prod = tk.Button(self.frame_buttons, text="Dodaj", width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_add_prod.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))

    def set_product_image(self, image):
        self.default_image = image
        self.prod_image = get_image_from_bytes(self.default_image)
        img_width, img_height = scale_image(self.prod_image, self.shared_view.ADD_ITEM_IMG_SIZE)
        self.prod_image = self.prod_image.resize((img_width, img_height))
        self.avatar_render = ImageTk.PhotoImage(self.prod_image)
        self.canvas_avatar.itemconfig(self.canvas_image_avatar, image=self.avatar_render)
        self.new_image = True
