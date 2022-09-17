import requests
import json
from jsonschema import validate
import pandas as pd

# Variables
header1 = {'content/type': 'application/json', 'charset': 'UTF-8'}
uri = 'https://jsonplaceholder.typicode.com/'
path_param = 1
post_body = "{'title': 'foo', 'body': 'bar','userId': path_param}"
put_body = {'id': path_param, 'title': 'foo', 'body': 'bar', 'userId': 1}


# Function to validate that API response is adhering the expected schema
def validate_schema(file_name, val):
    with open(file_name) as f:
        schema1 = json.load(f)
    person = json.loads(val.text)
    validate(instance=person, schema=schema1)
    print("Schema of response matches with expected Schema!!")


# pytest -rA  test_API_Get.py::test_GET1 --html=report.html

def test_GET1():
    get_url_1 = uri + 'posts'
    response_get1 = requests.get(get_url_1, headers=header1)
    assert response_get1.status_code == 200
    print("Response code = ", response_get1.status_code)
    assert len(response_get1.json()) >= 100
    validate_schema("schema_GET1.json", response_get1)


# pytest -rA  test_API_Get.py::test_GET2 --html=report.html

def test_GET2():
    get_url_2 = uri + 'posts/' + str(path_param)
    response_get_2 = requests.get(url=get_url_2, headers=header1)
    assert response_get_2.status_code == 200
    print("Response code = ", response_get_2.status_code)
    validate_schema("schema_GET2.json", response_get_2)
    #Asserting that response has only 1 record
    assert len(pd.DataFrame(response_get_2.json(), index=[1])) == 1
    #Asseting that id in response matches the input
    assert response_get_2.json()['id'] == path_param


# pytest -rA  test_API_Get.py::test_GET3 --html=report.html

def test_GET3():
    get_url_3 = uri + 'invalidposts'
    response_get_3 = requests.get(url=get_url_3, headers=header1)
    assert response_get_3.status_code == 404
    print("Response code = ", response_get_3.status_code)
    print("header=", header1, "\n", "url=", get_url_3)
    print("Response_code=", response_get_3.status_code, '\nResponse Text =', response_get_3.text)


# pytest -rA  test_API_Get.py::test_POST --html=report.html

def test_POST():
    post_url = uri + 'posts'
    response_post = requests.post(url=post_url, headers=header1, data=post_body)
    assert response_post.status_code == 201
    print("Response code = ", response_post.status_code)
    validate_schema("schema_POST.json", response_post)
    print("Response:", '\n', response_post.text)
    print("User Id Created = ", response_post.json()['id'])
    #Validating that a record has been created successfully
    assert response_post.json()['id'] is not None


# pytest -rA  test_API_Get.py::test_PUT --html=report.html

def test_PUT():
    put_url = uri + 'posts/' + str(path_param)
    response_put = requests.put(url=put_url, headers=header1, json=put_body)
    assert response_put.status_code == 200
    print("Response code = ", response_put.status_code)
    validate_schema("schema_POST.json", response_put)
    print("Response:", '\n', response_put.text)
    print("User Id Updated = ", response_put.json()['id'])
    assert response_put.json()['id'] == path_param


# pytest -rA  test_API_Get.py::test_DELETE --html=report.html

def test_DELETE():
    delete_url = uri + 'posts/' + str(path_param)
    response_delete = requests.delete(url=delete_url, headers=header1)
    assert response_delete.status_code == 200
    print("Response code = ", response_delete.status_code)
    print("Response:", '\n', response_delete.text)
    #Validating the response
    assert len(response_delete.json()) == 0
