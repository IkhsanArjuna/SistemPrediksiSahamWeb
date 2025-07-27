import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import os

from django.conf import settings
import plotly.graph_objs as go

def load_datatlkm():
    try:
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'tlkm.csv')  # lokasi file CSV
        df = pd.read_csv(csv_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df[['Date', 'Close']]
        df.dropna(inplace=True)

        if len(df) < 61:
            print("❌ Data tidak cukup untuk pelatihan (minimal 61 baris)")
            return pd.DataFrame()
        return df
    except Exception as e:
        print(f"❌ Error load_data(): {e}")
        return pd.DataFrame()

def train_lstm_modeltlkm(df):
    df = df.copy()
    df.set_index('Date', inplace=True)

    # Scaling
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

    # Sequence
    sequence_length = 60
    X_train, y_train = [], []
    for i in range(sequence_length, len(scaled_data)):
        X_train.append(scaled_data[i - sequence_length:i, 0])
        y_train.append(scaled_data[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, batch_size=32, epochs=5, verbose=0)

    return model, scaler, df, scaled_data

def predict_next_7_daystlkm(model, scaler, df, scaled_data, period=7):
    last_sequence = scaled_data[-60:]
    X_test = np.array([last_sequence])
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predictions = []
    for _ in range(period):
        pred = model.predict(X_test, verbose=0)[0, 0]
        predictions.append(pred)
        next_input = np.append(X_test[0, 1:], [[pred]], axis=0)
        X_test = np.array([next_input])

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    future_dates = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=period)
    forecast_df = pd.DataFrame(data=predictions, index=future_dates, columns=['Prediction'])

    return forecast_df

def plot_historicaltlkm(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Harga Historis"))
    fig.update_layout(title_text='Data Historis', xaxis_rangeslider_visible=False)
    return fig

def plot_forecasttlkm(df, forecast_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Historis"))
    fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['Prediction'], name="Prediksi"))
    fig.update_layout(title_text='Prediksi Harga 7 Hari ke Depan', xaxis_rangeslider_visible=False)
    return fig
