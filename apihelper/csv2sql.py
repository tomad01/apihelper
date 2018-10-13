#!/usr/bin/env python
#
#    loadcsv.py Load a file with CSV data into a database
#    Copyright (C) 2009  Ferran Pegueroles <ferran@pegueroles.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
"""
  Simple script wrapper

"""
import csv,sys,os,string,itertools,pdb,argparse
from six import string_types, text_type
from optparse import OptionParser
from StringIO import StringIO
__version__ = '0.4'


def _guess_types(reader, number_of_columns, max_sample_size=100):
    '''Guess column types (as for SQLite) of CSV.

    :param fileobj: read-only file object for a CSV file.
    '''
    # we default to text for each field
    types = ['text'] * number_of_columns
    # order matters
    # (order in form of type you want used in case of tie to be last)
    options = [
        ('text', text_type),
        ('real', float),
        ('integer', int)
        # 'date',
        ]
    # for each column a set of bins for each type counting successful casts
    perresult = {
        'integer': 0,
        'real': 0,
        'text': 0
        }

    results = [ dict(perresult) for x in range(number_of_columns) ]
    sample_counts = [ 0 for x in range(number_of_columns) ]

    for row_index,row in enumerate(reader):
        for column,cell in enumerate(row):
            cell = cell.strip()
            if len(cell) == 0:
                continue

            # replace ',' with '' to improve cast accuracy for ints and floats
            if(cell.count(',') > 0):
               cell = cell.replace(',', '')
               if(cell.count('E') == 0):
                  cell = cell + "E0"

            for data_type,cast in options:
                try:
                    cast(cell)
                    results[column][data_type] += 1
                    sample_counts[column] += 1
                except ValueError:
                    pass

        have_max_samples = True
        for column,cell in enumerate(row):
            if sample_counts[column] < max_sample_size:
                have_max_samples = False

        if have_max_samples:
            break

    for column,colresult in enumerate(results):
        for _type, _ in options:
            if colresult[_type] > 0 and colresult[_type] >= colresult[types[column]]:
                types[column] = _type

    return types
def get_types(fo):

    try:
        dialect = csv.Sniffer().sniff(fo.readline())
    except TypeError:
        dialect = csv.Sniffer().sniff(str(fo.readline()))
    fo.seek(0)

    reader = csv.reader(fo, dialect)
    headers = [header.strip() for header in next(reader)]
    fo.seek(0)

    # guess types
    type_reader = csv.reader(fo, dialect)
    next(type_reader)
    types = _guess_types(type_reader, len(headers))
    fo.close()
    return types




def create_table(datafile,tblname,namefmt = '0'):
        ##if len(sys.argv)<2:
        ##	print "\nUsage: csv2tbl.py path/datafile.csv (0,1,2,3 = column name format):"
        ##	print "\nFormat: 0 = TitleCasedWords"
        ##	print "        1 = Titlecased_Words_Underscored"
        ##	print "        2 = lowercase_words_underscored"
        ##	print "        3 = Words_underscored_only (leave case as in source)"
        ##	sys.exit()
        ##else:
        ##	if len(sys.argv)==2:
        ##		dummy, datafile, = sys.argv
        ##		namefmt = '0'
        ##	else: dummy, datafile, namefmt = sys.argv

        namefmt = int(namefmt)
        #outfile = os.path.basename(datafile)
##        tblname = os.path.basename(datafile).split('.')[0]
        outfile = os.path.dirname(datafile) + '\\' + tblname + '.sql'

        # Create string translation tables
        allowed = ' _01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        delchars = ''
        for i in range(255):
                if chr(i) not in allowed: delchars = delchars + chr(i)
        deltable = string.maketrans(' ','_')

        # Create list of column [names],[widths]
        reader = csv.reader(file(datafile),dialect='excel')
        row = reader.next()
        nc = len(row)
        cols = []
        for col in row:
                # Format column name to remove unwanted chars
                col = string.strip(col)
                col = string.translate(col,deltable,delchars)
                fmtcol = col
                if namefmt < 3:
                        # Title case individual words, leaving original upper chars in place
                        fmtcol = ''
                        for i in range(len(col)):
                                if col.title()[i].isupper(): fmtcol = fmtcol + col[i].upper()
                                else: fmtcol = fmtcol + col[i]
                if namefmt == 2: fmtcol = col.lower()
                if namefmt == 0: fmtcol = string.translate(fmtcol,deltable,'_')   # Remove underscores
                
                d = 0
                dupcol = fmtcol	
                while dupcol in cols:
                        d = d + 1
                        dupcol = fmtcol + '_' + str(d)
                cols.append([dupcol,1])

        # Determine max width of each column in each row
        rc = 0
        for row in reader:
                rc = rc + 1
                if len(row) == nc:
                        for i in range(len(row)):
                                fld = string.strip(row[i])
                                if len(fld) > cols[i][1]:
                                        cols[i][1] = len(fld)
                else: print 'Warning: Line %s ignored. Different width than header' % (rc)

        print

        sql = 'CREATE TABLE %s\n(' % (tblname)
##        types = get_types(open(datafile))
        for ind,col in enumerate(cols):
                sql = sql + ('\n\t%s VARCHAR(%s),' % (col[0],col[1]))
        print sql[:len(sql)-1] + ');'
        
def conn_mysql(attrs):
    """ Connection for mysql database """

    try:
        import MySQLdb
        return MySQLdb.connect(host=attrs.get('host'), user=attrs.get('user'),
                               passwd=attrs.get('password'), port=int(attrs.get('port')),
                               db=attrs.get('dbname'))

    except ImportError:
        print " MySQLdb driver not installed"
        sys.exit(2)


def conn_pgsql(attrs):
    """ Connection for postgresql database """
    dsn = " ".join(["%s=%s" % (k, v) for k, v in attrs.items()])
    try:
        import psycopg2
        return psycopg2.connect(dsn)
    except ImportError:
        try:  
            import psycopg
            return psycopg.connect(dsn)
        except ImportError:
            print "psycopg driver not installed"
            sys.exit(2)


def conn_sqlite(attrs):
    """ Connection for sqlite database """
    filename = attrs['dbname']
    try:
        import sqlite3
        return sqlite3.connect(filename)
    except ImportError:
        pass

    try:
        import sqlite
        return sqlite.connect(filename)
    except ImportError:
        pass

    try:
        from pysqlite2 import dbapi2 as sqlite
        return sqlite.connect(filename)
    except ImportError:
        pass

    print "sqlite driver not installed"
    sys.exit(2)

DRIVERS = {
    'mysql': conn_mysql,
    'pgsql': conn_pgsql,
    'sqlite': conn_sqlite,
}


def generate_sql_insert(tablename, columns, placeholder="%s"):
    """ Generate the sql statment template for all the inserts """
    fields = ",".join(columns)
    places = ",".join([placeholder] * len(columns))
    sql = "insert into %s values (%s);" % (tablename, places)
    
    return sql.encode('utf8')


def prepare_values(values):
    """ Prepate the values for the SQL output """
    prepared = []
    for value in values:
        if value == None:
            prepared.append('')
        else:
            prepared.append(unicode(value).strip().encode('utf8'))
    return tuple(prepared)


def output_sql(outfile, table, columns, iter_input, placeholder="%s"):
    """ Output SQL to outfile reading input from iter_input """
    insert_sql = generate_sql_insert(table, columns, placeholder)
    for row in itertools.ifilter(None, iter_input):
        row  = ','.join(["'"+i.replace('"','')+"'" for i in row[0].split(',')])
        outfile.write(insert_sql % row + "\n")


def output_sql_from_file(outfile, table, inputfile, placeholder="%s",
                          delimiter=','):
    """
        Output SQL to outfile reading input from inputfile
        Inputfile is a open file formated as CSV
    """
    input_ = csv.reader(inputfile, dialect='excel', delimiter=delimiter)
    columns = input_.next()
    return output_sql(outfile, table, columns, input_, placeholder)


def get_sql(tablename, inputfile, delimiter=';'):
    """
         Get all SQL as a single value
    """
    strout = StringIO()
    output_sql_from_file(strout, tablename, inputfile,
                                    delimiter=delimiter)
    return strout.getvalue()


def load(cursor, table, columns, input_, placeholder='?'):
    """
         Load a input iterator to a database cursor
    """
    insert_sql = generate_sql_insert(table, columns, placeholder)
    for row in itertools.ifilter(None, input_):
        cursor.execute(insert_sql, prepare_values(row))


def load_file(cursor, table, inputfile, placeholder='?', delimiter=','):
    """
         Load a CSV file to a database cursor
    """
    input_ = csv.reader(inputfile, dialect='excel', delimiter=delimiter)
    columns = input_.next()
    load(cursor, table, columns, input_, placeholder)


def parse_args(argv):
    """
       Parse and validate args
    """
    usage = "usage: %prog [options] filename.csv\n" + \
            "If no database provided, display SQL to stdout"

    parser = OptionParser(usage=usage, version=__version__)

    parser.add_option("-D", "--driver", dest="driver",
         help="database driver [%s]" % ",".join(DRIVERS))
    parser.add_option("-H", "--hostname", dest="hostname",
                 help="database server hostname,defaults to localhost",
                 metavar="HOSTNAME")
    parser.add_option("-d", "--dbname", dest="dbname",
         help="database name (filename on sqlite)")
    parser.add_option("-u", "--user", dest="user",
                 help="database username")
    parser.add_option("-p", "--password", dest="password",
                 help="database password")
    parser.add_option("-P", "--port", dest="port",
                 help="database port")
    parser.add_option("-t", "--table", dest="table",
                 help="database table to load")
    parser.add_option("", "--test", action="store_true", dest="test",
                 help="run text, do no commit to the database")
    parser.add_option("--delimiter", dest="delimiter", default=";",
                 help="CSV file field delimiter, by default semi-colon")
    parser.add_option("-o", "--output", dest="output", metavar="FILE",
                 help="Output file for SQL commands")
    options, args = parser.parse_args(args=argv)

    if len(args) != 1:
        parser.error("Filename not provided")

    if not options.table:
        parser.error("table is required")

    if options.driver and options.driver not in DRIVERS:
        parser.error("database driver not suported")

    if options.driver and not options.dbname:
        parser.error("database is required")

    return options, args


def get_dsn_attrs(options):
    """ Get dsn_attrs from command line options """
    dsn_attrs = {}
    if options.hostname:
        dsn_attrs['host'] = options.hostname
    if options.dbname:
        dsn_attrs['dbname'] = options.dbname
    if options.password:
        dsn_attrs['password'] = options.password
    if options.user:
        dsn_attrs['user'] = options.user
    if options.port:
        dsn_attrs['port'] = options.port

    return dsn_attrs


def main(argv=None):
    """ Script entry point """
    if not argv:
        argv = sys.argv[1:]

    options, args = parse_args(argv)
##    pdb.set_trace()
    create_table(argv[2],argv[1],namefmt = '0')
    if options.driver:

        dsn_attrs = get_dsn_attrs(options)

        connection = DRIVERS[options.driver]
        conn = connection(dsn_attrs)
        cur = conn.cursor()

        if options.driver == "mysql":
            load_file(cur, options.table, open(args[0]), placeholder='%s', \
                        delimiter=options.delimiter)
        else:
            load_file(cur, options.table, open(args[0]), \
                        delimiter=options.delimiter)

        if not options.test:
            conn.commit()
    else:
        if not options.output or options.output == "-":
            out = sys.stdout
        else:
            out = open(options.output, "w")

        output_sql_from_file(out, options.table, open(args[0]), \
                delimiter=options.delimiter)

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
