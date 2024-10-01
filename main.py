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

    # Get all keys in the HashMap (for debugging purposes)
    def keys(self):
        all_keys = []
        for bucket in self.table:
            for pair in bucket:
                all_keys.append(pair[0])
        return all_keys

# Node class for the AVL tree
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # New nodes are initially added at leaf

# AVL Tree for maintaining sorted rooms
class AVLTree:
    def insert(self, root, key):
        # 1. Perform the normal BST insertion
        if root is None:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2. Update the height of this ancestor node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Get the balance factor
        balance = self.get_balance(root)

        # If the node becomes unbalanced, then there are 4 cases

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete_node(self, root, key):
        # STEP 1: PERFORM STANDARD BST DELETE
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

            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right, temp.key)

        # STEP 2: UPDATE HEIGHT OF THIS ANCESTOR NODE
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # STEP 3: GET THE BALANCE FACTOR OF THIS ANCESTOR NODE
        balance = self.get_balance(root)

        # If this node becomes unbalanced, then there are 4 cases

        # Left Left Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right Case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left Case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self, root, sorted_rooms):
        if root:
            self.inorder_traversal(root.left, sorted_rooms)
            sorted_rooms.append(root.key)
            self.inorder_traversal(root.right, sorted_rooms)

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
        self.avl_tree = AVLTree()  # AVL Tree for room number sorting
        self.avl_tree.root = None  # Initialize root of AVL tree

    # Function to add a guest manually
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

    # Function to remove a guest manually
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

    # Function to sort room numbers
    def sort_rooms(self):
        start_time = time.time()
        sorted_rooms = self.avl_tree.get_sorted_rooms()
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
    chanel = ['Channel 1', 'Channel 2', 'Channel 3']

    # Adding guests to rooms
    for i in range(2000000):
        hotel.add_guest(i, ch(chanel))

    # Writing data to file
    hotel.write_output_to_file('hilberts_hotel_output.txt')
