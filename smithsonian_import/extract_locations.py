from ...euc_import import Dataset

chesapeake = Dataset("", "chesapeake_marsh.csv")
chesapeake.get_locations(to_file="locations.csv")
