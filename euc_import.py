import json
import pandas as pd


class Dataset:

    def __init__(self, path, dataset_file="data.csv",
                 location_keyfile="location.json",
                 sample_keyfile="sample.json",
                 metadata_keyfile="metadata.json"):

        # Initialize data object
        self.data = {'location': [], 'sample': [], 'metadata': []}

        # Load the mappings to columns
        self.keys = {}
        self.load_keys(path + '/' + location_keyfile, 
                       path + '/' + sample_keyfile,
                       path + '/' + metadata_keyfile)

        # Load the data from csv file and store as a data object
        self.read_csv(path + '/' + dataset_file)

    def load_keys(self, location_keyfile=None, sample_keyfile=None, metadata_keyfile=None):

        files = {'location': location_keyfile,
                 'sample': sample_keyfile,
                 'metadata': metadata_keyfile}

        for key in files.keys():
            with open(files[key]) as f:
                self.keys[key] = json.load(f)

    def read_csv(self, filename):

        dataframe = pd.read_csv(filename)

        # Parse dataframe into location, sample, and metadata "sections"
        for idx, row in dataframe.iterrows():

            # Initialize data object
            data = {}
            for section_key in self.keys.keys():
                data[section_key] = {}

            for dataframe_col in dataframe.columns:

                for section_key in self.keys.keys():
                    if dataframe_col in self.keys[section_key]['keys']:
                        data[section_key][dataframe_col] = row[dataframe_col]

            for section_key in self.keys.keys():
                self.data[section_key].append(data[section_key])

    def get_locations(self, unique=True, to_file=None):

        location_array = []

        for location in self.data['location']:
            if unique:
                if location not in location_array:
                    location_array.append(location)
            else:
                location_array.append(location)

        if to_file:

            for location in location_array:
                location['biome_id'] = None
                location['biome_name'] = None
                location['environmental_feature_id'] = None
                location['environmental_feature_name'] = None

            columns = location_array[0].keys()

            df = pd.DataFrame(columns=columns)
            for location in location_array:
                data = []

                for key in location.keys():
                    data.append(location[key])

                df = df.append(pd.DataFrame(columns=columns, data=[data]), ignore_index=True)
            df.to_csv(to_file, index=False)

        return location_array


# Add ontology tag to object
def add_tag(self, data_object, key, tag_id=None, tag_name=None):
    new_object = {
        'id': tag_id,
        'name': tag_name
    }
    data_object[key] = new_object

    return data_object
