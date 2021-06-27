class Address:
    def __init__(
            self,
            id: int,
            address: str,
            zip_code: str,
            province: str,
            city: str,
            floor: str = None,
            apartment: str = None
    ):
        self.id = id
        self.address = address
        self.zip_code = zip_code
        self.province = province
        self.city = city
        self.floor = floor
        self.apartment = apartment

    def to_json(self):
        return {
            "id": self.id,
            "address": self.address,
            "zip_code": self.zip_code,
            "province": self.province,
            "city": self.city,
            "floor": self.floor,
            "apartment": self.apartment
        }
