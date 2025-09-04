"""
JSON Schemas for API validation
"""
import jsonschema


CAR_SCHEMA = {
    "type": "object",
    "properties": {
        "make": {"type": "string"},
        "model": {"type": "string"},
        "year": {"type": "integer", "minimum": 1900, "maximum": 2030},
        "class": {"type": ["string", "null"]},  # Car class (e.g., "midsize car")
        "fuel_type": {"type": ["string", "null"]},
        "drive": {"type": ["string", "null"]},
        "cylinders": {"type": ["integer", "null"]},
        "displacement": {"type": ["number", "null"]},
        "transmission": {"type": ["string", "null"]},
        "city_mpg": {"type": ["string", "number", "null"]},
        "highway_mpg": {"type": ["string", "number", "null"]},
        "combination_mpg": {"type": ["string", "number", "null"]}
    },
    "required": ["make", "model", "year"],
    "additionalProperties": False
}

CARS_RESPONSE_SCHEMA = {
    "type": "array",
    "items": CAR_SCHEMA,
    "minItems": 0
}

# Helper function to validate car data
def validate_car_data(car_data):
    """Validate single car data against schema"""
    jsonschema.validate(car_data, CAR_SCHEMA)

def validate_cars_response(cars_data):
    """Validate cars response against schema"""
    jsonschema.validate(cars_data, CARS_RESPONSE_SCHEMA)
