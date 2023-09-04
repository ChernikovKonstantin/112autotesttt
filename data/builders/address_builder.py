from dataclasses import dataclass
from typing import Optional

from data.builders.base_builder import BaseBuilder


@dataclass
class AddressFormData:
    full_address: Optional[str] = None
    country: Optional[str] = None
    subject: Optional[str] = None
    city: Optional[str] = None
    object_: Optional[str] = None
    admin_area: Optional[str] = None
    admin_district: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    housing: Optional[str] = None
    building: Optional[str] = None
    flat: Optional[str] = None
    entrance: Optional[str] = None
    floor: Optional[str] = None
    entrance_code: Optional[str] = None
    address_description: Optional[str] = None
    longitude: Optional[int] = None
    latitude: Optional[int] = None


class AddressBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self._full_address: Optional[str] = None
        self._country: Optional[str] = None
        self._subject: Optional[str] = None
        self._city: Optional[str] = None
        self._object_: Optional[str] = None
        self._admin_area: Optional[str] = None
        self._admin_district: Optional[str] = None
        self._street: Optional[str] = None
        self._house_number: Optional[str] = None
        self._housing: Optional[str] = None
        self._building: Optional[str] = None
        self._flat: Optional[str] = None
        self._entrance: Optional[str] = None
        self._floor: Optional[str] = None
        self._entrance_code: Optional[str] = None
        self._address_description: Optional[str] = None
        self._longitude: Optional[int] = None
        self._latitude: Optional[int] = None

    def with_full_address(self, full_address: str):
        self._full_address = full_address
        return self

    def with_country(self, country: str):
        self._country = country
        return self

    def with_subject(self, subject: str):
        self._subject = subject
        return self

    def with_city(self, city: str):
        self._city = city
        return self

    def with_object_(self, object_: str):
        self._object_ = object_
        return self

    def with_admin_area(self, admin_area: str):
        self._admin_area = admin_area
        return self

    def with_admin_district(self, admin_district: str):
        self._admin_district = admin_district
        return self

    def with_street(self, street: str):
        self._street = street
        return self

    def with_house_number(self, house_number: str):
        self._house_number = house_number
        return self

    def with_housing(self, housing: str):
        self._housing = housing
        return self

    def with_building(self, building: str):
        self._building = building
        return self

    def with_flat(self, flat: str):
        self._flat = flat
        return self

    def with_entrance(self, entrance: str):
        self._entrance = entrance
        return self

    def with_floor(self, floor: str):
        self._floor = floor
        return self

    def with_entrance_code(self, entrance_code: str):
        self._entrance_code = entrance_code
        return self

    def with_address_description(self, address_description: str):
        self._address_description = address_description
        return self

    def with_coordinates(self, longitude: int, latitude: int):
        self._longitude = longitude
        self._latitude = latitude
        return self

    def build(self):
        return AddressFormData(
            full_address=self._full_address,
            country=self._country,
            subject=self._subject,
            city=self._city,
            object_=self._object_,
            admin_area=self._admin_area,
            admin_district=self._admin_district,
            street=self._street,
            house_number=self._house_number,
            housing=self._housing,
            building=self._building,
            flat=self._flat,
            entrance=self._entrance,
            floor=self._floor,
            entrance_code=self._entrance_code,
            address_description=self._address_description,
            longitude=self._longitude,
            latitude=self._latitude,
        )
