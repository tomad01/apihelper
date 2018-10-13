try:
    from apihelper.apihelper import *
except:
    from apihelper import *
from dateutil.parser import parse
import operator,json,csv,pdb,math

def get_nr_lines(file_name):
    print 'counting lines...'
    f = open(file_name, 'rb')
    suma =  sum((1 for _ in f))
    f.close()
    return suma

def read_csv(inputfile):
    dialect = csv.Sniffer().sniff(inputfile.readline())
    inputfile.seek(0)
    return csv.reader(inputfile, dialect = dialect)
class Buffer(object):
    def __init__(self,json_name,key):
        self.cnt = 0
        self.json_name = json_name 
        self.struc = {}
        self.key = key
        self.struc[self.key] = []
        self.list_size = 500000

    def append(self,value):
        self.struc[self.key].append(value)
        if len(self.struc[self.key])==self.list_size:
            self.cnt += 1
            dump_json(self.struc,self.json_name+'_'+str(self.cnt) + '.json')
            self.struc[self.key] = []

    def end(self):
        if self.struc[self.key]:
            self.cnt += 1
            dump_json(self.struc,self.json_name+'_'+str(self.cnt) + '.json')
            
def is_ok(nr):
    if nr and is_float(nr) and not math.isnan(float(nr)):
        return True
    return False

def how_much(good,bad):
    maxim_go = max(good); minim_go = min(good)
    maxim_ba = max(bad); minim_ba = min(bad)
    match_er = [ii for ii,nr in enumerate(bad) if not minim_go<=nr<=maxim_go]
    match_go = [ii for ii,nr in enumerate(good) if not minim_ba<=nr<=maxim_ba]
    coef_er = len(match_er)/float(len(bad))
    coef_go = len(match_go)/float(len(good))
    return ['%.3f'%coef_er,'%.3f'%coef_go,'%d'%len(match_er),'%d'%len(bad),'%d'%len(match_go),'%d'%len(good)],[match_go,match_er]

def get_string_cols(data):
    cols = []
    for k,v in data.items():
        strings = filter(lambda x: is_not_float(x) or is_empty(x),v)
        gaps    = filter(lambda x: is_empty(x),v)
        if len(strings)>0 and len(gaps)<len(v) and len(set(strings))>1:
            cols.append(k)
    return cols

def get_float_cols(data):
    cols = []
    for k,v in data.items():
        if len(filter(lambda x: is_float(x) or is_empty(x),v))>0 and len(filter(lambda x: is_empty(x),v))<len(v) and len(set(v))>1:
            cols.append(k)            
    return cols

def check_none(data):
    cols = []
    for k,v in data.items():
        if len(filter(lambda x: type(x)==type(None),v))>0:
            cols.append(k)            
    return cols

def csv_to_dic(csvname,rows=None,exclude=[],include=[]):
    with open(csvname,'r') as inputfile:
        try:
            dialect = csv.Sniffer().sniff(inputfile.readline())
        except TypeError:
            dialect = csv.Sniffer().sniff(str(inputfile.readline()))
        inputfile.seek(0)
        iter_input = csv.reader(inputfile, dialect=dialect)    
        header=iter_input.next()
############################################################
        index_get = range(len(header))        
        data = {}
        for ii,head in enumerate(header):
            if head in exclude:
                index_get.remove(ii)
            else:
                data[head] = []           
############################################################
        
        if include:
            index_get = []
            data = {}
            for ii,head in enumerate(header):
                if head in include:
                    index_get.append(ii)
                    data[head] = []
############################################################
                
        cnt=0
        if rows is None:
            rows = get_nr_lines(csvname)
        wb = Wait_bar(rows/1000)    
        try:
            for line in iter_input:        
                cnt+=1
                for ii,ll in enumerate(line):
                      if ii in index_get:
                          data[header[ii]].append(ll)
##                if cnt%1000==0:
##                    wb.display()
                if cnt==rows:
                    break
        except Exception as er:
            print(str(er))
    return data,header

def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False
    
def is_int(string):
    try: 
        int(string)
        return True
    except ValueError:
        return False
    
def is_empty(x):
    if x=='':
        return True
    else:
        return False
    
def load_json(name):
    with open(name,'r') as fd:
        data = json.load(fd)
    return data

def dump_json(struc,name):
    with open(name,'w') as fd:
        data = json.dump(struc,fd)

def is_float(string):
    try: 
        float(string)
        return True
    except (ValueError,TypeError):
        return False

def is_not_float(string):
    try: 
        float(string)
        return False
    except ValueError:
        return False
def get_header_info(filename):
    with open(filename,'rb') as inputfile:
        dialect = csv.Sniffer().sniff(inputfile.readline())
        inputfile.seek(0)
        iter_input = csv.reader(inputfile, dialect=dialect)    
        header = next(iter_input)
    return header
def find_doubles(vec):
    dic = {i:0 for i in set(vec)}
    for item in dic:
        dic[item]+=1
    return sorted(dic.items(), key=operator.itemgetter(1),reverse = True)

def diff(li):
    res = []
    for ii in range(len(li)-1):
        res.append(li[ii+1]-li[ii])
    return res

def update_file(vals,types,filen,exclude=None):
    try:
        with open(filen,'r') as fd:        
            data = json.load(fd)
    except IOError:
        with open(filen,'w') as fd:        
            json.dump({},fd)
        data = {}
    if exclude:
        with open(exclude,'r') as fd:        
            data_ex = json.load(fd)
    else:
        data_ex = {}
    for val in vals:
        if val not in data.keys() and val not in data_ex.keys():
            data[val]=types
    with open(filen,'w') as fd:
        json.dump(data,fd)
