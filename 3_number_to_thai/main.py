"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_thai(self, number: int) -> str:
        digits = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
        places = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
        if number < 0:
            return "number can not less than 0"
        if number > 10000000:
            return "number can not more than 10,000,000"
        if number == 0:
            return "ศูนย์"
        
        def conver_number_to_thai(number):
            num_str = str(number)
            length = len(num_str)
            result = ""

            for i in range(length):
                current_number = int(num_str[i])
                position = length - i - 1
                if position == 0 and current_number == 1 and length > 1:
                    result += "เอ็ด"
                elif position == 1 and current_number == 1:
                    result += "สิบ"
                elif position == 1 and current_number == 2:
                    result += "ยี่สิบ"
                else:
                    result += digits[current_number] + places[position]
            return result
        
        if number < 1000000:
            return conver_number_to_thai(number)
        else:
            millions = number // 1000000
            less_than_million = number % 1000000
            result = conver_number_to_thai(millions) + "ล้าน"
            if less_than_million > 0:
                result += conver_number_to_thai(less_than_million)
            return result
        
s = Solution()
print(s.number_to_thai(101))
print(s.number_to_thai(-1))