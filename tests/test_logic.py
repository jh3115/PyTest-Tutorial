import json
import logging
import unittest
from io import BytesIO

import pandas as pd
import pytest
from numpy.random import seed

from logic import (
    add, divide,
    log_random, sort_by,
    fizzbuzz, get_best_customer,
    get_unique_customer
)

BUCKET_NAME = 'aws-nothing'


class MyTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add22(self):
        self.assertEqual(add(2, 2), 4)





@pytest.mark.maths_test
def test_add22():
    assert add(2, 2) == 4

@pytest.mark.maths_test
def test_add_neg():
    assert add(3, -1) == 2

@pytest.mark.maths_test
def test_all_add():
    assert add(2, 2) == 4
    assert add(3, -1) == 2
    assert add(-4, -20) == -24



@pytest.mark.parametrize('a,b, expected', [
    (2, 2, 4),
    (3, -1, 2),
    (-4, -20, -24)
])
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.xfail(raises=ZeroDivisionError, strict=True)
def test_divide_raises_error():
    # with pytest.raises(ZeroDivisionError):
    divide(3, 0)


def test_divide_raises_zero_error():
    with pytest.raises(ZeroDivisionError):
        divide(3, 0)



##############
#  Fixtures  #
##############

@pytest.fixture
def list_of_dictionaries():
    dicts = [
        {
            'Name': 'Jake',
            'Age': 29,
            'FavouriteColour': 'Blue'
        },
        {
            'Name': 'James',
            'Age': 25,
            'FavouriteColour': 'Red'
        },
        {
            'Name': 'Emma',
            'Age': 32,
            'FavouriteColour': 'Yellow'
        },
    ]
    yield dicts


def test_bad_example(list_of_dictionaries):


    sorted_dicts = sort_by(list_of_dictionaries, 'Age')

    assert sorted_dicts == [
        {
            'Name': 'James',
            'Age': 25,
            'FavouriteColour': 'Red'
        },
        {
            'Name': 'Jake',
            'Age': 29,
            'FavouriteColour': 'Blue'
        },
        {
            'Name': 'Emma',
            'Age': 32,
            'FavouriteColour': 'Yellow'
        },
    ]


@pytest.mark.aws
def test_s3_client_put_get(mocked_s3_client_local):
    df = pd.DataFrame({
        'C': [3, 2, 1],
        'D': [30, 20, 10]
    })

    buf = BytesIO()
    df.to_parquet(buf, index=True)
    key = f'path/to/my/df.parquet'
    mocked_s3_client_local.put_object(
        Bucket=BUCKET_NAME, Key=key, Body=buf.getvalue()
    )

    buf = mocked_s3_client_local.get_object(
        Bucket='aws-nothing', Key=key
    )['Body'].read()

    df_returned = pd.read_parquet(BytesIO(buf))

    assert df_returned.columns.tolist() == ['C', 'D']
    print(len(mocked_s3_client_local.list_objects(Bucket='aws-nothing')['Contents']))


@pytest.mark.aws
def test_s3_client_query(mocked_s3_client_local):

    buf = mocked_s3_client_local.get_object(
        Bucket='aws-nothing', Key='data-sources/my-data/dataframe_1.parquet'
    )['Body'].read()

    df = pd.read_parquet(BytesIO(buf))

    assert df.query('B >= 30')['A'].tolist() == [3, 4, 5]
    print(len(mocked_s3_client_local.list_objects(Bucket='aws-nothing')['Contents']))


@pytest.mark.aws
def test_s3_client_groupby(mocked_s3_client_local):

    buf = mocked_s3_client_local.get_object(
        Bucket='aws-nothing', Key='data-sources/my-data/dataframe_2.parquet'
    )['Body'].read()

    df = pd.read_parquet(BytesIO(buf))

    assert df.groupby('A')['B'].sum().tolist() == [200, 600, 500]
    print(len(mocked_s3_client_local.list_objects(Bucket='aws-nothing')['Contents']))


def test_best_customers(customer_df):
    assert get_best_customer(customer_df) == 'Fred'


def test_get_customers(customer_df):
    assert get_unique_customer(customer_df).tolist() == ['Mary', 'John', 'Fred', 'Emma']


def test_output(caplog):
    seed(123)
    caplog.set_level(logging.INFO)
    log_random()
    logs = caplog.records
    assert logs[-1].message == 'Selected: 2'


def test_file_write(tmpdir):
    filename = tmpdir.join('abc.json')
    print(filename)
    data = {
        'foo': 'Foo',
        'bar': 'Bar'
    }
    with open(filename, 'w') as file_out:
        json.dump(data, file_out)

    with open(filename) as file_in:
        read_data = json.load(file_in)

    assert data == read_data


@pytest.fixture
def fixt(request):
    marker = request.node.get_closest_marker("fixt_data")
    if marker is None:
        # Handle missing marker in some way...
        data = None
    else:
        data = marker.args[0]

    # Do something with the data
    return data * 2


@pytest.mark.fixt_data(2)
def test_fixt(fixt):
    assert fixt == 4

#############
## Plugins ##
#############


def test_fizzbuzz():

    assert fizzbuzz(3) == [1, 2, 'Fizz']

# pip install pytest-sugar  # UI
###  pytest --verbose
###  pytest -p no:sugar

# pip install pytest-cov   # coverage
### pytest tests --cov=. --cov-report html

# pip instal pytest-stress   # good for profiling

############
## Honourable Mentions
# pytest-parallel: allows you to run tests quickly using multiprocessing and multithreading.
# pytest-diff for checking dictionary differences
# flake-8 formatter
# freezegun - time related tests.
