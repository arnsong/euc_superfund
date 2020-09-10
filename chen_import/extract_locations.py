from euc_import import Dataset
from euc_import import write_out_unique_locations

mapped_columns = {
    'location': {
        "site name": "site_name",
        "site code": "site_code"
    }
}

sediment = Dataset("", "sediment_individual.csv", location_keyfile='../location.json', mapped_columns=mapped_columns)
sediment_locations = sediment.get_locations()

biota = Dataset("", "biota_individual.csv", location_keyfile='../location.json', mapped_columns=mapped_columns)
biota_locations = biota.get_locations()

water = Dataset("", "water_individual.csv", location_keyfile='../location.json', mapped_columns=mapped_columns)
water_locations = water.get_locations()
write_out_unique_locations(sediment_locations + biota_locations + water_locations)
