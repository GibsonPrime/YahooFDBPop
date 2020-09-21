import yfinance as yf

sym = "SRNE"


msft = yf.Ticker(sym)

# get stock info
info = msft.info
print(info)

# get historical market data
hist = msft.history(period="max")
#print(hist)

data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = sym,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "5d",
        # start = "2005-07-23",        
		# end = "2005-07-24",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        # 1m = 30 days
        # 5m = 60 days
        # 15m = 60 days
        # 30m = 60 days
        # 60m = 730 days
        # 90m = 60 days
        # 1d + inf
        interval = "1d",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )

# print(data)