#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-05-27 13:23:48
# @Last Modified by:   anchen
# @Last Modified time: 2016-05-27 20:08:13
import MySQLdb
import sys

class MoneyTransfer(object):
    """docstring for MoneyTransfer"""
    def __init__(self, Connect):
        self.Connect = Connect
    
    def MoneyTransferProcess(self,source,target,money):
        try:
            self.CheckAcoutIdExist(source)
            self.CheckAcoutIdExist(target)
            self.CheckAcoutMoneyEnough(source,money)
            self.DesAcoutMoney(source,money)
            self.AddAcoutMoney(target,money)
            self.Connect.commit()
        except Exception, e:
            self.Connect.rollback()
            raise
        finally:
            print"done"

    def CheckAcoutIdExist(self,user_id):
        cursor = self.Connect.cursor()
        try:
            sql_select = "select * from bank where id =%s"%(user_id)
            cursor.execute(sql_select)
            rs = cursor.fetchall()
            if len(rs)!=1:
                raise Exception("%s is not exist!"%user_id)
            print "CheckAcoutIdExist"
        finally:
            cursor.close()

    def CheckAcoutMoneyEnough(self,user_id,user_money):
        cursor = self.Connect.cursor()
        try:
            sql_select = "select * from bank where id =%s and money >=%s"%(user_id,user_money)
            cursor.execute(sql_select)
            rs = cursor.fetchall()
            if len(rs)!=1:
                raise Exception("%s has not enough money!"%user_id)
            print"CheckAcoutMoneyEnough"
        finally:
            cursor.close()

    def AddAcoutMoney(self,user_id,user_money):
        cursor = self.Connect.cursor()
        try:
            sql_select = "update bank set money = money + %s where id = %s"%(user_money,user_id)
            cursor.execute(sql_select)
            if cursor.rowcount!=1:
                raise Exception("%s add fail!"%user_id)
            print"AddAcoutMoney"
        finally:
            cursor.close()

    def DesAcoutMoney(self,user_id,user_money):
        cursor = self.Connect.cursor()
        try:
            sql_select = "update bank set money = money - %s where id = %s"%(user_money,user_id)
            cursor.execute(sql_select)
            if cursor.rowcount!=1:
                raise Exception("%s des fail!"%user_id)
            print"DesAcoutMoney"
        finally:
            cursor.close()

if __name__ == '__main__':
    conn = MySQLdb.Connect( host = "127.0.0.1",port = 3306,user = "root",passwd = "sheldon",db = "sheldon",charset = "utf8")
    try:
        tans = MoneyTransfer(conn)
        tans.MoneyTransferProcess(102,101,150)
    except Exception as e:
        raise e
    finally:
        conn.close()