from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

fake_room_id = "44523d5325dsdf"
fake_org_id = "1223209805sdfsa902"
fake_message_data = {
        "sender_id": "425324132312",
        "room_id": fake_room_id,
        "text": "does it work well?",
        "reactions": [],
        "files": [],
        "saved_by": [],
        "is_pinned": False,
        "is_edited": False,
        "created_at": "2021-12-11 01:44:37.582879",
        "threads": []
        }

def test_send_message():
    """ test for the send message endpoint"""

    fake_response_output = {
        "message_id": "33090940900",
        "message_data": fake_message_data
    }

    response = client.post(
        "/org/{org_id}/rooms/{room_id}/sender/{sender_id}/messages",
        json= fake_message_data
        )
    assert response.status_code == 201
    assert response.json() == fake_response_output

def test_message_not_sent():
    """test response when message is not sent successfully"""

    response = client.post(
        "/org/{org_id}/rooms/{room_id}/sender/{sender_id}/messages",
        json= fake_message_data
        )
    
    assert response.status_code == 424
    assert response.json() == {"detail": {"message not sent": {}}}








    from fastapi.testclient import TestClient



client = TestClient(app)

fake_room_id = "44523d5325dsdf"
fake_org_id = "1223209805sdfsa902"
fake_message_data = {
    "sender_id": "425324132312",
    "room_id": fake_room_id,
    "text": "does it work well?",
    "reactions": [],
    "files": [],
    "saved_by": [],
    "is_pinned": False,
    "is_edited": False,
    "created_at": "2021-12-11 01:44:37.582879",
    "threads": [],
}
fake_updated_message = {
    "sender_id": "425324132312",
    "text": "can I change this text?",
}
fake_updated_message_payload = {
    "sender_id": "1234567893458",
    "text": "can I change this text?",
}


def test_send_message():
    """test for the send message endpoint"""

    fake_response_output = {
        "message_id": "33090940900",
        "message_data": fake_message_data,
    }

    response = client.post(
        "/org/{org_id}/rooms/{room_id}/sender/{sender_id}/messages",
        json=fake_message_data,
    )
    assert response.status_code == 201
    assert response.json() == fake_response_output


def test_message_not_sent():
    """test response when message is not sent successfully"""

    response = client.post(
        "/org/{org_id}/rooms/{room_id}/sender/{sender_id}/messages",
        json=fake_message_data,
    )

    assert response.status_code == 424
    assert response.json() == {"detail": {"message not sent": {}}}


def test_update_message():
    """test for the update message endpoint"""

    fake_response = {"message_id": "33090940900", "message_data": fake_updated_message}

    response = client.put(
        "/org/{org_id}/rooms/{room_id}/messages/{message_id}", json=fake_updated_message
    )
    assert response.status_code == 200
    assert response.json() == fake_response


def test_message_not_updated():
    """test response when message is not updated successfully"""

    response = client.put(
        "/org/{org_id}/rooms/{room_id}/messages/{message_id}", json=fake_updated_message
    )

    assert response.status_code == 424
    assert response.json() == {"detail": {"message not edited": {}}}


def test_user_is_authorized_to_edit():
    """test response when user is authorized to edit message"""

    fake_updated_message["sender_id"] == fake_message_data["sender_id"]
    fake_response = {"message_id": "33090940900", "message_data": fake_updated_message}

    response = client.put(
        "/org/{org_id}/rooms/{room_id}/messages/{message_id}", json=fake_updated_message
    )

    assert response.status_code == 200
    assert response.json() == fake_response


def test_user_is_not_authorized_to_edit():
    """test response when user is not authorized to edit message"""

    fake_updated_message_payload["sender_id"] != fake_message_data["sender_id"]

    response = client.put(
        "/org/{org_id}/rooms/{room_id}/messages/{message_id}", json=fake_updated_message
    )

    assert response.status_code == 401
    assert response.json() == {"detail": {"unauthorized user": {}}}
