import pytest
import requests
import json

url = 'http://localhost:5000'

headers = {'Content-Type': 'application/json'}


def test_should_have_hello():
    r = requests.get(url + '/')
    assert r.json() == {'Hello': 'World!'}


def test_should_get_big_json_blob():
    data = json.dumps({})
    r = requests.post(url + '/payload/receive', headers = headers, data = data)
    r.raise_for_status()
    assert 'entities' in r.json()

def test_should_send_big_json_blob():
    data = json.dumps({})
    r = requests.post(url + '/payload/send', headers = headers, data = data)
    r.raise_for_status()
    assert r.json() == {'size': 2}