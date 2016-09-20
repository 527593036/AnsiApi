# -*-coding: utf-8-*-
'''
Created on 2016年9月16日

@author: zhujin
'''


import pymongo


class Mongo(object):
    def __init__(self,mgdbconfig):
        try:
            self.conn = pymongo.Connection(
                "mongodb://%s:%s@%s:%d" % (mgdbconfig['user'],
                    mgdbconfig['password'],
                    mgdbconfig['host'],
                    mgdbconfig['port'])
            )
            self.db = self.conn[mgdbconfig['db']]
        except pymongo.errors, e:
            raise e
            
    def find(self, coll, require):
        return self.db[coll].find(require)
        
    def find_one(self, coll, require):
        return self.db[coll].find_one(require)
        
    def insert(self, coll, require):
        return self.db[coll].insert(require)
        
    def insert_many(self, coll, require):
        return self.db[coll].insert_many(require)
        