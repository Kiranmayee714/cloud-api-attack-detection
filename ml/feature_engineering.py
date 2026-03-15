import pandas as pd

df = pd.read_csv(r"C:\Users\user\Cloud_API_Attack_Detection\data\api_logs.csv")

# failed request feature
df["failed_request"] = df["status"].apply(lambda x: 1 if x >= 400 else 0)

# requests per IP
requests_per_ip = df.groupby("ip").size().rename("requests_per_ip")

# failed requests per IP
failed_per_ip = df.groupby("ip")["failed_request"].sum().rename("failed_requests")

# unique endpoints accessed
endpoint_per_ip = df.groupby("ip")["endpoint"].nunique().rename("unique_endpoints")

# average payload size
avg_payload = df.groupby("ip")["bytes"].mean().rename("avg_bytes")

# combine features
features = pd.concat(
    [requests_per_ip, failed_per_ip, endpoint_per_ip, avg_payload],
    axis=1
)

features.reset_index(inplace=True)

print(features.head())

features.to_csv(r"C:\Users\user\Cloud_API_Attack_Detection\data\api_features.csv", index=False)

print("\nFeature dataset created!")