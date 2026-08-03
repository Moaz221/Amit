# # def sum(x,y):
# #     return x+y

# # def get_info(name:str,age:int):
# #     ''' function for personal info

# #     Args:
# #     parameter_1 : name get the name of person
# #     type of param_1: str
# #     param_2:age get the age form usr
# #     type_parameter_2: int

# #     return: this fun return the name and age 
# #     type_return : str, int

# #     '''
# #     return f"my name is{name}, age{age}"

# def main():
#     """Run the calculator program."""

#     def add(num1, num2):
#         """Return the sum of two numbers.

#         Args:
#             num1 (float): The first number.
#             num2 (float): The second number.

#         Returns:
#             float: The sum of the two numbers.
#         """
#         return num1 + num2

#     def subtract(num1, num2):
#         """Return the difference between two numbers.

#         Args:
#             num1 (float): The first number.
#             num2 (float): The second number.

#         Returns:
#             float: The difference between the two numbers.
#         """
#         return num1 - num2

#     def multiply(num1, num2):
#         """Return the product of two numbers.

#         Args:
#             num1 (float): The first number.
#             num2 (float): The second number.

#         Returns:
#             float: The product of the two numbers.
#         """
#         return num1 * num2

#     def divide(num1, num2):
#         """Return the division of two numbers.

#         Args:
#             num1 (float): The first number.
#             num2 (float): The second number.

#         Returns:
#             float: The division result.
#         """
#         return num1 / num2

#     print("=" * 40)
#     print("         SIMPLE CALCULATOR")
#     print("=" * 40)

#     try:
#         num1 = float(input("Enter the first number : "))
#         num2 = float(input("Enter the second number: "))

#         print("\n" + "=" * 40)
#         print("OPERATIONS")
#         print("=" * 40)
#         print(" +  Addition")
#         print(" -  Subtraction")
#         print(" *  Multiplication")
#         print(" /  Division")
#         print("=" * 40)

#         operation = input("Enter your choice: ")

#         if operation == "+":
#             result = add(num1, num2)

#         elif operation == "-":
#             result = subtract(num1, num2)

#         elif operation == "*":
#             result = multiply(num1, num2)

#         elif operation == "/":
#             result = divide(num1, num2)

#         else:
#             print("\nError: Invalid operation.")
#             return

#         print("\n" + "=" * 40)
#         print("CALCULATION")
#         print("=" * 40)
#         print(f"First Number : {num1}")
#         print(f"Operation    : {operation}")
#         print(f"Second Number: {num2}")
#         print("-" * 40)
#         print(f"{num1} {operation} {num2} = {result}")
#         print("=" * 40)

#     except ValueError:
#         print("\nError: Please enter valid numbers.")

#     except ZeroDivisionError:
#         print("\nError: You cannot divide by zero.")

#     except Exception as e:
#         print(f"\nUnexpected Error: {e}")

# main()

import tkinter as tk

root = tk.Tk()
root.title("My App")

tk.Label(root, text="Hello Moaz!").pack()

root.mainloop()