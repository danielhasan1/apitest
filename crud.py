from sqlalchemy.orm import Session

from . import models,schemas
#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))





def get_loc_by_pincode(db:Session, pincode: str):
    return db.query(models.pin).filter(models.pin.loc == pincode).first()


def get_loc_by_lat_lon(db:Session, latitude: float, longitude: float):
    return db.query(models.pin).filter(models.pin.lat == latitude and models.pin.lon == longitude).first()

def get(db: Session):
    return db.query(models.pin).all()

def get_b(db:Session):
    return db.query(models.pol).all()


def create_record(db: Session, location: schemas.Loc):
    #print(location.loc, location.address,location.lat,location.lon,location.city,location.accuracy)
    db_record = models.pin(loc = location.loc, address=location.address,city=location.city,lat=location.lat,lon=location.lon,accuracy=location.accuracy)
    return_record = dict(loc = location.loc, address=location.address,city=location.city,lat=location.lat,lon=location.lon,accuracy=location.accuracy)
    print(db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return return_record
