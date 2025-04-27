import time
import psutil
import os
import tracemalloc
from functools import wraps

def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Memory tracking
        tracemalloc.start()
        process = psutil.Process(os.getpid())
        
        # Time tracking
        start_time = time.time()
        
        # Run the function
        result = func(*args, **kwargs)
        
        # Calculate metrics
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Print benchmark results
        file = "log.txt"
        with open(file, "w") as f:
            f.write("\n" + "="*50)
            f.write(f"Benchmark for {func.__name__}:")
            f.write(f"Execution Time: {(end_time - start_time):.4f} seconds")
            f.write(f"Memory Usage - Current: {current / 10**6:.2f} MB")
            f.write(f"Memory Usage - Peak: {peak / 10**6:.2f} MB")
            f.write(f"CPU Usage: {process.cpu_percent()}%")
            f.write("="*50 + "\n")
        f.close()

        print("\n" + "="*50)
        print(f"Benchmark for {func.__name__}:")
        print(f"Execution Time: {(end_time - start_time):.4f} seconds")
        print(f"Memory Usage - Current: {current / 10**6:.2f} MB")
        print(f"Memory Usage - Peak: {peak / 10**6:.2f} MB")
        print(f"CPU Usage: {process.cpu_percent()}%")
        print("="*50 + "\n")
        return result
    return wrapper