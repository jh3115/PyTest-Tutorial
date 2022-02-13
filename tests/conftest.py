from io import BytesIO

import pytest

import pandas as pd
from moto import mock_s3
import boto3

CUSTOMERS = {
    'Customer': ['Mary', 'John', 'Fred', 'Mary', 'Emma'],
    'Sale': [100, 50, 300, 20, 80]
}

S3_DATAFRAME_1 = {
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50]
}

S3_DATAFRAME_2 = {
    'A': [10, 10, 30, 30, 50],
    'B': [100, 100, 300, 300, 500]
}

BUCKET_NAME = 'aws-nothing'


@pytest.fixture(scope='module')
def mocked_s3_client():
    print('***** Setting up s3 clients *****')
    with mock_s3():
        client = boto3.client('s3', region_name='us-east-1')
        client.create_bucket(Bucket='aws-nothing')

        yield client


@pytest.fixture(scope='module')
def mocked_s3_client_local(mocked_s3_client):

    data_source = 'my-data'
    # Making metadata available in mocked S3
    for index_, df_ in enumerate([S3_DATAFRAME_1, S3_DATAFRAME_2], start=1):
        buf = BytesIO()
        df = pd.DataFrame(df_)
        df.to_parquet(buf, index=True)
        key = make_dataframe_key(index_, data_source)
        mocked_s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=buf.getvalue())

    yield mocked_s3_client


@pytest.fixture(scope='session')
def customer_df():
    yield pd.DataFrame(CUSTOMERS)


def make_dataframe_key(index_, data_source):
    return f'data-sources/{data_source}/dataframe_{index_}.parquet'
