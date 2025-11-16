import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(layout="wide", page_title="Stock Forecasting App")
st.title("Stock Market Forecasting with ARIMA")

# Sidebar inputs
ticker = st.sidebar.text_input("Ticker (e.g., AAPL, TSLA, GOOGL)", value="AAPL").upper()
period = st.sidebar.selectbox("Historical period", ["1y", "2y", "5y", "10y"], index=2)
forecast_days = st.sidebar.slider("Forecast days", 30, 180, 60)

st.write(f"Fetching data for **{ticker}** for the last **{period}**...")

# Fetch data
@st.cache_data
def load_data(ticker, period):
    df = yf.download(ticker, period=period, progress=False)
    df.reset_index(inplace=True)
    return df

df = load_data(ticker, period)

if df.empty:
    st.error("No data found for that ticker.")
    st.stop()

# Plot historical closing prices
st.subheader("Closing Price History")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close'))
fig.update_layout(title=f"{ticker} Closing Price", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig, use_container_width=True)

# Prepare data for ARIMA
data = df['Close']

# Fit ARIMA model
with st.spinner("Training ARIMA model..."):
    model = ARIMA(data, order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_days)
    forecast_index = pd.date_range(start=df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=forecast_days)
    forecast_df = pd.DataFrame({"Date": forecast_index, "Forecast": forecast})

# Plot forecast
st.subheader(f"Forecast for next {forecast_days} days")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Historical'))
fig2.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Forecast'], name='Forecast'))
fig2.update_layout(title=f"{ticker} Forecast", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig2, use_container_width=True)

# Download forecast CSV
csv = forecast_df.to_csv(index=False)
st.download_button("Download Forecast CSV", csv, file_name=f"{ticker}_forecast.csv", mime="text/csv")