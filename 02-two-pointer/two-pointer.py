"""
Two-Pointer technique examples (Python).
See two-pointer-notes.md for full documentation.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Beginner: Opposite-direction (converging)
# ---------------------------------------------------------------------------

def two_sum_sorted(arr: list[int], target: int) -> list[int]:
    """Two Sum in sorted array. Returns 1-based indices or []."""
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return []


def is_palindrome(s: str) -> bool:
    """Check if string is palindrome (ignore non-alphanumeric, case)."""
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


# ---------------------------------------------------------------------------
# Beginner: Same-direction (read/write)
# ---------------------------------------------------------------------------

def remove_duplicates(arr: list[int]) -> int:
    """Remove duplicates in-place (sorted). Returns new length."""
    if not arr:
        return 0
    write = 0
    for read in range(1, len(arr)):
        if arr[read] != arr[write]:
            write += 1
            arr[write] = arr[read]
    return write + 1


def move_zeros(arr: list[int]) -> None:
    """Move all zeros to end in-place."""
    write = 0
    for read in range(len(arr)):
        if arr[read] != 0:
            arr[write], arr[read] = arr[read], arr[write]
            write += 1


# ---------------------------------------------------------------------------
# Intermediate: Sliding window + hashmap
# ---------------------------------------------------------------------------

def length_of_longest_substring(s: str) -> int:
    """Longest substring without repeating characters. Two-pointer + last-seen map."""
    seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in seen and seen[c] >= left:
            left = seen[c] + 1
        seen[c] = right
        best = max(best, right - left + 1)
    return best


def three_sum(nums: list[int]) -> list[list[int]]:
    """All unique triplets that sum to 0. Sort + one loop + two-pointer."""
    nums = sorted(nums)
    result: list[list[int]] = []
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


# ---------------------------------------------------------------------------
# Two-pointer + hashmap
# ---------------------------------------------------------------------------

def two_sum_unsorted(nums: list[int], target: int) -> list[int]:
    """Two Sum (unsorted). One pass + hashmap (complement)."""
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []


def at_most_k_distinct(arr: list[int], k: int) -> int:
    """Count subarrays with at most k distinct elements. Sliding window + frequency map."""
    count: dict[int, int] = {}
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


# ---------------------------------------------------------------------------
# Advanced: Trapping rain water
# ---------------------------------------------------------------------------

def trap(height: list[int]) -> int:
    """Trapping rain water. Converging two-pointer + left_max/right_max."""
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


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Two sum sorted
    print(two_sum_sorted([1, 2, 3, 4, 6], 6))  # [1, 3]

    # Palindrome
    print(is_palindrome("A man, a plan, a canal: Panama"))  # True

    # Remove duplicates
    a = [1, 1, 2, 2, 3]
    n = remove_duplicates(a)
    print(a[:n])  # [1, 2, 3]

    # Longest substring
    print(length_of_longest_substring("abcabcbb"))  # 3

    # Two sum unsorted
    print(two_sum_unsorted([2, 7, 11, 15], 9))  # [0, 1]

    # At most K distinct
    print(at_most_k_distinct([1, 2, 1, 2, 3], 2))  # 12

    # Trap
    print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # 6
