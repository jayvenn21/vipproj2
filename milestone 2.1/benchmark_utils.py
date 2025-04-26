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
        print("\n" + "="*50)
        print(f"Benchmark for {func.__name__}:")
        print(f"Execution Time: {(end_time - start_time):.4f} seconds")
        print(f"Memory Usage - Current: {current / 10**6:.2f} MB")
        print(f"Memory Usage - Peak: {peak / 10**6:.2f} MB")
        print(f"CPU Usage: {process.cpu_percent()}%")
        print("="*50 + "\n")
        
        return result
    return wrapper