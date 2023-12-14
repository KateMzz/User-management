# class Solution(object):
#     def gcd(self, a, b):
#         if a % b == 0:
#             return b
#         return self.gcd(b, a % b)
#
#     def gcdOfStrings(self, str1, str2):
#         """
#         :type str1: str
#         :type str2: str
#         :rtype: str
#         """
#
#         if str1 + str2 != str2 + str1:
#             return ""
#         else:
#             return str1[: self.gcd(len(str1), len(str2))]
#
#
# hey = Solution()
# print(hey.gcdOfStrings(str1="ABCABC", str2="ABC"))

# numbers = [
#     input(),
#     input(),
#     input(),
#     input()
# ]
#
# result = reduce(lambda a,b,c,d:a+(b-d)*c,map(lambda i: int(i), numbers))
# print(result)
# 100,10,12,15
# Считываем входные данные
# A, B, C, D = map(int, numbers)
#
# # Вычисляем суммарные расходы Кости на интернет
# total = A - min(0, B-D) * C
# # Выводим результат
# print(total)


# numbers = [input()]
# num = int("".join(numbers))
# print(num//2+num%2)

import math

N = int(input())
min_cuts = math.gcd(N, 2) + 1
print(min_cuts)
