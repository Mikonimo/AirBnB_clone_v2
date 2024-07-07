#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship('Review', cascade='all, delete-orphan', backref='place')

    @property
    def reviews(self):
        """Returns the list of review instances"""
        from models import storage
        reviews_list = []
        instances = storage.all(Review)

        for inst in instances.values():
            if Review.place_id == self.id:
                reviews_list.append(inst)
        return reviews_list

    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)

    @property
    def amenities(self):
        """Getter for amenities - returns the list of Amenity instances"""
        from models import storage

        amenity_objs = []
        for amenity_id in self.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenity_objs.append(amenity)
        return amenity_objs

    @amenities.setter
    def amenities(self, obj):
        """Setter for amenities - append an Amenity object to the amenity_ids list"""
        if isinstance(obj, Amenity):
            if obj.id not in self.amenity_ids:
                self.amenities_ids.append(obj.id)
        else:
            return
