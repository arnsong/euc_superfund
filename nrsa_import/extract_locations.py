from euc_import import Dataset

mapped_columns = {
    'location':  {
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Site.Type": "urban",
        "State": "state",
        "site_id": "site_name"
    }
}

nrsa = Dataset("", "nrsa.csv", mapped_columns=mapped_columns, location_keyfile='../location.json')
nrsa.get_locations(to_file="locations.csv")
