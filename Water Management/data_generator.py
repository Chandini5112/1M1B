import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

data = []

start = datetime.now() - timedelta(days=7)

for i in range(7 * 24):  # 7 days, hourly data
    time = start + timedelta(hours=i)
    usage = random.randint(80, 150)

    # simulate leak
    leak = 0
    if random.random() < 0.05:
        leak = random.randint(30, 80)
        usage += leak

    data.append({
        "timestamp": time,
        "water_usage": usage,
        "leak": leak
    })

df = pd.DataFrame(data)
df.to_csv("water_data.csv", index=False)
print("water_data.csv generated")
