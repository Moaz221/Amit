SMS = "&&&**$gnirtS PLIO!!@1234"
SMS = SMS.strip("!@#$%^&*()123456789")
print(SMS)
words = SMS.split(" ")

print("Before Swaping :.......................")
print(words[0])
print(words[1])

print("After swaping and replacement: ........ ")

reverse_SMS1 = words[0][::-1]
print(reverse_SMS1)
words[1] = words[1].replace("I","E")
words[1] = words[1].replace("O","U")

print(words[1])

print("Join..............")
print(reverse_SMS1," ",words[1])