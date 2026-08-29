class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """

        chars = list(s)

        n = len(chars)
        write = 0
        read = 0

        while read < n:

            while read < n and chars[read] == ' ':
                read += 1

            while read < n and chars[read] != ' ':
                chars[write] = chars[read]
                write += 1
                read += 1

            while read < n and chars[read] == ' ':
                read += 1

            if read < n:
                chars[write] = ' '
                write += 1

        chars = chars[:write]
        chars.reverse()
        start = 0

        for i in range(len(chars) + 1):
            if i == len(chars) or chars[i] == ' ':
                chars[start:i] = chars[start:i][::-1]
                start = i + 1

        return ''.join(chars)