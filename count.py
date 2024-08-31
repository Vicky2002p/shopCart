import tkinter as tk
from PIL import Image, ImageTk

class Product:
    def __init__(self, name, image_path, stock_count):
        self.name = name
        self.image_path = image_path
        self.stock_count= stock_count

class Card:
    def __init__(self, master, product, cart):
        self.master = master
        self.product = product
        self.cart = cart
        self.count = 0
        self.photo = ImageTk.PhotoImage(Image.open(self.product.image_path).resize((100, 100)))
        
        self.frame = tk.Frame(self.master, bg='grey', highlightbackground="black", highlightthickness=1)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.lable=tk.Label(self.frame, text=product.name, font=("Arial", 16))
        self.lable.grid(row=0, column=0, padx=10, pady=10)

        self.button = tk.Button(self.frame, image=self.photo, command=self.add_to_cart)
        self.button.image = self.photo
        self.button.grid(row=1, column=0, padx=10, pady=10)

        self.count_label = tk.Label(self.frame, text="Count: 0", font=("Arial", 16))
        self.count_label.grid(row=2, column=0, padx=10, pady=10)

        self.stock_label = tk.Label(self.frame, text=f"Stock: {product.stock_count}", font={"Arial", 16})
        self.stock_label.grid(row=3, column=0, padx=10, pady=10)
    
    def add_to_cart(self):
        if self.product.stock_count > 0:
            self.count += 1
            self.count_label.config(text=f"Count: {self.count}")
            self.product.stock_count -= 1
            self.stock_label.config(text=f"Stock: {self.product.stock_count}")
            self.cart.add_product(self.product, 1, self)

    def update_stock(self):
        self.count_label.config(text=f"Count: {self.count}")
        self.stock_label.config(text=f"Stock: {self.product.stock_count}")

class Cart:
    def __init__(self, master):
        self.master = master
        self.products = {}
        self.product_cards = {}
        self.frame = tk.Frame(self.master, bg='grey', highlightbackground="black", highlightthickness=1)
        self.frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')
        self.lable=tk.Label(self.frame, text="Cart", font=("Arial", 16))
        self.lable.grid(row=0, column=0, padx=10, pady=10)
        self.product_labels = {}

    def add_product(self, product, count, card):
        if product in self.products:
            self.products[product] += count
        else:
            self.products[product] = count
            self.product_cards[product] = card
        self.update_cart()

    def update_cart(self):
        for label in self.product_labels.values():
            label.destroy()
        self.product_labels = {}
        row = 1
        for product, count in self.products.items():
            label_frame = tk.Frame(self.frame)
            label_frame.grid(row=row, column=0, padx=10, pady=10)
            label= tk.Label(label_frame, text=f"{product.name}: ", font=("Arial", 16))
            label.pack(side=tk.LEFT)
            count_button = tk.Button(label_frame, text=str(count), font=("Arial", 16), command=lambda p=product: self.reduce_product(p))
            count_button.pack(side=tk.LEFT)
            self.product_labels[product.name] = label_frame
            row += 1

    def reduce_product(self, product):
        if product in self.products:
            if self.products[product] <= 1:
                del self.products[product]
            else:
                self.products[product] -= 1
            card = self.product_cards[product]
            card.count -= 1
            product.stock_count += 1
            self.product_cards[product].update_stock()
            self.update_cart()

class ProductList:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.canvas = tk.Canvas(self.frame, width=600, height=window_height, scrollregion=(0, 0, 600, 800))
        self.canvas.grid(row=0, column=0)
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)
        self.product_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.product_frame, anchor='nw')
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.row = 0
        self.column = 0

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_product(self, product, cart):
        card = Card(self.product_frame, product, cart)
        card.frame.grid(row=self.row, column=self.column, padx=10, pady=10)
        self.column += 1
        if self.column == 4:
            self.column = 0
            self.row += 1
        self.product_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
root = tk.Tk()
root.title("Products")

# Getting screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Window size
window_width = 800
window_height = 600

# x and y coordinates for window
x = (screen_width - window_width)//2
y = (screen_height -window_height)//2

# Window's position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

cart = Cart(root)
product_list = ProductList(root)

products = [
    Product("Butter", "./image/butter.jpg", 20),
    Product("Curd", "./image/curd.jpg", 12),
    Product("Flour", "./image/flour.jpg", 15),
    Product("Milk", "./image/milk.jpg", 10),
    Product("Rice", "./image/rice.jpg", 18),
]

for product in products:
    product_list.add_product(product, cart)

root.mainloop()