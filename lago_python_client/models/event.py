from lago_python_client.models.base_model import BaseModel


class Event(BaseModel):

    def __init__(self, transaction_id=None, customer_id=None, code=None, timestamp=None, properties=None):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.code = code
        self.timestamp = timestamp
        self.properties = properties

    def to_dict(self):
        result = {
            'transaction_id': self.transaction_id,
            'customer_id': self.customer_id,
            'code': self.code,
            'timestamp': self.timestamp,
            'properties': self.properties
        }
        return result
