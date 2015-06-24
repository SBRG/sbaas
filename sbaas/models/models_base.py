"""Module to implement ORM to the sbaas database"""

from types import MethodType
from os import system

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as _SA_Session
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, Boolean,\
    String, Float, Text, ForeignKey, and_, or_, not_, distinct, select, Sequence,\
    DateTime, Date, UniqueConstraint, ForeignKeyConstraint,PrimaryKeyConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable, DropTable
from sqlalchemy.exc import SQLAlchemyError

import json

from sbaas.data import sbaas_settings as settings

Base = declarative_base()

engine = create_engine("postgresql://%s:%s@%s/%s" %
    (settings.user, settings.password, settings.host, settings.database))

metadata = MetaData(bind=engine)
#metadata = MetaData(bind=engine, schema=settings.schema)

def make_table(table_name):
    """function to create a table with the default parameters"""
    return Table(table_name, metadata, autoload=True);

def select_table(session_I,select_cmd_I,from_cmd_I,where_cmd_I=None,group_by_cmd_I=None,order_by_cmd_I=None,
                 fetch_I = None, fetch_many_I = 10):
    '''SELECT query for a table
    INPUT:
    session_I = session object
    select_cmd_I = list of table columns or *
    from_cmd_I = list of tables
    where_cmd_I = string reprentation of the filter criteria
    group_by_cmd_I = list of table columns to group by or *
    order_by_cmd_I = list of tuples/lists of table columns and ASC or DESC
    fetch_I = rows to fetch, e.g. "one","many", or "all"
        if None, the result query object is returned
    fetch_many_I = number of rows to fetch if fetch_I = many
    OUTPUT:
    data_O = keyed-tuple object will be returned
    TEST:
    select_table(session,['*'],['sample'],"sample_type LIKE 'QC'",None,[['sample_name','ASC']]);
    '''

    query_cmd = '';

    select_cmd = 'SELECT ';
    for d in select_cmd_I:
        if d=='*':
            select_cmd += ('%s, ' %(d));
        elif '.' in d:
            select_cmd += ('%s, ' %(d));
        else:
            select_cmd += ('"%s", ' %(d));
    select_cmd = select_cmd[:-2]; #remove trailing comma
    query_cmd += select_cmd + ' ';

    from_cmd = 'FROM ';
    for d in from_cmd_I:
        from_cmd += ('"%s", ' %(d));
    from_cmd = from_cmd[:-2]; #remove trailing comma
    query_cmd += from_cmd + ' ';

    if where_cmd_I:
        where_cmd = 'WHERE ';
        where_cmd += where_cmd_I;
        query_cmd += where_cmd + ' ';

    if group_by_cmd_I:
        group_by_cmd = 'GROUP BY ';
        for d in group_by_cmd_I:
            if d=='*':
                group_by_cmd += ('%s, ' %(d));
            else:
                group_by_cmd += ('"%s", ' %(d));
        group_by_cmd = group_by_cmd[:-2]; #remove trailing comma
        query_cmd += group_by_cmd + ' ';

    if order_by_cmd_I:
        order_by_cmd = 'ORDER BY ';
        for d in order_by_cmd_I:
            if '.' in d[0]:
                order_by_cmd += ('%s %s, ' %(d[0],d[1]));
            else:
                order_by_cmd += ('"%s" %s, ' %(d[0],d[1]));
        order_by_cmd = order_by_cmd[:-2]; #remove trailing comma
        query_cmd += order_by_cmd + ' ';

    query_cmd = query_cmd[:-1]; #remove trailing whitespace
    query_cmd +=';';

    data_O = None;
    try:
        data_O = session_I.execute(query_cmd);
    except SQLAlchemyError as e:
        print(e); 
    
    if fetch_I:
        if fetch_I == 'one':
            return data_O.fetchone();
        elif fetch_I == 'all':
            return data_O.fetchall();
        elif fetch_I == 'many':
            return data_O.fetchmany(fetch_many_I);

    return data_O;

def update_table(session_I,update_cmd_I,set_cmd_I,where_cmd_I):
    '''UPDATE query for a table
    INPUT:
    session_I = session object
    update_cmd_I = table to update
    set_cmd_I = dictionary of columns to update
    where_cmd_I = string reprentation of the filter criteria
    fetch_many_I = number of rows to fetch if fetch_I = many
    OUTPUT:
    data_O = keyed-tuple object will be returned
    TEST:
    select_table(session,['*'],['sample'],"sample_type LIKE 'QC'",None,[['sample_name','ASC']]);
    '''
    query_cmd = '';

    update_cmd = 'UPDATE ';
    update_cmd += ('"%s"' %(update_cmd_I));
    query_cmd += update_cmd + ' ';

    set_cmd = 'SET ';
    for d in set_cmd_I:
        if type(d) == type(1) or type(d) == type(1.0):
            set_cmd += ('%s, ' %(update_cmd_I)); #int or float
        else:
            set_cmd += ("'%s', " %(update_cmd_I)); #string
    set_cmd = group_by_cmd[:-2]; #remove trailing comma
    query_cmd += set_cmd + ' ';

    if where_cmd_I:
        where_cmd = 'WHERE ';
        where_cmd += where_cmd_I;

    query_cmd += where_cmd; #remove trailing whitespace
    query_cmd +=';';

    data_O = None;
    try:
        data_O = session_I.execute(query_cmd);
    except SQLAlchemyError as e:
        print(e); 


class _Session(_SA_Session):
    """an sqlalchemy session object to interact with the SBaaS database

    This object can used to make queries against the SBaaS database. For
    example, a query without using any ORM looks like this
    >>> session = Session()
    >>> session.execute("SELECT name from genes where bnum='b0001'").fetchone()
    (u'thrL',)
    Using the sqlalchemy ORM gives more descriptive objects. For example:
    >>> b0001 = session.query(Gene).filter(Gene.bnum=="b0001").first()
    >>> b0001.name
    u'thrL'
    Raw queries which return ORM objects are also possible:
    >>> sql_statement = "SELECT * from genes where bnum='b0001'"
    >>> b0001 = session.query(Gene).from_statement(sql_statement).first()
    >>> b0001.name
    u'thrL'

    The Session will automatically set the search_path to settings.schema
    """
    def __init__(self, *args, **kwargs):
        super(_Session, self).__init__(*args, **kwargs)
        #self.execute("set search_path to %s;" % (settings.schema)) TODO: settings file
        self.commit()
        self.get_or_create = MethodType(get_or_create, self)
        #self.search_by_synonym = MethodType(search_by_synonym, self)

    def __repr__(self):
        return "SBaaS session %d" % (self.__hash__())


def get_or_create(session, class_type, **kwargs):
    """gets an object using filter_by on the kwargs. If no such object
    is found in the database, a new one will be created which satisfies
    these constraints"""
    result = session.query(class_type).filter_by(**kwargs).first()
    if result is None:
        result = class_type()
        for key, value in kwargs.items():
            setattr(result, key, value)
        session.add(result)
        session.commit()
    return result

Session = sessionmaker(bind=engine, class_=_Session)


if __name__ == "__main__":
    session = Session()