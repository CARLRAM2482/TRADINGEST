import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Descargar los datos del oro (Golden) - Usando el símbolo 'GC=F' para futuros del oro
gold_data = yf.download('GC=F', start='2023-01-01', end='2023-12-31')

# Calcular la EMA de 50 periodos
gold_data['EMA_50'] = gold_data['Close'].ewm(span=50, adjust=False).mean()

# Función para calcular el Supertrend
def supertrend(df, period=10, multiplier=3):
    hl2 = (df['High'] + df['Low']) / 2
    df['ATR'] = df['High'].rolling(period).max() - df['Low'].rolling(period).min()
    df['Upperband'] = hl2 + (multiplier * df['ATR'])
    df['Lowerband'] = hl2 - (multiplier * df['ATR'])
    df['Supertrend'] = np.where(df['Close'] > df['Upperband'], df['Upperband'], df['Lowerband'])
    return df

# Aplicar Supertrend
gold_data = supertrend(gold_data)

# Crear un gráfico para visualizar la estrategia
plt.figure(figsize=(12, 8))

# Precio de cierre
plt.plot(gold_data.index, gold_data['Close'], label='Precio Cierre Oro', color='gold')

# EMA 50
plt.plot(gold_data.index, gold_data['EMA_50'], label='EMA 50', color='blue')

# Supertrend
plt.plot(gold_data.index, gold_data['Supertrend'], label='Supertrend', color='green')

# Añadir título y leyendas
plt.title('Oro (GC=F) con EMA 50 y Supertrend', fontsize=16)
plt.xlabel('Fecha', fontsize=12)
plt.ylabel('Precio (USD)', fontsize=12)
plt.legend(loc='upper left')

# Mostrar el gráfico
plt.show()
