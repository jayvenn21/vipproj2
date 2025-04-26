import json
import matplotlib.pyplot as plt
import numpy as np
def grapher():

    data = "memory_usage_data.json"
    with open(data, "r") as f:
        data = json.load(f)

    # Step 2: Extract memory usage and timestamps
    memory_usage = data['memory_usage']
    timestamps = [entry['timestamp'] for entry in memory_usage]
    memory_values = [entry['memory'] for entry in memory_usage]

    # Step 3: Find the highest memory value
    max_memory = max(memory_values)
    max_timestamp = timestamps[memory_values.index(max_memory)]

    # Step 4: Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, memory_values, label="Memory Usage")
    plt.xlabel('Timestamp')
    plt.ylabel('Memory')
    plt.title('Memory Usage Over Time')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.tight_layout()
    plt.grid(True)
    plt.legend()

    # Show the plot

    plt.show()
    area = np.trapezoid(memory_values, timestamps)  # Integrating with respect to x
    print(f"Area under the curve: {area}")
    # Step 5: Print the highest memory value
    print(f"Highest memory value: {max_memory} at timestamp {max_timestamp}")
    return f"Total memory used: {area}\nHighest memory value: {max_memory} at timestamp {max_timestamp}"