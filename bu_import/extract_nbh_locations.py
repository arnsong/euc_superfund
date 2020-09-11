from dataset import Dataset

mapped_columns = {
    'location':  {
        "station": "site_name",
        "AOC_name": "subsite",
    }
}

nbh = Dataset("", "NBHFishTissueData_2003-2016.csv", mapped_columns=mapped_columns,
              location_keyfile='../location.json')
nbh_locations = nbh.get_locations(to_file="nbh_locations.csv")
