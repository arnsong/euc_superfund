SEDIMENT_FIELD_MAP = {
    "location": {
        "site_name": "site name",
        "site_code": "site code",
        "state": "state",
        "system": "system",
        "subsite": "subsite",
        "coordinates": {
            "latitude": "latitude",
            "longitude": "longitude"
        },
        "biome": {
            "id": "",
            "name": ""
        },
        "environmental_feature": {
            "id": "",
            "name": ""
        }
    },
    "date": "",  # Special case "sample_year-sample_month"
    "sample": {
        "sampling_type": "sample type",
        "depth": {
            "value": "sample depth (cm)",
            "units": {
                "id": "",
                "name": ""
            }
        },
        "environmental_material": {
            "id": "",
            "name": ""
        },
        "compounds": [
            {
                "id": "CHEBI:49747",  # Use logic to insert this label if it's not found in the field names
                "name": "methylmercury(1+)",
                "value": "sediment MeHg (ng/g DW)",
                "units": {
                    "id": "UO:0000163",
                    "name": "mass percentage",
                    "numerator": {
                        "id": "UO:0000024",
                        "name": "nanogram"
                    },
                    "denominator": {
                        "id": "UO:0000021",
                        "name": "gram"
                    },
                    "description": "dry weight"
                }
            },
            {
                "id": "CHEBI:25706",
                "name": "total mercury",
                "value": "sediment THg (ng/g DW)",
                "units": {
                    "id": "UO:0000163",
                    "name": "mass percentage",
                    "numerator": {
                        "id": "UO:0000024",
                        "name": "nanogram"
                    },
                    "denominator": {
                        "id": "UO:0000021",
                        "name": "gram"
                    },
                    "description": "dry weight"
                }
            }
        ],
        "LOI": {
            "value": "%LOI",
            "long name": "loss on ignition"
        }
    }
}

# SITE_FIELD_MAP = {
#     "name": "site name",
#     "code": "site code",
#     "state": "state",
#     "system": "system",
#     "latitude": "latitude",
#     "longitude": "longitude",
# }
#
# SAMPLE_FIELD_MAP = {
#     "month": "sample month",
#     "day": "sample day",
#     "year": "sample day",
#     "type": "sample type",
#     "depth": "sample depth (cm)"
# }
