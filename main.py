import os
import time
import win32evtlogutil
import win32evtlog
import win32con

# Define the path to the Suricata log file
log_file_path = "<path to fast.log>"

# Define the Event Log name and source
event_log_name = "Suricata/Operational"
event_source = "Suricata"

# Create the Event Log if it doesn't exist
try:
    win32evtlogutil.AddSourceToRegistry(event_source, event_log_name)
except win32evtlog.error:
    pass  # Ignore if the event source already exists

# Function to write a message to the Event Log
def write_to_event_log(message):
    win32evtlogutil.ReportEvent(
        event_source,
        1,
        eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
        strings=[message]
    )

# Track the last read position
last_read_position = 0

def process_new_lines():
    global last_read_position
    with open(log_file_path, 'r') as file:
        file.seek(last_read_position)
        new_lines = file.readlines()
        if new_lines:
            for line in new_lines:
                write_to_event_log(line.strip())
            last_read_position = file.tell()

# Create a function to monitor the log file
def monitor_log_file():
    while True:
        process_new_lines()
        time.sleep(1)

# Start monitoring the log file
if __name__ == "__main__":
    monitor_log_file()
