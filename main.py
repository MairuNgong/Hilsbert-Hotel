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
          i = 1  # Counter to track how many attempts
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


initial_guest = int(input("Initail Guest: "))
for i in range(initial_guest) :
    hotel.add_room(0, 0, 0, i)
while (True) :
    print("===================================")
    print("MENU: ")
    print("1. add guest")
    print("2. print sort room")
    print("3. print empty room")
    print("4. search room")
    print("5. remove room")
    print("6. save to file")
    print("x. exit..")
    opt = input("select: ")
    if opt == '1' :
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("1.  add n guest")
        print("2.  add n guest on m bus")
        print("3.  add n guest on m bus on l ship")
        print("4.  add n guest on m bus on l ship in k fleet")
        opt = input("select: ")
        if opt == "1" :
            print("add n guest")
            n = int(input("n = "))
            for a in range(n) : hotel.add_room(0, 0, 0, b)
        elif opt == "2" :
            print("add n guest on m bus")
            n = int(input("n = "))
            m = int(input("m = "))
            for b in range(m) :
                for a in range(n) : hotel.add_room(0, 0, a, b)
        elif opt == "3" :
            print("add n guest on m bus on l ship")
            n = int(input("n = "))
            m = int(input("m = "))
            l = int(input("l = "))
            for c in range(l) :
                for b in range(m) :
                    for a in range(n) : hotel.add_room(0, c, b, a)
        elif opt == "4" :
            print("add n guest on m bus on l ship in k fleet")
            n = int(input("n = "))
            m = int(input("m = "))
            l = int(input("l = "))
            k = int(input("k = "))
            for d in range(k) :
                for c in range(l) :
                    for b in range(m) :
                        for a in range(n) : hotel.add_room(d, c, b, a)

    elif opt == '2' :
        print("Sorted Rooms:", hotel.sort_rooms())
    elif opt == '3' :
        print("Empty Rooms:", hotel.empty_rooms())
    elif opt == '4' :
        room_number = int(input("room number : "))
        print("Find room",room_number,":", hotel.find_room(room_number))
    elif opt == '5' :
        room_number = int(input("room number : "))
        hotel.remove_room(room_number)
    elif opt == '6' :
        hotel.save_to_file("./hotel_rooms.csv")
    elif opt == 'x' :
        break
    else :
        print("selection invalid!")
