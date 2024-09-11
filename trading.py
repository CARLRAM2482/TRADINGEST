import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Descargar datos históricos de Apple (AAPL)
ticker = 'AAPL'
data = yf.download(ticker, start='2023-01-01', end='2024-07-31')

# Calcular EMA 50
data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

# Calcular Supertrend
def Supertrend(df, period=10, multiplier=3):
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    tr1 = pd.Series(high - low)
    tr2 = pd.Series(abs(high - close.shift(1)))
    tr3 = pd.Series(abs(low - close.shift(1)))
    tr = pd.Series(tr1.combine(tr2, max).combine(tr3, max))
    
    atr = tr.rolling(window=period).mean()
    
    hl2 = (high + low) / 2
    basic_upperband = hl2 + (multiplier * atr)
    basic_lowerband = hl2 - (multiplier * atr)
    
    final_upperband = pd.Series(basic_upperband)
    final_lowerband = pd.Series(basic_lowerband)
    
    for i in range(period, len(df)):
        if close[i-1] <= final_upperband[i-1]:
            final_upperband[i] = min(basic_upperband[i], final_upperband[i-1])
        else:
            final_upperband[i] = basic_upperband[i]
            
        if close[i-1] >= final_lowerband[i-1]:
            final_lowerband[i] = max(basic_lowerband[i], final_lowerband[i-1])
        else:
            final_lowerband[i] = basic_lowerband[i]
            
    supertrend = pd.Series(index=df.index, dtype='float64')
    supertrend = final_upperband
    for i in range(period, len(df)):
        if close[i] <= final_upperband[i]:
            supertrend[i] = final_upperband[i]
        else:
            supertrend[i] = final_lowerband[i]
    
    return supertrend

data['Supertrend'] = Supertrend(data)

# Crear gráficos
fig, ax = plt.subplots(figsize=(14, 7))

# Gráfico de precios, EMA y Supertrend
ax.plot(data['Close'], label='Precio de Cierre', color='blue')
ax.plot(data['EMA_50'], label='EMA 50', color='orange')
ax.plot(data['Supertrend'], label='Supertrend', color='green')
ax.set_title('AAPL - Precio de Cierre, EMA 50 y Supertrend')
ax.legend()

plt.tight_layout()
plt.show()
