from pymongo import MongoClient
from pprint import pformat

class MongoStore(object):
    """
    A simple persistent hashtable-style storage backed up Mongo DB
    """

    def __init__(self, collection, hostname='localhost', port=27017,
                 db='python-mongo-store'):

        self.client = MongoClient()
        self.client = MongoClient('localhost', 27017)

        # get a database
        self.db = self.client[db]
        # get a collection
        self.collection_name = collection
        self.collection = self.db[collection]

    def __getitem__(self, key):
        return self.collection.find_one({'key': ind})

    def __setitem__(self, key, value):
        self.collection.remove({'key': key})
        self.collection.insert({'key': key, 'value': value})

    def to_dict(self):
        d = {}
        for o in self.collection.find():
            d[o['key']] = o['value']
        return d

    def __str__(self):
        return pformat(self.to_dict())

    def __repr__(self):
        header = 'MongoStore "%s"\n' % self.collection_name
        return header + str(self)

    def fsync(self, **kwargs):
        self.client.fsync(**kwargs)
