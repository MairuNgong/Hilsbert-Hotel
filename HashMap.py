class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        bucket_index = self.hash_function(key)
        bucket = self.table[bucket_index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def search(self, key):
        bucket_index = self.hash_function(key)
        bucket = self.table[bucket_index]
        for k, v in bucket:
            if key == k:
                return v
        return None

    def remove(self, key):
        bucket_index = self.hash_function(key)
        bucket = self.table[bucket_index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                del bucket[i]
                return True
        return False

    def display(self):
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"Bucket {i}: {bucket}")