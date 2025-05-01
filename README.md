# AstroScheduler

**AstroScheduler** is a Python library for constructing EcoStruxure Building Operation (EBO)–compatible XML files programmatically. It is designed primarily for generating astronomical time schedules (e.g. multistate schedules with sunrise/sunset offset events) but is extensible to support any EBO object type.

## Features

- Generate EBO-compliant `<ObjectSet>` XML exports.
- Build multistate schedules with special events and time-value pairs.
- Auto-assign names and indices to schedule objects.
- Output readable, pretty-printed XML to file.
- Modular design for future object types (via `EBOXMLBuilder` base class).

## Example Usage

```python
from astroscheduler.schedule_builder import ScheduleBuilder

# Create builder
sb = ScheduleBuilder()

# Define special event
event = sb.create_special_event(index=1, name="Holiday", month=12)
sb.add_integer_value_pairs_to_event(event, [
    {"Hour": 6, "Minute": 0, "Value": 1},
    {"Hour": 18, "Minute": 0, "Value": 0}
])

# Create schedule and add event
schedule = sb.create_multistate_schedule("Office Lighting", schedule_default=0)
sb.add_special_events_to_schedule(schedule, [event])
sb.add_to_exported_objects(schedule)

# Output to file
sb.to_pretty_xml_file("office_lighting_schedule.xml")
