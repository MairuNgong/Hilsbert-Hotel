import time
import sys
from HashMap import HashMap
from AVLTree import AVLTree
from random import choice as ch

class HilbertsHotel:
    def __init__(self):
        self.rooms = HashMap()  # HashMap to store guest data
        self.empty_rooms = set()  # Set to track empty rooms
        self.channel_data = HashMap()  # HashMap to store the channel from which the guest arrived
        self.avl_tree = AVLTree()  # AVL Tree for room number sorting
        self.avl_tree.root = None  
  
    def add_guest(self, room_number, channel):
        start_time = time.time()
        if self.rooms.contains(room_number):
            print(f"Room {room_number} is already occupied.")
        else:
            self.rooms.insert(room_number, True)
            self.channel_data.insert(room_number, channel)
            self.avl_tree.root = self.avl_tree.insert(self.avl_tree.root, room_number)  # Add room number to AVL Tree
            if room_number in self.empty_rooms:
                self.empty_rooms.remove(room_number)
            print(f"Guest added to room {room_number} from channel {channel}.")
        end_time = time.time()
        print(f"Time to add guest: {end_time - start_time:.6f} seconds.")

    def remove_guest(self, room_number):
        start_time = time.time()
        if self.rooms.contains(room_number):
            self.rooms.remove(room_number)
            self.channel_data.remove(room_number)
            self.avl_tree.root = self.avl_tree.delete_node(self.avl_tree.root, room_number)  # Remove room number from AVL Tree
            self.empty_rooms.add(room_number)
            print(f"Guest removed from room {room_number}.")
        else:
            print(f"Room {room_number} is already empty.")
        end_time = time.time()
        print(f"Time to remove guest: {end_time - start_time:.6f} seconds.")

    def sort_rooms(self):
        start_time = time.time()
        sorted_rooms = self.avl_tree.get_sorted_rooms()
        end_time = time.time()
        print(f"Sorted rooms: {sorted_rooms}")
        print(f"Time to sort rooms: {end_time - start_time:.6f} seconds.")
        return sorted_rooms

    def search_room(self, room_number):
        start_time = time.time()
        if self.rooms.contains(room_number):
            print(f"Room {room_number} is occupied by a guest.")
        else:
            print(f"Room {room_number} is empty.")
        end_time = time.time()
        print(f"Time to search room: {end_time - start_time:.6f} seconds.")

    def display_empty_rooms(self):
        start_time = time.time()
        total_empty = len(self.empty_rooms)
        print(f"Number of empty rooms: {total_empty}")
        end_time = time.time()
        print(f"Time to display empty rooms: {end_time - start_time:.6f} seconds.")
        return total_empty

    def display_memory_usage(self):
        rooms_memory = sys.getsizeof(self.rooms)
        channel_data_memory = sys.getsizeof(self.channel_data)
        empty_rooms_memory = sys.getsizeof(self.empty_rooms)
        total_memory = rooms_memory + channel_data_memory + empty_rooms_memory
        print(f"-->Memory usage (in bytes): Rooms: {rooms_memory}, Channel Data: {channel_data_memory}, Empty Rooms: {empty_rooms_memory}")
        print(f"Total memory usage: {total_memory} bytes.")
        return total_memory

    def write_output_to_file(self, file_name):
        start_time = time.time()
        with open(file_name, 'w') as f:
            for room in self.rooms.keys():
                channel = self.channel_data.get(room)
                f.write(f"Room {room}, Channel = {channel}\n")
        end_time = time.time()
        print(f"Data written to {file_name}. Time: {end_time - start_time:.6f} seconds.")


if __name__ == "__main__":
    hotel = HilbertsHotel()
    chanel = ['Channel 1', 'Channel 2', 'Channel 3']

    for i in range(1000):
        hotel.add_guest(i, ch(chanel))

    # Writing data to file
    hotel.write_output_to_file('hilberts_hotel_output.txt')
