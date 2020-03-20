from pymongo import MongoClient

client = MongoClient()

db = client.euc_test

site = {"name": "Above",
        "code": "A",
        "state": "ME",
        "system": "Penobscot River",
        "latitude": 44.76309,
        "longitude": -68.80048}

sites = db.sites
site_id = sites.insert_one(site).inserted_id
sample = {"month": "July",
          "year": 2016,
          "type": "grab",
          "depth": "0-2",
          "kind": "sediment",
          "molecule": "methylmercury",
          "units": "ng/g DW",
          "value": 1.62,
          "sited_id": site_id,
          "chebi_id": 30785}

samples = db.samples
samples.insert_one(sample)
