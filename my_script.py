import time
import sys
import random
from tqdm import tqdm

"""
Script de prueba "Hello, World!"
"""

def animated_text(text, delay=0.2, variation=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay + random.uniform(-variation, variation))
    print()


    
if __name__ == "__main__":


    for i in tqdm(range(10), desc="> Loading message"):
        time.sleep(random.uniform(0.1, 2.0))

    print("\n" + "*"*23)
    print(f"*" + ' '*21 + "*")
    animated_text(f"|  ~ Hello, World! ~  |")
    print(f"*" + ' '*21 + "*")
    print("*"*23)
    
    print("\nExecution finished.")
    
    
