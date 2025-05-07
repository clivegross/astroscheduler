from datetime import date, timedelta
from astral import LocationInfo
from astral.sun import sun
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
import pandas as pd
import os

def generate_sunrise_sunset_df(latitude, longitude, year):
    """
    Generate a DataFrame containing sunrise and sunset times for every day in a given year.

    :param latitude: Latitude of the location.
    :param longitude: Longitude of the location.
    :param year: Year for which to generate the data.
    :return: A pandas DataFrame with columns ['Date', 'Sunrise', 'Sunset'].
    """
    # Determine the timezone using TimezoneFinder
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=latitude, lng=longitude)
    if not tz_name:
        raise ValueError("Could not determine timezone for the given latitude and longitude.")
    tz = ZoneInfo(tz_name)

    # Define location object for Astral
    location = LocationInfo(name="Custom", region="None", timezone=tz_name,
                            latitude=latitude, longitude=longitude)

    # Generate dates for the entire year
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # Calculate sunrise and sunset times
    sunrise_times = []
    sunset_times = []
    for d in dates:
        s = sun(location.observer, date=d, tzinfo=tz)
        sunrise_times.append(s['sunrise'].time())
        sunset_times.append(s['sunset'].time())

    # Create a DataFrame
    df = pd.DataFrame({
        "Date": pd.to_datetime(dates),
        "Sunrise": sunrise_times,
        "Sunset": sunset_times
    })

    return df

def get_sunrise_or_sunset_time(df, event, transition="Sunrise"):
    """
    Get the sunrise or sunset time for a specific event based on its DayOfMonth and Month.

    :param df: A pandas DataFrame produced by generate_sunrise_sunset_df, containing
               columns ['Date', 'Sunrise', 'Sunset'].
    :param event: A dictionary containing event details (DayOfMonth, Month).
    :return: A dictionary with the sunrise time {"Hour": x, "Minute": y}.
    :raises ValueError: If the event date is not found in the DataFrame.
    """
    # Extract the DayOfMonth and Month from the event
    day = event.get("DayOfMonth")
    month = event.get("Month")

    if day is None or month is None:
        raise ValueError("Event must contain 'DayOfMonth' and 'Month' keys.")

    # Filter the DataFrame for the matching date
    matching_row = df[(df["Date"].dt.day == day) & (df["Date"].dt.month == month)]

    if matching_row.empty:
        raise ValueError(f"No matching date found in the DataFrame for Day: {day}, Month: {month}.")

    # Extract the sunrise time
    sunrise_time = matching_row.iloc[0][transition]  # Sunrise is a datetime.time object

    return {"Hour": sunrise_time.hour, "Minute": sunrise_time.minute}

def get_sunrise_time(df, event):
    """
    Get the sunrise time for a specific event based on its DayOfMonth and Month.

    :param df: A pandas DataFrame produced by generate_sunrise_sunset_df, containing
               columns ['Date', 'Sunrise', 'Sunset'].
    :param event: A dictionary containing event details (DayOfMonth, Month).
    :return: A dictionary with the sunrise time {"Hour": x, "Minute": y}.
    :raises ValueError: If the event date is not found in the DataFrame.
    """
    return get_sunrise_or_sunset_time(df, event, "Sunrise")

def get_sunset_time(df, event):
    """
    Get the sunrise time for a specific event based on its DayOfMonth and Month.

    :param df: A pandas DataFrame produced by generate_sunrise_sunset_df, containing
               columns ['Date', 'Sunrise', 'Sunset'].
    :param event: A dictionary containing event details (DayOfMonth, Month).
    :return: A dictionary with the sunrise time {"Hour": x, "Minute": y}.
    :raises ValueError: If the event date is not found in the DataFrame.
    """
    return get_sunrise_or_sunset_time(df, event, "Sunset")
    


if __name__ == "__main__":
    # Example inputs
    latitude = 37.7749  # San Francisco
    longitude = -122.4194
    year = 2025

    # Generate sunrise and sunset DataFrame
    df = generate_sunrise_sunset_df(latitude, longitude, year)

    # Print timezone and first few rows of the DataFrame
    print(f"Timezone: {TimezoneFinder().timezone_at(lat=latitude, lng=longitude)}")
    print(df.head())

    # Save the DataFrame to a JSON file
    output_file = os.path.join(os.path.dirname(__file__), "sunrise_sunset.json")
    df.to_json(output_file, orient="records", date_format="iso")
    print(f"Sunrise and sunset data saved to: {output_file}")

