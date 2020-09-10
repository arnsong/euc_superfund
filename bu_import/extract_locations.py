from euc_import import Dataset
from euc_import import write_out_unique_locations

mapped_columns = {
    'location':  {
        "station": "site_name",
        "AOC_name": "subsite",
    }
}

sweden_mapped_columns = {
    'location':  {
        "Station": "site_name",
        "Stat_id": "site_id",
        "Longitute": "longitude",
        "Latitude": "latitude",
        "Kommun": "city",
        "county code": "county_code"
    }
}
nbh = Dataset("", "NBHFishTissueData_2003-2016.csv", mapped_columns=mapped_columns,
              location_keyfile='../location.json')
nbh_locations = nbh.get_locations()

sweden = Dataset("", "sweden_data.csv", mapped_columns=sweden_mapped_columns, location_keyfile='../location.json')
sweden_locations = sweden.get_locations()
write_out_unique_locations(nbh_locations + sweden_locations)
