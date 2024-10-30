import yfinance as yf
import matplotlib.pyplot as plt

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gains = (delta.where(delta > 0, 0)).fillna(0)
    losses = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gains.rolling(window=period, min_periods=1).mean()
    avg_loss = losses.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def plot_rsi(data, rsi_values, ticker):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(10, 6))
    ax1.plot(data['Close'], label='Close Price', color='blue')
    ax1.set_ylabel('Close Price')
    ax1.legend(loc='upper left')

    ax2.plot(rsi_values, label='RSI', color='orange')
    ax2.axhline(70, color='b', linestyle='--', label='Overbought (70)')
    ax2.axhline(30, color='g', linestyle='--', label='Oversold (30)')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper left')

    plt.title(f'RSI and Close Price for {ticker}')
    plt.show()

def main():
    tickers = [
    'AAR','HMC','SWDBY','NVS','AVTE','LAD','STTK','BABA','SEZL','ON','TM','AMR','AMD','DIS', 'LIT','GOOGL','AMZN','AAPL','MSFT','META','TSLA','NVDA','NKE','SGML','F','JPM','GS','BAC','JNJ','PFE','DOLE','USFD','TSN','PLL','BA','APH','LMT','GNRC','GSAT','ACM','MOD','ALL','XOM','CVX','BP','COP','SLB','HAL','BKR','NEE','DUK','SO','D','AEP','PCG','ES','PPL','FE','EXC','CNP',
    '2222.SR','E','PSX','VLO','MPC','HES','OXY','SU','CNQ','EOG','APC','DVN']

    tickers = sorted(tickers)
    start_date = '2024-03-01'
    end_date = '2024-10-31'

    a = []
    for ticker in tickers:
        print(f"Processing {ticker}...")
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        
        if not stock_data.empty:
            rsi_values = calculate_rsi(stock_data)
            last_rsi = rsi_values.iloc[-1]
            
            if last_rsi < 40:
                print(f"{ticker}: Last RSI = {last_rsi:.2f} (RSI < 45)")
                plot_rsi(stock_data, rsi_values, ticker)
            else:
                print(f"{ticker}: Last RSI = {last_rsi:.2f} (RSI >= 45), skipping plot.")
            a.append(f"{last_rsi:.1f} - {ticker}")    
    print(a)

if __name__ == "__main__":
    main()
