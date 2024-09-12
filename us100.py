import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Descargar datos históricos del NASDAQ 100
data = yf.download('^NDX', start='2020-01-01', end='2024-01-01', interval='1d')

# Calcular la EMA de 50 periodos
data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

# Calcular Supertrend
def calculate_supertrend(df, atr_period=10, atr_multiplier=3):
    high = df['High']
    low = df['Low']
    close = df['Close']

    # ATR
    df['ATR'] = df['High'].rolling(atr_period).max() - df['Low'].rolling(atr_period).min()

    # Calcular Supertrend básico
    df['Supertrend_upper'] = ((high + low) / 2) + (atr_multiplier * df['ATR'])
    df['Supertrend_lower'] = ((high + low) / 2) - (atr_multiplier * df['ATR'])

    # Señales de compra/venta
    df['Supertrend'] = np.where(close > df['Supertrend_lower'], df['Supertrend_lower'], df['Supertrend_upper'])
    df['Supertrend_signal'] = np.where(close > df['Supertrend'], 'buy', 'sell')
    return df

# Aplicar la función Supertrend
data = calculate_supertrend(data)

# Visualización
plt.figure(figsize=(12, 8))
plt.plot(data['Close'], label='US100 Close Price', color='blue')
plt.plot(data['EMA_50'], label='EMA 50', color='orange')
plt.plot(data['Supertrend'], label='Supertrend', color='green')

# Añadir señales de compra y venta
buy_signals = data[data['Supertrend_signal'] == 'buy']
sell_signals = data[data['Supertrend_signal'] == 'sell']

plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', alpha=1)

plt.title('US100 Trading Strategy (EMA 50 + Supertrend)')
plt.legend(loc='best')
plt.show()
