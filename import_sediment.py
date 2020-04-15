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


client = MongoClient()
db = client.euc_prototype

examples = db.examples

with open('chen_import/sediment_individual.csv', newline='') as csv_file:
    reader = DictReader(csv_file)
    for current_row in reader:
        document = deepcopy(constant.SEDIMENT_FIELD_MAP)
        assign_values(document, current_row)
        examples.insert_one(document)
