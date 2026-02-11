## Two-Pointer Technique (Beginner to Advanced)

### 1. What is Two-Pointer?

- **High-level idea**: You maintain **two indices** (pointers) into a sequence (array, string, linked list) and move them according to some rule. This often lets you solve in **one pass** instead of nested loops.
- **Goal**: Achieve **O(n)** or O(n log n) time with **O(1)** extra space (when not using auxiliary structures).

Why it works:
- Instead of checking every pair with two nested loops (O(n²)), you move pointers in a way that **eliminates impossible candidates** and only do O(n) steps.

---

### 2. Core Concepts and Terminology

- **Left pointer** (`left`, `i`, `slow`): Usually the “start” of a window or the slower-moving index.
- **Right pointer** (`right`, `j`, `fast`): Usually the “end” of a window or the faster-moving index.
- **Converging pointers**: Start at **opposite ends** and move toward each other (e.g. `left = 0`, `right = n - 1`).
- **Same-direction pointers**: Both move **left → right** (e.g. one “read” and one “write”, or sliding window).
- **Sliding window**: A contiguous segment `[left, right]`; you expand (`right++`) or shrink (`left++`) to maintain a condition.

---

### 3. When to Use Two-Pointer

| Scenario | Typical pattern |
|----------|------------------|
| Sorted array, find pair/triplet with given sum | Converging pointers |
| Palindrome check, compare from both ends | Converging pointers |
| In-place removal (duplicates, zeros, element) | Same-direction (read/write) |
| Subarray/substring with a condition (sum, distinct count) | Sliding window (two pointers) |
| Linked list: cycle, middle, nth-from-end | Slow + fast pointer |

---

### 4. Beginner Level

#### 4.1 Opposite-Direction (Converging) Pointers

Two pointers start at **opposite ends** and move toward each other. Best when the array is **sorted** (or can be sorted).

**Example: Two Sum in a sorted array**

Find two numbers that add up to `target`. Return their 1-based indices.

```python
def two_sum_sorted(arr: list[int], target: int) -> list[int]:
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left + 1, right + 1]  # 1-based
        if total < target:
            left += 1   # need larger sum
        else:
            right -= 1  # need smaller sum
    return []
```

- If `total < target`, we need a larger sum → move `left` right (bigger element).
- If `total > target`, we need a smaller sum → move `right` left (smaller element).

**Time**: O(n), **Space**: O(1).

---

#### 4.2 Valid Palindrome

Check if a string reads the same forward and backward (ignoring non-alphanumeric and case).

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

---

#### 4.3 Same-Direction: Read/Write Pointers

Both move left → right. One index **reads**, the other **writes** (e.g. in-place removal).

**Example: Remove duplicates in-place (sorted array)**

Return the new length; keep only unique elements at the front.

```python
def remove_duplicates(arr: list[int]) -> int:
    if not arr:
        return 0
    write = 0
    for read in range(1, len(arr)):
        if arr[read] != arr[write]:
            write += 1
            arr[write] = arr[read]
    return write + 1
```

**Example: Move zeros to end**

```python
def move_zeros(arr: list[int]) -> None:
    write = 0
    for read in range(len(arr)):
        if arr[read] != 0:
            arr[write], arr[read] = arr[read], arr[write]
            write += 1
```

---

### 5. Intermediate Level

#### 5.1 Sliding Window (Variable Size)

Maintain a window `[left, right]` and a condition (e.g. sum, count). Expand with `right`, shrink with `left` when the condition is violated.

**Example: Longest substring without repeating characters**

Use two pointers for the window and a **hashmap** to store the **last seen index** of each character.

```python
def length_of_longest_substring(s: str) -> int:
    seen = {}  # char -> last index
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in seen and seen[c] >= left:
            left = seen[c] + 1
        seen[c] = right
        best = max(best, right - left + 1)
    return best
```

This is **two-pointer + hashmap**: pointers define the window; hashmap gives O(1) “where did I last see this char?” so we can jump `left`.

---

#### 5.2 Three Pointers (e.g. 3Sum)

Fix one index, then use two pointers for the rest (like two sum on the remaining slice).

**Example: 3Sum — find all triplets that sum to 0**

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result
```

**Time**: O(n²), **Space**: O(1) excluding output.

---

### 6. Advanced Level

#### 6.1 Trapping Rain Water

Two pointers from both ends; track `left_max` and `right_max`. At each step, add water that can be trapped at the shorter side.

```python
def trap(height: list[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] <= height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

#### 6.2 Linked List: Slow and Fast Pointer (Tortoise and Hare)

Also called **Floyd's cycle detection** or **tortoise and hare**. Both pointers start at the head:
- **Slow**: moves 1 step per iteration
- **Fast**: moves 2 steps per iteration

**Why it works**: The fast pointer catches up to the slow one inside a cycle because the gap between them decreases by 1 each step. In one pass you get **O(n)** time and **O(1)** space.

---

**1. Cycle detection**

Does the list have a cycle?

- **No cycle**: fast reaches the end (`None`) and we stop.
- **Cycle**: fast eventually meets slow inside the cycle.

```text
Start:  S F
        ↓ ↓
        1 → 2 → 3 → 4
              ↑_____↓

Step 1:   S   F
Step 2:       S     F
Step 3:           S F   ← meet!
```

```python
def has_cycle(head) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

---

**2. Finding the middle**

When `fast` reaches the end, `slow` is at the middle (or second middle if length is even). Fast moves 2x, so when fast has traveled n nodes, slow has traveled n/2.

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

---

**3. Finding the start of a cycle**

After slow and fast meet inside the cycle:
1. Put one pointer at the **head**, keep the other at the **meeting point**.
2. Move both **one step at a time**.
3. They meet at the cycle start.

**Why**: Let `a` = distance head → cycle start, `b` = cycle start → meeting point, `c` = rest of cycle. When they meet: slow has gone `a + b`, fast has gone `2(a + b)`. So `a + b` equals the cycle length (mod cycle), and `a ≡ c`. So a pointer at head and one at meeting, both moving 1 step, meet after `a` steps at the cycle start.

```python
def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            p = head
            while p != slow:
                p = p.next
                slow = slow.next
            return p
    return None
```

---

**4. Nth node from the end**

- Move `fast` **n steps** ahead.
- Move both one step at a time until `fast` is at the end.
- `slow` is at the nth node from the end.

```python
def nth_from_end(head, n):
    fast = head
    for _ in range(n):
        if not fast:
            return None
        fast = fast.next
    slow = head
    while fast:
        slow = slow.next
        fast = fast.next
    return slow
```

---

**Slow/fast summary**

| Problem        | Slow step | Fast step | Extra logic                                |
|----------------|-----------|-----------|--------------------------------------------|
| Cycle detection| 1         | 2         | `slow == fast` ⇒ cycle exists              |
| Middle         | 1         | 2         | Stop when fast reaches end                 |
| Cycle start    | 1         | 2         | Then reset one to head, both move 1        |
| Nth from end   | 1         | 1 (lead n)| Fast leads by n, then both move 1 together |

#### 6.3 Dutch National Flag (Partition)

Partition array into three regions (e.g. 0s, 1s, 2s) using one pass and O(1) space with three pointers: `low`, `mid`, `high`.

---

### 7. Two-Pointer + HashMap

Combine when you need:
- **Fast lookups** (value → index, or frequency) from a **hashmap**.
- **Scanning or shrinking a window** in one pass with **two pointers**.

#### 7.1 Roles

| Component | Role |
|-----------|------|
| Two pointers | Define the current window `[left, right]` or one pointer scanning while the “other” is implied by the map. |
| HashMap | Store “complement” (two sum), “last seen index” (longest substring), or **frequency** (distinct count in window). |

#### 7.2 Pattern 1: Hashmap for complement (Two Sum, unsorted)

One pointer = current index; the “other” index comes from the map (complement).

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []
```

#### 7.3 Pattern 2: Sliding window + frequency map

**Subarray with at most K distinct elements** (count of such subarrays or max length).

- **Two pointers**: `left`, `right` = window.
- **HashMap**: `count[x]` = frequency of `x` in current window.
- Expand: add `arr[right]` to `count`.
- Shrink: move `left` and decrement `count[arr[left]]` until `len(count) <= k`.

```python
def at_most_k_distinct(arr: list[int], k: int) -> int:
    count = {}
    left = 0
    result = 0
    for right, x in enumerate(arr):
        count[x] = count.get(x, 0) + 1
        while len(count) > k:
            count[arr[left]] -= 1
            if count[arr[left]] == 0:
                del count[arr[left]]
            left += 1
        result += right - left + 1
    return result
```

#### 7.4 Pattern 3: Last-seen index (no repeating character)

Already shown in “Longest substring without repeating”: `seen[c] = right`; when we see a repeat, set `left = seen[c] + 1`. Two-pointer = window; hashmap = last index per character.

---

### 8. Decision Guide

| Problem type | Prefer |
|--------------|--------|
| Sorted array, pair/triplet sum | Opposite-direction two-pointer (often no hashmap). |
| Unsorted, “find two indices” | Hashmap (complement) + one scan. |
| Substring/subarray with “distinct” or “frequency” | Sliding window (two-pointer) + hashmap (count or last-seen). |
| Palindrome, “from both ends” | Converging two-pointer. |
| In-place removal/partition | Same-direction or three pointers. |

---

### 9. Time and Space Summary

| Pattern | Time | Space |
|---------|------|--------|
| Converging on sorted array | O(n) | O(1) |
| Same-direction read/write | O(n) | O(1) |
| Sliding window + hashmap | O(n) | O(k) or O(1) for fixed charset |
| 3Sum (sort + two-pointer) | O(n²) | O(1) |

---

### 10. Practice Order (Python)

1. **Two Sum (sorted)** — opposite two-pointer.
2. **Valid Palindrome** — converging.
3. **Two Sum (unsorted)** — hashmap (one “pointer” + map).
4. **Longest substring without repeating** — two-pointer + hashmap (last seen).
5. **3Sum** — sort + one loop + two-pointer.
6. **Subarray with at most K distinct** — two-pointer + frequency hashmap.
7. **Trapping Rain Water** — converging two-pointer.
8. **Linked list cycle / middle** — slow and fast pointer.

See `two-pointer.py` in this folder for runnable implementations of the examples above.
