import pytest
import requests
import json

url = 'http://localhost:5000'

star = {'name': 'hello', 'distance': 100}
headers = {'Content-Type': 'application/json'}

def test_should_get_no_stars():
    r = requests.get(url + '/star')
    r.raise_for_status()
    assert r.json() == {'result': []}


def test_should_add_one_star():
    data = json.dumps(star)
    r = requests.post(url + '/star', headers = headers, data = data)
    r.raise_for_status()
    r = requests.get(url + '/star')
    assert r.json() == {'result': [star]}
