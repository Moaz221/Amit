class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """

        stack = []
        num = 0
        operator = '+'

        for i in range(len(s)):

            if s[i].isdigit():
                num = num * 10 + int(s[i])

            if (not s[i].isdigit() and s[i] != ' ') or i == len(s) - 1:

                if operator == '+':
                    stack.append(num)

                elif operator == '-':
                    stack.append(-num)

                elif operator == '*':
                    stack.append(stack.pop() * num)

                elif operator == '/':
                    previous = stack.pop()

                    # Division truncated toward zero
                    stack.append(int(previous / num))

                operator = s[i]
                num = 0

        return sum(stack)