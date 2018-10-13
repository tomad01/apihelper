from datetime import datetime
from apihelper.apihelper import *
import pdb,re

class LogParser(object):
    def __init__(self,sep=',',date_format='%Y-%m-%d %H:%M:%S'):
        """
        lines =
                [
                    [('type',value),...]
                    ...
                ]
        """
        self.spaces = re.compile(r'\s+')
        self.date_format = date_format
        self.default_date_format = "%d-%m-%Y %H:%M:%S.%f"
        self.sep         = sep
        
        
    def chew(self,lines,file_descriptor,_from='unknown'):        
        if lines:
            rows = []
            for line in lines:
                rows.append(self.sep.join([self.check(k,v,_from) for k,v in line]))
            file_descriptor.write('\n'.join(rows)+'\n')
            file_descriptor.flush()
        
    def check(self,k,v,mes):
        if k=='datetime':
            return self.valid_datetime(v)
        elif k=='string':
            return self.clean_strin(v,mes)
        elif k=='int':
            return self.check_int(v,mes)
        elif k=='float':
            return self.check_float(v,mes)
        elif k=='empty':
            return v
        else:
            raise Exception('unrecognized field')
        
    def valid_datetime(self,date_text):
##        try:
##            datetime.strptime(date_text,self.date_format)
##        except ValueError:
##            print 'Incorrect data format for "%s", should be "%s"'%(date_text,self.date_format)
##        date_text = ChTimeForm(date_text,self.date_format,self.default_date_format)
        return date_text

    def clean_strin(self,x,mes='unknown'):
        clean = x.replace('"','').replace(self.sep,' ').strip()
        return self.spaces.sub(' ',clean)
        
    def check_int(self,x,mes='unknown'): 
        try:
            int(x)
        except ValueError:
            print('"%s" not int type for %s'%(x,mes))
        return x.strip()
    
    def check_float(self,x,mes='unknown'): 
        try:
            float(x)
        except ValueError:
            print('"%s" not float type for %s'%(x,mes))
        return x.strip()
######################################################################################################
class LogParser_new(object):
    def __init__(self,sep=',',date_format='%Y-%m-%d %H:%M:%S'):
        """
        lines =
                [
                    [('type',value),...]
                    ...
                ]
        """
        self.spaces = re.compile(r'\s+')
        self.date_format = date_format
        self.default_date_format = "%d-%m-%Y %H:%M:%S.%f"
        self.sep         = sep
        
        
    def chew(self,lines,db_conn,_from='unknown'):        
        if lines:
            for line in lines:
                db_conn.inserts(line)
##                db_conn.inserts([self.check(k,v,_from) for k,v in line])
            db_conn.commit()
            
        
    def check(self,k,v,mes):
        if k=='datetime':
            return self.valid_datetime(v)
        elif k=='string':
            return self.clean_strin(v,mes)
        elif k=='int':
            return self.check_int(v,mes)
        elif k=='float':
            return self.check_float(v,mes)
        elif k=='empty':
            return v
        else:
            raise Exception('unrecognized field')
        
    def valid_datetime(self,date_text):
        try:
            datetime.strptime(date_text,self.date_format)
        except ValueError:
            print('Incorrect data format for "%s", should be "%s"'%(date_text,self.date_format))     
        return ChTimeForm(date_text,self.date_format,self.default_date_format)

        

    def clean_strin(self,x,mes='unknown'):
        clean = x.replace('"','').replace(self.sep,' ').strip()
        return self.spaces.sub(' ',clean)
        
    def check_int(self,x,mes='unknown'): 
        try:
            int(x)
        except ValueError:
            print('"%s" not int type for %s'%(x,mes))
        return x.strip()
    
    def check_float(self,x,mes='unknown'): 
        try:
            float(x)
        except ValueError:
            print('"%s" not float type for %s'%(x,mes))
        return x.strip()
