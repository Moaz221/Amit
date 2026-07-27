email ="Amit_ml@gmail.edu"
num_of_atSign= email.count("@")

AtIndex = email.index("@")
Email_AfterAt = email[AtIndex+1:]
Email_beforeAt = email[:AtIndex]
dot_Index = Email_AfterAt.rfind(".")
domain = Email_AfterAt[:dot_Index]
if num_of_atSign == 1 and Email_AfterAt.count(".") == 1 :
    print("Valid Email")
else:
    print("Invalid Email")

print("User name is: ", Email_beforeAt)
print("Your Domain is : ", domain)

if email.endswith(".com"):
    print("Commertial Domain")
elif email.endswith(".edu"):
    print("Education Domain")
else:
    print("Other Domain")
