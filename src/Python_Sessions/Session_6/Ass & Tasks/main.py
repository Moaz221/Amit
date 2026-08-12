from model import (
    MultiplicationTable,
    TwinPrime,
    PrimeFactors,
    DecimalToBinary,
    PerfectNumbers,
    Calculator,
    FileManager
)



num = int(
    input(
        "Hey Bro Enter a number to multiply it: "
    )
)

range_limit = int(
    input(
        "You need to multiply to number? : "
    )
)

s1 = MultiplicationTable(
    num,
    range_limit
)

s1.multiply()


s2 = TwinPrime(1000)

s2.print_twin_primes()


num = int(
    input(
        "BROOO Enter num to get its Factors: (^_^): "
    )
)

s3 = PrimeFactors(num)

s3.get_factors()


s4 = DecimalToBinary(11)

s4.convert()


s5 = PerfectNumbers()

s5.print_perfect_numbers(
    0,
    100
)


s6 = Calculator()

s6.welcome_user()

s6.calculate()



num_files = int(
    input(
        "Enter the number of files: "
    )
)

s7 = FileManager(
    "Thanous",
    num_files
)

s7.run()