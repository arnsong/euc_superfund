from euc_import import Dataset
import pandas as pd

mapped_columns = {
    'location':  {
        "SITE": "site name"
    }
}

plot_mapped_columns = {
    'location':  {
        "SITE_NAME": "site name"
    }
}
marsh = Dataset("", "chesapeake_marsh.csv", mapped_columns=mapped_columns, location_keyfile='../location.json')
marsh_locations = marsh.get_locations()

plot = Dataset("", "chesapeake_plot.csv", mapped_columns=plot_mapped_columns, location_keyfile='../location.json')
plot_locations = plot.get_locations()

unique_locations = []

for location in (marsh_locations + plot_locations):
    if location not in unique_locations:
        unique_locations.append(location)

for location in unique_locations:
    location['biome_id'] = None
    location['biome_name'] = None
    location['environmental_feature_id'] = None
    location['environmental_feature_name'] = None

columns = unique_locations[0].keys()
df = pd.DataFrame(columns=columns)

for location in unique_locations:
    data = []

    for key in location.keys():
        data.append(location[key])
    df = df.append(pd.DataFrame(columns=columns, data=[data]), ignore_index=True)

df.to_csv("locations.csv", index=False)
