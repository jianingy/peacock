from pecan import conf
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

_SESSION = scoped_session(sessionmaker())

ModelBase = declarative_base()


def _engine_from_config(configuration):
    configuration = dict(configuration)
    url = configuration.pop('url')
    return create_engine(url, **configuration)

def init_model():
    conf.sqlalchemy.engine = _engine_from_config(conf.sqlalchemy)
    return conf.sqlalchemy.engine

def start():
    _SESSION.bind = conf.sqlalchemy.engine
    ModelBase.metadata.bind = _SESSION.bind

def start_read_only():
    _SESSION.bind = conf.sqlalchemy.engine
    ModelBase.metadata.bind = _SESSION.bind

def commit():
    _SESSION.commit()

def rollback():
    _SESSION.rollback()

def clear():
    _SESSION.remove()

def get_session():
    return _SESSION

def db_sync():
    ModelBase.metadata.create_all()
