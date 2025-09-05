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
        "class": {"type": ["string", "null"]},
        "fuel_type": {"type": ["string", "null"]},
        "drive": {"type": ["string", "null"]},
        "cylinders": {"type": ["integer", "null"]},
        "displacement": {"type": ["number", "null"]},
        "transmission": {"type": ["string", "null"]},
        "city_mpg": {"type": ["string", "number", "null"]},
        "highway_mpg": {"type": ["string", "number", "null"]},
        "combination_mpg": {"type": ["string", "number", "null"]},
    },
    "required": ["make", "model", "year"],
    "additionalProperties": False,
}

CARS_RESPONSE_SCHEMA = {"type": "array", "items": CAR_SCHEMA, "minItems": 0}

VINLOOKUP_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "vin": {"type": "string"},
        "country": {"type": "string"},
        "manufacturer": {"type": "string"},
        "model": {"type": "string"},
        "class": {"type": "string"},
        "region": {"type": "string"},
        "wmi": {"type": "string"},
        "vds": {"type": "string"},
        "vis": {"type": "string"},
        "year": {"type": "integer"},
    },
}


def validate_cars_response(cars_data):
    """Validate cars response against schema"""
    jsonschema.validate(cars_data, CARS_RESPONSE_SCHEMA)


def validate_vin_response(vin_data):
    """Validate VIN response against schema"""
    jsonschema.validate(vin_data, VINLOOKUP_RESPONSE_SCHEMA)
