from euc_import import Dataset

mapped_columns = {
    'location':  {
        "station": "site_name",
        "stat_alt": "site_code"
    }
}

ncca = Dataset("", "ncca.csv", mapped_columns=mapped_columns, location_keyfile='../location.json')
ncca.get_locations(to_file="locations.csv")
