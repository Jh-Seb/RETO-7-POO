import json
from collections import deque, namedtuple


MenuSet = namedtuple("MenuSet", ["category", "items"])

class MenuItem:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

class Beverage(MenuItem):
    def __init__(self, name, price, size, is_cold, has_ice):
        super().__init__(name, price)
        self._size = size
        self._is_cold = is_cold
        self._has_ice = has_ice

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def is_cold(self):
        return self._is_cold

    @is_cold.setter
    def is_cold(self, value):
        self._is_cold = value

    @property
    def has_ice(self):
        return self._has_ice

    @has_ice.setter
    def has_ice(self, value):
        self._has_ice = value

    def __str__(self):
        return (
            f"{self.name} (Price: {self.price}, Size: {self.size}, "
            f"Cold: {self.is_cold}, Ice: {self.has_ice})"
        )

class Appetizer(MenuItem):
    def __init__(self, name, price, appetizer_type):
        super().__init__(name, price)
        self._appetizer_type = appetizer_type

    @property
    def appetizer_type(self):
        return self._appetizer_type

    @appetizer_type.setter
    def appetizer_type(self, value):
        self._appetizer_type = value

    def __str__(self):
        return f"{self.name} (Price: {self.price}, Type: {self.appetizer_type})"

class MainCourse(MenuItem):
    def __init__(self, name, price, ingredients, salad):
        super().__init__(name, price)
        self._ingredients = ingredients
        self._salad = salad

    @property
    def ingredients(self):
        return self._ingredients

    @ingredients.setter
    def ingredients(self, value):
        self._ingredients = value

    @property
    def salad(self):
        return self._salad

    @salad.setter
    def salad(self, value):
        self._salad = value

    def __str__(self):
        return (
            f"{self.name} (Price: {self.price}, Ingredients: {self.ingredients}, "
            f"Salad: {self.salad})"
        )

class Order:
    def __init__(self):
        self.plates = []
        self.menu = {}  

    def add_plate(self, plate):
        self.plates.append(plate)

    def remove_plate(self, plate):
        self.plates.remove(plate)

    def total(self):
        return self.calculate_total_price()

    def calculate_total_price(self):
        total = sum(plate.price for plate in self.plates)
        has_main_course = any(isinstance(plate, MainCourse) for plate in self.plates)
        if has_main_course:
            discount = sum(
                plate.price * 0.1 for plate in self.plates if isinstance(plate, Beverage)
            )
            total -= discount
        return total

    def get_plate_details(self):
        return [str(plate) for plate in self.plates]

    def __str__(self):
        plate_details = "\n".join(self.get_plate_details())
        return f"Order:\n{plate_details}\nTotal: {self.total()}"


    def load_menu(self, filename="menu.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.menu = json.load(f)
            print("Menú cargado exitosamente.")
        except FileNotFoundError:
            print("Archivo de menú no encontrado. Se creará uno nuevo.")
            self.menu = {}

    def save_menu(self, filename="menu.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.menu, f, indent=4, ensure_ascii=False)
        print("Menú guardado exitosamente.")

    def create_menu(self, categories=None):
      
        if categories is None:
            categories = ["Beverages", "Appetizers", "MainCourses"]
        self.menu = {category: [] for category in categories}
        self.save_menu()

    def add_menu_item(self, category, item_dict):
      
        if category not in self.menu:
            self.menu[category] = []
        self.menu[category].append(item_dict)
        self.save_menu()

    def update_menu_item(self, category, item_name, updated_item):
       
        if category in self.menu:
            for idx, item in enumerate(self.menu[category]):
                if item.get("name") == item_name:
                    self.menu[category][idx] = updated_item
                    self.save_menu()
                    return True
        return False

    def delete_menu_item(self, category, item_name):
        
        if category in self.menu:
            for idx, item in enumerate(self.menu[category]):
                if item.get("name") == item_name:
                    del self.menu[category][idx]
                    self.save_menu()
                    return True
        return False

class Payment:
    def __init__(self, order, payment_method):
        self.order = order
        self.payment_method = payment_method

    def process_payment(self):
        print(
            f"Processing payment of {self.order.total()} using {self.payment_method}..."
        )
        print("Payment successful!")

class Restaurant:
    def __init__(self):
        self.orders = deque()  

    def add_order(self, order):
        self.orders.append(order)
        print("Orden agregada a la cola.")

    def process_next_order(self):
        if self.orders:
            order = self.orders.popleft()
            print("Procesando la siguiente orden:")
            print(order)
        else:
            print("No hay órdenes para procesar.")

# Ejemplo de uso:

# --- Gestión del menú ---
order = Order()
order.create_menu(["Beverages", "Appetizers", "MainCourses"])

# Agregar items al menú usando diccionarios
order.add_menu_item("Beverages", {
    "name": "Coca Cola", "price": 2000, "size": "Large", "is_cold": True, "has_ice": True
})
order.add_menu_item("MainCourses", {
    "name": "Spaghetti", "price": 25000, "ingredients": "Pasta and tomato sauce", "salad": False
})

# Actualizar un item del menú
order.update_menu_item("Beverages", "Coca Cola", {
    "name": "Coca Cola", "price": 1800, "size": "Medium", "is_cold": True, "has_ice": True
})

# Eliminar un item del menú
order.delete_menu_item("MainCourses", "Spaghetti")

# Cargar menú para verificar cambios
order.load_menu()

# --- Gestión de órdenes y procesamiento de pagos ---
# Crear una orden y agregar platos
order.add_plate(MainCourse("Spaghetti", 25000, "Pasta and tomato sauce", False))
order.add_plate(Beverage("Coca Cola", 2000, "Large", True, True))

print(order)

payment = Payment(order, "Credit Card")
payment.process_payment()

# --- Gestión de múltiples órdenes en el restaurante ---
restaurant = Restaurant()
restaurant.add_order(order)
# Aquí se pueden agregar más órdenes y procesarlas en orden FIFO
restaurant.process_next_order()
