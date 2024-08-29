class SimpleHashset:
    def __init__(self, size):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def hash_function(self, value):
        sum = 0
        for ch in value:
            sum += ord(ch)
        return sum % 10

    def add(self, value):
        index = self.hash_function(value)
        bucket = self.buckets[index]
        if value not in bucket:
            bucket.append(value)

    def remove(self, value):
        index = self.hash_function(value)
        bucket = self.buckets[index]
        if value in bucket:
            bucket.remove(value)

    def print_set(self):
        print("contents in hash set: ")
        for index, bucket in enumerate(self.buckets):
            print(f"Bucket {index} : {bucket}")

hashset = SimpleHashset(size=10)
hashset.add("Reuben")
hashset.add("Mutuka")
hashset.add("Khisa")
hashset.print_set()
