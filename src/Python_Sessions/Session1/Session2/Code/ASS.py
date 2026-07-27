Input_list = ["math", "learning", "python", "machine learning", "data science", "deep learning"]

item = input("Enter item to remove it: ")

Input_list.remove(item)

print(Input_list)
# .........

my_list = [1,2,3]
index_of_2 = my_list.index(2)

#...............
degree = float(input("Enter the student's degree: "))

if 90 <= degree <= 100:
    print("Grade: A")
elif 80 <= degree < 90:
    print("Grade: B")
elif 70 <= degree < 80:
    print("Grade: C")
elif 60 <= degree < 70:
    print("Grade: D")
elif 0 <= degree < 60:
    print("Grade: F")
else:
    print("Invalid degree")