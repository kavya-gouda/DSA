"""
Custom HashMap implementation in Python (separate chaining).
For learning DSA — in practice use built-in dict.
"""


class _Entry:
    """Single key-value node in a bucket chain."""

    __slots__ = ("key", "value", "next")

    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class HashMap:
    """
    HashMap with separate chaining.
    - put(key, value): O(1) average
    - get(key): O(1) average
    - remove(key): O(1) average
    - Keys must be hashable (immutable).
    """

    DEFAULT_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, capacity=None):
        cap = capacity or self.DEFAULT_CAPACITY
        self._buckets = [None] * cap
        self._size = 0
        self._capacity = cap

    def _index(self, key):
        """Compute bucket index from key."""
        return hash(key) % self._capacity

    def put(self, key, value):
        """Insert or update key -> value."""
        idx = self._index(key)
        head = self._buckets[idx]

        # Update if key exists
        node = head
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        # Insert at head of chain
        self._buckets[idx] = _Entry(key, value, self._buckets[idx])
        self._size += 1

        if self._load_factor() >= self.LOAD_FACTOR_THRESHOLD:
            self._resize()

    def get(self, key, default=None):
        """Return value for key, or default if not found."""
        idx = self._index(key)
        node = self._buckets[idx]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return default

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)
        return self.get(key, None)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        idx = self._index(key)
        node = self._buckets[idx]
        while node is not None:
            if node.key == key:
                return True
            node = node.next
        return False

    def remove(self, key):
        """Remove key. No-op if key not present."""
        idx = self._index(key)
        node = self._buckets[idx]
        prev = None
        while node is not None:
            if node.key == key:
                if prev is None:
                    self._buckets[idx] = node.next
                else:
                    prev.next = node.next
                self._size -= 1
                return
            prev = node
            node = node.next

    def _load_factor(self):
        return self._size / self._capacity

    def _resize(self):
        """Double capacity and rehash all entries."""
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for head in old_buckets:
            node = head
            while node is not None:
                self.put(node.key, node.value)
                node = node.next

    def __len__(self):
        return self._size

    def keys(self):
        """Yield all keys."""
        for head in self._buckets:
            node = head
            while node is not None:
                yield node.key
                node = node.next

    def values(self):
        """Yield all values."""
        for head in self._buckets:
            node = head
            while node is not None:
                yield node.value
                node = node.next

    def items(self):
        """Yield all (key, value) pairs."""
        for head in self._buckets:
            node = head
            while node is not None:
                yield (node.key, node.value)
                node = node.next


# --- Example usage (same interface as dict for basic ops) ---
if __name__ == "__main__":
    m = HashMap()
    m.put("a", 1)
    m.put("b", 2)
    m["c"] = 3
    print(m.get("a"), m["b"], m.get("x", -1))  # 1 2 -1
    print(len(m), list(m.keys()))               # 3 ['a', 'b', 'c']
    m.remove("b")
    print(len(m), "b" in m)                     # 2 False
