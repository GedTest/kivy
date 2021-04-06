from sqlalchemy import create_engine, Column, Integer, String, Enum, BLOB, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLITE = 'sqlite'

Base = declarative_base()


class Brick(Base):
    """This class is meant for individual LEGO brick pieces"""
    __tablename__ = 'bricks'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    quantity = Column(Integer)
    color = Column()

    TYPE = ('standard', 'special')
    type = Column(Enum(TYPE))
    image = Column(BLOB)


class Manual(Base):
    """Every LEGO sets have manual that describes how to built it"""
    __tablename__ = 'manuals'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=200))
    number_of_pages = Column(Integer)
    image = Column(BLOB)


class Set(Base):
    """Entire class for LEGO set"""
    __tablename__ = 'sets'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=200))
    image = Column(BLOB)
    year = Column(Integer)
    number_of_pieces = Column(Integer)
    price = Column(Integer)

    # Foreing keys
    manual = Column(String(3), ForeignKey('manuals.id'))
    bricks = Column(ARRAY(Brick), ForeignKey('bricks.id'))


class Database:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='lego.db'):

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
