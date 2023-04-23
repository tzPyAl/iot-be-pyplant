import pytest

def test_create_sensor(test_user, authorized_client):
    response = authorized_client.post("/sensors/", json={"id":test_user["id"], "name":"qa_automation"})
    new_sensor = response.json()
    assert response.status_code == 201
    assert new_sensor["name"] == "qa_automation"

@pytest.mark.parametrize("name, i", [("1st title", 0), ("2nd title", 1), ("3rd title", 2)])
def test_get_all_sensors(authorized_client, test_sensors, name, i):
    response = authorized_client.get("/sensors/")
    assert response.status_code == 200
    all_sensors = response.json()
    assert name == all_sensors[i]["name"]

@pytest.mark.parametrize("name, i", [("1st title", 0), ("2nd title", 1), ("3rd title", 2)])
def test_get_sensor_by_id(authorized_client, test_sensors, name, i):
    response = authorized_client.get(f"/sensors/{i+1}")
    assert response.status_code == 200
    sensor = response.json()
    assert name == sensor["name"]

@pytest.mark.parametrize("name, i", [("1st title", 0), ("2nd title", 1), ("3rd title", 2)])
def test_update_sensor(authorized_client, test_sensors, name, i):
    response = authorized_client.put(f"/sensors/{i+1}", json={"name":"qa_automation"})
    assert response.status_code == 200
    sensor = response.json()
    assert sensor["name"] == "qa_automation"
