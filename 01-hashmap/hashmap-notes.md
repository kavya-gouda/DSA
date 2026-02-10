## HashMap (Beginner to Advanced)

### 1. What is a HashMap?

- **High-level idea**: A HashMap (or hash table, dictionary, map) stores data as **key → value** pairs and lets you:
  - Insert a value by key
  - Look up a value by key
  - Delete a value by key
- **Goal**: Do these operations in **average \(O(1)\)** time.

Common names:
- **Java**: `HashMap<K, V>`
- **C++**: `unordered_map<Key, T>`
- **Python**: `dict`
- **JavaScript**: `Map` (and plain objects `{}` used as maps)

### 2. Core Concepts and Terminology

- **Key**: The identifier (e.g. string `"abc"`, int `42`).
- **Value**: The data stored (e.g. `user`, `count`, `price`).
- **Hash function**: A function that converts a key into an integer:
  \[
  \text{index} = \text{hash(key)} \bmod \text{capacity}
  \]
- **Bucket**: A slot in the underlying array. Many languages implement a hash map as:
  - An **array of buckets** internally.
- **Collision**: When two different keys map to the **same bucket index**.
- **Load factor**:
  \[
  \text{load factor} = \frac{\text{number of stored entries}}{\text{number of buckets}}
  \]
  - When load factor gets too high, performance degrades.
  - Implementation usually **resizes** (grows the array) when load factor crosses a threshold (like 0.75).

### 3. Internal Structure (Conceptual)

Think of a HashMap as:

```text
index:   0      1      2      3      4      5
bucket: [ - ]  [ - ]  [ - ]  [ - ]  [ - ]  [ - ]
```

Steps when inserting `(key, value)`:
1. Compute `h = hash(key)`.
2. Compute `index = h % capacity`.
3. Go to `bucket[index]` and insert the pair there.

When we **search** for a key:
1. Compute `h = hash(key)`.
2. Compute `index = h % capacity`.
3. Look in `bucket[index]` for that key, and if found, return its value.

### 4. How Do We Handle Collisions?

Two popular strategies:

#### 4.1 Separate Chaining (Very common in interviews)

- Each **bucket is a list** (linked list or dynamic array) of entries.
- Each entry: `(key, value, next)` if using a linked list.
- On **collision**, you simply append another `(key, value)` to the bucket's list.

Pros:
- Easy to implement.
- Works well until buckets get very long.

Cons:
- In worst case (all keys collide), time becomes \(O(n)\).

#### 4.2 Open Addressing (Used by some languages, e.g. some C++ implementations)

- Each bucket can hold **at most one** key-value pair.
- On collision, we **probe** (look at other indices) according to a rule:
  - **Linear probing**: try `i, i+1, i+2, ...` (wrapping around).
  - **Quadratic probing**: try `i, i+1^2, i+2^2, ...`.
  - **Double hashing**: use a second hash function for step size.

Pros:
- Better cache locality (everything in one array).

Cons:
- More complex to implement deletions.
- Sensitive to the choice of hash function and probing scheme.

### 5. Time and Space Complexity

For a well-designed hash map with a good hash function and a controlled load factor:

- **Average case**:
  - Insert: \(O(1)\)
  - Search: \(O(1)\)
  - Delete: \(O(1)\)
- **Worst case**:
  - All of them can degrade to \(O(n)\) if many keys collide badly.
- **Space complexity**:
  - \(O(n)\) to store `n` key-value pairs plus overhead for buckets.

### 6. Simple Pseudocode Implementation (Separate Chaining)

#### 6.1 Data Structures

```text
Entry:
  key
  value
  next  (pointer to next Entry)

HashMap:
  buckets: array of Entry* (size = capacity)
  size: number of key-value pairs
  capacity: length of buckets array
```

#### 6.2 Hash Function (Example Idea)

For integers:

```text
hash(key) = key
```

For strings (simple polynomial rolling hash idea):

```text
hash(s) = (s[0]*p^0 + s[1]*p^1 + ... + s[n-1]*p^(n-1)) mod M
```

Where:
- \(p\) is a small prime (e.g. 31, 131).
- \(M\) is a large prime (e.g. \(10^9 + 7\)).

#### 6.3 Insert (Put)

High level pseudocode (separate chaining):

```text
function put(key, value):
    index = hash(key) mod capacity
    head = buckets[index]

    # Check if key already exists; if so, update
    node = head
    while node != null:
        if node.key == key:
            node.value = value
            return
        node = node.next

    # Insert new node at head
    newNode = new Entry(key, value, next = head)
    buckets[index] = newNode
    size += 1

    if loadFactor() > threshold:
        resize()
```

#### 6.4 Get (Search)

```text
function get(key):
    index = hash(key) mod capacity
    node = buckets[index]

    while node != null:
        if node.key == key:
            return node.value
        node = node.next

    return NOT_FOUND
```

#### 6.5 Remove (Delete)

```text
function remove(key):
    index = hash(key) mod capacity
    node = buckets[index]
    prev = null

    while node != null:
        if node.key == key:
            if prev == null:
                buckets[index] = node.next
            else:
                prev.next = node.next
            size -= 1
            return
        prev = node
        node = node.next
```

### 7. Resizing and Rehashing

When load factor exceeds a threshold (e.g. 0.75):

1. **Create a new buckets array** with larger capacity, usually:
   - `newCapacity = oldCapacity * 2` (and often rounded to a power of 2 or a prime).
2. **Rehash all existing keys** into the new array:
   - For each old entry `(key, value)`:
     - Recompute `index = hash(key) % newCapacity`.
     - Insert into the new buckets.

This **rehashing** step is \(O(n)\), but it doesn’t happen on every operation, so the **amortized** cost of insert remains \(O(1)\).

### 8. Practical Usage Patterns in DSA Problems

Hash maps are extremely useful in coding interviews and competitive programming. Here are common patterns:

#### 8.1 Frequency Counting

- **Problem pattern**: "Find the most frequent element", "check if two strings are anagrams", etc.
- Approach:
  - Iterate through items.
  - Maintain `freq[key] = count`.

Example pseudocode:

```text
freq = empty map
for each x in array:
    if x not in freq:
        freq[x] = 0
    freq[x] += 1
```

#### 8.2 Two Sum / Pair with Given Sum

- **Problem pattern**: Does there exist `i, j` such that `a[i] + a[j] = target`?
- Approach:
  - For each number `x`, check if `target - x` has been seen before.
  - Use a hash map to store `value → index`.

Pseudocode:

```text
map = empty map   # value -> index
for i from 0 to n-1:
    complement = target - a[i]
    if complement in map:
        return (map[complement], i)
    map[a[i]] = i
```

#### 8.3 Prefix Sum with Hash Map

- **Problem pattern**: Subarray sum equals `k`, or longest subarray with sum `k`.
- Approach:
  - Maintain prefix sum `prefix[i]`.
  - At index `i` with sum `S`, we want a previous prefix sum `S - k`.
  - Store `sum → earliest index` in a map.

Pseudocode (counting subarrays with sum = k):

```text
map = {0: 1}   # sum 0 occurs once (before we start)
sum = 0
count = 0

for x in array:
    sum += x
    if (sum - k) in map:
        count += map[sum - k]
    if sum in map:
        map[sum] += 1
    else:
        map[sum] = 1
```

#### 8.4 Sliding Window with HashMap

- **Problem pattern**: Longest substring without repeating characters, at most `k` distinct characters, etc.
- Approach:
  - Use two pointers `left`, `right`.
  - Use map to track character counts (or last seen index).

Example: length of longest substring without repeating characters:

```text
map = empty map  # char -> last index
left = 0
best = 0

for right from 0 to n-1:
    c = s[right]
    if c in map and map[c] >= left:
        left = map[c] + 1
    map[c] = right
    best = max(best, right - left + 1)
```

### 9. Important Practical Details

#### 9.1 Good Keys for HashMaps

- Prefer **immutable** keys (especially in Java, C++):
  - Numbers (`int`, `long`).
  - Strings that are not modified after insertion.
  - Immutable structs/objects (all fields are final/const).
- If keys are mutable and you change a field that affects the hash or equality, the entry can become "lost" in the table.

#### 9.2 Equality and Hash

For custom key types, you must define:
- A **hash function**: `hash(key)` that is:
  - Deterministic (same key → same hash every time).
  - Distributes keys fairly uniformly.
- An **equality** comparison: two keys that are equal **must** have the same hash.

In many languages:
- **Java**: if you override `equals`, you must override `hashCode` with the contract:
  - If `a.equals(b)` then `a.hashCode() == b.hashCode()`.
- **C++ `unordered_map`**: you can define `std::hash<Key>` and `operator==`.

#### 9.3 Load Factor and Performance

- Larger load factor =>
  - Less memory.
  - But higher chance of collisions → slower operations.
- Smaller load factor =>
  - More memory.
  - Fewer collisions → faster operations.

Typical default load factors:
- Java `HashMap`: `0.75`.

### 10. HashMap vs Other Data Structures

- **HashMap vs Array**:
  - Array: index must be an integer and usually small range; access is O(1).
  - HashMap: keys can be any hashable type (string, object, etc.), O(1) average.
- **HashMap vs TreeMap / map (ordered)**:
  - HashMap: average O(1) operations, **no ordering** of keys.
  - TreeMap (balanced BST): O(\(\log n\)) operations, keys kept **sorted**.
- **HashMap vs Set**:
  - Set is usually implemented with a hash map **without values** (or dummy values).

### 11. Advanced Topics (High-Level)

You rarely need to implement these in interviews, but you should know them conceptually:

- **Perfect hashing**:
  - Hash function with no collisions for a fixed set of keys.
- **Cuckoo hashing**:
  - Uses two hash functions and can move elements around ("kicking out") on insert.
  - Guarantees O(1) lookup with high probability.
- **Concurrent hash maps**:
  - Thread-safe hash maps that allow concurrent reads/writes.
  - Use techniques like lock striping or lock-free algorithms.
- **Robin Hood hashing** (open addressing variant):
  - Aims to equalize the probe lengths, improving worst-case behavior.

### 12. How to Think About HashMap Problems in Interviews

When you see:
- **"Find if something appears more than once"** → consider a `set` or `map`.
- **"Count frequency"** → `map<value, count>`.
- **"Lookup by some ID / key quickly"** → `map<key, value>`.
- **"Subarray / substring with some property"** → often `prefix sums + map` or `sliding window + map`.

General thought process:
1. Ask: *Can I use a map from X to Y to store partial information I need?*
2. Typical mappings:
   - value → count
   - value → first index / last index
   - prefix sum → number of occurrences
   - character → last seen index
3. Analyze complexity:
   - If each access to the map is O(1) average, and you traverse the array/string once, you get O(n) time.

### 13. Summary (Key Points to Remember)

- **HashMap = key → value with O(1) average operations.**
- Uses:
  - **Hash function** to compute index into an array of **buckets**.
  - **Collision handling** via separate chaining or open addressing.
  - **Resizing** when load factor is high; this keeps average O(1) time.
- In problems:
  - Think **frequency maps**, **presence checks**, **two-sum**, **prefix sums**, **sliding windows**.
- Implementation details (when coding your own):
  - Correct hash function and equality.
  - Handle collisions properly.
  - Implement resize/rehash.

Use this file as a quick reference:
- Before interviews or practice sessions, skim **Sections 2–5**.
- For problem patterns, revisit **Section 8**.
- For conceptual depth, refer to **Sections 7, 9–11**.

---

## 14. Python: Custom HashMap & Built-in `dict`

### 14.1 Built-in Usage

In Python, use **`dict`** for hashmaps. It's highly optimized and supports:

```python
d = {}
d["a"] = 1
d["b"] = 2
print(d["a"])           # 1
print(d.get("c", -1))   # -1 (default if missing)
print("a" in d)         # True
del d["b"]
for k, v in d.items():
    print(k, v)
```

- **Keys**: must be **hashable** (immutable: `int`, `str`, `tuple`, etc.). Lists and dicts cannot be keys.
- **`collections.defaultdict`**: dict that auto-creates default values for missing keys (e.g. `defaultdict(int)` for frequency counts).

### 14.2 Custom Implementation (Learning)

See **`hashmap.py`** in the repo root for a minimal HashMap with:

- Separate chaining (list of `_Entry` nodes per bucket).
- `put`, `get`, `remove`, `__contains__`, `__getitem__`, `__setitem__`.
- Resize when load factor ≥ 0.75.

Run it:

```bash
python hashmap.py
```

### 14.3 Python Idioms for HashMap Problems

| Pattern | Idiom |
|--------|--------|
| Frequency count | `from collections import Counter` or `defaultdict(int)` |
| First/last index | `dict[key] = index` (overwrite for last) |
| Presence check | `key in d` or `d.get(key) is not None` (if None not stored) |
| Default value | `d.get(key, default)` or `defaultdict(lambda: value)` |

---

## 15. Practice Problems (Easy → Hard)

Use **hashmap / dict** (and sometimes **set**) for these. Order: easy → medium → hard.

### Easy

| # | Problem | Idea |
|---|--------|------|
| 1 | **Two Sum** – indices where `nums[i] + nums[j] = target` | Map `value → index`; for each `x` check `target - x` in map. |
| 2 | **First Unique Character** – first non-repeating char in string | Frequency map; then scan string for first char with count 1. |
| 3 | **Valid Anagram** – are two strings anagrams? | Count chars in first string; decrement with second; all counts 0. |
| 4 | **Contains Duplicate** – any duplicate in array? | Use a set (or dict) of seen values. |
| 5 | **Intersection of Two Arrays** | Set of one array; collect from other if in set. |

### Medium

| # | Problem | Idea |
|---|--------|------|
| 6 | **Group Anagrams** – group strings that are anagrams | Key = sorted string (or tuple of counts); value = list of strings. |
| 7 | **Subarray Sum Equals K** – count subarrays with sum = k | Prefix sum + map: `prefix_count[sum - k]`; maintain `prefix_count`. |
| 8 | **Longest Substring Without Repeating Characters** | Sliding window + map: `char → last index`; move `left` on repeat. |
| 9 | **Longest Consecutive Sequence** – longest consecutive integers in unsorted array | Put all in set; for each `x`, if `x-1` not in set, extend streak from `x`. |
| 10 | **Top K Frequent Elements** | Frequency map; then bucket by frequency or heap (or quickselect). |

### Hard

| # | Problem | Idea |
|---|--------|------|
| 11 | **Substring with Concatenation of All Words** | Sliding window; map word → count; match window counts. |
| 12 | **Minimum Window Substring** – smallest window containing all chars of target | Two pointers + two maps (need vs have); shrink when valid. |
| 13 | **LFU Cache** | HashMap + frequency structure (e.g. dict of doubly linked lists per frequency). |

### Where to Find Them

- **LeetCode**: Search by problem name (e.g. "Two Sum", "Group Anagrams").
- **Practice order**: Do Easy 1–5, then Medium 6–10; use **Section 8** for pattern hints.

