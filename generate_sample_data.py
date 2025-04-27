import csv
import os
import random
import requests
from datetime import datetime

# Create necessary folders
os.makedirs("test_data/good", exist_ok=True)
os.makedirs("test_data/bad", exist_ok=True)

def generate_good_csv(file_path):
    headers = [
        "batch_id", "timestamp", "reading1", "reading2", "reading3", "reading4",
        "reading5", "reading6", "reading7", "reading8", "reading9", "reading10"
    ]
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        used_batch_ids = set()
        for _ in range(10):  # generate 10 rows
            batch_id = random.randint(1000, 9999)
            while batch_id in used_batch_ids:
                batch_id = random.randint(1000, 9999)
            used_batch_ids.add(batch_id)

            readings = [round(random.uniform(0, 9.8), 3) for _ in range(10)]
            writer.writerow([batch_id, "14:01:04", *readings])

def generate_bad_csv(file_path):
    # Randomly choose what type of bad file to create
    bad_type = random.choice(["wrong_header", "duplicate_batch", "high_value", "missing_column", "empty_file"])
    
    if bad_type == "empty_file":
        open(file_path, 'w').close()  # create a 0-byte empty file
        return

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        
        if bad_type == "wrong_header":
            writer.writerow(["batch", "time", "r1", "r2", "r3", "r4"])
        
        else:
            headers = [
                "batch_id", "timestamp", "reading1", "reading2", "reading3", "reading4",
                "reading5", "reading6", "reading7", "reading8", "reading9", "reading10"
            ]
            writer.writerow(headers)

            used_batch_ids = set()
            for _ in range(10):
                batch_id = random.randint(1000, 9999)
                if bad_type == "duplicate_batch" and random.random() < 0.2:
                    batch_id = list(used_batch_ids)[0]  # force a duplicate

                used_batch_ids.add(batch_id)

                readings = []
                for _ in range(10):
                    if bad_type == "high_value" and random.random() < 0.2:
                        readings.append(round(random.uniform(10, 15), 3))  # invalid value
                    else:
                        readings.append(round(random.uniform(0, 9.8), 3))
                
                if bad_type == "missing_column" and random.random() < 0.2:
                    readings.pop()  # remove one reading randomly
                
                writer.writerow([batch_id, "14:01:04", *readings])

def fetch_guid():
    try:
        response = requests.get("https://www.uuidtools.com/api/generate/v1")
        if response.status_code == 200:
            guid = response.json()[0]
            return guid
    except Exception as e:
        print(f"Error fetching GUID: {e}")
    return "NOGUID"

def log_bad_file(file_path):
    guid = fetch_guid()
    with open("test_data/error_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} | {file_path} | Error GUID: {guid}\n")

def create_sample_data():
    # Create 5 good files
    for _ in range(5):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"MED_DATA_{timestamp}.csv"
        full_path = os.path.join("test_data/good", filename)
        generate_good_csv(full_path)

    # Create 5 bad files
    for _ in range(5):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"BAD_DATA_{timestamp}.csv"
        full_path = os.path.join("test_data/bad", filename)
        generate_bad_csv(full_path)
        log_bad_file(full_path)

if __name__ == "__main__":
    create_sample_data()
    print("Sample data generation completed!")
