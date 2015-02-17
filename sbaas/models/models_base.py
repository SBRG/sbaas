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

import json
#import simplejson

from data import sbaas_settings as settings

Base = declarative_base()

engine = create_engine("postgresql://%s:%s@%s/%s" %
    (settings.user, settings.password, settings.host, settings.database))

metadata = MetaData(bind=engine)
#metadata = MetaData(bind=engine, schema=settings.schema)

def make_table(table_name):
    """function to create a table with the default parameters"""
    return Table(table_name, metadata, autoload=True)


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
        for key, value in kwargs.iteritems():
            setattr(result, key, value)
        session.add(result)
        session.commit()
    return result

Session = sessionmaker(bind=engine, class_=_Session)


if __name__ == "__main__":
    session = Session()