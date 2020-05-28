from fractions import Fraction


def test_exponential():
    # exponential operator
    print(2 ** 10)
    print(8 ** (1 / 3))


def test_fractions():
    f = Fraction(3, 4)
    print(f)
    print(f + 1 + 1.5)
    print(Fraction(3, 4) + 1 + Fraction(1 / 4))


def test_complex_number():
    # imaginary part identified by the letter j or J (as opposed to the letter i used in mathematical)
    a = 2 + 3j
    print(type(a))
    b = complex(1, 3)
    print(type(b))
    print(a - b)
    # get the real and imaginary part
    print(a.real, a.imag)


def test_user_input():
    try:
        a = input('Input an integer: ')
        print(type(a))
        num_a = int(a)
        print(num_a, type(num_a))

        b = Fraction(input('Input a fraction: '))
        print(b, type(b))

        z = complex(input('Input a complex number: '))
        print(z, type(z))

    except ValueError:
        print('You entered an invalid number')

    except ZeroDivisionError:
        print('You entered an zero division number')


def test_factor_of_integer():
    def is_factor(a: int, b: int):
        if b % a == 0:
            return True
        else:
            return False

    def find_factors(from_num: int) -> list:
        factors = []
        for num in range(1, from_num + 1):
            if is_factor(num, from_num):
                factors.append(num)

        return factors

    # print(is_factor(7, 1024))
    print(find_factors(9))


if __name__ == '__main__':
    # test_exponential()
    # test_fractions()
    # test_complex_number()
    # test_user_input()
    test_factor_of_integer()
