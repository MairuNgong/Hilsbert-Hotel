import pandas as pd
import sys
import time
from AVLTree import AVLTree
from HashMap import HashTable

import time

def exec_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time()
        print(f"{func.__name__} takes {stop - start:.4f} seconds")
        return result
    return wrapper

class Hotel:
    def __init__(self, size: int = 100):
        self.avl_tree = AVLTree()
        self.root = None
        self.hash_table = HashTable(size)
        self.max_room_number = 0

    def calculate_room_number(self, fleet: int, ship: int, bus: int, guest: int) -> int:
        return (fleet ** 7) * (ship ** 5) * (bus ** 3) * (guest ** 2)

    @exec_time
    def add_room(self, fleet: int, ship: int, bus: int, guest: int) -> int:
        room_number = self.calculate_room_number(fleet, ship, bus, guest)
        if self.hash_table.search(room_number) is None:
            self.hash_table.insert(room_number, (fleet, ship, bus, guest))
            self.root = self.avl_tree.insert(self.root,room_number)
            self.max_room_number = max(self.max_room_number, room_number)
        return room_number

    @exec_time
    def remove_room(self, room_number: int):
        if self.hash_table.search(room_number):
            self.hash_table.remove(room_number)

    @exec_time
    def sort_rooms(self):
        result = []
        self.avl_tree.inorder_traversal(self.root, result)
        return result

    @exec_time
    def find_room(self, room_number: int):
        result = self.hash_table.search(room_number)
        return result

    @exec_time
    def empty_rooms(self) -> int:
        total_rooms = self.max_room_number
        room_count = sum(len(bucket) for bucket in self.hash_table.table)
        return total_rooms - room_count

    @exec_time
    def save_to_file(self, file_name: str):
        data = [(key, value) for bucket in self.hash_table.table for key, value in bucket]
        df = pd.DataFrame(data, columns=["Room Number", "Details"])
        df.to_csv(file_name, index=False)

    def memory_usage(self):
        return sys.getsizeof(self.hash_table) + sys.getsizeof(self.root)

hotel = Hotel(size=100)

for i in range(10) :
    for j in range(3):
        hotel.add_room(1,1,j,i)

sorted_rooms = hotel.sort_rooms()

print("Sorted Rooms:", sorted_rooms)


print("number of empty room:", hotel.empty_rooms())



print("Find room 128:", hotel.find_room(128))

hotel.remove_room(128)

print("Find room 128:", hotel.find_room(128))

hotel.save_to_file("./hotel_rooms.csv")

print("Memory Usage:", hotel.memory_usage())
