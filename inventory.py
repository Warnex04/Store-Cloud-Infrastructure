
class StockItem:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, sold_quantity):
        if sold_quantity > self.quantity:
            raise ValueError("Not enough stock to sell")
        self.quantity -= sold_quantity

    def restock(self, additional_quantity):
        self.quantity += additional_quantity

class StockManager:
    def __init__(self):
        self.items = {}

    def add_product(self, product_id, name, price, quantity):
        if product_id in self.items:
            raise ValueError("Product ID already exists")
        self.items[product_id] = StockItem(product_id, name, price, quantity)

    def sell_product(self, product_id, quantity):
        if product_id not in self.items:
            raise ValueError("Product not found")
        self.items[product_id].update_quantity(quantity)

    def restock_product(self, product_id, quantity):
        if product_id not in self.items:
            raise ValueError("Product not found")
        self.items[product_id].restock(quantity)

    def get_inventory(self):
        return {product_id: vars(item) for product_id, item in self.items.items()}
