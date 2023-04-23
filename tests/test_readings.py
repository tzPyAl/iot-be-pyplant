import pytest

def test_create_reading(authorized_client, test_readings, test_user):
    response = authorized_client.post("/readings/", json={"sensor_id":1, "name":"qa_automation", "reading":11})
    new_reading = response.json()
    assert response.status_code == 201
    assert new_reading["name"] == "qa_automation"
    assert new_reading["reading"] == "11"
    assert new_reading["sensor"]["id"] == 1
    assert new_reading["sensor"]["name"] == "1st title"
    print(f"OVDJE {test_user}")
    assert new_reading["sensor"]["owner"]["id"] == test_user["id"]
    assert new_reading["sensor"]["owner"]["email"] == test_user["email"]

def test_get_all_sensors(authorized_client, test_readings):
    response = authorized_client.get("/sensors/")
    assert response.status_code == 200
