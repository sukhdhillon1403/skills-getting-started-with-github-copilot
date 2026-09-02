from copy import deepcopy

from fastapi.testclient import TestClient

import src.app as app_module


def test_unregister_participant():
    original_activities = deepcopy(app_module.activities)
    client = TestClient(app_module.app)

    response = client.delete("/activities/Chess%20Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]

    app_module.activities.clear()
    app_module.activities.update(original_activities)


def test_unregister_missing_participant():
    original_activities = deepcopy(app_module.activities)
    client = TestClient(app_module.app)

    response = client.delete("/activities/Chess%20Club/participants/ghost@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}

    app_module.activities.clear()
    app_module.activities.update(original_activities)
