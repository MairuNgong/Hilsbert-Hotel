class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]

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

    # Get all keys in the HashMap
    def keys(self):
        all_keys = []
        for bucket in self.table:
            for pair in bucket:
                all_keys.append(pair[0])
        return all_keys