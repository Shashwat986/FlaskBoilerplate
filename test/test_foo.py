import requests
import random

BASE_URL = "http://localhost:5000"


def test_foo():
    r = requests.get(BASE_URL + "/foo")
    assert r.status_code == 200

    json = r.json()

    assert "hello" in json
    assert json["hello"] == "world"


def test_bar_validation_failure():
    r = requests.post(BASE_URL + "/bar", json={"input": "asdf"})
    assert r.status_code == 200

    json = r.json()

    assert "success" in json
    assert json["success"] == False


def test_bar():
    i = [str(random.randint(1, 10)) for _ in range(2)]
    r = requests.post(
        BASE_URL + "/bar",
        json={"hello": "world", "world": [{"color": i[0]}, {"color": i[1]}]},
    )
    assert r.status_code == 200

    json = r.json()
    print(json)

    assert json["count"] == 2
    assert len(json["data"]) == 2
    assert json["data"] == i


def test_bar_password_failure():
    i = [str(random.randint(1, 10)) for _ in range(2)]
    r = requests.post(
        BASE_URL + "/bar",
        json={"hello": "not-world", "world": [{"color": i[0]}, {"color": i[1]}]},
    )
    assert r.status_code == 200

    json = r.json()

    assert "success" in json
    assert json["success"] == False
    assert json["message"] == "Password Error"
