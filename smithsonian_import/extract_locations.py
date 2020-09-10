from euc_import import Dataset
from euc_import import write_out_unique_locations

mapped_columns = {
    'location':  {
        "SITE": "site_name"
    }
}

plot_mapped_columns = {
    'location':  {
        "SITE_NAME": "site_name"
    }
}
marsh = Dataset("", "chesapeake_marsh.csv", mapped_columns=mapped_columns, location_keyfile='../location.json')
marsh_locations = marsh.get_locations()

plot = Dataset("", "chesapeake_plot.csv", mapped_columns=plot_mapped_columns, location_keyfile='../location.json')
plot_locations = plot.get_locations()
write_out_unique_locations(marsh_locations + plot_locations)
