import os
from astroscheduler.astroschedule import AstroSchedule
from astroscheduler.config import AstroSchedulerConfig
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Example usage
config = AstroSchedulerConfig()

print('\nCreate a schedule Excel config file')
# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Define paths for input and output directories
data_dir = os.path.join(script_dir, "../data")
input_dir = os.path.join(data_dir, "sample_input")
output_dir = os.path.join(data_dir, "sample_output")
output_json = os.path.join(output_dir, 'config.json')
output_xml = os.path.join(output_dir, 'schedule.xml')
output_xml_2 = os.path.join(output_dir, 'schedule_2.xml')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

config_spreadsheet = os.path.join(input_dir, "ExampleTimeScheduleConfig.xlsx")
config.copy_sample_template(config_spreadsheet)

print('\nMake schedule from an Excel config file')

# Example make an Excel configuration template

config_spreadsheet_2 = os.path.join(input_dir, "TimeScheduleConfig.xlsx")
config.from_spreadsheet(config_spreadsheet_2)

print('This is what the config looks like', config.to_dict())

# write to json
config.to_json(output_json)

# create astroschedule builder
schedule = AstroSchedule(config=config)


# now write to file
schedule.write_xml(output_xml)

print('\nNow make schedule without using Excel config file')
# Initialize the configuration class
schedule = AstroSchedule()

# Manually set the schedule configuration
schedule.default_value = 0 # default schedule value when no schedule events
schedule.ebo_version = "5.0.3.117"
schedule.latitude = -27.467778 # latitude for Brisbane Australia CBD 
schedule.longitude = 153.028056 # longitude for Brisbane Australia CBD
# Manually add schedule event entries
schedule.add_entry(time_ref="SunriseOffset", hour="0", minute="0", value="1") # start 45min before sunrise
schedule.add_entry(time_ref="SunsetOffset", hour="0", minute="0", value=None) # end (return to default value) at 4:30 PM

output_xml_2 = os.path.join(output_dir, 'schedule_2.xml')
# Write the XML tree to a file
schedule.write_xml(output_xml_2)

print('\nNow create multiple schedules using same event entries but different geolocations and combine them into a single XML file')
schedules = []

# Make Brisbane sunrise/sunset schedule
schedule.schedule_name = "Brisbane"
schedule.latitude = -27.467778 # latitude for Brisbane Australia CBD 
schedule.longitude = 153.028056 # longitude for Brisbane Australia CBD
schedules.append(schedule.schedule)

# Make Berlin sunrise/sunset schedule
schedule.schedule_name = "Berlin"
schedule.latitude = 52.520008 # latitude for Berlin
schedule.longitude = 13.404954 # longitude for Berlin
schedules.append(schedule.schedule)

# Make Andover sunrise/sunset schedule
schedule.schedule_name = "Andover"
schedule.latitude = 42.656029 # latitude for Andover
schedule.longitude = -71.157059 # longitude for Andover
schedules.append(schedule.schedule)

# Make Singapore sunrise/sunset schedule
schedule.schedule_name = "Singapore"
schedule.latitude = 1.290270 # latitude for Singapore
schedule.longitude = 103.851959 # longitude for Singapore
schedules.append(schedule.schedule)

# Make Paris sunrise/sunset schedule
schedule.schedule_name = "Paris"
schedule.latitude = 48.864716 # latitude for Paris
schedule.longitude = 2.349014 # longitude for Paris
schedules.append(schedule.schedule)

# Combine all schedules into a single ExportedObjects element
schedule.set_exported_objects(schedules)
output_xml = os.path.join(output_dir, 'city sunrise sunset schedules.xml')
# Write the XML tree to a file
schedule.write_xml(output_xml)
