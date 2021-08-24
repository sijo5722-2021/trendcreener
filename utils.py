import pandas as pd
from nsepy.history import get_history


file_base_path='/home/sijo/Documents/NSE_index_data/'


def get_sector_stocks(sector):
    nse_stocks_file = file_base_path+sector.lower()+'.csv'
    df = read_csv_file(nse_stocks_file)
    return df['Symbol'].tolist()


def validate_nifty_sectoral_index(ticker, start, end):
    try:
        response = get_history(ticker, start, end, index=True)
        return validate(ticker, start, end, index=True)
    except IndexError:
        print("Error")
        return False


def moving_average(dataframe, column, window):
    return dataframe[column].rolling(window, min_periods=window).mean()


def minimum(dataframe, column):
    return dataframe[column].min()


def maximum(dataframe, column):
    return dataframe[column].max()


def validate(ticker, start ,end, index=False):
    intermediate_df = get_history(ticker, start, end, index)
    intermediate_df['Close_50dma'] = moving_average(intermediate_df, window=50, column='Close')
    intermediate_df['Close_150dma'] = moving_average(intermediate_df, window=150, column='Close')
    intermediate_df['Close_200dma'] = moving_average(intermediate_df, window=200, column='Close')
    week_52_low = minimum(intermediate_df, column='Low')
    week_52_high = maximum(intermediate_df, column='High')
    latest_close = intermediate_df.tail(1)['Close'].values[0]
    dma50 = intermediate_df.tail(1)['Close_50dma'].values[0]
    dma150 = intermediate_df.tail(1)['Close_150dma'].values[0]
    dma200 = intermediate_df.tail(1)['Close_200dma'].values[0]

    condition1 = latest_close > dma50 > dma150 > dma200
    condition2 = latest_close >= 1.3 * week_52_low
    condition3 = latest_close >= 0.75 * week_52_high

    if condition1 and condition2 and condition3:
        print(f"Stock- {ticker} has been shortlisted")
        return True
    else:
        print(f"Stock- {ticker} has been excluded")
        return False


def read_csv_file(path):
    return pd.read_csv(path)
