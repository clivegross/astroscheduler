import os
from astroscheduler.config import AstroSchedulerConfig

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

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

config_spreadsheet = os.path.join(input_dir, "ExampleTimeScheduleConfig.xlsx")

# Example make an Excel configuration template
config.copy_sample_template(config_spreadsheet)

config.from_spreadsheet(config_spreadsheet)
# Print all attributes of the config object
print("Config Attributes:")
for attr, value in vars(config).items():
    print(f"{attr}: {value}")

# print dict
print(config.to_dict())

# write to json
config.to_json(output_json)

