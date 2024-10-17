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
        self.hash_table = HashTable(size)
        self.root = None
        self.max_room_number = 0
        self.total_colli = 0

    def calculate_room_number(self, fleet: int, ship: int, bus: int, guest: int) -> int:
        return ((fleet+1) ** 7) * ((ship+1) ** 5) * ((bus+1) ** 3) * ((guest+1) ** 2)

    @exec_time
    def add_room(self, fleet: int, ship: int, bus: int, guest: int) -> int:
        room_number = self.calculate_room_number(fleet, ship, bus, guest)
        if self.hash_table.search(room_number) is None:
            self.hash_table.insert(room_number, (fleet, ship, bus, guest))
            self.root = self.avl_tree.insert(self.root,room_number)
            self.max_room_number = max(self.max_room_number, room_number)
        else:
          i = 1  
          while self.hash_table.search(room_number) is not None:
              self.total_colli += 1
              room_number += i ** 2
              i += 1
          
          self.hash_table.insert(room_number, (fleet, ship, bus, guest))
          self.root = self.avl_tree.insert(self.root, room_number)
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

#add person only
# for i in range(10) :
#     #Hotel start with room number 1
#     hotel.add_room(1,1,1,i)
# for i in range(10) :
#     #Hotel start with room number 1
#     hotel.add_room(0,0,0,i)

# #add person on bus on ship on fleet
# for i in range(10) :
#     hotel.add_room(1,1,1,i)


# room_number = 2

# sorted_rooms = hotel.sort_rooms()
# print("Sorted Rooms:", sorted_rooms)

# print("Total Collision:", hotel.total_colli)

# print("number of empty room:", hotel.empty_rooms())


# print("Find room",room_number,":", hotel.find_room(room_number))

# hotel.remove_room(room_number)
# print("Find room",room_number,":", hotel.find_room(room_number))
# print("number of empty room:", hotel.empty_rooms())

# hotel.save_to_file("./hotel_rooms.csv")

# print("Memory Usage:", hotel.memory_usage())
