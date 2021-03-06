from typing import List
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response
import sqlalchemy as sqla
import crud, models, schemas
import re
import math as m
from database import SessionLocal, engine
from math import sin, cos, sqrt, atan2, radians
import csv
import json
import os
#models.Base.metadata.create_all(bind=engine) alternative of this is create which create everything at runtime
from starlette.testclient import TestClient
app = FastAPI()

#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))


@app.get("/")
async def root():
	return {"message": "Go to '/docs'"}

client = TestClient(root)

def t():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Go to '/docs'"}

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db

@app.post("/post_location/", response_model=schemas.Loc)
def post_location(loc:schemas.Loc, db: Session = Depends(get_db)):
    db_check = crud.get_loc_by_pincode(db,pincode = loc.loc)
    #print(loc.loc)
    if db_check:
        raise HTTPException(status_code=400, detail="pincode already exist")
    db_check = crud.get_loc_by_lat_lon(db,latitude = loc.lat, longitude=loc.lon)
    if db_check:
        raise HTTPException(status_code=400, detail="coordinates already exist")
    row = db.execute("SELECT * FROM pincode WHERE earth_box(ll_to_earth({},{}),2500/1.609) @> ll_to_earth(lat,lon)" .format(loc.lat,loc.lon))
    for i in row:
        st = "coordinates are not accurate too close to existing " + str(i[1]) + ' ' + str(i[2]) + ' ' + str(i[4]) + ' ' + str(i[5])
        raise HTTPException(status_code=400,detail=st)
    return (crud.create_record(db=db,location=loc))
    return {'df':32}


@app.get("/get_using_self/{lat}/{lon}/{rad}")
def get_near(lat:float,lon:float,rad:float,db: Session = Depends(get_db)):
    R = 6373.0
    li = []
    row = crud.get(db)
    lat1 = radians(lat)
    lon1 = radians(lon)
    given_radii = rad
    for i in row:
        if i.lat is None or i.lon is None:
            continue
        lat2 = radians(float(i.lat))
        lon2 = radians(float(i.lon))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2.0)**2.0 + cos(lat1) * cos(lat2) * sin(dlon / 2.0)**2.0
        c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a))
        distance = R * c
        if distance <= given_radii:
            #print(distance)
            li.append(i)
    return li
@app.get('/create')
def create(db: Session = Depends(get_db)):
    if os.name == 'nt':
        ospath = "\\"
    else:
        ospath = "/"
    with open (os.getcwd()+ospath+'IN.csv','r') as f:
        reader = csv.reader(f)
        columns = next(reader) 
        value = 2000000000
        #cursor = connection.cursor()
        cursor = engine.connect()
        #cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION cube")
        cursor.execute("CREATE EXTENSION earthdistance")
        cursor.execute("CREATE TABLE pincode (id serial primary key, loc character varying(20) NOT NULL,address character varying(50),city character varying(50),lat double precision,lon double precision,accuracy character varying(10))")

        for row in reader: # Iterate through csv
            cursor.execute("INSERT INTO pincode(loc,address,city,lat,lon,accuracy) VALUES ('{}', '{}', '{}', '{}', '{}','{}')" .format(row[0], row[1], row[2], row[3] if row[3] else value, row[4] if row[4] else value,row[5] if row[5] else value))
        f.close()
    cursor.execute("CREATE TABLE poly(name character varying(50) primary key, parent character varying(50), cord text)")
    with open (os.getcwd()+ospath+'map.json','r') as f:
        ff = json.load(f)
        for i in ff['features']:
            #print(i['properties']['name'])
            cursor.execute("INSERT INTO poly VALUES ('{}', '{}', '{}')" .format(i['properties']['name'], i['properties']['parent'], i['geometry']['coordinates']))

    '''
    with open (os.getcwd()+'/'+'IN.csv','r') as f:
        reader = csv.reader(f)
        columns = next(reader) 
        value = 2000000000
        idd = 1
        db.execute("CREATE EXTENSION cube")
        db.execute("CREATE EXTENSION earthdistance")
        #row = db.execute("select * from pincod limit 10")
        
        #l = [{'address':i[1],'loc':i[0],'lat':i[3],'lon':i[4],'city':i[2]} for i in row]
        #print(l)
        #return l
        
        db.execute("CREATE TABLE pincod (loc character varying(20) NOT NULL,address character varying(50),city character varying(50),lat double precision,lon double precision,accuracy character varying(10))")
        for row in reader: # Iterate through csv
            db.execute("INSERT INTO pincod VALUES ({},'{}', '{}', '{}', '{}', '{}','{}')" .format(idd,row[0], row[1], row[2], row[3] if row[3] else value, row[4] if row[4] else value,row[5] if row[5] else value))
            idd += 1
    db.execute("CREATE TABLE poly(name character varying(50), parent character varying(50), cord text)")
    with open (os.getcwd()+'/'+'map.json','r') as f:
        ff = json.load(f)
        for i in ff['features']:
            db.execute("INSERT INTO poly VALUES ('{}', '{}', '{}')" .format(i['properties']['name'], i['properties']['parent'], i['geometry']['coordinates']))
'''
@app.get('/get_using_postgres/{lat}/{lon}/{rad}')
def get_near2(lat:float,lon:float,rad:float,db: Session = Depends(get_db)):
    rad = rad * 1000
    '''
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    user = session.query().from_statement(
    text("SELECT * FROM pincode")).all()
    '''
    row = db.execute("SELECT * FROM pincode WHERE earth_box(ll_to_earth({},{}),{}) @> ll_to_earth(lat,lon)" .format(lat,lon,rad))
    for i in row:
        l = [{'address':i[1],'loc':i[0],'lat':i[3],'lon':i[4],'city':i[2]} for i in row]
        #print(l)
    return l


def angle2D(y1,x1,y2,x2,PI,TWOPI):
    theta1 = m.atan2(y1,x1)
    theta2 = m.atan2(y2,x2)
    dtheta = theta2-theta1
    while dtheta > PI:
        dtheta -= TWOPI
    while dtheta < -PI:
        dtheta +=TWOPI
    return dtheta

@app.get('/detect/{user_lat}/{user_lon}')
def detec(user_lat:float, user_lon:float,db: Session = Depends(get_db)):
    PI = (3.14159265)
    TWOPI = 2 * PI
    angle = 0
    row = crud.get_b(db)
    size = len(row)
    for i in row:
        s = i.cord
        #print(i.name)
        m = re.search(r"\[([0-9,. ]+)\]",s)
        lat = []
        lon = []
        while m:
            s = s[:m.start()] +'-'+ s[m.end() + 1:]
            raw_string = m.group(1).split(',')
            temp1 = float(raw_string[1])
            lat.append(temp1)
            temp1 = float(raw_string[0])
            lon.append(temp1)
            m = re.search(r"\[([0-9,. ]+)\]",s)
        n = len(lat)
        for j in range(n):
            point1Lat = lat[j] - user_lat
            point1Lon = lon[j] - user_lon
            point2Lat = lat[(j+1)%n] - user_lat
            point2Lon = lon[(j+1)%n] - user_lon
            angle += float(angle2D(point1Lat,point1Lon,point2Lat,point2Lon,PI,TWOPI))
        if abs(angle) < PI:
            angle = 0
            if i == size-1:
                return []
            continue
        else:
            return {'Place':i.name,'Region':i.parent}
                

    return {'detail':'given cordinates might not be accurate to match any given boundary cordinates plz try more accurate cordinates like 28.6333,77.2167 or 28.5555, 77.1111'}

