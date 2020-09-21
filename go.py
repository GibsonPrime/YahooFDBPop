from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yfinance as yf
from model import Currency, Country, Timezone, Market, Exchange, Symbol

# Globals
symbols = []
goodsymbols = []
badsymbols = []

# Parameters for the database
protocol = "mssql+pyodbc"
user = "SQLLogin"
password = "SQLLogin123!"
host = "localhost\\SQLEXPRESS"
port = 1433
dbname = "MarketData"
driver =  "ODBC+Driver+17+for+SQL+Server"

# Create engine
conn_str = '{0}://{1}:{2}@{3}/{4}?driver={5}'.format(protocol, user, password, host, dbname, driver)
engine = create_engine(conn_str, encoding='utf8')

# Create session
Session = sessionmaker(bind=engine)
conn = engine.connect()
session = Session(bind=conn)

# Read symbols
sym_file = open(".\\symbols_all.txt", "r")
for line in sym_file:
	symbols.append(line.rstrip())


# Method queries table where search_column = value and returns first hit return_column.
# If no hit, returns None.  If return_column is None, returns True on hit.
def sqlalchemy_get(session, table, search_column, value, return_column):
	query = session.query(table).filter(getattr(table, search_column) == value)

	if len(query.all()) == 0:
		return None
	elif not(return_column == None):
		return getattr(query[0], return_column)
	else:
		return True

# Method to add item to table
def sqlalchemy_add(session, table, new_row_object):
	session.add(new_row_object)
	session.commit()

# Execute stuff - this should be run for each operation
try:
	for sym in symbols:		
		ticker = yf.Ticker(sym)
		step = ""
		try:
			info = ticker.info

			# Currency
			step = "Currency"
			currency_id = sqlalchemy_get(session, Currency, "name", info.get('currency'), "id")
			if(currency_id == None):
				sqlalchemy_add(session, Currency, Currency(name = info.get('currency')))
				currency_id = sqlalchemy_get(session, Currency, "name", info.get('currency'), "id")

			# Country
			step = "Country"
			countryName = ""
			if(info.get('country') == None or info.get('country') == "NULL"):
				countryName = "NULL"
			else:
				countryName = info.get('country')

			country_id = sqlalchemy_get(session, Country, "name", countryName, "id")
			if(country_id == None):
					sqlalchemy_add(session, Country, Country(name = countryName))
					country_id = sqlalchemy_get(session, Country, "name", countryName, "id")

			# Timezone
			step = "Timezone"
			timezone_id = sqlalchemy_get(session, Timezone, "shortname", info.get('exchangeTimezoneShortName'), "id")
			if(timezone_id == None):
				sqlalchemy_add(session, Timezone, Timezone(name = info.get('exchangeTimezoneName'), 
															shortname = info.get('exchangeTimezoneShortName')))
				timezone_id = sqlalchemy_get(session, Timezone, "shortname", info.get('exchangeTimezoneShortName'), "id")	

			# Market
			step = "Market"
			market_id = sqlalchemy_get(session, Market, "name", info.get('market'), "id")
			if(market_id == None):
				sqlalchemy_add(session, Market, Market(name = info.get('market'), 
														currency_id = currency_id, 
														timezone_id = timezone_id))
				market_id = sqlalchemy_get(session, Market, "name", info.get('market'), "id")

			# Exchange
			step = "Exchange"
			exchange_id = sqlalchemy_get(session, Exchange, "name", info.get('exchange'), "id")
			if(exchange_id == None):
				sqlalchemy_add(session, Exchange, Exchange(name = info.get('exchange'), market_id = market_id))
				exchange_id = sqlalchemy_get(session, Exchange, "name", info.get('exchange'), "id")

			# Symbol
			step = "Symbol"
			symbol_id = sqlalchemy_get(session, Symbol, "symbol", info.get('symbol'), "id")
			if(symbol_id == None):
				sqlalchemy_add(session, Symbol, Symbol(symbol = info.get('symbol'), 
														exchange_id = exchange_id,
														country_id = country_id,
														shortname = info.get('shortName'),
														longname = info.get('longName')))
				symbol_id = sqlalchemy_get(session, Symbol, "symbol", info.get('symbol'), "id")


			print(sym)
			goodsymbols.append(sym)
		except Exception as e:
			print(sym + " - FAILED")
			badsymbols.append(sym + "\n STEP: " + step + "\n EXCEPTION: " + str(e))
except:
	session.rollback()
	raise
finally:
	out_file = open(".\\symbols_all_GOOD.txt", "w")
	for s in goodsymbols:
		out_file.write(s+"\n")
	out_file.close()

	out_file = open(".\\symbols_all_BAD.txt", "w")
	for s in badsymbols:
		out_file.write(s+"\n")
		out_file.write("==============================================\n\n")
	out_file.close()
	session.close()
