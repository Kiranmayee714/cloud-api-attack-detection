from pathlib import Path
import boto3

BUCKET_NAME = "api-attack-detection-kiranmayee"

s3 = boto3.client("s3")

def download_file(s3_key: str, local_path: str):
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(BUCKET_NAME, s3_key, local_path)

if __name__ == "__main__":
    download_file("data/api_features.csv", "data/api_features.csv")
    download_file("model/api_attack_model.pkl", "model/api_attack_model.pkl")
    print("Files downloaded from S3 successfully!")