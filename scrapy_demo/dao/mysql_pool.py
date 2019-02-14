# coding=utf8
# Copyright 2018 AGGRX Inc. All Rights Reserved.

"""
@author: ZengYaoPeng (zengyaopeng@tv365.net)
@time: 2018/10/8 下午6:58
"""

import threading

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB


class MysqlPoolClient(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn

    备注：单步进入
    """
    # 连接池对象
    __pool = {}
    __lock = threading.Lock()

    # TODO(YaoPeng): 反复加锁影响性能，但是爬虫场景下，可以暂时容忍
    def __init__(self, db_conf):
        MysqlPoolClient.__lock.acquire()
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        # pip install DBUtils
        self._conn = MysqlPoolClient.__getConn(db_conf)
        self._cursor = self._conn.cursor()
        MysqlPoolClient.__lock.release()

    def __del__(self):
        self.dispose()

    @staticmethod
    def __getConn(db_conf):
        pool_name = db_conf.DB_FULL_NAME
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if pool_name not in MysqlPoolClient.__pool:
            MysqlPoolClient.__pool[pool_name] = PooledDB(creator=MySQLdb,
                                                         mincached=1,
                                                         maxcached=20,
                                                         host=db_conf.DBHOST,
                                                         port=int(db_conf.DBPORT),
                                                         user=db_conf.DBUSER,
                                                         passwd=db_conf.DBPWD,
                                                         db=db_conf.DBNAME,
                                                         use_unicode=False,
                                                         charset=db_conf.DBCHAR,
                                                         cursorclass=DictCursor)
        return MysqlPoolClient.__pool[pool_name].connection()

    def getAll(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            query_result = self._cursor.fetchall()
        else:
            query_result = False
        return query_result

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            query_result = self._cursor.fetchone()
        else:
            query_result = False
        return query_result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            query_result = self._cursor.fetchmany(num)
        else:
            query_result = False
        return query_result

    def insertOne(self, sql, value=None):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql, value)
        return self.__getInsertId()

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def updateMany(self, sql, values):
        """
        @summary: 向数据表更新多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None, commit=True):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if commit:
            self._conn.commit()
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, is_end=1):
        """
        @summary: 释放连接池资源
        """
        MysqlPoolClient.__lock.acquire()
        if is_end == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()
        MysqlPoolClient.__lock.release()
