from lago_python_client.models.base_model import BaseModel


class Customer(BaseModel):

    def __init__(self, customer_id=None, address_line1=None, address_line2=None, city=None, country=None, email=None,
                 legal_name=None, legal_number=None, logo_url=None, name=None, phone=None, state=None, url=None,
                 vat_rate=None, zipcode=None):
        self.customer_id = customer_id
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.country = country
        self.email = email
        self.legal_name = legal_name
        self.legal_number = legal_number
        self.logo_url = logo_url
        self.name = name
        self.phone = phone
        self.state = state
        self.url = url
        self.vat_rate = vat_rate
        self.zipcode = zipcode

    def to_dict(self):
        result = {
            'customer_id': self.customer_id,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'country': self.country,
            'email': self.email,
            'legal_name': self.legal_name,
            'legal_number': self.legal_number,
            'logo_url': self.logo_url,
            'name': self.name,
            'phone': self.phone,
            'state': self.state,
            'url': self.url,
            'vat_rate': self.vat_rate,
            'zipcode': self.zipcode
        }
        return result
