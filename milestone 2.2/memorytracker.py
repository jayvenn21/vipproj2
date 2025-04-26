# track_memory.py
print("the script is loaded")
import subprocess
import sys
subprocess.call([sys.executable, "-m", "pip", "install", "psutil"])
import time
import psutil
import json
#import stdtest


print("everything is imported")
# Get the PID passed as an argument
pid = int(sys.argv[1])

# Create a Process object for the specified PID
process = psutil.Process(pid)
# Function to track memory usage
start_time = time.time()
print(psutil.virtual_memory().total)
def get_memory_usage():
    #process = psutil.virtual_memory().used
    #memory_info = process.memory_info()
    return process.memory_info().rss / (1024 ** 3)  # Convert to GB

# File to store memory usage data
output_file = "memory_usage_data.json"

# Open the file in append mode
with open(output_file, "w") as f:
    f.write('{"memory_usage": []}\n')  # Initialize JSON structure

while True:
    # Get the current memory usage in GB
    memory_usage = get_memory_usage()

    # Get the current timestamp (in seconds)
    timestamp = int(time.time() - start_time)

    # Read the existing data
    with open(output_file, "r") as f:
        data = json.load(f)

    # Append the new data
    data["memory_usage"].append({"timestamp": timestamp, "memory": memory_usage})

    # Write the updated data back to the file
    with open(output_file, "w") as f:
        json.dump(data, f)

    # Sleep for 1 second before recording again
    time.sleep(1)