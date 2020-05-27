from fractions import Fraction


def test_exponential():
    # exponential operator
    print(2 ** 10)
    print(8 ** (1 / 3))


def test_fractions():
    f = Fraction(3, 4)
    print(f)
    print(f + 1 + 1.5)
    print(Fraction(3, 4) + 1 + Fraction(1/4))


def test_complex_number():
    # imaginary part identified by the letter j or J (as opposed to the letter i used in mathematical)
    a = 2 + 3j
    print(type(a))
    b = complex(1, 3)
    print(type(b))
    print(a - b)
    # get the real and imaginary part
    print(a.real, a.imag)


if __name__ == '__main__':
    # test_exponential()
    # test_fractions()
    test_complex_number()
