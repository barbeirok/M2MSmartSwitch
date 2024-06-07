class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def add(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def get(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        raise KeyError("Key not found")

    def remove(self, key):
        index = self._hash(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return
        raise KeyError("Key not found")

    def get_first_pair(self):
        for bucket in self.table:
            if bucket:
                return bucket[0][0]
        return None

    """def get_next_key_value(self, key):
        if key is None:
            return self.get_first_pair()
        all_pairs = []
        print(f"asdasd - {self.table}")
        for bucket in self.table:
            if bucket:
                for pair in bucket:
                    all_pairs.append(pair)
        for i, pair in enumerate(all_pairs):
            if pair[0] == key:
                if i + 1 < len(all_pairs):
                    print(all_pairs[i + 1])
                    return all_pairs[i + 1]
                else:
                    return None  # No next key-value pair found
        raise KeyError("Key not found")"""

    def get_next_key_value(self, key):
        found = False
        for bucket in self.table:
            for pair in bucket:
                if found:
                    return pair[0]
                if pair[0] == key:
                    found = True
        return self.get_first_pair()  # Retorna o primeiro par se a chave for None


    def print_table(self):
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"Bucket {i}: {bucket}")
            else:
                print(f"Bucket {i}: Empty")
