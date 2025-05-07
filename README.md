# AstroScheduler

**AstroScheduler** is a Python library for constructing EcoStruxure Building Operation (EBO) Multistate Time Schedule objects with daily astronomical (sunrise/sunset offset) events. Sunrise and sunset times are automatically calculated based on provided latitude and longitude using the `astral` library.

## Features

- Generate EBO-compliant `<ObjectSet>` XML exports, ready for import into EBO.
- Simplify time schedule configuration using an Excel spreadsheet. Template provided.
- Create a combination of absolute time referenced and sunrise/sunset time referenced schedule events in the same schedule.
- Modular design for future object types (via `EBOXMLBuilder` base class).

---

## Example Usage

### AstroSchedulerConfig Example

The AstroSchedulerConfig class is used to manage configuration data, including loading from an Excel spreadsheet, converting to a dictionary, and exporting to JSON.

#### Usage

```python
import os
from astroscheduler.config import AstroSchedulerConfig

# Initialize the configuration class
config = AstroSchedulerConfig()

# Copy a sample Excel template to a desired location
template = "TimeScheduleConfig.xlsx"
config.copy_sample_template(template)

# … edit the template Excel file, save and close.

# Load configuration from the Excel file
config.from_spreadsheet(template)

# Access configuration attributes
print("Latitude:", config.latitude)
print("Longitude:", config.longitude)
print("Schedule Type:", config.schedule_type)
print("Entries:", config.entries)

# Export configuration to a JSON file
output_json = os.path.join(os.path.dirname(__file__), "data/sample_output/config.json")
config.to_json(output_json)
```
- [ ] 
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

### AstroScheduler Example

The AstroSchedulerConfig class is used to build the astronomical time schedule object based on the provided config and write to EBO-compliant XML, ready for import.

#### Usage

TODO: add usage.
