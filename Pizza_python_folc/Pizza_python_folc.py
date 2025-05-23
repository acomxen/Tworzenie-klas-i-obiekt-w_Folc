import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os






class Topping:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Pizza:
    def __init__(self, name, base_price, image_path):
        self.name = name
        self.base_price = base_price
        self.image_path = image_path

class Order:
    def __init__(self):
        self.items = []
        self.address = ""

    def add_pizza(self, pizza, toppings, size, crust):
        self.items.append((pizza, toppings, size, crust))

    def get_total(self):
        total = 0
        for pizza, toppings, size, crust in self.items:
            size_multiplier = {"Mała": 1, "Średnia": 1.3, "Duża": 1.6}[size]
            crust_price = {"Cienkie": 0, "Klasyczne": 2, "Grube": 3}[crust]
            toppings_price = sum(t.price for t in toppings)
            total += (pizza.base_price + toppings_price + crust_price) * size_multiplier
        return round(total, 2)







class PizzaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zamów pizzę")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)
        self.order = Order()

        
        logo_img = Image.open("images/logo.png").resize((500, 130))
        self.logo = ImageTk.PhotoImage(logo_img)
        tk.Label(root, image=self.logo, bg="#1e1e1e").pack(pady=10)

        self.toppings_list = [
            Topping("Ser", 2), Topping("Pieczarki", 2),
            Topping("Szynka", 3), Topping("Oliwki", 2),
            Topping("Papryka", 2), Topping("Ananas", 3)
        ]

        self.pizza_list = [
            Pizza("Małgorzatka", 28, "images/picka.png"),
            Pizza("Palimordka", 36, "images/picka.png"),
            Pizza("Salami", 40, "images/picka.png"),
            Pizza("Hawajska", 38, "images/picka.png"),
            Pizza("Polska", 45, "images/picka.png"),
            Pizza("Prosscutto", 35, "images/picka.png"),
            Pizza("Nemo", 46, "images/picka.png"),
            Pizza("Studencka", 50, "images/picka.png"),
        ]

        self.container = tk.Frame(self.root, bg="#1e1e1e")
        self.container.pack(fill="both", expand=True)

        self.main_frame = tk.Frame(self.container, bg="#1e1e1e")
        self.compose_frame = tk.Frame(self.container, bg="#1e1e1e")
        self.cart_frame = tk.Frame(self.container, bg="#1e1e1e")

        self.frames = {
            "main": self.main_frame,
            "compose": self.compose_frame,
            "cart": self.cart_frame
        }

        self.active_pizza = None
        self.setup_main_page()
        self.show_frame("main")



    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def setup_main_page(self):
        canvas = tk.Canvas(self.main_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_frame, command=canvas.yview)
        frame = tk.Frame(canvas, bg="#1e1e1e")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        for index, pizza in enumerate(self.pizza_list):
            row = index // 2
            col = index % 2

            f = tk.Frame(frame, bg="#2a2a2a", bd=1, relief=tk.RIDGE, padx=10, pady=10)

            try:
                img = Image.open(pizza.image_path).resize((200, 200))
                img_tk = ImageTk.PhotoImage(img)
                label_img = tk.Label(f, image=img_tk, bg="#2a2a2a")
                label_img.image = img_tk
                label_img.pack()
            except Exception:
                tk.Label(f, text="[Brak obrazu]", fg="white", bg="#2a2a2a").pack()

            tk.Label(f, text=f"{pizza.name} - {pizza.base_price} zł", fg="white", bg="#2a2a2a", font=("Arial", 12)).pack(pady=5)
            tk.Button(f, text="Wybierz", command=lambda p=pizza: self.dodatki_pizza(p), bg="#3a3a3a", fg="white", relief="flat").pack(pady=5)
            f.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        canvas.pack(fill="both", expand=True, side="left")
        scrollbar.pack(fill="y", side="right")

        
        cart_img = Image.open("images/cart_icon.png").resize((70, 70))
        self.cart_icon = ImageTk.PhotoImage(cart_img)
        tk.Button(self.main_frame, text="", image=self.cart_icon, compound="center", command=self.wozek, bg="#3a3a3a", fg="white", relief="flat").pack(pady=15)







    def dodatki_pizza(self, pizza):
        self.active_pizza = pizza
        self.show_frame("compose")

        for widget in self.compose_frame.winfo_children():
            widget.destroy()

        size_var = tk.StringVar(value="Średnia")
        crust_var = tk.StringVar(value="Klasyczne")
        topping_vars = {}

        tk.Label(self.compose_frame, text=pizza.name, font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

        tk.Label(self.compose_frame, text="Rozmiar:", fg="white", bg="#1e1e1e").pack()
        for size in ["Mała", "Średnia", "Duża"]:
            tk.Radiobutton(self.compose_frame, text=size, variable=size_var, value=size, fg="white", bg="#1e1e1e", selectcolor="#2a2a2a").pack(anchor="w")

        tk.Label(self.compose_frame, text="Ciasto:", fg="white", bg="#1e1e1e").pack()
        for crust in ["Cienkie", "Klasyczne", "Grube"]:
            tk.Radiobutton(self.compose_frame, text=crust, variable=crust_var, value=crust, fg="white", bg="#1e1e1e", selectcolor="#2a2a2a").pack(anchor="w")

        tk.Label(self.compose_frame, text="Składniki:", fg="white", bg="#1e1e1e").pack()
        for topping in self.toppings_list:
            var = tk.BooleanVar()
            tk.Checkbutton(self.compose_frame, text=f"{topping.name} (+{topping.price} zł)", variable=var, fg="white", bg="#1e1e1e", selectcolor="#2a2a2a").pack(anchor="w")
            topping_vars[topping] = var

        def add_composed():
            selected_toppings = [t for t, var in topping_vars.items() if var.get()]
            self.order.add_pizza(pizza, selected_toppings, size_var.get(), crust_var.get())
            messagebox.showinfo("Dodano", "Pizza dodana do koszyka")
            self.show_frame("main")

        tk.Button(self.compose_frame, text="Dodaj do koszyka", command=add_composed, bg="#3a3a3a", fg="white", relief="flat").pack(pady=10)
        tk.Button(self.compose_frame, text="Wróć", command=lambda: self.show_frame("main"), bg="#3a3a3a", fg="white", relief="flat").pack(pady=5)







    def wozek(self):
        self.show_frame("cart")
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        if not self.order.items:
            tk.Label(self.cart_frame, text="Koszyk jest pusty.", fg="white", bg="#1e1e1e").pack()
            tk.Button(self.cart_frame, text="Wróć", command=lambda: self.show_frame("main"), bg="#3a3a3a", fg="white", relief="flat").pack(pady=10)
            return

        def remove_item(index):
            del self.order.items[index]
            self.wozek()

        for idx, (pizza, toppings, size, crust) in enumerate(self.order.items):
            item_frame = tk.Frame(self.cart_frame, bg="#1e1e1e")
            item_frame.pack(fill="x", padx=10, pady=5)
            desc = f"{pizza.name} ({size}, {crust})\n + " + ", ".join(t.name for t in toppings)
            tk.Label(item_frame, text=desc, fg="white", bg="#1e1e1e", justify="left").pack(side="left", anchor="w", fill="x", expand=True)
            tk.Button(item_frame, text="Usuń", command=lambda i=idx: remove_item(i), bg="#ff4c4c", fg="white", relief="flat").pack(side="right")

        tk.Label(self.cart_frame, text=f"Suma: {self.order.get_total()} zł", fg="white", bg="#1e1e1e", font=("Arial", 12)).pack(pady=10)

        tk.Label(self.cart_frame, text="Adres dostawy:", fg="white", bg="#1e1e1e").pack()
        address_entry = tk.Entry(self.cart_frame, width=40)
        address_entry.pack(pady=5)





        def zamowienie():
            address = address_entry.get().strip()
            if not address:
                messagebox.showerror("Błąd", "Podaj adres dostawy.")
                return
            time = random.randint(45, 120)
            messagebox.showinfo("Dziękujemy!", f"Dostawa za {time} minut.\nAdres: {address}")
            self.show_frame("main")

        tk.Button(self.cart_frame, text="Zamów", command=zamowienie, bg="#3a3a3a", fg="white", relief="flat").pack(pady=10)
        tk.Button(self.cart_frame, text="Wróć", command=lambda: self.show_frame("main"), bg="#3a3a3a", fg="white", relief="flat").pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x700")
    app = PizzaApp(root)
    root.mainloop()