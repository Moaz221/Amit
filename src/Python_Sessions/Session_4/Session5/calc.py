class Calculator:

    def welcome_user(self):
        """
        Display a welcome message and show the calculator layout.

        :return: None
        :rtype: None
        """
        print("Hi Bro, What do you need to calculate?\n")

        calc = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            ("#", 0, "*")
        )

        for row in calc:
            print(*row)

        print("\nOperations:")
        print("+ : Addition")
        print("- : Subtraction")
        print("* : Multiplication")
        print("/ : Division")
        print("E : Exit")

    def get_numbers(self):
        """
        Get two valid numbers from the user.

        :return: Two numbers.
        :rtype: tuple
        """
        while True:
            try:
                num1 = float(input("Enter number 1: "))
                num2 = float(input("Enter number 2: "))
                return num1, num2
            except ValueError:
                print("Please enter valid numbers.\n")

    def calculate(self):
        """
        Perform the selected arithmetic operation.

        :return: None
        :rtype: None
        """
        while True:
            op = input("\nEnter Operation (+, -, *, /, E): ").strip()

            if op.upper() == "E":
                print("Why you use this calculator 😐")
                break

            if op not in ["+", "-", "*", "/"]:
                print("Invalid operation!")
                continue

            num1, num2 = self.get_numbers()

            if op == "+":
                result = num1 + num2
                print(f"The result of adding {num1} and {num2} is {result}")

            elif op == "-":
                result = num1 - num2
                print(f"The result of subtracting {num2} from {num1} is {result}")

            elif op == "*":
                result = num1 * num2
                print(f"The result of multiplying {num1} and {num2} is {result}")

            elif op == "/":
                try:
                    result = num1 / num2
                    print(f"The result of dividing {num1} by {num2} is {result}")
                except ZeroDivisionError:
                    print("Error: Cannot divide by zero.")
                    continue

            again = input("\nDo you want another calculation? (yes/no): ").strip().lower()

            if again != "yes":
                print("Why you use this calculator 😐")
                break