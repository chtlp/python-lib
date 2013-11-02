from pymongo import MongoClient
from pprint import pformat

class MongoStore(object):
    """
    A simple persistent hashtable-style storage backed up Mongo DB
    """

    def __init__(self, collection, host='localhost', port=27017,
                 db='python-mongo-store'):
        self.host, self.port, self.db_name, self.collection_name = \
            host, port, db, collection
        self.client = MongoClient(host,port)

        # get a database
        self.db = self.client[db]
        # get a collection
        self.collection = self.db[collection]

    def __getitem__(self, key):
        return self.collection.find_one({'key': key})['value']

    def __delitem__(self, key):
        self.collection.remove({'key': key})

    def __setitem__(self, key, value):
        self.collection.remove({'key': key})
        self.collection.insert({'key': key, 'value': value})

    def to_dict(self):
        d = {}
        for o in self.collection.find():
            d[o['key']] = o['value']
        return d

    def backup(self, new_collection_name):
        '''
        backup to another collection
        '''
        other_store = MongoStore(
            new_collection_name,
            self.host, self.port, self.db_name)
        for k, v in self.to_dict().iteritems():
            other_store[k] = v
        return other_store

    def __str__(self):
        return pformat(self.to_dict())

    def __repr__(self):
        header = 'MongoStore "%s"\n' % self.collection_name
        return header + str(self)

    def fsync(self, **kwargs):
        self.client.fsync(**kwargs)
