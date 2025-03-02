import json
from collections import deque

class MenuItem:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

class Beverage(MenuItem):
    def __init__(self, name, price, size, is_cold, has_ice):
        super().__init__(name, price)
        self.__size = size
        self.__is_cold = is_cold
        self.__has_ice = has_ice

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size

    def get_is_cold(self):
        return self.__is_cold

    def set_is_cold(self, is_cold):
        self.__is_cold = is_cold

    def get_has_ice(self):
        return self.__has_ice

    def set_has_ice(self, has_ice):
        self.__has_ice = has_ice

    def __str__(self):
        return "{} (Price: {}, Size: {}, Cold: {}, Ice: {})".format(
            self.get_name(), self.get_price(), self.__size, self.__is_cold, self.__has_ice
        )

class Appetizer(MenuItem):
    def __init__(self, name, price, appetizer_type):
        super().__init__(name, price)
        self.__appetizer_type = appetizer_type

    def get_appetizer_type(self):
        return self.__appetizer_type

    def set_appetizer_type(self, appetizer_type):
        self.__appetizer_type = appetizer_type

    def __str__(self):
        return "{} (Price: {}, Type: {})".format(
            self.get_name(), self.get_price(), self.__appetizer_type
        )

class MainCourse(MenuItem):
    def __init__(self, name, price, ingredients, salad):
        super().__init__(name, price)
        self.__ingredients = ingredients
        self.__salad = salad

    def get_ingredients(self):
        return self.__ingredients

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients

    def get_salad(self):
        return self.__salad

    def set_salad(self, salad):
        self.__salad = salad

    def __str__(self):
        return "{} (Price: {}, Ingredients: {}, Salad: {})".format(
            self.get_name(), self.get_price(), self.__ingredients, self.__salad
        )

class Order:
    def __init__(self):
        self.__plates = []       # Lista de platos
        self.__menu = {}         # Menú representado como diccionario

    def add_plate(self, plate):
        self.__plates.append(plate)

    def remove_plate(self, plate):
        try:
            self.__plates.remove(plate)
        except ValueError as e:
            print("Error al eliminar el plato:", e)

    def calculate_total_price(self):
        total = sum(plate.get_price() for plate in self.__plates)
        has_main_course = any(isinstance(plate, MainCourse) for plate in self.__plates)
        if has_main_course:
            discount = sum(plate.get_price() * 0.1 for plate in self.__plates if isinstance(plate, Beverage))
            total -= discount
        return total

    def get_plate_details(self):
        return [str(plate) for plate in self.__plates]

    def __str__(self):
        details = "\n".join(self.get_plate_details())
        return "Order:\n" + details + "\nTotal: " + str(self.calculate_total_price())

    def load_menu(self, filename="menu.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.__menu = json.load(f)
            print("Menú cargado exitosamente.")
        except FileNotFoundError:
            print("Archivo de menú no encontrado. Se creará uno nuevo.")
            self.__menu = {}
        except json.JSONDecodeError:
            print("Error al decodificar el archivo de menú.")
            self.__menu = {}

    def save_menu(self, filename="menu.json"):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.__menu, f, indent=4, ensure_ascii=False)
            print("Menú guardado exitosamente.")
        except Exception as e:
            print("Error al guardar el menú:", e)

    def create_menu(self, categories=None):
        if categories is None:
            categories = ["Beverages", "Appetizers", "MainCourses"]
        self.__menu = {category: [] for category in categories}
        self.save_menu()

    def add_menu_item(self, category, item_dict):
        if category not in self.__menu:
            self.__menu[category] = []
        self.__menu[category].append(item_dict)
        self.save_menu()

    def update_menu_item(self, category, item_name, updated_item):
        if category in self.__menu:
            for idx, item in enumerate(self.__menu[category]):
                if item.get("name") == item_name:
                    self.__menu[category][idx] = updated_item
                    self.save_menu()
                    return True
        return False

    def delete_menu_item(self, category, item_name):
        if category in self.__menu:
            for idx, item in enumerate(self.__menu[category]):
                if item.get("name") == item_name:
                    del self.__menu[category][idx]
                    self.save_menu()
                    return True
        return False

class Payment:
    def __init__(self, order, payment_method):
        self.order = order
        self.payment_method = payment_method

    def process_payment(self):
        print("Processing payment of {} using {}...".format(self.order.calculate_total_price(), self.payment_method))
        print("Payment successful!")

class Restaurant:
    def __init__(self):
        self.__orders = deque()  # Cola (queue) de órdenes

    def add_order(self, order):
        self.__orders.append(order)
        print("Orden agregada a la cola.")

    def process_next_order(self):
        if self.__orders:
            order = self.__orders.popleft()
            print("Procesando la siguiente orden:")
            print(order)
        else:
            print("No hay órdenes para procesar.")

# Ejemplo de uso:

# --- Gestión del menú ---
order = Order()
order.create_menu(["Beverages", "Appetizers", "MainCourses"])

# Agregar ítems al menú usando diccionarios
order.add_menu_item("Beverages", {
    "name": "Coca Cola", "price": 2000, "size": "Large", "is_cold": True, "has_ice": True
})
order.add_menu_item("MainCourses", {
    "name": "Spaghetti", "price": 25000, "ingredients": "Pasta and tomato sauce", "salad": False
})

# Actualizar un ítem del menú
order.update_menu_item("Beverages", "Coca Cola", {
    "name": "Coca Cola", "price": 1800, "size": "Medium", "is_cold": True, "has_ice": True
})

# Eliminar un ítem del menú
order.delete_menu_item("MainCourses", "Spaghetti")

# Cargar menú para verificar cambios
order.load_menu()

# --- Gestión de órdenes y procesamiento de pagos ---
order.add_plate(MainCourse("Spaghetti", 25000, "Pasta and tomato sauce", False))
order.add_plate(Beverage("Coca Cola", 2000, "Large", True, True))

print(order)

payment = Payment(order, "Credit Card")
payment.process_payment()

# --- Gestión de múltiples órdenes en el restaurante ---
restaurant = Restaurant()
restaurant.add_order(order)
restaurant.process_next_order()
