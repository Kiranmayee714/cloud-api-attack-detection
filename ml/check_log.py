file_path = r"C:\Users\user\Cloud_API_Attack_Detection\data\access.log"

with open(file_path, "r") as f:
    for i in range(10):
        print(f.readline())