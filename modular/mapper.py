from modular.mysql_connect import connect_dbfrom modular.sqlserve_connect import serverConnect_db# wmsdb = "ods_mysql"class connect_DB(object):    def __init__(self, wms_db="ods_mysql"):        # wmsdb = connect_db(wmsdb="ods_mysql")        self.wmsdb = connect_db(wms_db)        self.cursor = self.wmsdb.cursor()        # return self.cursor    def execute(self, sql):        self.cursor.execute(sql)    def fetchone(self, sql):        self.execute(sql)        return self.cursor.fetchone()    def fetchall(self, sql):        self.execute(sql)        return self.cursor.fetchall()    def commit(self):        self.wmsdb.commit()    def close(self):        self.wmsdb.close()        pass    def commitAndClose(self):        self.commit()        self.close()class ConnectWSPdb(connect_DB):    def __init__(self, wms_db="wsp_mysql"):        self.wmsdb = connect_db(wms_db)        self.cursor = self.wmsdb.cursor()class connect_sqlserve(object):    def __init__(self, server_db='sql_servetest'):        # wmsdb = connect_db(wmsdb="ods_mysql")        self.wmsdb = serverConnect_db(server_db)        self.cursor = self.wmsdb.cursor()        # return self.cursor    def execute(self, sql):        self.cursor.execute(sql)    def fetchone(self, sql):        self.execute(sql)        return self.cursor.fetchone()    def fetchall(self, sql):        self.execute(sql)        return self.cursor.fetchall()    def commit(self):        self.wmsdb.commit()    def close(self):        self.wmsdb.close()        pass    def commitAndClose(self):        self.commit()        self.close()