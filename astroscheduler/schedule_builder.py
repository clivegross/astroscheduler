import xml.etree.ElementTree as ET
from xml.dom import minidom
from astroscheduler.ebo_xml_builder import EBOXMLBuilder

class ScheduleBuilder(EBOXMLBuilder):
    """
    A class to build a schedule XML structure for importing objects into EBO.
    This class extends the EBOXMLBuilder class and provides methods to create
    schedule-related XML elements.
    Example XML structure:
    <OI NAME="Multistate Schedule" TYPE="schedule.NSPMultistateSchedule">
    <PI Name="ScheduleDefault" Value="{{ScheduleDefault}}"/>
    <OI NAME="ES00001" TYPE="system.schedulecommon.propertytypes.SpecialEvent" hidden="1">
      <PI Name="EventIndex" Value="1"/>
      <PI Name="EventName" Value="05-01"/>
      <PI Name="EventPriority" Value="16"/>
      <OI NAME="EP" TYPE="system.schedulecommon.propertytypes.calentry.DateCalendarEntry" hidden="1">
        <PI Name="Month" Value="5"/>
        <PI Name="Year" Value="2155"/>
      </OI>
      <OI NAME="TVP00001" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Value" Value="7"/>
      </OI>
      <OI NAME="TVP00002" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Hour" Value="6"/>
        <PI Name="Minute" Value="13"/>
        <PI Name="Value" Value="1"/>
      </OI>
      <OI NAME="TVP00003" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Hour" Value="16"/>
        <PI Name="Minute" Value="30"/>
        <PI Name="Value" Value="9"/>
      </OI>
      <OI NAME="TVP00004" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Hour" Value="17"/>
        <PI Name="Minute" Value="16"/>
        <PI Name="Value" Value="2"/>
      </OI>
      <OI NAME="TVP00005" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Hour" Value="18"/>
        <PI Name="Minute" Value="16"/>
        <PI Name="Value" Value="3"/>
      </OI>
    </OI>
    <OI NAME="ES00002" TYPE="system.schedulecommon.propertytypes.SpecialEvent" hidden="1">
      <PI Name="EventIndex" Value="2"/>
      <PI Name="EventName" Value="05-02"/>
      <PI Name="EventPriority" Value="16"/>
      <OI NAME="EP" TYPE="system.schedulecommon.propertytypes.calentry.DateCalendarEntry" hidden="1">
        <PI Name="DayOfMonth" Value="2"/>
        <PI Name="Month" Value="5"/>
        <PI Name="Year" Value="2155"/>
      </OI>
      <OI NAME="TVP00001" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Hour" Value="6"/>
        <PI Name="Minute" Value="13"/>
        <PI Name="Value" Value="1"/>
      </OI>
      <OI NAME="TVP00002" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Hour" Value="16"/>
        <PI Name="Minute" Value="30"/>
        <PI Name="Value" Null="1"/>
      </OI>
    </OI>
    <OI NAME="ES00003" TYPE="system.schedulecommon.propertytypes.SpecialEvent" hidden="1">
      <PI Name="EventIndex" Value="3"/>
      <PI Name="EventName" Value="any-10"/>
      <PI Name="EventPriority" Value="16"/>
      <OI NAME="EP" TYPE="system.schedulecommon.propertytypes.calentry.DateCalendarEntry" hidden="1">
        <PI Name="DayOfMonth" Value="10"/>
        <PI Name="Month" Value="255"/>
        <PI Name="Year" Value="2025"/>
      </OI>
      <OI NAME="TVP00001" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Hour" Value="6"/>
        <PI Name="Minute" Value="10"/>
        <PI Name="Value" Value="1"/>
      </OI>
      <OI NAME="TVP00002" TYPE="system.schedulecommon.propertytypes.tvp.IntegerValuePair" hidden="1">
        <PI Name="Hour" Value="17"/>
        <PI Name="Value" Null="1"/>
      </OI>
    </OI>
  </OI>
    Example usage:
        builder = ScheduleBuilder()
        event_1 = builder.create_schedule_special_event(event_name="05-01", day_of_month=1, month=5)
        event_2 = builder.create_schedule_special_event(event_name="05-02", day_of_month=2, month=5)
        builder.add_integer_value_pairs_to_event(event_1, tvp_values_event_1)
        builder.add_integer_value_pairs_to_event(event_2, tvp_values_event_2)
        schedule = builder.create_multistate_schedule("Office Light Schedule", schedule_default=0)
        builder.add_special_events_to_schedule(schedule, [event_1, event_2])
        builder.add_to_exported_objects(schedule)
    """
    def __init__(self, version="6.0.4.90", server_full_path="/Server 1"):
        super().__init__(version, server_full_path)

    @staticmethod
    def create_schedule_default(value):
        """
        Creates a <PI> element for ScheduleDefault.

        Parameters:
            value (int or str): The default value for the schedule.

        Returns:
            Element: The <PI> XML element.
        """
        return ET.Element("PI", {"Name": "ScheduleDefault", "Value": str(value)})

    @staticmethod
    def create_schedule_event_integer_value_pair(name, hour, minute, value, hidden="1"):
        entry = ET.Element("OI", {
            "NAME": name,
            "TYPE": "system.schedulecommon.propertytypes.tvp.IntegerValuePair",
            "hidden": hidden
        })
        ET.SubElement(entry, "PI", {"Name": "Hour", "Value": str(hour)})
        ET.SubElement(entry, "PI", {"Name": "Minute", "Value": str(minute)})
        ET.SubElement(entry, "PI", {"Name": "Value", "Value": str(value)})
        return entry

    @staticmethod
    def create_schedule_special_event(index=1, event_name="Event", day_of_month="255", month="255", year="2155", priority="16", hidden="1"):
        """
        Creates a SpecialEvent element with the given parameters.
        Parameters:
            name (str): The name of the event.
            index (int): The event index.
            event_name (str): The name of the event.
            day_of_month (int): The day of the month.
            month (str, optional): The month. Default is "255" (Any Month).
            year (str, optional): The year. Default is "2155" (Any Year).
            priority (str, optional): The event priority. Default is "16".
            hidden (str, optional): Whether the event is hidden. Default is "1".
        """
        event = ET.Element("OI", {
            "NAME": f"ES{str(index).zfill(5)}",
            "TYPE": "system.schedulecommon.propertytypes.SpecialEvent",
            "hidden": hidden
        })
        ET.SubElement(event, "PI", {"Name": "EventIndex", "Value": str(index)})
        ET.SubElement(event, "PI", {"Name": "EventName", "Value": event_name})
        ET.SubElement(event, "PI", {"Name": "EventPriority", "Value": str(priority)})

        ep = ET.SubElement(event, "OI", {
            "NAME": "EP",
            "TYPE": "system.schedulecommon.propertytypes.calentry.DateCalendarEntry",
            "hidden": "1"
        })
        ET.SubElement(ep, "PI", {"Name": "DayOfMonth", "Value": str(day_of_month)})
        ET.SubElement(ep, "PI", {"Name": "Month", "Value": str(month)})
        ET.SubElement(ep, "PI", {"Name": "Year", "Value": str(year)})
        return event

    @staticmethod
    def add_integer_value_pairs_to_event(event_elem, tvp_values, start_index=1):
        for i, val in enumerate(tvp_values, start=start_index):
            name = f"TVP{str(i).zfill(5)}"
            pair = ScheduleBuilder.create_schedule_event_integer_value_pair(
                name, val["Hour"], val["Minute"], val["Value"]
            )
            event_elem.append(pair)

    @staticmethod
    def create_multistate_schedule(name, schedule_default=None):
        schedule = ET.Element("OI", {
            "NAME": name,
            "TYPE": "schedule.NSPMultistateSchedule"
        })
        if schedule_default is not None:
            schedule.append(ScheduleBuilder.create_schedule_default(schedule_default))
        return schedule

    @staticmethod
    def add_special_events_to_schedule(schedule_elem, events, start_index=1):
        for i, event in enumerate(events, start=start_index):
            name = f"ES{str(i).zfill(5)}"
            event.set("NAME", name)
            # Find and update the EventIndex PI
            for pi in event.findall("PI"):
                if pi.attrib.get("Name") == "EventIndex":
                    pi.set("Value", str(i))
                    break
            schedule_elem.append(event)


if __name__ == "__main__":
    # Example usage
    # Step 1: Create TVP values for events
    builder = ScheduleBuilder()

    tvp_values_event_1 = [
        {"Hour": 6, "Minute": 13, "Value": 1},
        {"Hour": 16, "Minute": 30, "Value": 9},
        {"Hour": 17, "Minute": 16, "Value": 2},
        {"Hour": 18, "Minute": 16, "Value": 3},
    ]

    tvp_values_event_2 = [
        {"Hour": 6, "Minute": 13, "Value": 1},
        {"Hour": 16, "Minute": 30, "Value": 9}
    ]

    event_1 = builder.create_schedule_special_event(event_name="05-01", day_of_month=1, month=5)
    event_2 = builder.create_schedule_special_event(event_name="05-02", day_of_month=2, month=5)

    builder.add_integer_value_pairs_to_event(event_1, tvp_values_event_1)
    builder.add_integer_value_pairs_to_event(event_2, tvp_values_event_2)

    schedule = builder.create_multistate_schedule("Office Light Schedule", schedule_default=0)
    builder.add_special_events_to_schedule(schedule, [event_1, event_2])

    builder.add_to_exported_objects(schedule)
    print(builder.to_pretty_xml())
    builder.write_pretty_xml("schedule.xml")

    
