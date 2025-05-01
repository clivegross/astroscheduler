from datetime import date, timedelta
from astral import LocationInfo
from astral.sun import sun
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
import pandas as pd

# Input coordinates
latitude = -27.467778
longitude = 153.028056

# Get timezone
tf = TimezoneFinder()
tz_name = tf.timezone_at(lat=latitude, lng=longitude)
tz = ZoneInfo(tz_name)

# Define location object for Astral
location = LocationInfo(name="Custom", region="None", timezone=tz_name,
                        latitude=latitude, longitude=longitude)

# Generate data
dates = [date(2025, 1, 1) + timedelta(days=i) for i in range(365)]
sunrise_times = []
sunset_times = []

for d in dates:
    s = sun(location.observer, date=d, tzinfo=tz)
    sunrise_times.append(s['sunrise'].time())
    sunset_times.append(s['sunset'].time())

df = pd.DataFrame({
    "Date": dates,
    "Sunrise": sunrise_times,
    "Sunset": sunset_times
})

print(f"Timezone: {tz_name}")
print(df.head())

# Show entire DataFrame regardless of size
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

df.to_json("sunrise_sunset.json", orient="records", date_format="iso")