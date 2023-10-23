#!/usr/bin/python3

"""
A module that defines Place class using ORM
"""
from os import getenv
from sqlalchemy import Table
from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import ColumnDefault
from sqlalchemy.orm import relationship
from models.base_model import Base
from models.base_model import BaseModel

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """
    Defines attributes for a Place table
    """
    __tablename__ = 'places'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            'Review', backref='place', cascade='all, delete, delete-orphan'
        )
        amenities = relationship(
            'Amenity', secondary=place_amenity,
            back_populates='place_amenities', viewonly=False
        )
    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Fetches reviews related to a place object from file storage"""
            from models import storage
            from models.review import Review
            revs = list(storage.all(Review).values())
            return [r for r in revs if r.place_id == self.id]

        @property
        def amenities(self):
            """
            Returns (list): List of Amenities linked to Place instance
            """
            from models import storage
            from models.amenity import Amenity
            amenitees = storage.all(Amenity).values()
            return [a for a in amenitees if a.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """
            Appends an Amenity object to amenity_ids
            """
            from models.amenity import Amenity
            if isinstance(obj, Amenity) and type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
