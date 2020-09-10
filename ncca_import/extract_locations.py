from euc_import import Dataset

mapped_columns = {
    'location':  {
        "station": "site name",
        "stat_alt": "site code"
    }
}

ncca = Dataset("", "ncca.csv", mapped_columns=mapped_columns)
ncca.get_locations(to_file="locations.csv")
