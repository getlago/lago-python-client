from lago_python_client.models.base_model import BaseModel


class Subscription(BaseModel):

    def __init__(self, customer_id=None, plan_code=None):
        self.plan_code = plan_code
        self.customer_id = customer_id

    def to_dict(self):
        result = {
            'plan_code': self.plan_code,
            'customer_id': self.customer_id
        }
        return result
