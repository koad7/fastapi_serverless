import uuid  # new

import boto3  # new
import pytest
from fastapi import status
from moto import mock_dynamodb  # new
from starlette.testclient import TestClient

from main import app
from models import Task  # new
from store import TaskStore  # new


# ... previous tests

@pytest.fixture
def dynamodb_table():
    with mock_dynamodb():
        client = boto3.client("dynamodb")
        table_name = "test-table"
        client.create_table(
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield table_name


def test_added_task_retrieved_by_id(dynamodb_table):
    repository = TaskStore(table_name=dynamodb_table)
    task = Task.create(uuid.uuid4(), "Clean your office", "john@doe.com")

    repository.add(task)

    assert repository.get_by_id(task_id=task.id, owner=task.owner) == task