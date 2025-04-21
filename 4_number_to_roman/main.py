"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_roman(self, number: int) -> str:
        num = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syms = ["M", "CM", "D", "CD","C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

        if number <= 0:
            return "number can not less than 0"
        
        result = ""
        for i in range(len(num)):
            div = number // num[i]
            number %= num[i]
            for _ in range(div):
                result += syms[i]
        return result
