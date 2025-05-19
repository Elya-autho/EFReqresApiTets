import httpx
import pytest
import jsonschema
from jsonschema import validate
from core.contracts import USER_DATA_SCHEMA
from core.contracts import LIST_RESOURCE_SCHEMA
HEADERS = {
    "x-api-key": "reqres-free-v1"
}
BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
SINGLE_USERS = "api/users/2"
NOT_FOUND_USER = "api/users/23"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "api/unknown/23"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS ="-image.jpg"
def test_get_list_users():
    responce = httpx.get(BASE_URL+LIST_USERS, headers=HEADERS)
    assert responce.status_code == 200
    data = responce.json()["data"]
    for item in data:
        validate(item, USER_DATA_SCHEMA)
        assert item["email"].endswith(EMAIL_ENDS)
        assert item["avatar"].endswith(str(item['id']) + AVATAR_ENDS)

def test_single_user():

    responce = httpx.get(BASE_URL + SINGLE_USERS, headers=HEADERS)
    assert responce.status_code == 200
    data = responce.json()["data"]

    assert data["email"].endswith(EMAIL_ENDS)
    assert data["avatar"].endswith(str(data['id']) + AVATAR_ENDS)

def test_user_not_found():

    responce = httpx.get(BASE_URL + NOT_FOUND_USER, headers=HEADERS)
    assert responce.status_code == 404

def test_list_resource():
    responce = httpx.get(BASE_URL + LIST_RESOURCE, headers=HEADERS)
    assert responce.status_code == 200
    data = responce.json()["data"]
    for item in data:
        validate(item, LIST_RESOURCE_SCHEMA)

def test_single_resource():
    responce = httpx.get(BASE_URL + SINGLE_RESOURCE, headers=HEADERS)
    assert responce.status_code == 200
    data = responce.json()["data"]
    jsonschema.validate(data,LIST_RESOURCE_SCHEMA)

def test_single_resource_not_found():
    responce = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND, headers=HEADERS)
    assert responce.status_code == 404
