import pandas as pd
import re

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
log_file = BASE_DIR / "data" / "access.log"

data = []

pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?) (.*?) HTTP.*" (\d+) (\d+)'

with open(log_file, "r") as f:
    for line in f:
        match = re.search(pattern, line)

        if match:
            ip = match.group(1)
            timestamp = match.group(2)
            method = match.group(3)
            endpoint = match.group(4)
            status = int(match.group(5))
            bytes_sent = int(match.group(6))

            data.append([ip, timestamp, method, endpoint, status, bytes_sent])

df = pd.DataFrame(
    data,
    columns=["ip", "timestamp", "method", "endpoint", "status", "bytes"]
)

df.to_csv(r"C:\Users\user\Cloud_API_Attack_Detection\data\api_logs.csv", index=False)

print("CSV dataset created!")
print(df.head())