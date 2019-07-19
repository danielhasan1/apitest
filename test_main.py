from starlette.testclient import TestClient
from . main import app
client = TestClient(app)
'''
To run pytest on this file you have to change some importing of modules please do so in this order
first from main.py
replace line 11 with from .database import SessionLocal, engine
replace line 8 with from . import crud, models, schemas
from crud.py
replace line 2 with from . import models,schemas
from models.py
replace line 4 with from .database import Base
This is done becuase pytest module and uvicorn are located in different dirctories one is at parent level and another is in localvirtualenv 
it creates import with no known parent package
'''
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

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Go to '/docs'"}

class test_post:
  def test_post_location(self):
    response = client.post(
      "/post_location/",
      json={'loc':'1100000', 'address':'New New Delhi', 'city':'New Delhi', 'lat':2200, 'lon': 77000, 'accuracy': '3'}
      )
    assert response.status_code == 200
  #i = response.json()
  
    assert response.json() == {'loc':'1100000', 'address':'New New Delhi', 'city':'New Delhi', 'lat':2200, 'lon': 77000, 'accuracy': '3'}

  def test_adding_existing_record(self):
    response = client.post(
      "/post_location/",
      json={'loc':'1100000', 'address':'New New Delhi', 'city':'New Delhi', 'lat':2200, 'lon': 77000, 'accuracy': '3'}
      )
    assert response.status_code == 400
  def test_adding_nearby(self):
    response = client.post(
      "/post_location/",
      json={'loc':'11000001', 'address':'New New Delhi', 'city':'New Delhi', 'lat':28.6334, 'lon': 77.2168, 'accuracy': '3'}
      )
    assert response.status_code == 400
def test_call_on_post():
  t = test_post()
  t.test_post_location()
  t.test_adding_existing_record()
  t.test_adding_nearby()


def test_get_detect():
  response = client.get("/detect/28.6333/77.2167")
  assert response.status_code == 200
  assert response.json() == {
                            "Place": "Central Delhi",
                            "Region": "Delhi"
                            }
