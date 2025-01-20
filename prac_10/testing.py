"""
CP1404/CP5632 Practical
Testing code using assert and doctest
"""

import doctest
from prac_06.car import Car


def repeat_string(s, n):
    """Repeat string s, n times, with spaces in between."""
    return s * n


def is_long_word(word, length=5):
    """
    Determine if the word is as long or longer than the length passed in
    >>> is_long_word("not")
    False
    >>> is_long_word("supercalifrag")
    True
    >>> is_long_word("Python", 6)
    True
    """
    return len(word) > length


def run_tests():
    """Run the tests on the functions."""
    # assert test with no message - used to see if the function works properly
    assert repeat_string("Python", 1) == "Python"
    # the test below should fail
    assert repeat_string("hi", 2) == "hi hi"

def repeat_string(s, n):
    """Repeat string s, n times, with spaces in between."""
    return " ".join([s] * n)


def run_tests():
    """Run the tests on the functions."""
    # Assert test for repeat_string function
    assert repeat_string("Python", 1) == "Python"
    assert repeat_string("hi", 2) == "hi hi"  # This should now pass

    # Car fuel tests
    car = Car(fuel=10)
    assert car.fuel == 10, "Car's fuel should be set to 10"  # Corrected this line

    car2 = Car()  # Should use default fuel value of 0
    assert car2.fuel == 0, "Car's fuel should be set to 0 (default)"

def is_long_word(word, length=5):
    return len(word) >= length

def format_sentence(phrase):
    return phrase.capitalize() + '.'


run_tests()

doctest.testmod()

