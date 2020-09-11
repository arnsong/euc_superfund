from dataset import Dataset

sweden_mapped_columns = {
    'location':  {
        "Station": "site_name",
        "Stat_Id": "site_id",
        "Longitude": "longitude",
        "Latitude": "latitude",
        "Kommun": "city",
        "county code": "county_code"
    }
}

sweden = Dataset("", "sweden_data.csv", mapped_columns=sweden_mapped_columns, location_keyfile='../location.json')
sweden_locations = sweden.get_locations(to_file="sweden_locations.csv")
