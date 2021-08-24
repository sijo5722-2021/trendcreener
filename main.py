from utils import moving_average, minimum, maximum, validate, read_csv_file, validate_nifty_sectoral_index, \
    get_sector_stocks
from datetime import date, timedelta


start: date = date(2020, 6, 26)
end: date = date(2021, 6, 20)

sectors_in_trend = {}
sectors = ['NIFTY_AUTO', 'NIFTY_BANK', 'NIFTY_ENERGY', 'NIFTY_FIN_SERVICE', 'NIFTY_FMCG',
           'NIFTY_HEALTHCARE', 'NIFTY_IT', 'NIFTY_MEDIA', 'NIFTY_METAL', 'NIFTY_PHARMA', 'NIFTY_REALTY',
           'NIFTY_CONSUMER_DURABLES', 'NIFTY_PSU_BANK', 'NIFTY_PVT_BANK', 'NIFTY_OIL_AND_GAS']

for sector in sectors:
    sectors_in_trend[sector] = validate_nifty_sectoral_index(sector, start, end)
print(sectors_in_trend)

stocks_initial_list = []
for sector in sectors:
    if sectors_in_trend[sector]:
        stocks_initial_list = stocks_initial_list + get_sector_stocks(sector)

print(stocks_initial_list)


shortlisted_stocks = set()
for stock in stocks_initial_list:
    try:
        if validate( stock, start, end):
            shortlisted_stocks.add(stock)
    except IndexError:
        print("Error")

print(shortlisted_stocks)
