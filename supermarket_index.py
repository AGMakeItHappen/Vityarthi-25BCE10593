import json
import os
#importing json and os to create and use a file to store the indexes of added items in the Supermarket Item Index List

class SupermarketItem:
    # class to crete items and functions for the items including the attributes/ properties of the items like name, cost, sp, stock, serial number
    def __init__(self, serialnumber: str, name: str, cost: float, sellprice: float, stock: int):
        self.serialnumber = serialnumber
        self.name = name
        self.cost = cost
        self.sellprice = sellprice
        self.stock = stock

    def __str__(self):
        return f"Serial: {self.serialnumber} | Name: {self.name} | Cost: {self.cost:.2f} | Sell price: {self.sellprice:.2f} | Stock: {self.stock}"

    def to_dict(self):
        return {
            'serialnumber': self.serialnumber,
            'name': self.name,
            'cost': self.cost,
            'sellprice': self.sellprice,
            'stock': self.stock
        }

    @staticmethod
    def from_dict(d):
        return SupermarketItem(
            d['serialnumber'], d['name'], d['cost'], d['sellprice'], d['stock']
        )


class SupermarketIndex:
    FILENAME = 'items.json'

    def __init__(self):
        self.items = {}
        self.load_items()

    def save_items(self):
        with open(self.FILENAME, 'w') as f:
            json.dump([item.to_dict() for item in self.items.values()], f, indent=2)

    def load_items(self):
        if os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'r') as f:
                try:
                    items_list = json.load(f)
                    self.items = {item['serialnumber']: SupermarketItem.from_dict(item) for item in items_list}
                except Exception:
                    self.items = {}

    def additem(self, serialnumber, name, cost, sellprice, stock):
        if serialnumber in self.items:
            print("Item with this serial number already exists.")
            return
        item = SupermarketItem(serialnumber, name, cost, sellprice, stock)
        self.items[serialnumber] = item
        self.save_items()
        print("Item added successfully.")
        self.lowstocklossalert(item)

    def listitems(self):
        if not self.items:
            print("No items in index.")
            return
        print("--- Supermarket Item Index ---")
        for item in self.items.values():
            print(item)
            self.lowstocklossalert(item)
        print("------------------------------")

    def finditem(self, serialnumber):
        return self.items.get(serialnumber)

    def updatestock(self, serialnumber, newstock):
        item = self.finditem(serialnumber)
        if item is None:
            print("Item not found.")
            return
        item.stock = newstock
        self.save_items()
        print("Stock updated successfully.")
        self.lowstocklossalert(item)

    def removeitem(self, serialnumber):
        if serialnumber in self.items:
            del self.items[serialnumber]
            self.save_items()
            print("Item removed successfully.")
        else:
            print("Item not found.")

    def lowstocklossalert(self, item):
        if item.stock < 100 and item.sellprice < item.cost:
            print(
                f"ALERT! Item {item.name} (Serial: {item.serialnumber}) has low stock ({item.stock}) and is being sold at a loss! Cost price: {item.cost:.2f}, Sell price: {item.sellprice:.2f}")


def printmenu():
    print("--- Supermarket Item Index ---")
    print("1. Add item")
    print("2. List all items")
    print("3. Update item stock")
    print("4. Remove an item")
    print("5. Stop/Quit")


def main():
    index = SupermarketIndex()
    # making sure that the code runs when main is called
    while True:
        printmenu()
        # calling the menu function made above
        choice = input("Enter your choice (1-5): ").strip()
        # showing choices using if/elif statements for the person to choose what to do next
        if choice == "1":
            print("Add a new item")
            serial = input("Serial number: ").strip()
            name = input("Item name: ").strip()
            try:
                cost = float(input("Cost: "))
                sellprice = float(input("Sell price: "))
                stock = int(input("Number of items in stock: "))
            except ValueError:
                print("Invalid number entered. Item not added.")
                continue
            index.additem(serial, name, cost, sellprice, stock)
        elif choice == "2":
            index.listitems()
        elif choice == "3":
            print("Update stock")
            serial = input("Serial number: ").strip()
            try:
                newstock = int(input("New stock value: "))
            except ValueError:
                print("Invalid stock value.")
                continue
            index.updatestock(serial, newstock)
        elif choice == "4":
            print("Remove item")
            serial = input("Serial number: ").strip()
            index.removeitem(serial)
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
