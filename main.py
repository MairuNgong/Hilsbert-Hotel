import time
import sys
from random import choice as ch

# Implementation of a HashMap (open hashing)
class HashMap:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(size)]

    # Hash function to compute the index
    def _hash(self, key):
        return hash(key) % self.size

    # Insert a key-value pair into the HashMap
    def insert(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    # Retrieve a value by key from the HashMap
    def get(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

    # Delete a key-value pair from the HashMap
    def remove(self, key):
        index = self._hash(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return True
        return False

    # Check if a key exists in the HashMap
    def contains(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return True
        return False
# ==========================================================
    # Get all keys in the HashMap (for debugging purposes)
    def keys(self):
        all_keys = []
        for bucket in self.table:
            for pair in bucket:
                all_keys.append(pair[0])
        return all_keys
# ==========================================================

# Node class for the binary search tree
class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# Binary Search Tree (BST) for maintaining sorted rooms
class RoomBST:
    def __init__(self):
        self.root = None

    # Helper function to insert a key in the BST
    def insert(self, root, key):
        if root is None:
            return TreeNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    # Function to add a room number to the BST
    def add_room(self, key):
        self.root = self.insert(self.root, key)

    # Helper function to find the inorder successor (used in deletion)
    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Helper function to delete a key in the BST
    def delete_node(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right, temp.key)
        return root

    # Function to remove a room number from the BST
    def remove_room(self, key):
        self.root = self.delete_node(self.root, key)

    # Inorder traversal of the BST (sorted room numbers)
    def inorder_traversal(self, root, sorted_rooms):
        if root:
            self.inorder_traversal(root.left, sorted_rooms)
            sorted_rooms.append(root.key)
            self.inorder_traversal(root.right, sorted_rooms)

    # Get sorted list of room numbers
    def get_sorted_rooms(self):
        sorted_rooms = []
        self.inorder_traversal(self.root, sorted_rooms)
        return sorted_rooms

# Main class for Hilbert's Hotel
class HilbertsHotel:
    def __init__(self):
        self.rooms = HashMap()  # HashMap to store guest data
        self.empty_rooms = set()  # Set to track empty rooms
        self.channel_data = HashMap()  # HashMap to store the channel from which the guest arrived
        self.bst = RoomBST()  # Binary Search Tree for room number sorting

    # Function to add a guest manually
    def add_guest(self, room_number, channel):
        start_time = time.time()
        if self.rooms.contains(room_number):
            print(f"Room {room_number} is already occupied.")
        else:
            self.rooms.insert(room_number, True)
            self.channel_data.insert(room_number, channel)
            self.bst.add_room(room_number)  # Add room number to BST
            if room_number in self.empty_rooms:
                self.empty_rooms.remove(room_number)
            print(f"Guest added to room {room_number} from channel {channel}.")
        end_time = time.time()
        print(f"Time to add guest: {end_time - start_time:.6f} seconds.")

    # Function to remove a guest manually
    def remove_guest(self, room_number):
        start_time = time.time()
        if self.rooms.contains(room_number):
            self.rooms.remove(room_number)
            self.channel_data.remove(room_number)
            self.bst.remove_room(room_number)  # Remove room number from BST
            self.empty_rooms.add(room_number)
            print(f"Guest removed from room {room_number}.")
        else:
            print(f"Room {room_number} is already empty.")
        end_time = time.time()
        print(f"Time to remove guest: {end_time - start_time:.6f} seconds.")

    # Function to sort room numbers
    def sort_rooms(self):
        start_time = time.time()
        sorted_rooms = self.bst.get_sorted_rooms()
        end_time = time.time()
        print(f"Sorted rooms: {sorted_rooms}")
        print(f"Time to sort rooms: {end_time - start_time:.6f} seconds.")
        return sorted_rooms

    # Function to search for a room number
    def search_room(self, room_number):
        start_time = time.time()
        if self.rooms.contains(room_number):
            print(f"Room {room_number} is occupied by a guest.")
        else:
            print(f"Room {room_number} is empty.")
        end_time = time.time()
        print(f"Time to search room: {end_time - start_time:.6f} seconds.")

    # Function to display number of empty rooms
    def display_empty_rooms(self):
        start_time = time.time()
        total_empty = len(self.empty_rooms)
        print(f"Number of empty rooms: {total_empty}")
        end_time = time.time()
        print(f"Time to display empty rooms: {end_time - start_time:.6f} seconds.")
        return total_empty

    # Function to display memory usage
    def display_memory_usage(self):
        rooms_memory = sys.getsizeof(self.rooms)
        channel_data_memory = sys.getsizeof(self.channel_data)
        empty_rooms_memory = sys.getsizeof(self.empty_rooms)
        total_memory = rooms_memory + channel_data_memory + empty_rooms_memory
        print(f"-->Memory usage (in bytes): Rooms: {rooms_memory}, Channel Data: {channel_data_memory}, Empty Rooms: {empty_rooms_memory}")
        print(f"Total memory usage: {total_memory} bytes.")
        return total_memory

    # Function to write output to a file
    def write_output_to_file(self, file_name):
        start_time = time.time()
        with open(file_name, 'w') as f:
            for room in self.rooms.keys():
                channel = self.channel_data.get(room)
                f.write(f"Room {room}, Channel {channel}\n")
        end_time = time.time()
        print(f"Data written to {file_name}. Time: {end_time - start_time:.6f} seconds.")


# Example of using the HilbertsHotel class
if __name__ == "__main__":
    hotel = HilbertsHotel()
    chanel = ['chanel 1', 'chanel 2', 'chanel 3']

########################################
#    # import random                   #
#    # list1 = [1, 2, 3, 4, 5, 6]      #
#    # print(random.choice(list1))     #
########################################

    # Adding guests to rooms
    # hotel.add_guest(1, 'Channel 1')
    for i in range(100000) :
        hotel.add_guest(i, ch(chanel))

    # Removing a guest from a room

    # Sorting rooms

    # Searching for a specific room

    # Displaying number of empty rooms

    # Displaying memory usage

    # Writing data to file
    hotel.write_output_to_file('hilberts_hotel_output.txt')
