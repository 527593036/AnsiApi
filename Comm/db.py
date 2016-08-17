# -*-coding: utf-8-*-
'''
Created on 2016年6月1日

@author: zhujin
'''

import pymysql
import time

class MySQL(object):
    def __init__(self, dbconfig):
        try:
            self._conn = pymysql.connect(host=dbconfig['host'],
                        user=dbconfig['user'],
                        password=dbconfig['password'],
                        db=dbconfig['db'],
                        charset=dbconfig['charset'],
                        connect_timeout=1,
                    )
        except pymysql.Error, e:
            raise e
            
        self._cur = self._conn.cursor()
        
    def create(self, sql):
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except pymysql.Error, e:
            raise e
    
    def drop(self, sql):
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except pymysql.Error, e:
            raise e
    
    def query(self, sql):
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            result = self._cur.fetchall()
            return result
        except pymysql.Error, e:
            print e
            
    def update(self, sql):
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except pymysql.Error, e:
            raise e
       
    def insert(self, sql):
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except pymysql.Error, e:
            raise e
            
    def delete(self, sql):
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except pymysql.Error, e:
            raise e
            
    def fetchAllRows(self):
        return self._cur.fetchall()
    
    def fetchOneRow(self):
        return self._cur.fetchone()
    
    def __del__(self):
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass
        
    def close(self):
        self.__del__()
        
        
            
        



