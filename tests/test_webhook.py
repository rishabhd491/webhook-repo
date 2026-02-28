import pytest
from app import create_app, mongo
from unittest.mock import MagicMock
import mongomock

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    
    # Mock MongoDB using mongomock
    mongo.db = mongomock.MongoClient().db
    
    with app.test_client() as client:
        yield client

def test_push_event(client):
    payload = {
        "ref": "refs/heads/master",
        "after": "abcd1234efgh5678",
        "pusher": {"name": "Travis"}
    }
    headers = {"X-GitHub-Event": "push"}
    response = client.post("/webhook", json=payload, headers=headers)
    
    assert response.status_code == 201
    
    # Check MongoDB
    action = mongo.db.actions.find_one({"action": "PUSH"})
    assert action is not None
    assert action["author"] == "Travis"
    assert action["to_branch"] == "master"
    assert action["request_id"] == "abcd1234efgh5678"

def test_pull_request_opened(client):
    payload = {
        "action": "opened",
        "pull_request": {
            "id": 123,
            "user": {"login": "Travis"},
            "head": {"ref": "staging"},
            "base": {"ref": "master"}
        }
    }
    headers = {"X-GitHub-Event": "pull_request"}
    response = client.post("/webhook", json=payload, headers=headers)
    
    assert response.status_code == 201
    
    # Check MongoDB
    action = mongo.db.actions.find_one({"action": "PULL_REQUEST"})
    assert action is not None
    assert action["author"] == "Travis"
    assert action["from_branch"] == "staging"
    assert action["to_branch"] == "master"
    assert action["request_id"] == "123"

def test_merge_event(client):
    payload = {
        "action": "closed",
        "pull_request": {
            "merged": True,
            "merged_by": {"login": "Travis"},
            "head": {"ref": "dev"},
            "base": {"ref": "master"},
            "merge_commit_sha": "merge_hash_123"
        }
    }
    headers = {"X-GitHub-Event": "pull_request"}
    response = client.post("/webhook", json=payload, headers=headers)
    
    assert response.status_code == 201
    
    # Check MongoDB
    action = mongo.db.actions.find_one({"action": "MERGE"})
    assert action is not None
    assert action["author"] == "Travis"
    assert action["from_branch"] == "dev"
    assert action["to_branch"] == "master"
    assert action["request_id"] == "merge_hash_123"
