import os
import random


class MultiplicationTable:
    """
    Handles generating a multiplication table for a given number.

    Attributes:
        number (int): The number to multiply.
        range_limit (int): The upper limit of the multiplication table.
    """

    def __init__(self, number: int, range_limit: int = 12):
        self.number = number
        self.range_limit = range_limit

    def multiply(self):
        """
        Prints the multiplication table of the given number.

        Returns:
            None
        """
        for i in range(1, self.range_limit):
            print(f"{self.number:>5} * {i:<3} = {i * self.number:<5}")


class TwinPrime:
    """
    Handles checking prime numbers and finding twin prime numbers.

    Attributes:
        limit (int): The upper limit for searching twin primes.
    """

    def __init__(self, limit: int = 1000):
        self.limit = limit

    def is_prime(self, num: int):
        """
        Checks whether a number is prime.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is prime, otherwise False.
        """
        if num < 2:
            return False

        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False

        return True

    def print_twin_primes(self):
        """
        Prints all twin prime numbers up to the specified limit.

        Returns:
            None
        """
        print(f"|(*_*){'TWIN PRIME':^30}(^_^)|\n")

        for i in range(1, self.limit):
            if self.is_prime(i) and self.is_prime(i + 2):
                print(f" {i:>3} {'and':^5} {i + 2:<3}")


class PrimeFactors:
    """
    Handles finding the prime factors of a number.

    Attributes:
        number (int): The number whose prime factors will be found.
    """

    def __init__(self, number: int = 20):
        self.number = number

    def is_prime(self, num: int):
        """
        Checks whether a number is prime.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is prime, otherwise False.
        """
        if num < 2:
            return False

        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False

        return True

    def get_factors(self):
        """
        Finds and prints the prime factors of the number.

        Returns:
            list: A list containing the prime factors.
        """
        num = self.number
        result = []

        for i in range(2, num):
            while num % i == 0 and self.is_prime(i):
                result.append(i)
                num //= i

        print(result)
        return result


class DecimalToBinary:
    """
    Handles converting a decimal number to binary.

    Attributes:
        number (int): The decimal number to convert.
    """

    def __init__(self, number: int):
        self.number = number

    def convert(self):
        """
        Converts the decimal number to binary.

        Returns:
            str: The binary representation of the number.
        """
        if self.number == 0:
            return "0"

        remainder = []
        num = self.number

        while num > 0:
            remainder.append(str(num % 2))
            num //= 2

        binary = "".join(remainder[::-1])

        print(binary)
        return binary


class PerfectNumbers:
    """
    Handles checking and finding perfect numbers.

    Attributes:
        number (int): The number to check.
    """

    def __init__(self, number: int = 0):
        self.number = number

    def is_perfect(self):
        """
        Checks whether the number is a perfect number.

        Returns:
            bool: True if the number is perfect, otherwise False.
        """
        total = 0

        for i in range(1, self.number):
            if self.number % i == 0:
                total += i

        return total == self.number

    def print_perfect_numbers(self, start: int, end: int):
        """
        Prints all perfect numbers within a specified range.

        Args:
            start (int): The starting number.
            end (int): The ending number.

        Returns:
            None
        """
        for i in range(start, end):
            self.number = i

            if self.is_perfect():
                print(i)


class Calculator:
    """
    Handles basic arithmetic calculations.

    Attributes:
        operation (str): The selected arithmetic operation.
    """

    def __init__(self):
        self.operation = None

    def welcome_user(self):
        """
        Displays a welcome message and calculator layout.

        Returns:
            None
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
        Gets two valid numbers from the user.

        Returns:
            tuple: Two numbers entered by the user.
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
        Performs the selected arithmetic operation.

        Returns:
            None
        """
        while True:
            self.operation = input(
                "\nEnter Operation (+, -, *, /, E): "
            ).strip()

            if self.operation.upper() == "E":
                print("Why you use this calculator 😐")
                break

            if self.operation not in ["+", "-", "*", "/"]:
                print("Invalid operation!")
                continue

            num1, num2 = self.get_numbers()

            if self.operation == "+":
                result = num1 + num2
                print(
                    f"The result of adding {num1} and {num2} is {result}"
                )

            elif self.operation == "-":
                result = num1 - num2
                print(
                    f"The result of subtracting {num2} from {num1} is {result}"
                )

            elif self.operation == "*":
                result = num1 * num2
                print(
                    f"The result of multiplying {num1} and {num2} is {result}"
                )

            elif self.operation == "/":
                try:
                    result = num1 / num2
                    print(
                        f"The result of dividing {num1} by {num2} is {result}"
                    )

                except ZeroDivisionError:
                    print("Error: Cannot divide by zero.")
                    continue

            again = input(
                "\nDo you want another calculation? (yes/no): "
            ).lower()

            if again != "yes":
                print("Why you use this calculator 😐")
                break


class FileManager:
    """
    Handles creating and randomly deleting files.

    Attributes:
        folder_name (str): The name of the folder.
        num_files (int): The number of files to create.
    """

    def __init__(self, folder_name="Thanous", num_files=0):
        self.folder_name = folder_name
        self.num_files = num_files

    def create_files(self):
        """
        Creates the specified number of files inside the folder.

        Returns:
            None
        """
        os.makedirs(self.folder_name, exist_ok=True)

        for i in range(1, self.num_files + 1):
            file_name = os.path.join(
                self.folder_name,
                f"file{i}.txt"
            )

            open(file_name, "w").close()

    def delete_random_files(self):
        """
        Deletes half of the files randomly.

        Returns:
            None
        """
        files = os.listdir(self.folder_name)

        print(f"\nNumber of files before deleting: {len(files)}")

        num_to_delete = len(files) // 2

        random_files = random.sample(
            files,
            num_to_delete
        )

        for file in random_files:
            file_path = os.path.join(
                self.folder_name,
                file
            )

            os.remove(file_path)

    def show_remaining_files(self):
        """
        Displays the remaining files after deletion.

        Returns:
            None
        """
        remaining_files = os.listdir(self.folder_name)

        print(
            f"Number of files after deleting: "
            f"{len(remaining_files)}"
        )

        print("\nRemaining Files:")

        for file in remaining_files:
            print(file)

    def run(self):
        """
        Runs the complete file management process.

        Returns:
            None
        """
        self.create_files()
        self.delete_random_files()
        self.show_remaining_files()