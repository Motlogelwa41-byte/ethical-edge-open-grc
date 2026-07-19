# test_validation.py
from schemas import Category
from pydantic import ValidationError

def test_bad_data():
    bad_data = {"title": "Test Cat", "principles": []} # Missing fields/wrong types
    try:
        Category(**bad_data)
    except ValidationError:
        print("✅ Validation test passed: Rejected malformed data.")
