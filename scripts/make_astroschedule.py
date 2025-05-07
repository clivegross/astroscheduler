import os
from astroscheduler.astroschedule import AstroSchedule
from astroscheduler.config import AstroSchedulerConfig
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Example usage
config = AstroSchedulerConfig()
print(config.to_dict())

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Define paths for input and output directories
data_dir = os.path.join(script_dir, "../data")
input_dir = os.path.join(data_dir, "sample_input")
output_dir = os.path.join(data_dir, "sample_output")
output_json = os.path.join(output_dir, 'config.json')
output_xml = os.path.join(output_dir, 'schedule.xml')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

config_spreadsheet = os.path.join(input_dir, "ExampleTimeScheduleConfig.xlsx")
config_spreadsheet_2 = os.path.join(input_dir, "TimeScheduleConfig.xlsx")

# Example make an Excel configuration template
config.copy_sample_template(config_spreadsheet)

config.from_spreadsheet(config_spreadsheet_2)
# Print all attributes of the config object
print("Config Attributes:")
for attr, value in vars(config).items():
    print(f"{attr}: {value}")

# print dict
print(config.to_dict())

# write to json
config.to_json(output_json)

# create astroschedule builder
builder = AstroSchedule(config)
builder.create_events_for_year()
# print(builder.events)
print('\nEvent objects...')
# for i, event in enumerate(builder.create_event_objects()):
#     builder.create_event_objects()
#     rough = ET.tostring(event, 'utf-8')
#     print(minidom.parseString(rough).toprettyxml(indent="  "))
#     if i>5:
#         break

# now write to file
builder.builder.write_pretty_xml(output_xml)
    

