
class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name}\t{self.quantity}\t${self.price:.2f}\t${self.total_price():.2f}"

class Receipt:
    def __init__(self, store_name, store_address, seller_name, stock_manager):
        self.store_name = store_name
        self.store_address = store_address
        self.seller_name = seller_name
        self.stock_manager = stock_manager
        self.items = []

    def add_item(self, product_id, quantity):
        # Check if the product is in stock
        if product_id not in self.stock_manager.items:
            raise ValueError("Product not found in stock")
        
        # Check if enough quantity is available
        stock_item = self.stock_manager.items[product_id]
        if quantity > stock_item.quantity:
            raise ValueError("Not enough stock available")
        
        # Update stock and add item to the receipt
        self.stock_manager.sell_product(product_id, quantity)
        self.items.append(Item(stock_item.name, stock_item.price, quantity))

    def total(self):
        return sum(item.total_price() for item in self.items)

    def __str__(self):
        receipt_str = f"{self.store_name}\n{self.store_address}\n\nVendeur : {self.seller_name}\n\n"
        receipt_str += "Article\tQté\tPrix\tTotal\n"
        receipt_str += "\n".join(str(item) for item in self.items)
        receipt_str += f"\n\nTotal à payer: ${self.total():.2f}"
        return receipt_str

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
# Example usage:
stock_manager = StockManager()
stock_manager.add_product("001", "Apple", 0.50, 100)  # Add 100 apples at 0.50 each
stock_manager.add_product("002", "Milk", 1.50, 50)    # Add 50 milk at 1.50 each

# Create a receipt with the store details and the stock manager
receipt = Receipt("Supermarché Exemple", "123 Rue Exemple", "Jean Dupont", stock_manager)

# Add some items to the receipt, which will also update the stock
receipt.add_item("001", 5)  # Add 5 apples to the receipt and deduct from stock
receipt.add_item("002", 2)  # Add 2 milk to the receipt and deduct from stock

# Print the receipt
print(receipt)

# Print the updated stock
print("\nUpdated Stock:")
print(stock_manager.get_inventory())