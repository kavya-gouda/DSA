class Solution:
    def romanToInt(self, s: str) -> int:
        hashmap = {'I':1, 'V':5, 'X':10, 'L':50 , 'C':100, 'D':500, 'M':1000}
        result = 0
        for i in range(len(s)):
            curr = hashmap[s[i]]
            next = hashmap[s[i+1]] if i+1 < len(s) else 0
            if curr < next :
                result -= curr
            elif curr > next :
                result += curr
            elif curr == next:
                result +=curr
        return result