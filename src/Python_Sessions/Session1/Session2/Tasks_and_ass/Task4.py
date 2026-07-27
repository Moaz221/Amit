SMS = "##$$$@!yalpstcejorp EPUVT****9887"
SMS = SMS.strip("!@#$%^&*()123456789")
print(SMS)

words = SMS.split(" ")

print("Before Swaping :.......................")
print(words[0])
print(words[1])

print("After swaping and replacement: ........ ")

reverse_SMS1 = words[0][::-1]
print(reverse_SMS1)
words[1] = words[1].replace("E","A")
words[1] = words[1].replace("U","O")

print(words[1])

print("Join..............")
print(reverse_SMS1," ",words[1])