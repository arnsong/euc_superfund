from euc_import import Dataset

chesapeake = Dataset("smithsonian_import", "chesapeake_marsh.csv")
chesapeake.get_locations(to_file="smithsonian_locations.csv")
