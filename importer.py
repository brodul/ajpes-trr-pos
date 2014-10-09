raise NotImplementedError("This app is still in development")
import codecs
import xml.etree.ElementTree as et

from sqlalchemy import create_engine

from models import (
    DBSession,
    Base,
)

engine = create_engine("postgresql+pg8000://brodul:test@localhost/test")
__version__ = '0.1.0'

get_version = lambda: __version__

DBSession.remove()
DBSession.configure(bind=engine)

Base.metadata.bind = engine
Base.metadata.create_all(engine)
