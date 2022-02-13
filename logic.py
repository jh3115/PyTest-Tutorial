
import logging

from numpy import random

LOG = logging.getLogger(__name__)


def add(a, b):
    """
    Simple function to add two numbers.
    Demonstrate mark.parametrize
    """
    return a + b


def divide(a, b):
    """
    Test if ZeroDivision error raised when b == 0.
    """
    return a / b


def sort_by(dicts, key_to_sort=None):
    """
    List of Dictionaries sorter
    """
    if key_to_sort:
        new_list = sorted(dicts, key=lambda d: d[key_to_sort])
        return new_list

    return dicts


def log_random():
    """
    Log a random number to the terminal.
    """
    LOG.info(f'Selected: {random.randint(5)}')


def fizzbuzz(n):
    """
    Use for pytest-coverage case.
    """
    out = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            out.append('Fizzbuzz')
        elif i % 3 == 0:
            out.append('Fizz')
        elif i % 5 == 0:
            out.append('Buzz')
        else:
            out.append(i)
    return out


def get_best_customer(df):
    df = df.groupby('Customer').Sale.sum().reset_index()
    return df.iloc[df.Sale.argmax()].Customer


def get_unique_customer(df):
    return df.Customer.unique()
