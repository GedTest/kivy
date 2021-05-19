from sqlalchemy import create_engine, Column, Integer, String, Enum, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class Set(Base):
    """Entire class for LEGO set"""
    __tablename__ = 'sets'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=200))
    year = Column(Integer)
    number_of_pieces = Column(Integer)
    # price in $(USD)
    price = Column(Float(2))
    image = Column(String(100))

    # Foreing keys
    manual = Column(Integer, ForeignKey('manuals.id'))
    bricks = relationship('Brick', secondary='set_has_bricks')

    def __str__(self):
        return f'{self.name} [{self.id}] releasd in year: {self.year}, has {self.number_of_pieces} pieces!'


class Manual(Base):
    """Every LEGO sets have manual that describes how to built it"""
    __tablename__ = 'manuals'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=200))
    number_of_pages = Column(Integer)
    image = Column(String(100))
    set = relationship(Set, uselist=False, backref='manuals')

    def __str__(self):
        return f'{self.name} [{self.id}] has {self.number_of_pages} pages'


class Brick(Base):
    """This class is meant for individual LEGO brick pieces"""
    __tablename__ = 'bricks'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    color = Column(String(7))

    type = Column(Enum('standard', 'special'))
    image = Column(String(100))
    #sets = relationship(Set, secondary='set_has_bricks')

    def __str__(self):
        return f'{self.name} [{self.id}] is {self.type} type, of {self.color} color'


class SetHasBricks(Base):
    __tablename__ = 'set_has_bricks'

    set_id = Column(Integer, ForeignKey('sets.id'), primary_key=True)
    brick_id = Column(Integer, ForeignKey('bricks.id'), primary_key=True)
    count = Column(Integer)


class Database:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
     }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='lego.db'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    # # # # # # # # # #
    # CRUD METHODS
    # # # # # # # # # #
    def read(self, table, order="name"):
        return self.session.query(table).order_by(order).all()

    def read_by_id(self, table, id):
        try:
            if type(id) == int:
                return self.session.query(table).get(id)
        except:
            return False

    def read_by_name(self, table, name):
        return self.session.query(table).filter(table.name.like(f'%{name}%')).all()

    def read_last_id(self, table):
        try:
            return self.session.query(table).order_by(table.id.desc()).first().id
        except:
            return 0

    def create(self, table):
        try:
            self.session.add(table)
            self.session.commit()
            return True
        except:
            return False

    def update(self):
        try:
            self.session.commit()
            return True
        except:
            return False

    def delete(self, table, id):
        try:
            table_in_db = self.read_by_id(table, id)
            if table_in_db:
                self.session.delete(table_in_db)
                self.session.commit()
                return True
        except:
            return False
