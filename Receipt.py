
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
    def __init__(self, store_name, store_address, seller_name):
        self.store_name = store_name
        self.store_address = store_address
        self.seller_name = seller_name
        self.items = []

    def add_item(self, name, price, quantity):
        self.items.append(Item(name, price, quantity))

    def total(self):
        return sum(item.total_price() for item in self.items)

    def __str__(self):
        receipt_str = f"{self.store_name}\n{self.store_address}\n\nVendeur : {self.seller_name}\n\n"
        receipt_str += "Article\tQté\tPrix\tTotal\n"
        receipt_str += "\n".join(str(item) for item in self.items)
        receipt_str += f"\n\nTotal à payer: ${self.total():.2f}"
        return receipt_str

