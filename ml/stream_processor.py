import time
import os
import pandas as pd

LIVE_LOG_FILE = "data/live_requests.csv"


def process_stream():
    print("Streaming processor started...")
    last_processed_count = 0

    while True:
        if os.path.exists(LIVE_LOG_FILE):
            try:
                df = pd.read_csv(LIVE_LOG_FILE)

                if len(df) > last_processed_count:
                    new_rows = df.iloc[last_processed_count:]

                    for _, row in new_rows.iterrows():
                        event = row.to_dict()
                        print("STREAM EVENT:", event)

                    last_processed_count = len(df)

            except Exception as e:
                print("Stream processor error:", e)

        time.sleep(1)


if __name__ == "__main__":
    process_stream()