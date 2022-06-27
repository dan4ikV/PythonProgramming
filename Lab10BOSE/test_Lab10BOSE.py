import pytest


def is_prime(number):
    if type(number) is int or (type(number) is str and number.isnumeric()):
        number = int(number)
        if number < 0:
            return False
        for i in range(2, int(number / 2)):
            if number % i == 0:
                return False
        return True
    else:
        raise TypeError

def test_wrong_type():
    with pytest.raises(TypeError):
        is_prime("r")
    with pytest.raises(TypeError):
        is_prime(2.16)

def test_negative():
    assert is_prime(-17) == False

def test_numeric_string():
    assert is_prime("17")  == True

is_prime("17")