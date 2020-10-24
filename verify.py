import json
import jsonschema

# verify field names match
# verify item coverage (all products in JSON)
# verify field coverage (all items contain all fields)

# check for repeats -> best practice? seems reasonable to choose unique ID and add to list and check list for ID


with open('data.json') as f:              # sets JSON data to 'data'
    data = json.load(f)


schema = {                                # schema to check against JSON to validate values TODO put in own file?
    "$schema": "http://json-schema.org/draft/2019-09/schema#",
    "required": ["vendor", "url", "series", "category", "path", "release", "endofsale", "endofsupport", "downloads"],
    "properties": {
        "vendor": {
            "type": "string",
            "const": "cisco.com",          # Scrape is cisco products, so Cisco should always be the vendor
            },
        "url": {
            "type": "string",              # below regex checks for URL with 'cisco.com' optional 'www' and 'https://'
            "pattern": "^(https:\/\/)?(www.)?(cisco.com)(\/)[a-zA-Z\d+\!@#\$%&\/]{2,40}\/support\/[0-9a-zA-Z-\/]{4,}\/"
                       "(model|series).html"
        },
        "series": {
            "type": "string",
        },
        "category": {
            "type": "string",
        },
        "model": {
            "type": "string",
        },
        "path": {                    # check for unix structure
            "type": "string",
            "format": "uri",
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
            "required": ["latest", "filesname", "size", "md5", "all"],
            "items": {
                "type": "object",
                "properties": {
                    "latest": {"type": "string"},
                    "filename": {"type": "string"},
                    "size": {
                        "type": "string",
                        "pattern": "\d{7,8}",
                    },
                    "md5": {
                        "type": "string",
                        "pattern": "\w{32}",
                            },
                    "all": {"type": "string"}
                }
            },
        }
    }
}


def check_missing_keys(check_data):                  # check for keys likely to be missing
    optional_keys = ['endofsale', 'endofsupport']    # Checking for these keys because they may be null
    for product in check_data:                       # If other keys are missing data is irrelevant
        for key in optional_keys:
            if key not in product:
                product[key] = 'null'
    return check_data


def convert_int_to_str(json_data):
    for item in json_data:
        item['release'] = str(item['release'])
        item['endofsale'] = str(item['endofsale'])
        item['endofsupport'] = str(item['endofsupport'])
        item['downloads'][0]['size'] = str(item['downloads'][0]['size'])
    return json_data


def validate_data(cleaned_data):
    for i, item in enumerate(cleaned_data):
        print(f'item {i}: {jsonschema.validate(item, schema)}')
        # what best to return if data checks out?


# checks/formats data
all_keys = check_missing_keys(data)
data_as_strings = convert_int_to_str(all_keys)

# checks if data valid
validate_data(data_as_strings)                     # main checking function called with sterilized data

