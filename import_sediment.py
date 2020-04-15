import constant
from copy import deepcopy
from csv import DictReader
from pymongo import MongoClient


def assign_values(doc, row):
    for k, v in doc.items():
        if isinstance(v, list):
            for element in v:
                assign_values(element, row)
        elif isinstance(v, dict):
            assign_values(v, row)
        else:
            if v in row:
                doc[k] = row[v]
            else:
                doc[k] = v


with open('chen_import/sediment_individual.csv', newline='') as csv_file:
    reader = DictReader(csv_file)
    for current_row in reader:
        document = deepcopy(constant.SEDIMENT_FIELD_MAP)
        assign_values(document, current_row)
        print("Filled in doc: {0}".format(document))


# client = MongoClient()
#
# db = client.euc_test
#
# site = {"name": "Above",
#         "code": "A",
#         "state": "ME",
#         "system": "Penobscot River",
#         "latitude": 44.76309,
#         "longitude": -68.80048}
#
# sites = db.sites
# site_id = sites.insert_one(site).inserted_id
# sample = {"month": "July",
#           "year": 2016,
#           "type": "grab",
#           "depth": "0-2",
#           "kind": "sediment",
#           "molecule": "methylmercury",
#           "units": "ng/g DW",
#           "value": 1.62,
#           "sited_id": site_id,
#           "chebi_id": 30785}
#
# samples = db.samples
# samples.insert_one(sample)
