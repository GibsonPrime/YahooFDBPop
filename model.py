from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

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
	shortname = Column(String(60), nullable=False)
	longname = Column(String(120), nullable=False)

	exchange = relationship('Exchange', foreign_keys='Symbol.exchange_id')
	country = relationship('Country', foreign_keys='Symbol.country_id')	

	def __repr__(self):
		return '<Symbol id: %s>' % self.id
