from astroscheduler.schedule_builder import ScheduleBuilder
from datetime import date, timedelta, datetime
from astroscheduler.sunrise_sunset import generate_sunrise_sunset_df, get_sunrise_time, get_sunset_time

class AstroSchedule:
    def __init__(self, config, schedule_name="AstroSchedule"):
        """
        Initialize the ScheduleBuilderWithConfig class.

        :param config: An instance of AstroSchedulerConfig.
        """
        if not config:
            raise ValueError("A valid AstroSchedulerConfig instance is required.")
        self.config = config
        self.builder = ScheduleBuilder(version=self.config.ebo_version)
        self.schedule = self.builder.create_multistate_schedule(schedule_name, schedule_default=self.config.default_value)
        self.sunrise_sunset_df = generate_sunrise_sunset_df(self.config.latitude, self.config.longitude, self.config.reference_year)
        self.events = []
        self.build()

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
        event_object = self.builder.create_schedule_special_event(
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
            if entry.get("TimeReference") == "SunriseOffset":
                # if this entry is strunrise offset, get the sunrise hour and minute of this day and add the offsets from the entry
                sunrise_entry = get_sunrise_time(self.sunrise_sunset_df, event)
                offset_entry = entry.copy()
                offset_entry["Hour"] = sunrise_entry["Hour"] + entry["Hour"]
                offset_entry["Minute"] = sunrise_entry["Minute"] + entry["Minute"]
                entries.append(offset_entry)
            if entry.get("TimeReference") == "SunsetOffset":
                # if this entry is sunset offset, get the sunset hour and minute of this day and add the offsets from the entry
                sunset_entry = get_sunset_time(self.sunrise_sunset_df, event)
                offset_entry = entry.copy()
                offset_entry["Hour"] = sunset_entry["Hour"] + entry["Hour"]
                offset_entry["Minute"] = sunset_entry["Minute"] + entry["Minute"]
                entries.append(offset_entry)                
        self.builder.add_integer_value_pairs_to_event(event_object, entries)

    def build(self):
        """
        """
        # create event for every day in year
        self.create_events_for_year()
        # create event xml objects and insert event entries from config
        event_objects = self.create_event_objects()
        # add events to schedule xml object
        self.builder.add_special_events_to_schedule(self.schedule, event_objects)
        self.builder.add_to_exported_objects(self.schedule)
