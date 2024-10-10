import pandas as pd
import sys
import time
from AVLTree import AVLTree
from HashMap import HashTable

class Hotel:
    def __init__(self, size: int = 100):
        self.avl_tree = AVLTree()
        self.root = None
        self.hash_table = HashTable(size)
        self.max_room_number = 0

    def calculate_room_number(self, fleet: int, ship: int, bus: int, guest: int) -> int:
        return (fleet ** 7) * (ship ** 5) * (bus ** 3) * (guest ** 2)

    def add_room(self, fleet: int, ship: int, bus: int, guest: int) -> int:
        start_time = time.time()
        room_number = self.calculate_room_number(fleet, ship, bus, guest)
        if self.hash_table.search(room_number) is None:
            self.hash_table.insert(room_number, (fleet, ship, bus, guest))
            self.max_room_number = max(self.max_room_number, room_number)
            end_time = time.time()
        print(f"Time taken for add_room: {end_time - start_time} seconds")
        return room_number

    def remove_room(self, room_number: int):
        start_time = time.time()
        if self.hash_table.search(room_number):
            self.hash_table.remove(room_number)
        end_time = time.time()
        print(f"Time taken for remove_room: {end_time - start_time} seconds")

    def sort_rooms(self):
        start_time = time.time()
        result = []
        self.avl_tree.inorder_traversal(self.root, result)
        end_time = time.time()
        print(f"Time taken for sort_rooms: {end_time - start_time} seconds")
        return result

    def find_room(self, room_number: int):
        start_time = time.time()
        result = self.hash_table.search(room_number)
        end_time = time.time()
        print(f"Time taken for find_room: {end_time - start_time} seconds")
        return result

    def empty_rooms(self) -> int:
        start_time = time.time()
        total_rooms = self.max_room_number
        room_count = sum(len(bucket) for bucket in self.hash_table.table)
        end_time = time.time()
        print(f"Time taken for empty_rooms: {end_time - start_time} seconds")
        return total_rooms - room_count

    def save_to_file(self, file_name: str):
        start_time = time.time()
        data = [(key, value) for bucket in self.hash_table.table for key, value in bucket]
        df = pd.DataFrame(data, columns=["Room Number", "Details"])
        df.to_csv(file_name, index=False)
        end_time = time.time()
        print(f"Time taken for save_to_file: {end_time - start_time} seconds")

    def memory_usage(self):
        return sys.getsizeof(self.hash_table) + sys.getsizeof(self.root)

hotel = Hotel(size=100)

for i in range(2000) :
    hotel.add_room(1, 1, 1, i)


sorted_rooms = hotel.sort_rooms()
print("Sorted Rooms:", sorted_rooms)


print("number of empty room:", hotel.empty_rooms())

print("Find room 1050:", hotel.find_room(100))

hotel.save_to_file("./hotel_rooms.csv")

print("Memory Usage:", hotel.memory_usage())
