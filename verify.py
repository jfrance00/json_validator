import json
import jsonschema

with open('data.json') as f:          # sets JSON data to 'data'
    data = json.load(f)


schema = {                            # schema to check against JSON to validate values, mandates all values are present
    "$schema": "http://json-schema.org/draft/2019-09/schema#",
    "required": ["vendor", "url", "series", "category", "model", "path", "release", "endofsale", "endofsupport", "downloads"],
    "properties": {
        "vendor": {
            "type": "string",
            "const": "cisco.com",     # Scrape is cisco products, so Cisco should always be the vendor
            },
        "url": {
            "type": "string",         # below regex checks for URL with 'cisco.com' optional 'www' and 'https://'
            "pattern": "^(https:\/\/)?(www.)?(cisco.com)(\/)[a-zA-Z\d+\!@#\$%&\/]{2,40}\/support\/[0-9a-zA-Z-\/]{4,}\/"
                       "(model|series).html"
        },
        "series": {
            "type": "string",
            "pattern": "^(?!null)"   # checks for null values which are not permitted in necessary fields
        },
        "category": {
            "type": "string",
            "pattern": "^(?!null)"
        },
        "model": {
            "type": "string",
            "pattern": "^(?!null)"
        },
        "path": {                          # TODO define pattern by what permitted in unix path
            "type": "string",
        },
        "release": {
            "type": "string",
            "pattern": "\d{10}",
        },
        "endofsale": {
            "type": "string",
            "pattern": "\d{10}|[null]",
        },
        "endofsupport": {
            "type": "string",
            "pattern": "\d{10}|[null]",
        },
        "downloads": {
            "type": "array",
            "items": [
                {
                    "type": "object",
                    "required": ["latest", "filename", "size", "md5"],
                    "properties": {
                        "latest": {"type": "string"},
                        "filename": {"type": "string"},
                        "size": {
                            "type": "string",
                            "pattern": "\d{7,8}",
                        },
                        "md5": {
                            "type": "string",
                            "pattern": "\w{32}",               # checks that key is 32 characters
                            },
                    }
                },
                {
                    "type": "object",
                    "required": ["all"],
                    "properties": {
                        "all": {
                            "type": "string",
                            "pattern": "^(https:\/\/)?(www)?(software\.)?(cisco.com)(\/)(download)[a-zA-Z\d+\!@#\$%&\/]{2,60}",
                        }
                    }
                },
            ]
        }
    },
}


def check_missing_keys(check_data):                  # check for keys likely to be missing
    optional_keys = ['endofsale', 'endofsupport']    # Checking for these keys because they may be null
    for product in check_data:                       # If other keys are missing data is irrelevant
        for key in optional_keys:
            if key not in product:
                product[key] = 'null'                # creates key if val
    return check_data


def convert_int_to_str(json_data):
    for item in json_data:
        item['release'] = str(item['release'])
        item['endofsale'] = str(item['endofsale'])
        item['endofsupport'] = str(item['endofsupport'])
        item['downloads'][0]['size'] = str(item['downloads'][0]['size'])
    return json_data


def validate_data(finalized_data):
    for item in finalized_data:
        try:
            jsonschema.validate(item, schema)
        except jsonschema.exceptions.ValidationError:
            v = jsonschema.Draft7Validator(schema)
            errors = sorted(v.iter_errors(item), key=lambda e: e.path)
            for error in errors:
                print(f'{error.message} in {item["model"]}, {item["url"]}')
            return "Error in data"
    print('data passes')
    return "data passes"

check_missing_keys(data)
convert_int_to_str(data)

# checks if all keys and values valid
validate_data(data)

