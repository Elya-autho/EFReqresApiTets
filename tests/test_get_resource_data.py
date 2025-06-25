import httpx
import jsonschema
from jsonschema import validate
from core.contracts import LIST_RESOURCE_SCHEMA
HEADERS = {
    "x-api-key": "reqres-free-v1"
}
BASE_URL = "https://reqres.in/"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "api/unknown/23"

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