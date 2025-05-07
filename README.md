# AstroScheduler

**AstroScheduler** is a Python library for constructing EcoStruxure Building Operation (EBO)–compatible XML files programmatically. It is designed primarily for generating astronomical time schedules (e.g. multistate schedules with sunrise/sunset offset events) but is extensible to support any EBO object type.

## Features

- Generate EBO-compliant `<ObjectSet>` XML exports.
- Build multistate schedules with special events and time-value pairs.
- Auto-assign names and indices to schedule objects.
- Output readable, pretty-printed XML to file.
- Modular design for future object types (via `EBOXMLBuilder` base class).
- **NEW**: Manage configuration data with `AstroSchedulerConfig`.

---

## Example Usage

### **ScheduleBuilder Example**
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
```

### AstroSchedulerConfig Example

The AstroSchedulerConfig class is used to manage configuration data, including loading from an Excel spreadsheet, converting to a dictionary, and exporting to JSON.

#### Features

- Load configuration data from an Excel file.
- Access configuration attributes like latitude, longitude, schedule_type, etc.
- Export configuration data to a JSON file.

#### Usage

```python
import os
from astroscheduler.config import AstroSchedulerConfig

# Initialize the configuration class
config = AstroSchedulerConfig()

# Copy a sample Excel template to a desired location
output_dir = os.path.join(os.path.dirname(__file__), "data/sample_input")
os.makedirs(output_dir, exist_ok=True)
template_path = os.path.join(output_dir, "TimeScheduleConfig.xlsx")
config.copy_sample_template(template_path)

# Load configuration from the Excel file
config.from_spreadsheet(template_path)

# Access configuration attributes
print("Latitude:", config.latitude)
print("Longitude:", config.longitude)
print("Schedule Type:", config.schedule_type)
print("Entries:", config.entries)

# Export configuration to a JSON file
output_json = os.path.join(os.path.dirname(__file__), "data/sample_output/config.json")
config.to_json(output_json)
```

#### Example Output

JSON File (`config.json`):

```
{
    "latitude": 37.7749,
    "longitude": -122.4194,
    "schedule_type": "Multistate",
    "default_value": 0,
    "reference_year": 2025,
    "ebo_version": "4.0.1",
    "entries": [
        {
            "Description": "WEE HOURS",
            "TimeReference": "Absolute",
            "Hour": 0,
            "Minute": 0,
            "Value": 7,
            "Comments": "TimeReference Absolute means the entry starts at the time of day Hour:Minute"
        },
        {
            "Description": "DAY",
            "TimeReference": "SunriseOffset",
            "Hour": 0,
            "Minute": 0,
            "Value": 1,
            "Comments": "TimeReference SunriseOffset means the entry starts at sunrise plus Hours:Minutes"
        },
    ]
}
```

