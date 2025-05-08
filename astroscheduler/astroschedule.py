from astroscheduler.config import AstroSchedulerConfig
from astroscheduler.schedule_builder import ScheduleBuilder
from datetime import date, timedelta, datetime
from astroscheduler.sunrise_sunset import generate_sunrise_sunset_df, get_sunrise_time, get_sunset_time
from astroscheduler.ebo_xml_builder import print_pretty_xml, to_pretty_xml

class AstroSchedule(ScheduleBuilder):
    def __init__(self, config=None):
        if not config:
            config = AstroSchedulerConfig()
        self.config = config

        # Parent constructor
        super().__init__(ebo_version=config.ebo_version)

        self.events = []
        self._schedule = self.create_multistate_schedule(
            self.config.schedule_name, schedule_default=self.config.default_value
        )
        self._update_sunrise_sunset_df()
        self.build()

    # === Properties for schedule ===

    @property
    def schedule(self):
        """Generates schedule if it's not set or needs regeneration."""
        return self._schedule

    @property
    def schedule_name(self):
        return self.config.schedule_name

    @schedule_name.setter
    def schedule_name(self, value):
        if value != self.config.schedule_name:
            self.config.schedule_name = value
            self._schedule = self.create_multistate_schedule(
                self.config.schedule_name, schedule_default=self.config.default_value
            )  # Regenerate schedule
            self.build()

    @property
    def ebo_version(self):
        return self._ebo_version

    @ebo_version.setter
    def ebo_version(self, value):
        if value != self._ebo_version:
            self._ebo_version = value
            self.config.ebo_version = value
            self.object_set = self._create_object_set()           

    @property
    def default_value(self):
        return self.config.default_value

    @default_value.setter
    def default_value(self, value):
        if value != self.config.default_value:
            self.config.default_value = value
            self._schedule = self.create_multistate_schedule(
                self.config.schedule_name, schedule_default=self.config.default_value
            )  # Regenerate schedule
            self.build()

    # === Properties for sunrise/sunset df ===

    @property
    def sunrise_sunset_df(self):
        """Generates sunrise/sunset df if it needs regeneration."""
        return self._sunrise_sunset_df

    @property
    def latitude(self):
        return self.config.latitude

    @latitude.setter
    def latitude(self, value):
        if value != self.config.latitude:
            self.config.latitude = value
            self._update_sunrise_sunset_df()
            self.build()

    @property
    def longitude(self):
        return self.config.longitude

    @longitude.setter
    def longitude(self, value):
        if value != self.config.longitude:
            self.config.longitude = value
            self._update_sunrise_sunset_df()
            self.build()

    @property
    def reference_year(self):
        return self.config.reference_year

    @reference_year.setter
    def reference_year(self, value):
        if value != self.config.reference_year:
            self.config.reference_year = value
            self._update_sunrise_sunset_df()
            self.build()

    def _update_sunrise_sunset_df(self):
        lat = self.config.latitude
        lon = self.config.longitude
        year = self.config.reference_year

        if None in (lat, lon, year):
            self._sunrise_sunset_df = None
            return

        try:
            self._sunrise_sunset_df = generate_sunrise_sunset_df(lat, lon, year)
        except Exception as e:
            print(f"Failed to generate sunrise/sunset data: {e}")
            self._sunrise_sunset_df = None

    def create_events_for_year(self, year=None):
        """
        Create a list of events for every day of the given year.

        :param year: The year for which to create events. If not provided, it will
                    first try to use self.config.reference_year. If that is not set,
                    it will default to the current year.
        """
        # Determine the year to use
        if year is None:
            try:
                year = int(self.config.reference_year)
            except (AttributeError, ValueError) as e:
                year = datetime.now().year  # Default to the current year
                print(f'Failed to parse config ReferenceYear {self.config.reference_year}, got error {e}. Using current year {year} instead...')

        self.events = []  # Initialize or reset the events list

        # Generate dates for the entire year
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        current_date = start_date

        while current_date <= end_date:
            # Create an event dictionary for the current date
            event = {
                "EventName": current_date.strftime("%m-%d"),
                "DayOfMonth": current_date.day,
                "Month": current_date.month
            }
            self.events.append(event)

            # Move to the next day
            current_date += timedelta(days=1)

    def create_event_object(self, event, with_entries=True):
        """
        Create a single XML event object using ScheduleBuilder.

        :param event: A dictionary containing event details (EventName, DayOfMonth, Month).
        :return: An event object created using ScheduleBuilder.
        """
        event_object = self.create_schedule_special_event(
            event_name=event["EventName"],
            day_of_month=event["DayOfMonth"],
            month=event["Month"]
        )
        # add entries to the object
        if with_entries:
            self.process_event_with_entries(event_object, event)
        return event_object

    def create_event_objects(self):
        """
        Create a list of XML event objects using self.events.

        :return: A list of event objects created using ScheduleBuilder.
        """
        if not self.events:
            raise ValueError("No events found. Please call create_events_for_year first.")

        event_objects = []
        for event in self.events:
            # Use the helper function to create a single event object
            event_object = self.create_event_object(event)
            event_objects.append(event_object)

        return event_objects
    
    def process_event_with_entries(self, event_object, event=None):
        """
        Process an event object by looping through config.entries. If an entry has
        TimeReference = "Absolute", add its time-value pairs to the event object.

        :param event_object: An event object created using create_event_object.
        {
            "Description": "WEE HOURS",
            "TimeReference": "Absolute",
            "Hour": 0,
            "Minute": 0,
            "Value": 7,
            "Comments": "TimeReference Absolute means the entry starts at the time of day Hour:Minute"
        },
        """
        if not hasattr(self.config, "entries") or not self.config.entries:
            raise ValueError("No entries found in the configuration.")
        entries = []
        for entry in self.config.entries:
            # Check if the entry has TimeReference = "Absolute"
            if entry.get("TimeReference") == "Absolute":
                # Add time-value pairs to the event object
                entries.append(entry)
            if entry.get("TimeReference") == "SunriseOffset" and self.sunrise_sunset_df is not None:
                # if this entry is strunrise offset, get the sunrise hour and minute of this day and add the offsets from the entry
                sunrise_entry = get_sunrise_time(self.sunrise_sunset_df, event)
                offset_entry = self.offset_hour_minute(sunrise_entry, entry)
                entries.append(offset_entry)
            if entry.get("TimeReference") == "SunsetOffset" and self.sunrise_sunset_df is not None:
                # if this entry is sunset offset, get the sunset hour and minute of this day and add the offsets from the entry
                sunset_entry = get_sunset_time(self.sunrise_sunset_df, event)
                offset_entry = self.offset_hour_minute(sunset_entry, entry)
                entries.append(offset_entry)
        self.add_integer_value_pairs_to_event(event_object, entries)

    def offset_hour_minute(self, entry, offset):
        """
        Adjust the hour and minute of an entry by applying an offset, handling negative minutes
        and ensuring the time stays within valid ranges.

        :param entry: A dictionary containing "Hour" and "Minute".
        :param offset: A dictionary containing "Hour" and "Minute" to offset the entry.
        :return: A new dictionary with adjusted "Hour" and "Minute".
        """
        entry_with_offset = offset.copy()
        entry_with_offset["Hour"] = entry["Hour"] + offset["Hour"]
        entry_with_offset["Minute"] = entry["Minute"] + offset["Minute"]

        # Handle negative minutes
        while entry_with_offset["Minute"] < 0:
            entry_with_offset["Minute"] += 60
            entry_with_offset["Hour"] -= 1

        # Handle minutes greater than or equal to 60
        while entry_with_offset["Minute"] >= 60:
            entry_with_offset["Minute"] -= 60
            entry_with_offset["Hour"] += 1

        # Ensure the hour stays within valid ranges (0-23)
        if entry_with_offset["Hour"] < 0:
            entry_with_offset["Hour"] = 0
            entry_with_offset["Minute"] = 0  # Reset to midnight if hour goes negative
        elif entry_with_offset["Hour"] >= 24:
            entry_with_offset["Hour"] = 23
            entry_with_offset["Minute"] = 59  # Cap to the last minute of the day

        return entry_with_offset

    def add_entry(self, time_ref="Absolute", hour=0, minute=0, value=None):
        """
        Add a new entry to the schedule configuration and rebuild the schedule object.

        :param time_ref: The time reference for the entry (e.g., "Absolute", "SunriseOffset").
        :param hour: The hour of the entry.
        :param minute: The minute of the entry.
        :param value: The value associated with the entry.
        """
        print(f"Adding entry: TimeReference={time_ref}, Hour={hour}, Minute={minute}, Value={value}")
        self.config.add_entry(time_ref, hour, minute, value)
        # Rebuild the schedule object
        self.build()

    def build(self):
        """
        Build the schedule object based on the configuration.
        """
        self._schedule = self.create_multistate_schedule(
            self.schedule_name, schedule_default=self.default_value
        )
        if self.config.entries:
            # create a new schedule object
            # create event for every day in year
            self.create_events_for_year()
            # create event xml objects and insert event entries from config
            event_objects = self.create_event_objects()
            # add events to schedule xml object
            self.add_special_events_to_schedule(self.schedule, event_objects)
        self.set_exported_objects(self.schedule)

