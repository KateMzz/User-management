class Solution(object):
    def gcd(self, a, b):
        if a % b == 0:
            return b
        return self.gcd(b, a % b)

    def gcdOfStrings(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: str
        """

        if str1 + str2 != str2 + str1:
            return ""
        else:
            return str1[: self.gcd(len(str1), len(str2))]


hey = Solution()
print(hey.gcdOfStrings(str1="ABCABC", str2="ABC"))
