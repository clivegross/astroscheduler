import os
from astroscheduler.schedule_builder import ScheduleBuilder

# Example usage
builder = ScheduleBuilder()

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Define paths for input and output directories
data_dir = os.path.join(script_dir, "../data")
input_dir = os.path.join(data_dir, "sample_input")
output_dir = os.path.join(data_dir, "sample_output")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Example: Writing a file to the output directory
output_file = os.path.join(output_dir, "schedule.xml")

# Example: Reading a file from the input directory
input_file = os.path.join(input_dir, "sample_input_file.json")

# Step 1: Create TVP values for events
event_1 = builder.create_schedule_special_event(event_name="05-01", day_of_month=1, month=5)
tvp_values_event_1 = [
    {"Hour": 6, "Minute": 13, "Value": 1},
    {"Hour": 16, "Minute": 30, "Value": 9},
    {"Hour": 17, "Minute": 16, "Value": 2},
    {"Hour": 18, "Minute": 16, "Value": 3},
]

event_2 = builder.create_schedule_special_event(event_name="05-02", day_of_month=2, month=5)
tvp_values_event_2 = [
    {"Hour": 6, "Minute": 13, "Value": 1},
    {"Hour": 16, "Minute": 30, "Value": 9}
]
# Step 2: Add integer value pairs to events
builder.add_integer_value_pairs_to_event(event_1, tvp_values_event_1)
builder.add_integer_value_pairs_to_event(event_2, tvp_values_event_2)

# Step 3: Create a multistate schedule and add events to it
schedule = builder.create_multistate_schedule("Office Light Schedule", schedule_default=0)
builder.add_special_events_to_schedule(schedule, [event_1, event_2])

# Step 4: Add the schedule to the exported objects and print the XML
builder.add_to_exported_objects(schedule)
print(builder.to_pretty_xml())
builder.write_pretty_xml(output_file)