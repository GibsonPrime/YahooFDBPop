from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

# Parameters for the database
protocol = "mssql+pyodbc"
user = "SQLLogin"
password = "SQLLogin123!"
host = "localhost\\SQLEXPRESS"
port = 1433
dbname = "MarketData"
driver =  "ODBC+Driver+17+for+SQL+Server"
 
# Connect to the database
# Remote
# conn_str = '{0}://{1}:{2}@{3}:{4}/{5}?driver={6}'.format(protocol, user, password, host, port, dbname, driver)
# Local
conn_str = '{0}://{1}:{2}@{3}/{4}?driver={5}'.format(protocol, user, password, host, dbname, driver)
engine = create_engine(conn_str, encoding='utf8')
Base = declarative_base()

# Currencies table
class Currency(Base):
	__tablename__ = 'currency'

	id = Column(Integer, primary_key=True)
	name = Column(String(10), nullable=False, unique=True)

	def __repr__(self):
		return '<Currency id: %s>' % self.id

# Countries table
class Country(Base):
	__tablename__ = 'country'

	id = Column(Integer, primary_key=True)
	name = Column(String(120), nullable=False, unique=True)

	def __repr__(self):
		return '<Country id: %s>' % self.id

# Timezones table
class Timezone(Base):
	__tablename__ = 'timezone'

	id = Column(Integer, primary_key=True)
	name = Column(String(120), nullable=False)
	shortname = Column(String(10), nullable=False, unique=True)

	def __repr__(self):
		return '<Timezone id: %s>' % self.id

# Markets table
class Market(Base):
	__tablename__ = 'market'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(30), nullable=False, unique=True)
	currency_id = Column(Integer, ForeignKey(Currency.id))
	timezone_id = Column(Integer, ForeignKey(Timezone.id))

	currency = relationship('Currency', foreign_keys='Market.currency_id')
	timezone = relationship('Timezone', foreign_keys='Market.timezone_id')

	def __repr__(self):
		return '<Market id: %s>' % self.id

# Exchanges table
class Exchange(Base):
	__tablename__ = 'exchange'

	id = Column(Integer, primary_key=True)	
	name = Column(String(10), nullable=False, unique=True)
	market_id = Column(Integer, ForeignKey(Market.id))	

	market = relationship('Market', foreign_keys='Exchange.market_id')

	def __repr__(self):
		return '<Exchange id: %s>' % self.id

# Create Symbols table
class Symbol(Base):
	__tablename__ = 'symbol'

	id = Column(Integer, primary_key=True)    
	symbol = Column(String(10), unique=True)
	exchange_id = Column(Integer, ForeignKey(Exchange.id))
	country_id = Column(Integer, ForeignKey(Country.id))
	shortname = Column(String(60), nullable=False, unique=True)
	longname = Column(String(120), nullable=False, unique=True)

	exchange = relationship('Exchange', foreign_keys='Symbol.exchange_id')
	country = relationship('Country', foreign_keys='Symbol.country_id')	

	def __repr__(self):
		return '<Symbol id: %s>' % self.id

Base.metadata.create_all(engine)
"""
# Setup session - this should be setup globally for an application
Session = sessionmaker(bind=engine)
conn = engine.connect()
session = Session(bind=conn)

# Execute stuff - this should be run for each operation
try:    
    thinginst = Thing(name='ThingName1')
    session.add(thinginst)

    print(thinginst.id)

    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()"""


""" 
# define parameters to be passed in and out
parameterIn = 1
parameterOut = "@parameterOut"
try:
    cursor = connection.cursor()
    cursor.callproc("storedProcedure", [parameterIn, parameterOut])
    # fetch result parameters
    results = list(cursor.fetchall())
    cursor.close()
    connection.commit()
finally:
    connection.close() 
   """