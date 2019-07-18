from starlette.testclient import TestClient
from . main import app
client = TestClient(app)

def test_read_item():
    response = client.get("/get_using_postgres/28.6333/77.2167/2")
    assert response.status_code == 200
    assert response.json() == res

res = [
  {
    "address": "Aliganj",
    "loc": "IN/110003",
    "lat": 28.65,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Rashtrapati Bhawan",
    "loc": "IN/110004",
    "lat": 28.65,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Lower Camp Anand Parbat",
    "loc": "IN/110005",
    "lat": 28.65,
    "lon": 77.2,
    "city": "New Delhi"
  },
  {
    "address": "Bara Tooti",
    "loc": "IN/110006",
    "lat": 28.65,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Patel Nagar",
    "loc": "IN/110008",
    "lat": 28.65,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Azad Nagar",
    "loc": "IN/110051",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Wazirpur Phase Iii",
    "loc": "IN/110052",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Zafrabad",
    "loc": "IN/110053",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Civil Lines",
    "loc": "IN/110054",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Paharganj",
    "loc": "IN/110055",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Shakurbasti",
    "loc": "IN/110056",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Munirka",
    "loc": "IN/110057",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Janakpuri",
    "loc": "IN/110058",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  },
  {
    "address": "Uttam Nagar",
    "loc": "IN/110059",
    "lat": 28.6167,
    "lon": 77.2167,
    "city": "New Delhi"
  }
]
'''
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Go to '/docs'"}
    '''