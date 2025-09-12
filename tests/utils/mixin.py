import os


def mock_response(mock: str):
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    my_data_path = os.path.join(parent_dir, "fixtures/" + mock + ".json")

    with open(my_data_path, "rb") as applied_coupon_response:
        return applied_coupon_response.read()
