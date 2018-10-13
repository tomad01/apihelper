from file_analysis import *
from data_analysis import *
from apihelper import *
import sqlite3,pdb,os,subprocess


class Sqlib(object):
    def __init__(self,db_name,tb_name=None,columns=None):
        self.tb_name = db_name.rstrip('.db') if tb_name is None else tb_name
        self.conn = sqlite3.connect(db_name)
        self.cu = self.conn.cursor()
        if columns:
            self.columns,self.types = zip(*columns)
            self.all_cols = ','.join([i for i in self.columns if i!='id'])

            string = ','.join([k+' '+v for k,v in columns])
            try:
                self.cu.execute('''create table if not exists %s
                             (%s)'''%(tb_name,string))
            except Exception as er:
                print(str(er))                
            self.conn.commit()


    def black_magic(self,query):
        
        with open('sqlite_script_temp','w') as fd:
            fd.write('.mode csv\n')
            fd.write('.output temp.csv\n')
            fd.write('%s;\n'%query)
            fd.write('.output stdout\n')
            
        pr = subprocess.Popen('sqlite3.exe %s.db < sqlite_script_temp'%self.tb_name, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        pr.wait()
        error = pr.stderr.read()
        if error:
            return error
        
        with open('temp.csv', 'r') as csvfile:
            data = [ii.split(',') for ii in csvfile.read().split('\n') if ii.strip()]
            
        return data
        
        
    def execute(self,*args):
        self.cu.execute(args)

    def fetchall(self):
        return self.cu.fetchall()
        
    def inserts(self,line):
        self.cu.execute('insert into %s (%s) \
            values (%s)'%(self.tb_name,self.all_cols,','.join(['?']*len(line))),line)
            
    def close(self):
        os.remove('temp.csv')
        os.remove('sqlite_script_temp')
        self.conn.close()

    def commit(self):
        self.conn.commit()



