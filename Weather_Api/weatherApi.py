import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 38.3502,
    "longitude": 38.3167,
    "hourly": ["temperature_2m", "relative_humidity_2m"],
    "timezone": "auto",
    "past_days": 2,
    "forecast_days": 1
}


responses = openmeteo.weather_api(url, params=params)


response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

hourly_dataframe = pd.DataFrame(data=hourly_data)


last_2_days = hourly_dataframe.tail(48)


last_2_days['date'] = last_2_days['date'].dt.date
daily_averages = last_2_days.groupby('date').mean().reset_index()


for index, row in daily_averages.iterrows():
    print(f"Tarih: {row['date']}, Ortalama Sıcaklık: {row['temperature_2m']:.2f}°C, Ortalama Nem: {row['relative_humidity_2m']:.2f}%")