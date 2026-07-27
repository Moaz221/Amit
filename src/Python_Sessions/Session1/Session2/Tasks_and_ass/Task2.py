SMS = "###!!@mocleW EPGTQ!!!6789"
SMS = SMS.strip("#@!1234567890")
print(SMS)
words = SMS.split(" ")
print(words[0])
print(words[1])

print("After Reversing : ........................... ")
reverse_SMS1 = words[0][::-1]
print(reverse_SMS1)
reverse_SMS2 = words[1]
print(reverse_SMS2)

print("After Joining : ..............................")

print(reverse_SMS1 ," " , reverse_SMS2)


