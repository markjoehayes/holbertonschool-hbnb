from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.models.base_model import BaseModel, Base
from app.models.user import User
# import other models as needed: Place, Amenity, Review

class DBStorage:
    """Database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('sqlite:///hbnb.db', echo=True)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        if cls:
            return {obj.id: obj for obj in self.__session.query(cls).all()}
        result = {}
        for cl in [User]:  # add Place, Amenity, Review if needed
            for obj in self.__session.query(cl).all():
                result[obj.id] = obj
        return result

    def get(self, cls, obj_id):
        return self.__session.query(cls).get(obj_id)

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def reload(self):
        Base.metadata.create_all(self.__engine)

