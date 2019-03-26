#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/1/25 19:44
# @Author  : zengyang@tv365.net(ZengYang)
# @File    : db_conn.py
# @Software: PyCharm
# @ToUse  :

import pymysql, pymssql
from DBUtils.PooledDB import PooledDB


class Database:
    def __init__(self, *db):
        if len(db) == 5:
            # mysql数据库
            self.host = db[0]
            self.port = db[1]
            self.user = db[2]
            self.pwd = db[3]
            self.db = db[4]
        else:
            # sqlserver数据库
            self.host = db[0]
            self.port = None
            self.user = db[1]
            self.pwd = db[2]
            self.db = db[3]
        self._CreatePool()

    def _CreatePool(self):
        if not self.db:
            raise NameError + "没有设置数据库信息"
        if (self.port == None):
            self.Pool = PooledDB(creator=pymssql, mincached=2, maxcached=5, maxshared=3, maxconnections=6,
                                 blocking=True, host=self.host, user=self.user, \
                                 password=self.pwd, database=self.db, charset="utf8")
        else:
            self.Pool = PooledDB(creator=pymysql, mincached=2, maxcached=5, maxshared=3, maxconnections=6,
                                 blocking=True, host=self.host, port=self.port, \
                                 user=self.user, password=self.pwd, database=self.db, charset="utf8")

    def _Getconnect(self):
        self.conn = self.Pool.connection()
        cur = self.conn.cursor()
        if not cur:
            print "数据库连接不上"
        else:
            return cur

    # 查询sql
    def ExecQuery(self, sql):
        cur = self._Getconnect()
        cur.execute(sql)
        relist = cur.fetchall()
        cur.close()
        self.conn.close()
        return relist

    # 非查询的sql
    def ExecNoQuery(self, sql):
        cur = self._Getconnect()
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()
