import os
import sys

# Add the Pylom directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Pylom")))

from Pylom import Logger # Import Logger from the Logger.py file inside the Pylom package

# Ensure logs directory exists
logs_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(logs_dir, exist_ok=True)

def example_usage():
    # Define a custom timestamp format
    timestamp_format = "%Y-%m-%d %H:%M:%S"

    # Example 1: Using default settings
    with Logger() as log_default:
        log_default.info("Logging with default settings.")
        log_default.warn("A warning message.")

    # Example 2: Using a custom log file name
    with Logger(name="custom_log") as log_custom_name:
        log_custom_name.info("Logging with a custom log file name.")

    # Example 3: Using a custom log file object
    custom_log_file = open(os.path.join(logs_dir, "custom_log.txt"), "a")
    with Logger(file=custom_log_file) as log_custom_file:
        log_custom_file.info("Logging to a custom file object.")

    # Example 4: Using a custom log message template
    with Logger(template="[{_type}] {timestamp} - {message}", timestamp_format=timestamp_format) as log_custom_template:
        log_custom_template.info("Logging with a custom message template.")

    # Example 5: Using all custom options together
    with Logger(name="full_example", file=open(os.path.join(logs_dir, "full_example.log"), "a"),
                template="[{_type}] {timestamp} {file}:{line} {message}", timestamp_format=timestamp_format) as log_full:
        log_full.debug("This is a debug message with custom options.")
        log_full.info("This is an info message with custom options.")
        log_full.warn("This is a warning message with custom options.")
        log_full.error("This is an error message with custom options.")

    print("All logging examples completed.")

if __name__ == "__main__":
    example_usage()
